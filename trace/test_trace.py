import asyncio
import unittest
import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from tracer import trace
from examples import EXAMPLES

class TracerTests(unittest.TestCase):
    def test_alias_identity_and_fix(self):
        example = EXAMPLES[0]
        bad = trace(example['source'])
        self.assertIsNone(bad['error'])
        self.assertEqual(bad['stdout'], '[[], [], [], [], [], [], [], []]\n')
        final = bad['steps'][-1]
        results = final['stack'][0]['variables']['answer']['ref']
        refs = [item['ref'] for item in final['heap'][results]['items']]
        self.assertEqual(len(set(refs)), 1)
        self.assertEqual(final['heap'][refs[0]]['items'], [])
        good = trace(example['source'].replace(example['fix']['before'], example['fix']['after']))
        self.assertEqual(good['stdout'], example['expected'])
        final = good['steps'][-1]
        results = final['stack'][0]['variables']['answer']['ref']
        self.assertEqual(len(set(item['ref'] for item in final['heap'][results]['items'])), 8)

    def test_bounds(self):
        example = EXAMPLES[1]
        bad = trace(example['source'])
        self.assertEqual(bad['error']['type'], 'IndexError')
        failure = next(s for s in bad['steps'] if 'exception' in s)
        self.assertEqual(failure['line'], 5)
        self.assertEqual(failure['access'], {'name': 'numbers', 'index': 4, 'length': 4, 'valid': False})
        good = trace(example['source'].replace(example['fix']['before'], example['fix']['after']))
        self.assertEqual(good['stdout'], example['expected'])

    def test_recursion(self):
        result = trace(EXAMPLES[2]['source'])
        self.assertEqual(result['stdout'], '120\n')
        calls = [c for c in result['calls'] if c['name'] == 'factorial']
        self.assertEqual(len(calls), 5)
        self.assertEqual(calls[-1]['parent'], calls[-2]['id'])
        self.assertTrue(all(c['end'] is not None for c in calls))

    def test_before_line_semantics(self):
        result = trace('x = 1\nx = 2\nprint(x)')
        line_two = next(s for s in result['steps'] if s['event'] == 'line' and s['line'] == 2)
        self.assertEqual(line_two['stack'][0]['variables']['x'], 1)

    def test_limits_and_validation(self):
        self.assertEqual(trace('import os')['error']['type'], 'ValueError')
        self.assertEqual(trace('x = (')['error']['type'], 'SyntaxError')
        result = trace('while True:\n    pass')
        self.assertEqual(len(result['steps']), 600)
        self.assertEqual(result['error']['type'], 'RuntimeError')

    def test_cycle(self):
        result = trace('a = []\na.append(a)')
        last = result['steps'][-1]
        ref = last['stack'][0]['variables']['a']['ref']
        self.assertEqual(last['heap'][ref]['items'][0]['ref'], ref)

class IntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_live_mcp_and_frontend_api(self):
        async with httpx.AsyncClient(base_url='http://127.0.0.1:8765') as client:
            self.assertEqual((await client.get('/')).status_code, 200)
            response = await client.post('/api/run', json={'source': EXAMPLES[1]['source']})
            self.assertEqual(response.status_code, 200)
            run = response.json()
            response = await client.post('/api/ask', json={'run_id': run['id'], 'question': 'Show the error', 'step': 0})
            self.assertEqual(response.status_code, 200, response.text)
            answer = response.json()
            self.assertEqual(answer['protocol'], '2025-11-25')
            self.assertEqual(answer['transport'], 'Streamable HTTP')
            self.assertEqual(answer['evidence']['access']['index'], 4)
            self.assertGreater(answer['step'], 0)
            blocked = await client.post('/api/run', json={'source': 'print(1)'}, headers={'Origin': 'https://example.com'})
            self.assertEqual(blocked.status_code, 403)
        async with streamable_http_client('http://127.0.0.1:8765/mcp') as (read, write, _):
            async with ClientSession(read, write) as session:
                initialized = await session.initialize()
                self.assertEqual(initialized.protocolVersion, '2025-11-25')
                names = {tool.name for tool in (await session.list_tools()).tools}
                self.assertEqual(names, {'trace_python', 'inspect_step', 'navigate_trace'})
                result = await session.call_tool('trace_python', {'source': 'print(6 * 7)'})
                self.assertFalse(result.isError)

if __name__ == '__main__':
    unittest.main(verbosity=2)

