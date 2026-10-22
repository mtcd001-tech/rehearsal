import asyncio
import json
import unittest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
import live_interview as live
import server

class Socket:
 def __init__(self): self.sent=[];self.commands=asyncio.Queue()
 async def send_json(self,msg):
  self.sent.append(msg)
  if msg['type']=='content':await self.commands.put({'type':'websocket.receive','text':'{"type":"end"}'})
 async def receive(self): return await self.commands.get()
 async def close(self): pass

class Provider:
 def __init__(self,events):self.events=events;self.sent=[]
 async def send(self,msg): self.sent.append(json.loads(msg))
 async def recv(self):return '{"setupComplete":{}}'
 async def __aenter__(self):return self
 async def __aexit__(self,*args):pass
 async def __aiter__(self):
  for event in self.events:yield json.dumps(event)
  await asyncio.Future()

class LiveTests(unittest.IsolatedAsyncioTestCase):
 def state(self):return {'brief':{'role':'Intern','duration':'30'}}
 async def test_review_locked_during_interview(self):
  with patch.object(live,'gemini_json',new=AsyncMock()) as model:
   with self.assertRaisesRegex(ValueError,'after'):await live.final_review({'interview_active':True})
   model.assert_not_called()
 async def test_empty_interview_not_fabricated(self):
  with self.assertRaisesRegex(ValueError,'No spoken'):await live.final_review({'interview_ended':True,'interview_turns':[]})
 async def test_review_filters_evidence_and_caches(self):
  state=self.state();state.update(interview_ended=True,interview_turns=[{'role':'user','text':'I tested it.'}])
  report={'summary':'Review','answers':[{'quote':'invented'},{'quote':'I tested it.'}]}
  with patch.object(live,'gemini_json',new=AsyncMock(return_value=report)) as model:
   first=await live.final_review(state);second=await live.final_review(state)
   self.assertEqual(len(first['answers']),1);self.assertIs(first,second);self.assertEqual(model.await_count,1)
 async def test_end_releases_provider_and_unlocks_review(self):
  provider=Provider([{'serverContent':{'inputTranscription':{'text':'I tested it.'}}}]);ws=Socket();state=self.state()
  with patch.dict('os.environ',{'GEMINI_API_KEY':'fake'}),patch.object(live,'connect',return_value=provider):
   await asyncio.wait_for(live.run_interview(ws,state),3)
  self.assertTrue(state['interview_ended']);self.assertFalse(state['interview_active'])
  self.assertEqual(state['interview_turns'][0]['text'],'I tested it.')
  self.assertIn('ended',[m['type'] for m in ws.sent]);self.assertIn('contextWindowCompression',provider.sent[0]['setup'])
 async def test_resumes_goaway_without_restarting_interview(self):
  first=Provider([{'sessionResumptionUpdate':{'resumable':True,'newHandle':'resume-token'}},{'goAway':{}}])
  second=Provider([{'serverContent':{'inputTranscription':{'text':'Continuing.'}}}]);ws=Socket();state=self.state()
  with patch.dict('os.environ',{'GEMINI_API_KEY':'fake'}),patch.object(live,'connect',side_effect=[first,second]):
   await asyncio.wait_for(live.run_interview(ws,state),3)
  self.assertEqual(second.sent[0]['setup']['sessionResumption']['handle'],'resume-token')
  self.assertFalse(any('clientContent' in x for x in second.sent))
  self.assertIn('reconnecting',[m['type'] for m in ws.sent])
 async def test_timer_ends_without_button(self):
  state=self.state();state['brief']['duration']='0';ws=Socket()
  with patch.dict('os.environ',{'GEMINI_API_KEY':'fake'}),patch.object(live,'connect',return_value=Provider([])):
   await asyncio.wait_for(live.run_interview(ws,state),1)
  self.assertTrue(state['interview_ended']);self.assertIn('ended',[m['type'] for m in ws.sent])
 async def test_upstream_error_is_sanitized(self):
  ws=Socket();state=self.state()
  with patch.dict('os.environ',{'GEMINI_API_KEY':'fake'}),patch.object(live,'connect',side_effect=RuntimeError('secret-value')):
   await live.run_interview(ws,state)
  self.assertNotIn('secret-value',json.dumps(ws.sent));self.assertTrue(state['interview_ended'])
 def test_transcript_fragments_and_limit(self):
  state={'interview_turns':[]};live.capture_transcripts(state,{'inputTranscription':{'text':'I '}});live.capture_transcripts(state,{'inputTranscription':{'text':'tested.'}})
  self.assertEqual(state['interview_turns'],[{'role':'user','text':'I tested.'}])
  with self.assertRaises(ValueError):live.capture_transcripts(state,{'inputTranscription':{'text':'a'*180001}})
 def test_cross_origin_websocket_rejected(self):
  with TestClient(server.app) as client:
   with self.assertRaises(Exception):
    with client.websocket_connect('/api/interview/live?session_id=none',headers={'origin':'https://other.example'}):pass

if __name__=='__main__':unittest.main()
