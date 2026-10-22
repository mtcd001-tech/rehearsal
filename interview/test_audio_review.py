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
 async def test_quota_error(self):
  client=AsyncMock();client.post.return_value=MagicMock(is_success=False,status_code=429);manager=AsyncMock();manager.__aenter__.return_value=client
  with patch.dict('os.environ',{'GEMINI_API_KEY':'mock'}),patch.object(audio_review.httpx,'AsyncClient',return_value=manager):
   with self.assertRaisesRegex(ValueError,'quota'):await audio_review.review_audio(b'RIFF0000WAVE','q','')

if __name__=='__main__':unittest.main()
