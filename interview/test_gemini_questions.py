import unittest
from unittest.mock import AsyncMock, patch
import httpx
import server
from gemini_questions import PracticeQuestion

class QuestionTests(unittest.IsolatedAsyncioTestCase):
 async def test_endpoint_context_and_validation(self):
  async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.app),base_url='http://127.0.0.1:8766') as c:
   with patch.object(server,'practice_question',new=AsyncMock(return_value={'question':'How did you test the fix?','reason':'Verification'})) as generate:
    r=await c.post('/api/practice-question',json={'brief':{'role':'Intern','skills':'Clarity','round':'technical','duration':'5'},'previous_question':'Describe a bug.','previous_answer':'I fixed an index.','asked':['Describe a bug.']})
    self.assertEqual(r.status_code,200)
    self.assertEqual(generate.call_args.args[0]['skills'],'Clarity')
    self.assertEqual(generate.call_args.args[2],'I fixed an index.')
    r=await c.post('/api/practice-question',json={'brief':{'role':'Intern'},'previous_answer':'x'*12001});self.assertEqual(r.status_code,422)
    r=await c.post('/api/practice-question',json={'brief':{'role':'Intern'},'asked':['x'*1001]});self.assertEqual(r.status_code,400)
 def test_empty_question_rejected(self):
  with self.assertRaises(ValueError):PracticeQuestion(question='',reason='')

if __name__=='__main__':unittest.main()
