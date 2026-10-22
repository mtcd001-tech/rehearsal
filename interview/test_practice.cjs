// Pure unit tests: mocked browser APIs, no microphone or UI automation.
const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
function fixture(){
 const elements=new Map(),downloads=[],tracks=[],recorders=[],calls=[];
 function element(){return {value:'0',disabled:false,hidden:false,children:[],textContent:'',set innerHTML(v){this.children=[];},append(...xs){this.children.push(...xs);},querySelectorAll(){return [];},scrollIntoView(){},focus(){},click(){downloads.push(this);},getContext(){return {clearRect(){},beginPath(){},moveTo(){},lineTo(){},stroke(){}};}};}
 const $=id=>{if(!elements.has(id))elements.set(id,element());return elements.get(id);};
 const window={MediaRecorder:true,addEventListener(){}};
 const navigator={mediaDevices:{getUserMedia:async()=>{const t={stopped:false,stop(){this.stopped=true;}};tracks.push(t);return {getTracks:()=>[t]};}}};
 class Recorder{static isTypeSupported(){return true;}constructor(){this.state='inactive';this.mimeType='audio/webm';recorders.push(this);}start(){this.state='recording';}stop(){this.state='inactive';queueMicrotask(()=>{this.ondataavailable?.({data:new Blob(['audio'])});this.onstop?.();});}}
 const ctx={window,navigator,MediaRecorder:Recorder,Blob,URL:{createObjectURL:()=> 'blob:test',revokeObjectURL(){}},document:{createElement:element},$,mode:'sample',reset:async()=>window.localPractice?.clear(),speak:async()=>{},cancelSpeech(){},state(){},answerChecks:{check:async(text,question)=>{calls.push(['check',text,question]);return {result:{signals:[],priority:null},tool:'check_answer_text',protocol:'2025-11-25'};},compare:async(before,after)=>{calls.push(['compare',before,after]);return {result:{summary:'s',changes:[]},tool:'compare_answer_texts',protocol:'2025-11-25'};},renderCheck(box){box.hidden=false;box.rendered=(box.rendered||0)+1;},renderCompare(box){box.hidden=false;box.rendered=(box.rendered||0)+1;},renderError(box,e){box.error=e.message;}},toast(){},setInterval:()=>1,clearInterval(){},requestAnimationFrame:()=>1,cancelAnimationFrame(){},setTimeout:()=>1,AudioContext:class{constructor(){throw Error('No audio visualizer in unit test');}},Date,JSON,Number,String,Math};
 vm.runInNewContext(fs.readFileSync('static/practice.js','utf8'),ctx);
 return {$,ctx,tracks,recorders,downloads,calls};
}
(async()=>{
 let f=fixture();await f.$('local-start').onclick();assert.equal(f.ctx.mode,'local');assert.equal(f.$('local-practice').hidden,false);await f.$('record').onclick();assert.equal(f.recorders[0].state,'recording');f.$('stop-record').onclick();assert.equal(f.$('record').disabled,true);await Promise.resolve();assert.equal(f.tracks[0].stopped,true);assert.equal(f.$('takes').children.length,1);assert.equal(f.$('record').disabled,false);assert.equal(f.$('local-notes').disabled,false);
 f.ctx.window.localPractice.clear();assert.equal(f.$('local-practice').hidden,true);assert.equal(f.$('local-notes').disabled,true);
 f=fixture();let grant;f.ctx.navigator.mediaDevices.getUserMedia=()=>new Promise(r=>grant=r);const pending=f.$('record').onclick();f.ctx.window.localPractice.clear();let stopped=false;grant({getTracks:()=>[{stop(){stopped=true;}}]});await pending;assert.equal(stopped,true);assert.equal(f.recorders.length,0);
 f=fixture();f.ctx.navigator.mediaDevices.getUserMedia=async()=>{const e=Error();e.name='NotAllowedError';throw e;};await f.$('record').onclick();assert.equal(f.$('record').disabled,false);assert.match(f.$('record-state').textContent,/declined/);
 // Typed takes: rule check is gated on text, sends only the typed text, and stores the result.
 f=fixture();await f.$('local-start').onclick();f.$('type-take').onclick();let card=f.$('takes').children[0],area=card.children[2].children[0],actions=card.children[4],check=actions.children[0],box=card.children[5];
 assert.equal(card.children.some(c=>c.controls),false);assert.equal(actions.children.length,1);assert.equal(check.disabled,true);
 area.value='I inspected the slow query and wrote tests.';area.oninput();assert.equal(check.disabled,false);await check.onclick();
 assert.deepEqual(f.calls[0],['check','I inspected the slow query and wrote tests.',f.ctx.$('local-question').value==='0'?'Tell me about a time you solved a technical problem in a team project. What did you personally contribute?':'']);assert.equal(box.rendered,1);assert.equal(f.$('compare-takes').disabled,true);
 f.$('type-take').onclick();const area2=f.$('takes').children[1].children[2].children[0];area2.value='In my team I owned search, profiled queries, and added an index.';area2.oninput();assert.equal(f.$('compare-takes').disabled,false);
 await f.$('compare-takes').onclick();assert.deepEqual(f.calls[1],['compare','I inspected the slow query and wrote tests.','In my team I owned search, profiled queries, and added an index.']);assert.equal(f.$('take-compare').rendered,1);
 // A reset while a check is in flight must not render stale results.
 let release;f.ctx.answerChecks.check=()=>new Promise(r=>release=r);f=Object.assign(f,{});const stale=f.$('takes').children[0];const pendingCheck=stale.children[4].children[0].onclick();f.ctx.window.localPractice.clear();release({result:{},tool:'t'});await pendingCheck;assert.equal(stale.children[5].rendered,1);assert.equal(f.$('compare-takes').disabled,true);
 for(let i=0;i<5;i++)f.$('type-take').onclick();assert.equal(f.$('takes').children.length,4);
 console.log('PASS: record/stop saves a local take; reset clears; late permission releases microphone; permission denial recovers; typed takes check and compare text; stale checks ignored after reset; four-take limit.');
})().catch(e=>{console.error(e);process.exitCode=1;});
