import asyncio
import copy
import json
import unittest
from unittest.mock import AsyncMock, patch
import httpx
import server
import live_interview as live
import pressure_replay as replay
from test_live_interview import Provider

QUESTION='What did you personally change and how did you check it?'
BEFORE='We made the dashboard better. It worked well.'
AFTER='I added pagination and tested loading on a slow connection.'
FOLLOWUP='What if your users have fast connections but ten times more records?'
CHALLENGE='I would measure query time before choosing an index.'

def parent():
 return {'brief':{'role':'Intern','duration':'5'},'interview_ended':True,'interview_turns':[
  {'role':'assistant','text':QUESTION},{'role':'user','text':BEFORE}],
  'interview_review':{'answers':[{'question':'A model paraphrase','quote':'It worked well.',
                                'improvement':'Explain your own change and how you checked it.'}]}}
def report():
 return {'verdict':'clearer','summary':'More specific','changes':[{'before_quote':'It worked well.','after_quote':'I added pagination','observation':'Names an action.'}],
         'remaining_gap':'Explain the result.','follow_up_quote':CHALLENGE,'follow_up_feedback':'Names a measurement first.','next_step':'Add a truthful result.'}
def ready():
 s=replay.make_replay(parent(),0);s.update(interview_ended=True,replay_answers=[{'question':QUESTION,'answer':AFTER,'partial':False},{'question':FOLLOWUP,'answer':CHALLENGE,'partial':False}]);return s

class ReplayTests(unittest.IsolatedAsyncioTestCase):
 def test_choices_use_exact_question_and_unique_answer(self):
  p=parent();m=replay.replay_options(p)[0];self.assertEqual(m['question'],QUESTION);self.assertEqual(m['before'],BEFORE)
  p['interview_turns'] += p['interview_turns'];self.assertEqual(replay.replay_options(p),[])
 def test_replay_rejects_active_missing_and_recursive_choices(self):
  p=parent();p['interview_active']=True
  with self.assertRaises(ValueError):replay.make_replay(p,0)
  p['interview_active']=False
  with self.assertRaises(ValueError):replay.make_replay(p,4)
  child=replay.make_replay(p,0);child['interview_ended']=True
  with self.assertRaises(ValueError):replay.make_replay(child,0)
 def test_parent_not_modified(self):
  p=parent();original=copy.deepcopy(p);child=replay.make_replay(p,0);child['brief']['role']='Changed';child['replay_moment']['before']='Changed'
  self.assertEqual(p,original);self.assertEqual(child['duration_seconds'],90)
 def test_fragments_and_interruption_do_not_count_as_extra_answers(self):
  t=replay.ReplayTurns(QUESTION);t.feed({'outputTranscription':{'text':QUESTION},'turnComplete':True})
  t.feed({'inputTranscription':{'text':'I added '},'interrupted':True});self.assertFalse(t.feed({'turnComplete':True}))
  self.assertFalse(t.feed({'inputTranscription':{'text':'pagination.'},'outputTranscription':{'text':FOLLOWUP},'turnComplete':True}))
  self.assertEqual(t.snapshot()[0]['answer'],'I added pagination.')
  self.assertTrue(t.feed({'inputTranscription':{'text':CHALLENGE},'turnComplete':True}))
  self.assertEqual(t.snapshot()[1]['question'],FOLLOWUP)
 def test_partial_answer_kept_separate(self):
  t=replay.ReplayTurns(QUESTION);t.feed({'inputTranscription':{'text':'I added'}})
  self.assertTrue(t.snapshot()[0]['partial'])
 async def test_comparison_uses_retry_not_followup_for_evidence(self):
  s=ready();out=report();out['changes'].append({'before_quote':'It worked well.','after_quote':CHALLENGE,'observation':'Invalid comparison'})
  with patch.object(replay,'gemini_json',new=AsyncMock(return_value=out)) as model:
   result=await replay.compare_replay(s);await replay.compare_replay(s)
  self.assertEqual(len(result['changes']),1);self.assertEqual(model.await_count,1);self.assertEqual(result['challenge']['answer'],CHALLENGE)
 async def test_invalid_quotes_cannot_claim_improvement(self):
  s=ready();out=report();out['changes'][0]['before_quote']='Invented';out['follow_up_quote']='Invented'
  with patch.object(replay,'gemini_json',new=AsyncMock(return_value=out)):
   result=await replay.compare_replay(s)
  self.assertEqual(result['verdict'],'insufficient_evidence');self.assertEqual(result['follow_up_quote'],'')
 async def test_identical_and_partial_answers_not_claimed_as_improved(self):
  for text,partial,expected in [(BEFORE,False,'not_yet'),(AFTER,True,'insufficient_evidence')]:
   s=ready();s['replay_answers'][0].update(answer=text,partial=partial)
   with patch.object(replay,'gemini_json',new=AsyncMock(return_value=report())):self.assertEqual((await replay.compare_replay(s))['verdict'],expected)
 async def test_no_analysis_before_end_or_without_answer(self):
  s=ready();s['interview_active']=True
  with patch.object(replay,'gemini_json',new=AsyncMock()) as model:
   with self.assertRaises(ValueError):await replay.compare_replay(s)
   s['interview_active']=False;s['replay_answers']=[]
   with self.assertRaises(ValueError):await replay.compare_replay(s)
   model.assert_not_called()
 async def test_live_replay_auto_ends_after_two_answers(self):
  events=[{'serverContent':c} for c in [
   {'outputTranscription':{'text':QUESTION},'turnComplete':True},
   {'inputTranscription':{'text':AFTER}},
   {'outputTranscription':{'text':FOLLOWUP},'turnComplete':True},
   {'inputTranscription':{'text':CHALLENGE}},
   {'outputTranscription':{'text':'Thank you.'},'turnComplete':True}]]
  provider=Provider(events);ws=AsyncMock();ws.receive.side_effect=lambda:None
  async def wait():await asyncio.Future()
  ws.receive.side_effect=wait;s=replay.make_replay(parent(),0)
  with patch.dict('os.environ',{'GEMINI_API_KEY':'fake'}),patch.object(live,'connect',return_value=provider):
   await asyncio.wait_for(live.run_interview(ws,s),2)
  self.assertEqual(len(s['replay_answers']),2);self.assertTrue(s['interview_ended']);self.assertEqual(s['replay_answers'][0]['answer'],AFTER)
  setup=provider.sent[0]['setup']['systemInstruction']['parts'][0]['text'];self.assertIn('exactly ONE',setup)
  self.assertFalse(any('two minutes remain' in json.dumps(m) for m in provider.sent))
 async def test_create_route_cascading_clear_and_mcp_comparison(self):
  sid=server.create_session(server.Brief(role='Intern'))['session_id'];server.sessions[sid].update(parent());saved=copy.deepcopy(server.sessions[sid]);child=None
  try:
   async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.app),base_url='http://127.0.0.1:8766') as c:
    response=await c.post('/api/interview/replay',json={'session_id':sid,'answer_index':0});self.assertEqual(response.status_code,200);child=response.json()['session_id']
    self.assertEqual(server.sessions[sid],saved);self.assertNotEqual(child,sid)
    server.sessions[child].update(ready())
    with patch.object(replay,'gemini_json',new=AsyncMock(return_value=report())),patch.object(server,'via_mcp',new=AsyncMock(return_value={'tool':'compare_answer_texts'})) as mcp:
     compared=await c.post('/api/interview/replay-review',json={'session_id':child})
    self.assertEqual(compared.status_code,200);self.assertEqual(mcp.call_args.kwargs['arguments']['after'],AFTER)
    await c.post('/api/clear',json={'session_id':sid});self.assertNotIn(child,server.sessions)
  finally:
   server.sessions.pop(sid,None);server.sessions.pop(child,None)

if __name__=='__main__':unittest.main()
