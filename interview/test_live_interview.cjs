const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function element(){return {disabled:true,value:'30',hidden:true,children:[],style:{},classList:{add(){},remove(){}},append(...v){this.children.push(...v);},replaceChildren(){this.children=[];},insertBefore(){},addEventListener(){},showModal(){this.hidden=false;},close(){this.hidden=true;},click(){}};}
const nodes=new Map(),get=id=>{if(!nodes.has(id))nodes.set(id,element());return nodes.get(id);};get('stage').parentNode=element();get('stage').nextSibling=null;
let stopped=0,closed=0,requests=[],sockets=[],clock=0,intervals=[],permission=null;
class WS{static OPEN=1;constructor(){this.readyState=1;this.bufferedAmount=0;this.sent=[];sockets.push(this);}send(x){this.sent.push(x);}close(){this.readyState=3;this.onclose?.();}}
class AC{constructor(){this.audioWorklet={addModule:async()=>{}};this.currentTime=0;this.destination={};}async resume(){}async close(){closed++;}createMediaStreamSource(){return {connect(){},disconnect(){}};}createGain(){return {gain:{},connect(){},disconnect(){}};}}
const stream={getTracks:()=>[{stop(){stopped++;}}]};
const ctx={document:{getElementById:get,createElement:element,querySelector:()=>get('main'),querySelectorAll:()=>[],body:{style:{}}},window:{addEventListener(){}},navigator:{mediaDevices:{getUserMedia:()=>permission||Promise.resolve(stream)}},AudioContext:AC,AudioWorkletNode:class{constructor(){this.port={};}connect(){}disconnect(){}},WebSocket:WS,location:{protocol:'http:',host:'localhost:8766'},brief:{role:'Intern'},generation:0,disconnect(){},cancelSpeech(){},toast(){},Blob,URL,Int16Array,Date:{now:()=>clock},setInterval:f=>{intervals.push(f);return intervals.length;},clearInterval(){},setTimeout:()=>1,clearTimeout(){},fetch:async(path)=>{requests.push(path);return {ok:true,json:async()=>path==='/api/session'?{session_id:'s'}:path==='/api/interview/transcript'?{ended:true,turns:[{role:'user',text:'I tested it.'}]}:path==='/api/interview/review'?{summary:'Clear',strengths:[],priorities:[],answers:[]}:{} };}};
vm.runInNewContext(fs.readFileSync('static/interview.js','utf8'),ctx);
let PCM;const chunks=[];
vm.runInNewContext(fs.readFileSync('static/interview-pcm.js','utf8'),{AudioWorkletProcessor:class{constructor(){this.port={postMessage:b=>chunks.push(b)};}},sampleRate:48000,Int16Array,registerProcessor:(name,c)=>PCM=c});
const pcm=new PCM();for(let i=0;i<375;i++)pcm.process([[new Float32Array(128).fill(.5)]]);
assert.equal(chunks.reduce((n,b)=>n+b.byteLength,0),32000);assert.equal(new Int16Array(chunks[0])[0],16383);
const settle=async()=>{for(let i=0;i<25;i++)await Promise.resolve();};
(async()=>{
await get('interview-begin').onclick();const ws=sockets[0];ws.onmessage({data:JSON.stringify({type:'ready',remaining:1800})});
assert.equal(get('interview-room').hidden,false);assert.equal(requests.includes('/api/interview/review'),false);
clock=1800001;intervals.at(-1)();assert.equal(stopped,1);assert.ok(ws.sent.some(s=>s.includes('end')));assert.equal(requests.includes('/api/interview/review'),false);
ws.onclose();await settle();assert.equal(get('interview-results').hidden,false);assert.equal(requests.filter(p=>p==='/api/interview/review').length,1);assert.ok(closed>0);
get('interview-close-results').onclick();
let grant;permission=new Promise(r=>grant=r);const starting=get('interview-begin').onclick();await settle();get('interview-cancel').onclick();grant(stream);await starting;assert.equal(sockets.length,1);assert.equal(stopped,2);
console.log('PASS: no mid-interview review, timed end stops microphone, post-close analysis, late permission released after cancellation (mock browser/audio).');
})().catch(e=>{console.error(e);process.exitCode=1;});
