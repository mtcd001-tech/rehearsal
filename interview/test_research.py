import os
import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx
import research
import server

def provider_result():
    return {'status':'completed','output':[{'type':'web_search_call'},{'type':'message','content':[{'type':'output_text','text':'Official process [1]. Formats vary.','annotations':[{'type':'url_citation','start_index':17,'end_index':20,'url':'https://example.com/careers','title':'Careers'}]}]}]}

class ResearchTests(unittest.TestCase):
    def test_citations_preserve_text(self):
        r=research.parse_research(provider_result())
        self.assertEqual(''.join(x['text'] for x in r['blocks'][0]['parts']),'Official process [1]. Formats vary.')
        self.assertEqual(r['sources'][0]['url'],'https://example.com/careers')
    def test_unsafe_or_missing_citations_rejected(self):
        for url in ['javascript:alert(1)','https://user:password@example.com','']:
            r=provider_result();r['output'][1]['content'][0]['annotations'][0]['url']=url
            with self.assertRaises(ValueError):research.parse_research(r)
    def test_no_search_or_partial_rejected(self):
        r=provider_result();r['output']=r['output'][1:]
        with self.assertRaises(ValueError):research.parse_research(r)
        r=provider_result();r['status']='incomplete'
        with self.assertRaises(ValueError):research.parse_research(r)
    def test_unsupported_resume_evidence_removed(self):
        plan={'summary':'Prepare ownership stories','questions':[], 'gaps':['Ask for a measurement'], 'resume_suggestions':[
            {'resume_quote':'Built Python APIs','jd_quote':'Python','suggestion':'Emphasize the API work you actually did.'},
            {'resume_quote':'Managed 50 engineers','jd_quote':'Python','suggestion':'Invented'},
            {'resume_quote':'Built Python APIs','jd_quote':'CEO','suggestion':'Unsupported requirement'}]}
        r=research.validate_plan(plan,'Built Python APIs','We use Python')
        self.assertEqual(len(r['resume_suggestions']),1)

class ResearchAsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_feature_gated_without_calls(self):
        with patch.dict(os.environ,{'INTERVIEW_RESEARCH_ENABLED':'0'}),patch.object(server,'search_company',new=AsyncMock()) as search:
            with self.assertRaisesRegex(ValueError,'No web or AI request'):
                await server.research_brief(server.Brief(role='Intern',company='Example',job='Python'))
            search.assert_not_called()
    async def test_endpoint_mocked_provider_and_brief_roundtrip(self):
        public=research.parse_research(provider_result())
        with patch.dict(os.environ,{'INTERVIEW_RESEARCH_ENABLED':'1'}),patch.object(server,'search_company',new=AsyncMock(return_value=public)) as search,patch.object(server,'model_json',new=AsyncMock(return_value={'summary':'Practice explaining API work','questions':[],'resume_suggestions':[],'gaps':[]})) as model:
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.app),base_url='http://127.0.0.1:8766') as client:
                r=await client.post('/api/research',json={'role':'Intern','company':'Example','job':'Python','resume':'Private experience'})
                self.assertEqual(r.status_code,200,r.text)
                self.assertEqual(search.call_args.args[:2],('Example','Intern'))
                self.assertNotIn('Private experience',str(search.call_args))
                self.assertEqual(model.call_args.args[1]['resume'],'Private experience')
                saved=server.create_session(server.Brief(role='Intern',research='Cited context'))
                self.assertEqual(server.get_interview_brief(saved['session_id'])['brief']['research'],'Cited context')
                server.clear(server.SessionRef(**saved))
    async def test_search_payload_no_resume(self):
        fake=AsyncMock();response=MagicMock();response.is_success=True;response.json.return_value=provider_result();fake.post.return_value=response
        manager=AsyncMock();manager.__aenter__.return_value=fake
        with patch.dict(os.environ,{'OPENAI_API_KEY':'test-placeholder'}),patch.object(research.httpx,'AsyncClient',return_value=manager):
            await research.search_company('Example','Intern','https://example.invalid/responses')
        payload=fake.post.call_args.kwargs['json']
        self.assertFalse(payload['store']);self.assertEqual(payload['tool_choice'],'required')
        self.assertNotIn('resume',payload['input']);self.assertNotIn('jd',payload['input'])

if __name__=='__main__':unittest.main()
