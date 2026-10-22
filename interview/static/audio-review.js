/* Recorded audio is uploaded only after explicit review consent. No key in browser. */
(()=>{
function el(tag,text){const e=document.createElement(tag);if(text)e.textContent=text;return e;}
async function wav(blob){
 const ctx=new AudioContext();let decoded;
 try{decoded=await ctx.decodeAudioData(await blob.arrayBuffer());}finally{await ctx.close();}
 if(decoded.duration>125)throw Error('Please use a recording no longer than two minutes.');
 const offline=new OfflineAudioContext(1,Math.ceil(decoded.duration*16000),16000);
 const source=offline.createBufferSource();source.buffer=decoded;source.connect(offline.destination);source.start();
 const pcm=(await offline.startRendering()).getChannelData(0),buffer=new ArrayBuffer(44+pcm.length*2),v=new DataView(buffer);
 const str=(offset,s)=>{for(let i=0;i<s.length;i++)v.setUint8(offset+i,s.charCodeAt(i));};
 str(0,'RIFF');v.setUint32(4,36+pcm.length*2,true);str(8,'WAVE');str(12,'fmt ');v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,1,true);v.setUint32(24,16000,true);v.setUint32(28,32000,true);v.setUint16(32,2,true);v.setUint16(34,16,true);str(36,'data');v.setUint32(40,pcm.length*2,true);
 for(let i=0;i<pcm.length;i++){const x=Math.max(-1,Math.min(1,pcm[i]));v.setInt16(44+i*2,x<0?x*32768:x*32767,true);}
 return new Blob([buffer],{type:'audio/wav'});
}
function attach(card,t,text,isCurrent,auto,skills){
 const button=el('button','Analyze my recording with Gemini');button.className='primary';button.type='button';
 const status=el('p');status.setAttribute('role','status');const box=el('section');box.className='answer-improvement';box.hidden=true;
 const disclosure=el('p','Sends this recording, its question and your skill goals to Google Gemini for transcription and feedback. No resume is sent. Free-tier data may be used to improve Google products.');disclosure.className='privacy';
 card.append(disclosure,button,status,box);
 button.onclick=async()=>{button.disabled=true;status.textContent='Listening to your recording and preparing feedback...';const original=text.value;
 try{const audio=await wav(t.blob);if(!isCurrent())return;
 const r=await fetch('/api/audio-review?'+new URLSearchParams({question:t.question,skills}),{method:'POST',headers:{'Content-Type':'audio/wav'},body:audio});const data=await r.json();if(!r.ok)throw Error(data.detail||'Audio review failed.');if(!isCurrent())return;
 t.audio_review=data;box.replaceChildren();box.hidden=false;
 box.className='review-report';
 const heading=el('div');heading.className='review-heading';heading.append(el('span','YOUR ANSWER REVIEW'),el('h3','One answer. A clearer next step.'));box.append(heading);
 const overview=el('div');overview.className='review-overview';overview.append(el('p',data.summary));box.append(overview);
 const focus=el('div');focus.className='review-priority';focus.append(el('span','FOCUS FOR YOUR NEXT TRY'),el('p',data.retry_focus));box.append(focus);
 const strength=el('p',data.strength);strength.className='review-strength';box.append(strength);
 function detail(title,copy){const d=el('details'),summary=el('summary',title);d.className='review-detail';d.append(summary,el('p',copy));box.append(d);return d;}
 const analysis=detail('Explore the feedback','');
 for(const [title,key] of [['Structure','structure'],['Language clarity','language'],['Technical reasoning','knowledge'],['Delivery ? AI estimate','delivery']]){const section=el('section');section.append(el('h4',title),el('p',data[key]));analysis.append(section);}
 for(const e of data.evidence||[]){const quote=el('blockquote',e.quote);analysis.append(quote,el('p',e.observation+' '+e.suggestion));}
 const draft=detail('A clearer version of your answer',data.improved_answer);draft.append(el('p','Suggested draft: verify every fact and fill in missing details truthfully.'));
 for(const q of data.missing_details||[])draft.append(el('p',q));
 detail('Your transcript',data.transcript);
 const source=el('p',data.source);source.className='privacy';box.append(source);
 const retry=el('button','Practice this answer again');retry.className='secondary';retry.onclick=()=>{if(window.localPractice?.chooseQuestion(t.question)){$('local-focus').value=data.retry_focus||'';speak(t.question);}};box.append(retry);
 if(window.practiceQuestions){const next=el('button','Ask me a follow-up');next.className='secondary';next.onclick=()=>window.practiceQuestions.followup(t);box.append(next);}

 if(text.value===original&&!t.userEdited){text.value=data.transcript;text.oninput();}
 status.textContent='Review ready. Your original recording is unchanged.';
 }catch(e){if(isCurrent())status.textContent=e.message+' Your recording is still available.';}finally{if(isCurrent())button.disabled=false;}};
 if(auto)button.onclick();
}
window.audioReview={attach,wav};
})();
