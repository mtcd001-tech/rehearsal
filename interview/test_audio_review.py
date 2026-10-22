import unittest, json
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
import server, audio_review

class AudioTests(unittest.IsolatedAsyncioTestCase):
 async def test_input_validation(self):
  for data in (b'', b'bad', b'x'*(audio_review.MAX_AUDIO_BYTES+1)):
   with self.assertRaises(ValueError): await audio_review.review_audio(data,'q','')
 async def test_endpoint_bound(self):
  async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.app),base_url='http://127.0.0.1:8766') as c:
   with patch.object(server,'review_audio',new=AsyncMock(return_value={'transcript':'spoken'})) as review:
    r=await c.post('/api/audio-review?question=Question&skills=Clarity',content=b'RIFF0000WAVE')
    self.assertEqual(r.status_code,200);self.assertEqual(review.call_args.args,(b'RIFF0000WAVE','Question','Clarity'))
    r=await c.post('/api/audio-review',content=b'x'*(audio_review.MAX_AUDIO_BYTES+1));self.assertEqual(r.status_code,413)
 async def test_provider_schema_evidence_and_privacy(self):
  result={k:'Test' for k in ['transcript','summary','strength','structure','language','knowledge','delivery','retry_focus','improved_answer']}
  result.update(transcript='I tested the fix.',missing_details=[],evidence=[{'quote':'invented','observation':'x','suggestion':'x'},{'quote':'tested','observation':'x','suggestion':'x'}])
  response=MagicMock(is_success=True);response.json.return_value={'candidates':[{'finishReason':'STOP','content':{'parts':[{'text':json.dumps(result)}]}}]}
  client=AsyncMock();client.post.return_value=response;manager=AsyncMock();manager.__aenter__.return_value=client
  with patch.dict('os.environ',{'GEMINI_API_KEY':'mock-key'}),patch.object(audio_review.httpx,'AsyncClient',return_value=manager):
   out=await audio_review.review_audio(b'RIFF0000WAVE','Question','Clarity')
  self.assertEqual(len(out['evidence']),1)
  payload=client.post.call_args.kwargs['json'];self.assertIn('inlineData',payload['contents'][0]['parts'][1]);self.assertNotIn('resume',payload['contents'][0]['parts'][0]['text'])
 async def test_text_uses_same_gemini_helper(self):
  with patch.object(server,'gemini_json',new=AsyncMock(return_value={'reply':'Hello'})) as model:
   result=await server.model_json('Return reply',{'role':'Intern'})
  self.assertEqual(result['reply'],'Hello')
  self.assertIsNone(model.call_args.args[0])
  self.assertIn('Intern',model.call_args.args[2][0]['text'])
 async def test_legacy_live_endpoint_disabled(self):
  async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.app),base_url='http://127.0.0.1:8766') as c:
   r=await c.post('/api/token',json={'session_id':'obsolete'})
   self.assertEqual(r.status_code,410)

 async def test_quota_error(self):
  client=AsyncMock();client.post.return_value=MagicMock(is_success=False,status_code=429);manager=AsyncMock();manager.__aenter__.return_value=client
  with patch.dict('os.environ',{'GEMINI_API_KEY':'mock'}),patch.object(audio_review.httpx,'AsyncClient',return_value=manager):
   with self.assertRaisesRegex(ValueError,'quota'):await audio_review.review_audio(b'RIFF0000WAVE','q','')
  self.assertEqual(client.post.call_count,1)  # quota errors are never retried

 def gemini_client(self,*responses):
  client=AsyncMock();client.post.side_effect=list(responses);manager=AsyncMock();manager.__aenter__.return_value=client
  return client,manager

 async def test_transient_503_retried_then_succeeds(self):
  ok=MagicMock(is_success=True,status_code=200);ok.json.return_value={'candidates':[{'finishReason':'STOP','content':{'parts':[{'text':'{"reply":"Hi"}'}]}}]}
  client,manager=self.gemini_client(MagicMock(is_success=False,status_code=503),ok)
  with patch.dict('os.environ',{'GEMINI_API_KEY':'mock'}),patch.object(audio_review.httpx,'AsyncClient',return_value=manager),patch.object(audio_review.asyncio,'sleep',new=AsyncMock()) as sleep:
   out=await audio_review.gemini_json(None,'p',[{'text':'x'}],max_tokens=12288)
  self.assertEqual(out,{'reply':'Hi'});self.assertEqual(client.post.call_count,2);sleep.assert_awaited_once()
  self.assertEqual(client.post.call_args.kwargs['json']['generationConfig']['maxOutputTokens'],12288)

 async def test_transient_503_gives_up_after_bounded_attempts(self):
  client,manager=self.gemini_client(*[MagicMock(is_success=False,status_code=503) for _ in range(3)])
  with patch.dict('os.environ',{'GEMINI_API_KEY':'mock'}),patch.object(audio_review.httpx,'AsyncClient',return_value=manager),patch.object(audio_review.asyncio,'sleep',new=AsyncMock()):
   with self.assertRaisesRegex(ValueError,'temporarily unavailable \\(HTTP 503\\) after 3 attempts'):await audio_review.gemini_json(None,'p',[{'text':'x'}])
  self.assertEqual(client.post.call_count,3)

 async def test_network_error_retried(self):
  ok=MagicMock(is_success=True,status_code=200);ok.json.return_value={'candidates':[{'finishReason':'STOP','content':{'parts':[{'text':'{"a":1}'}]}}]}
  client,manager=self.gemini_client(httpx.ConnectTimeout('slow'),ok)
  with patch.dict('os.environ',{'GEMINI_API_KEY':'mock'}),patch.object(audio_review.httpx,'AsyncClient',return_value=manager),patch.object(audio_review.asyncio,'sleep',new=AsyncMock()):
   self.assertEqual(await audio_review.gemini_json(None,'p',[{'text':'x'}]),{'a':1})

if __name__=='__main__':unittest.main()
