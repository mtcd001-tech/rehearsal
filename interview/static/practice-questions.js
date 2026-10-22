/* Gemini question generation is explicit; only disclosed data leaves this app. */
(()=>{
let version=0,controller=null,asked=[];
const button=$('tailored-question'),status=$('question-status');
function cancel(){version++;controller?.abort();controller=null;button.disabled=false;status.textContent='';asked=[];}
async function generate(t){
 if(!window.localPractice?.canChange()){status.textContent='Finish recording first. If you have four takes, download your notes and Reset.';return;}
 controller?.abort();const gen=++version;controller=new AbortController();button.disabled=true;status.textContent='Maya is preparing a question...';
 try{const response=await fetch('/api/practice-question',{method:'POST',headers:{'Content-Type':'application/json'},signal:controller.signal,body:JSON.stringify({brief,previous_question:t?.question||'',previous_answer:(t?.transcript||t?.audio_review?.transcript||'').slice(0,12000),asked:asked.slice(-20)})});const data=await response.json();if(!response.ok)throw Error(data.detail||'Could not prepare a question.');if(gen!==version)return;
 if(window.localPractice.chooseQuestion(data.question)){asked.push(data.question);status.textContent=data.reason+' Listen with Hear the question, then record your answer.';}
 else status.textContent='Question was not changed. Finish recording and try again.';
 }catch(e){if(gen===version&&e.name!=='AbortError')status.textContent=e.message;}finally{if(gen===version)button.disabled=false;}
}
button.onclick=()=>generate();window.practiceQuestions={cancel,followup:generate};
})();
