// Self-view camera in the interview room: opt-in, video-only, local only, released on every exit (mock browser APIs).
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
function element(){return {disabled:true,value:'15',hidden:true,checked:false,children:[],style:{},textContent:'',classList:{set:new Set(),add(c){this.set.add(c);},remove(c){this.set.delete(c);},contains(c){return this.set.has(c);}},append(...v){this.children.push(...v);},replaceChildren(){this.children=[];},insertBefore(){},addEventListener(){},showModal(){this.hidden=false;},close(){this.hidden=true;},click(){},options:[]};}
const nodes=new Map(),get=id=>{if(!nodes.has(id))nodes.set(id,element());return nodes.get(id);};get('stage').parentNode=element();get('stage').nextSibling=null;
const requests=[],sockets=[],intervals=[],media=[];let clock=0,micStops=0,camStops=0,cameraFails=false;
class WS{static OPEN=1;constructor(){this.readyState=1;this.bufferedAmount=0;this.sent=[];sockets.push(this);}send(x){this.sent.push(x);}close(){this.readyState=3;this.onclose?.();}}
class AC{constructor(){this.audioWorklet={addModule:async()=>{}};this.currentTime=0;this.destination={};}async resume(){}async close(){}createMediaStreamSource(){return {connect(){},disconnect(){}};}createGain(){return {gain:{},connect(){},disconnect(){}};}}
const getUserMedia=async constraints=>{media.push(constraints);if(constraints.video){if(cameraFails)throw Object.assign(Error('denied'),{name:'NotAllowedError'});return {kind:'camera',getTracks:()=>[{stop(){camStops++;}}]};}return {kind:'mic',getTracks:()=>[{stop(){micStops++;}}]};};
const ctx={document:{getElementById:get,createElement:element,querySelector:()=>get('main'),querySelectorAll:()=>[],body:{style:{}}},window:{addEventListener(){}},navigator:{mediaDevices:{getUserMedia}},AudioContext:AC,AudioWorkletNode:class{constructor(){this.port={};}connect(){}disconnect(){}},WebSocket:WS,location:{protocol:'http:',host:'localhost:8766'},brief:{role:'Intern'},generation:0,disconnect(){},cancelSpeech(){},toast(){},Blob,URL,Int16Array,Date:{now:()=>clock},setInterval:f=>{intervals.push(f);return intervals.length;},clearInterval(){},setTimeout:()=>1,clearTimeout(){},fetch:async path=>{requests.push(path);return {ok:true,json:async()=>path==='/api/session'?{session_id:'s'}:path==='/api/interview/transcript'?{turns:[]}:{}};}};
vm.runInNewContext(fs.readFileSync('static/interview.js','utf8'),ctx);
const settle=async()=>{for(let i=0;i<25;i++)await Promise.resolve();};
(async()=>{
 // Unticked: only the microphone is requested.
 await get('interview-begin').onclick();await settle();
 assert.equal(media.length,1);assert.equal(media[0].video,false);assert.equal(get('self-view-tile').hidden,true);
 sockets[0].onclose();await settle();get('interview-close-results').onclick();
 // Ticked: a separate video-only stream is shown locally and never sent.
 get('interview-camera').checked=true;media.length=0;
 await get('interview-begin').onclick();await settle();
 assert.equal(media.length,2);assert.ok(media[1].video);assert.equal(media[1].audio,false);
 assert.equal(get('self-view').srcObject.kind,'camera');assert.equal(get('self-view-tile').hidden,false);assert.equal(get('self-view-label').textContent,'You');
 const ws=sockets[1];ws.onmessage({data:JSON.stringify({type:'ready',remaining:900})});
 assert.ok(ws.sent.every(m=>typeof m!=='object'||!m.kind),'camera stream must never be sent');
 // Toggle off releases the camera; toggle on asks again.
 get('camera-toggle').onclick();assert.equal(camStops,1);assert.equal(get('self-view').srcObject,null);assert.match(get('self-view-label').textContent,/camera off/);
 get('camera-toggle').onclick();await settle();assert.equal(media.filter(m=>m.video).length,2);assert.equal(get('self-view').srcObject.kind,'camera');
 // Ending the interview stops both microphone and camera and hides the tile.
 clock=900001;intervals.at(-1)();ws.onclose();await settle();
 assert.equal(camStops,2);assert.ok(micStops>=2);assert.equal(get('self-view-tile').hidden,true);assert.equal(get('self-view').srcObject,null);
 get('interview-close-results').onclick();
 // Camera denied: the interview continues with audio only.
 cameraFails=true;media.length=0;await get('interview-begin').onclick();await settle();
 assert.equal(get('interview-room').hidden,false);assert.equal(get('self-view-tile').hidden,true);assert.match(get('interview-room-note').textContent,/audio only/);
 console.log('PASS: camera is opt-in and video-only, shown locally, toggles off/on, released at the end, and a denial keeps the audio interview running (mock browser).');
})().catch(e=>{console.error(e);process.exitCode=1;});
