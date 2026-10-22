import json
import os
import unittest
from unittest.mock import AsyncMock, patch
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
import server
from sample import SAMPLE

BASE = f'http://127.0.0.1:{server.PORT}'  # set INTERVIEW_PORT to test a server on another port

class CoachTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.sid = server.create_session(server.Brief(**SAMPLE['brief']))['session_id']

    def tearDown(self):
        server.sessions.pop(self.sid, None)

    async def test_feedback_quotes_are_verified(self):
        server.transcript(server.Turn(session_id=self.sid, role='user', text=SAMPLE['first']))
        report = {**SAMPLE['coaching'], 'evidence': SAMPLE['coaching']['evidence'] + [{'quote': 'I improved latency by 80 percent', 'observation': 'invented', 'suggestion': 'bad'}]}
        with patch.object(server, 'model_json', new=AsyncMock(return_value=report)):
            result = await server.coach_latest_answer(self.sid)
        self.assertEqual(len(result['evidence']), 2)
        self.assertEqual(server.sessions[self.sid]['baseline'], SAMPLE['first'])
        self.assertEqual(result['metrics']['filler_tokens'], 1)

    async def test_retry_requires_new_answer_and_filters_quotes(self):
        with self.assertRaises(ValueError):
            await server.compare_retry(self.sid)
        server.sessions[self.sid]['baseline'] = SAMPLE['first']
        server.transcript(server.Turn(session_id=self.sid, role='user', text=SAMPLE['retry']))
        output = {**SAMPLE['comparison'], 'changes': SAMPLE['comparison']['changes'] + [{'before': 'not in answer', 'after': 'invented', 'why': 'bad'}]}
        with patch.object(server, 'model_json', new=AsyncMock(return_value=output)):
            result = await server.compare_retry(self.sid)
        self.assertEqual(len(result['changes']), 3)

    async def test_empty_answer_not_coached(self):
        with self.assertRaises(ValueError):
            await server.coach_latest_answer(self.sid)

    async def test_transcript_deduplicated(self):
        turn = server.Turn(session_id=self.sid, role='user', text='Hello', item_id='item1')
        self.assertTrue(server.transcript(turn)['saved'])
        self.assertFalse(server.transcript(turn)['saved'])
        self.assertEqual(len(server.get_interview_brief(self.sid)['turns']), 1)

    async def test_text_failure_does_not_save_fake_turn(self):
        with patch.object(server, 'model_json', new=AsyncMock(side_effect=ValueError('quota unavailable'))):
            with self.assertRaises(ValueError):
                await server.text_answer(server.TypedAnswer(session_id=self.sid, text='My actual answer'))
        self.assertEqual(server.sessions[self.sid]['turns'], [])

    async def test_invalid_feedback_schema_rejected(self):
        server.transcript(server.Turn(session_id=self.sid, role='user', text='I built a tool.'))
        with patch.object(server, 'model_json', new=AsyncMock(return_value={'summary': 'incomplete'})):
            with self.assertRaises(ValueError):
                await server.coach_latest_answer(self.sid)

    async def test_clear_removes_context(self):
        server.clear(server.SessionRef(session_id=self.sid))
        with self.assertRaises(ValueError):
            server.get_interview_brief(self.sid)

class LocalIntegration(unittest.IsolatedAsyncioTestCase):
    async def test_sample_and_mcp_without_provider_calls(self):
        async with httpx.AsyncClient(base_url=BASE) as client:
            self.assertEqual((await client.get('/')).status_code, 200)
            sample = (await client.get('/api/sample')).json()
            sid = (await client.post('/api/session', json=sample['brief'])).json()['session_id']
            response = await client.post('/api/tool', json={'session_id': sid, 'name': 'get_interview_brief'})
            self.assertEqual(response.status_code, 200, response.text)
            self.assertEqual(response.json()['protocol'], '2025-11-25')
            self.assertEqual(response.json()['result']['brief']['role'], 'Software Engineering Intern')
            self.assertIn('no-store', response.headers['cache-control'])
            blocked = await client.post('/api/session', json=sample['brief'], headers={'Origin': 'https://example.com'})
            self.assertEqual(blocked.status_code, 403)
            unknown = await client.post('/api/tool', json={'session_id': sid, 'name': 'not_a_tool'})
            self.assertEqual(unknown.status_code, 400)
            checked = await client.post('/api/check', json={'text': sample['first']})
            self.assertEqual(checked.status_code, 200, checked.text)
            self.assertEqual(checked.json()['tool'], 'check_answer_text')
            self.assertEqual(checked.json()['result']['priority']['id'], 'ownership')
            compared = await client.post('/api/compare-text', json={'before': sample['first'], 'after': sample['retry']})
            self.assertEqual(compared.status_code, 200, compared.text)
            self.assertTrue(compared.json()['result']['summary'].startswith('Moved'))
            same = await client.post('/api/compare-text', json={'before': 'We did it.', 'after': 'We did it.'})
            self.assertEqual(same.status_code, 400)
            app_res = (await client.get('/api/app-resource')).json()
            self.assertEqual(app_res['linked_tools'], ['check_answer_text', 'compare_answer_texts'])
            raw = await client.post('/api/app-call', json={'name': 'compare_answer_texts', 'arguments': {'before': sample['first'], 'after': sample['retry']}})
            self.assertIn('structuredContent', raw.json())
            self.assertEqual((await client.post('/api/app-call', json={'name': 'save_practice_result', 'arguments': {}})).status_code, 422)
            self.assertEqual((await client.get('/mcp-app-preview')).status_code, 200)
            progress = await client.get('/api/progress')
            self.assertEqual(progress.status_code, 200, progress.text)
            self.assertEqual(progress.json()['tool'], 'get_practice_progress')
            if os.getenv('INTERVIEW_HISTORY_FILE'):  # only write history when the server under test uses a throwaway file
                saved = await client.post('/api/progress', json={'question': sample['question'], 'first': sample['first'], 'retry': sample['retry']})
                self.assertEqual(saved.status_code, 200, saved.text)
                self.assertNotIn('database', json.dumps(saved.json()['result']['saved']))
                self.assertGreaterEqual((await client.get('/api/progress')).json()['result']['sessions'], 1)
                self.assertTrue((await client.delete('/api/progress')).json()['cleared'])
            await client.post('/api/clear', json={'session_id': sid})
        async with streamable_http_client(f'{BASE}/mcp') as (read, write, _):
            async with ClientSession(read, write) as client:
                initialized = await client.initialize()
                self.assertEqual(initialized.protocolVersion, '2025-11-25')
                self.assertIn('check_answer_text', initialized.instructions)
                tools = (await client.list_tools()).tools
                names = {tool.name for tool in tools}
                self.assertTrue(all(t.annotations.readOnlyHint for t in tools if t.name.startswith(('check_', 'compare_answer', 'get_practice'))))
                linked = {t.name for t in tools if (t.meta or {}).get('ui', {}).get('resourceUri') == server.APP_URI}
                self.assertEqual(linked, {'check_answer_text', 'compare_answer_texts'})
                resources = {str(r.uri): r for r in (await client.list_resources()).resources}
                self.assertEqual(resources[server.APP_URI].mimeType, 'text/html;profile=mcp-app')
                view = (await client.read_resource(server.APP_URI)).contents[0]
                self.assertEqual(view.mimeType, 'text/html;profile=mcp-app')
                self.assertIn('ui/initialize', view.text)
                called = await client.call_tool('check_answer_text', {'answer': 'We fixed it and it worked well.'})
                self.assertEqual(called.structuredContent['priority']['id'], 'ownership')
                self.assertTrue(called.content[0].text)  # text fallback for hosts without MCP Apps
                self.assertEqual(names, {'get_interview_brief', 'coach_latest_answer', 'compare_retry', 'check_answer_text', 'compare_answer_texts', 'save_practice_result', 'get_practice_progress'})

if __name__ == '__main__':
    unittest.main(verbosity=2)
