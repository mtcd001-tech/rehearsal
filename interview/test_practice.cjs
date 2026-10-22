// Pure unit tests: mocked browser APIs, no microphone or UI automation.
const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
function fixture(){
 const elements=new Map(),downloads=[],tracks=[],recorders=[];
 function element(){return {value:'0',disabled:false,hidden:false,children:[],textContent:'',append(...xs){this.children.push(...xs);},querySelectorAll(){return [];},scrollIntoView(){},click(){downloads.push(this);},getContext(){return {clearRect(){},beginPath(){},moveTo(){},lineTo(){},stroke(){}};}};}
 const $=id=>{if(!elements.has(id))elements.set(id,element());return elements.get(id);};
 const window={MediaRecorder:true,addEventListener(){}};
 const navigator={mediaDevices:{getUserMedia:async()=>{const t={stopped:false,stop(){this.stopped=true;}};tracks.push(t);return {getTracks:()=>[t]};}}};
 class Recorder{static isTypeSupported(){return true;}constructor(){this.state='inactive';this.mimeType='audio/webm';recorders.push(this);}start(){this.state='recording';}stop(){this.state='inactive';queueMicrotask(()=>{this.ondataavailable?.({data:new Blob(['audio'])});this.onstop?.();});}}
 const ctx={window,navigator,MediaRecorder:Recorder,Blob,URL:{createObjectURL:()=> 'blob:test',revokeObjectURL(){}},document:{createElement:element},$,mode:'sample',reset:async()=>window.localPractice?.clear(),speak:async()=>{},cancelSpeech(){},state(){},toast(){},setInterval:()=>1,clearInterval(){},requestAnimationFrame:()=>1,cancelAnimationFrame(){},setTimeout:()=>1,AudioContext:class{constructor(){throw Error('No audio visualizer in unit test');}},Date,JSON,Number,String,Math};
 vm.runInNewContext(fs.readFileSync('static/practice.js','utf8'),ctx);
 return {$,ctx,tracks,recorders,downloads};
}
(async()=>{
 let f=fixture();await f.$('local-start').onclick();assert.equal(f.ctx.mode,'local');assert.equal(f.$('local-practice').hidden,false);await f.$('record').onclick();assert.equal(f.recorders[0].state,'recording');f.$('stop-record').onclick();assert.equal(f.$('record').disabled,true);await Promise.resolve();assert.equal(f.tracks[0].stopped,true);assert.equal(f.$('takes').children.length,1);assert.equal(f.$('record').disabled,false);assert.equal(f.$('local-notes').disabled,false);
 f.ctx.window.localPractice.clear();assert.equal(f.$('local-practice').hidden,true);assert.equal(f.$('local-notes').disabled,true);
 f=fixture();let grant;f.ctx.navigator.mediaDevices.getUserMedia=()=>new Promise(r=>grant=r);const pending=f.$('record').onclick();f.ctx.window.localPractice.clear();let stopped=false;grant({getTracks:()=>[{stop(){stopped=true;}}]});await pending;assert.equal(stopped,true);assert.equal(f.recorders.length,0);
 f=fixture();f.ctx.navigator.mediaDevices.getUserMedia=async()=>{const e=Error();e.name='NotAllowedError';throw e;};await f.$('record').onclick();assert.equal(f.$('record').disabled,false);assert.match(f.$('record-state').textContent,/declined/);
 console.log('PASS: record/stop saves a local take; reset clears; late permission releases microphone; permission denial recovers.');
})().catch(e=>{console.error(e);process.exitCode=1;});
