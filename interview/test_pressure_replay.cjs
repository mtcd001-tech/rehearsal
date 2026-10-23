const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function element(){return {disabled:true,value:'5',hidden:true,checked:false,children:[],style:{},classList:{add(){},remove(){},contains(){return false;}},append(...v){this.children.push(...v);},replaceChildren(){this.children=[];},insertBefore(){},addEventListener(){},showModal(){this.hidden=false;},close(){this.hidden=true;},click(){}};}
const nodes=new Map(),get=id=>{if(!nodes.has(id))nodes.set(id,element());return nodes.get(id);};get('stage').parentNode=element();get('stage').nextSibling=null;
const requests=[],sockets=[],timers=[];let stopped=0,download,denied=false,empty=false;
class WS{static OPEN=1;constructor(){this.readyState=1;this.bufferedAmount=0;sockets.push(this);}send(){}close(){this.readyState=3;this.onclose?.();}}
class AC{constructor(){this.audioWorklet={addModule:async()=>{}};this.destination={};}async resume(){}async close(){}createMediaStreamSource(){return {connect(){},disconnect(){}};}createGain(){return {gain:{},connect(){},disconnect(){}};}}
const moment={answer_index:0,question:'What did you change?',quote:'We improved it.',before:'We improved it.',focus:'Name your action.'};
const original={summary:'Original debrief',strengths:[],priorities:[],answers:[],replay_options:[moment]};
const comparison={verdict:'clearer',summary:'The retry names an action.',changes:[{before_quote:'We improved it.',after_quote:'I added pagination.',observation:'Names ownership.'}],remaining_gap:'Explain testing.',next_step:'Explain your checks.',challenge:null,follow_up_feedback:'No challenge answer.',source:'Test',moment,retry:{answer:'I added pagination.'}};
const ctx={document:{getElementById:get,createElement:element,querySelector:()=>get('main'),querySelectorAll:()=>[],body:{style:{}}},window:{addEventListener(){}},navigator:{mediaDevices:{getUserMedia:async()=>{if(denied)throw Error('Microphone denied');return {getTracks:()=>[{stop(){stopped++;}}]};}}},AudioContext:AC,AudioWorkletNode:class{constructor(){this.port={};}connect(){}disconnect(){}},WebSocket:WS,location:{protocol:'http:',host:'localhost:8766'},brief:{role:'Intern'},generation:0,disconnect(){},cancelSpeech(){},toast(){},Blob,URL:{createObjectURL:b=>{download=b;return 'blob:test';},revokeObjectURL(){}},Int16Array,Date,setInterval:f=>{timers.push(f);return timers.length;},clearInterval(){},setTimeout:()=>1,clearTimeout(){},fetch:async(path,opt)=>{
 const body=JSON.parse(opt.body);requests.push({path,body});let data={};
 if(path==='/api/session')data={session_id:'original'};
 if(path==='/api/interview/replay')data={session_id:'child',moment,duration_seconds:90};
 if(path==='/api/interview/review')data=original;
 if(path==='/api/interview/replay-review')data=comparison;
 if(path==='/api/interview/transcript')data={ended:true,turns:body.session_id==='original'?[{role:'user',text:'We improved it.'}]:empty?[]:[{role:'user',text:'I added pagination.'}]};
 return {ok:true,json:async()=>data};}};
vm.runInNewContext(fs.readFileSync('static/interview.js','utf8'),ctx);
const settle=async()=>{for(let i=0;i<60;i++)await Promise.resolve();};
async function stop(ws){get('interview-end').onclick();ws.onclose();await settle();}
function ready(ws,remaining=90){ws.onmessage({data:JSON.stringify({type:'ready',remaining})});}
(async()=>{
 await get('interview-begin').onclick();ready(sockets[0],300);await stop(sockets[0]);
 assert.equal(get('pressure-replay').hidden,false);assert.equal(get('replay-quote').textContent,'We improved it.');
 const originalNodes=get('interview-report').children;
 await get('replay-start').onclick();ready(sockets[1]);assert.equal(get('interview-results').hidden,true);assert.equal(get('interview-end').textContent,'End replay');
 assert.equal(requests.find(r=>r.path==='/api/interview/replay').body.session_id,'original');
 assert.equal(requests.filter(r=>r.path==='/api/interview/replay-review').length,0);
 await stop(sockets[1]);assert.equal(get('interview-results').hidden,false);assert.equal(get('replay-result').hidden,false);
 assert.equal(get('interview-report').children,originalNodes);assert.equal(requests.filter(r=>r.path==='/api/interview/review').length,1);
 get('interview-export').onclick();const payload=JSON.parse(await download.text());assert.equal(payload.transcript[0].text,'We improved it.');assert.equal(payload.review.summary,'Original debrief');assert.equal(payload.replay.transcript[0].text,'I added pagination.');
 denied=true;await get('replay-start').onclick();assert.equal(get('interview-results').hidden,false);assert.match(get('replay-status').textContent,/original debrief is unchanged/);assert.equal(get('interview-report').children,originalNodes);denied=false;
 empty=true;await get('replay-start').onclick();ready(sockets[2]);sockets[2].onmessage({data:JSON.stringify({type:'error',message:'Quota unavailable'})});sockets[2].onclose();await settle();assert.match(get('replay-status').textContent,/original interview is unchanged/);assert.equal(requests.filter(r=>r.path==='/api/interview/replay-review').length,1);
 get('interview-close-results').onclick();assert.equal(requests.at(-1).body.session_id,'original');assert.ok(stopped>=3);
 console.log('PASS: replay creation/end-only comparison, original debrief preserved, combined export, permission/provider failures recover to original, parent cleanup (mock browser).');
})().catch(e=>{console.error(e);process.exitCode=1;});
