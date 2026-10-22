import os
import unittest
from unittest.mock import patch, AsyncMock, MagicMock
import httpx
import research
import server

def provider_result():
    return {'candidates':[{'finishReason':'STOP','content':{'parts':[{'text':'Official process. Formats vary.'}]},'groundingMetadata':{'webSearchQueries':['Example hiring'],'groundingChunks':[{'web':{'uri':'https://example.com/careers','title':'Careers'}}],'groundingSupports':[{'segment':{'endIndex':17},'groundingChunkIndices':[0]}]}}]}

class ResearchTests(unittest.TestCase):
    def test_round_and_duration_validation(self):
        self.assertEqual(server.Brief(role='Intern').duration, '15')
        for fields in ({'round':'unknown'}, {'duration':'90'}):
            with self.assertRaises(ValueError):
                server.Brief(role='Intern', **fields)

    def test_citations_preserve_text(self):
        r=research.parse_research(provider_result())
        self.assertEqual(''.join(x['text'] for x in r['blocks'][0]['parts'] if 'url' not in x),'Official process. Formats vary.')
        self.assertEqual(r['sources'][0]['url'],'https://example.com/careers')
    def test_utf8_and_part_offsets(self):
        r = provider_result()
        r['candidates'][0]['content']['parts'] = [{'text':'Intro. '}, {'text':'Caf\u00e9 hiring.'}]
        r['candidates'][0]['groundingMetadata']['groundingSupports'][0]['segment'] = {'partIndex':1,'endIndex':len('Caf\u00e9 hiring.'.encode('utf-8'))}
        result = research.parse_research(r)
        self.assertEqual(result['blocks'][0]['parts'][0]['text'],'Intro. Caf\u00e9 hiring.')
        self.assertIn('url',result['blocks'][0]['parts'][1])

    def test_unsafe_or_missing_citations_rejected(self):
        for url in ['javascript:alert(1)','https://user:password@example.com','']:
            r=provider_result();r['candidates'][0]['groundingMetadata']['groundingChunks'][0]['web']['uri']=url
            with self.assertRaises(ValueError):research.parse_research(r)
    def test_no_search_or_partial_rejected(self):
        r=provider_result();r['candidates'][0]['groundingMetadata']['webSearchQueries']=[]
        with self.assertRaises(ValueError):research.parse_research(r)
        r=provider_result();r['candidates'][0]['finishReason']='MAX_TOKENS'
        with self.assertRaises(ValueError):research.parse_research(r)
    def test_unsupported_resume_evidence_removed(self):
        plan={'summary':'Prepare ownership stories','questions':[], 'gaps':['Ask for a measurement'], 'experience_probes':[
            {'resume_quote':'Built Python APIs','jd_quote':'Python','listen_for':'Specific decisions','follow_up':'Emphasize the API work you actually did.'},
            {'resume_quote':'Managed 50 engineers','jd_quote':'Python','listen_for':'Specific decisions','follow_up':'Invented'},
            {'resume_quote':'Built Python APIs','jd_quote':'CEO','listen_for':'Specific decisions','follow_up':'Unsupported requirement'}]}
        r=research.validate_plan(plan,'Built Python APIs','We use Python')
        self.assertEqual(len(r['experience_probes']),1)

class ResearchAsyncTests(unittest.IsolatedAsyncioTestCase):
    async def test_feature_gated_without_calls(self):
        with patch.dict(os.environ,{'INTERVIEW_RESEARCH_ENABLED':'0'}),patch.object(server,'search_company',new=AsyncMock()) as search:
            with self.assertRaisesRegex(ValueError,'No web or AI request'):
                await server.research_brief(server.Brief(role='Intern',company='Example',job='Python'))
            search.assert_not_called()
    async def test_endpoint_mocked_provider_and_brief_roundtrip(self):
        public=research.parse_research(provider_result())
        with patch.dict(os.environ,{'INTERVIEW_RESEARCH_ENABLED':'1'}),patch.object(server,'search_company',new=AsyncMock(return_value=public)) as search,patch.object(server,'model_json',new=AsyncMock(return_value={'summary':'Practice explaining API work','questions':[],'experience_probes':[],'gaps':[]})) as model:
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.app),base_url='http://127.0.0.1:8766') as client:
                r=await client.post('/api/research',json={'role':'Intern','company':'Example','job':'Python','resume':'Private experience','skills':'Explain tradeoffs','round':'technical','duration':'5'})
                self.assertEqual(r.status_code,200,r.text)
                self.assertEqual(search.call_args.args[:2],('Example','Intern'))
                self.assertNotIn('Private experience',str(search.call_args))
                self.assertEqual(model.call_args.args[1]['resume'],'Private experience')
                self.assertEqual(model.call_args.args[1]['skills'],'Explain tradeoffs')
                self.assertEqual(model.call_args.args[1]['round'],'technical')
                self.assertEqual(model.call_args.args[1]['duration'],'5')
                self.assertNotIn('Explain tradeoffs', str(search.call_args))
                saved=server.create_session(server.Brief(role='Intern',research='Cited context'))
                self.assertEqual(server.get_interview_brief(saved['session_id'])['brief']['research'],'Cited context')
                server.clear(server.SessionRef(**saved))
    async def test_text_interviewer_receives_tailored_plan(self):
        saved = server.create_session(server.Brief(role='Intern', skills='Clear explanations', research='Probe API testing; listen for edge cases'))
        try:
            with patch.object(server, 'model_json', new=AsyncMock(return_value={'reply':'How did you test your API?'})) as model:
                await server.text_answer(server.TypedAnswer(session_id=saved['session_id'], text='__start__'))
                prompt, context = model.call_args.args
                self.assertIn('proposed simulation plan', prompt)
                self.assertIn('adapt follow-ups', prompt)
                self.assertIn('skills as learning goals', prompt)
                self.assertEqual(context['brief']['skills'], 'Clear explanations')
                self.assertEqual(context['brief']['research'], 'Probe API testing; listen for edge cases')
        finally:
            server.clear(server.SessionRef(**saved))

    async def test_search_payload_no_resume(self):
        fake=AsyncMock();response=MagicMock();response.is_success=True;response.json.return_value=provider_result();fake.post.return_value=response
        manager=AsyncMock();manager.__aenter__.return_value=fake
        with patch.dict(os.environ,{'GEMINI_API_KEY':'test-placeholder'}),patch.object(research.httpx,'AsyncClient',return_value=manager):
            await research.search_company('Example','Intern')
        payload=fake.post.call_args.kwargs['json']
        self.assertEqual(payload['tools'],[{'google_search':{}}])
        context=payload['contents'][0]['parts'][0]['text']
        self.assertNotIn('resume',context);self.assertNotIn('jd',context)

if __name__=='__main__':unittest.main()
