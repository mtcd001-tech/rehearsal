const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('static/app.js','utf8');
const clock=source.slice(source.indexOf('function clock()'),source.indexOf('function addTurn('));
for(const mode of ['text','sample'])for(const duration of ['5','15','30']){
 let now=0,tick,stops=0,messages=[];
 const ctx={mode,brief:{duration},clockTimer:null,started:0,Date:{now:()=>now},clearInterval(){},setInterval(fn){tick=fn;},$:()=>({textContent:''}),disconnect(){stops++;},toast(m){messages.push(m);}};
 vm.runInNewContext(clock+';clock();',ctx);
 now=Number(duration)*60000-1000;tick();assert.equal(messages.length,0);
 now+=1000;tick();tick();assert.equal(stops,0);assert.equal(messages.length,mode==='sample'?0:1);
}
console.log('PASS: duration boundaries, single reminder, text continues, sample unaffected (mock timers).');
