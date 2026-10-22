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
            await client.post('/api/clear', json={'session_id': sid})
        async with streamable_http_client(f'{BASE}/mcp') as (read, write, _):
            async with ClientSession(read, write) as client:
                initialized = await client.initialize()
                self.assertEqual(initialized.protocolVersion, '2025-11-25')
                self.assertIn('check_answer_text', initialized.instructions)
                tools = (await client.list_tools()).tools
                names = {tool.name for tool in tools}
                self.assertTrue(all(t.annotations.readOnlyHint for t in tools if t.name.startswith(('check_', 'compare_answer'))))
                self.assertEqual(names, {'get_interview_brief', 'coach_latest_answer', 'compare_retry', 'check_answer_text', 'compare_answer_texts'})

if __name__ == '__main__':
    unittest.main(verbosity=2)
