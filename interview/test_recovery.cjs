const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const code=fs.readFileSync('static/app.js','utf8');const nodes=new Map();const $=id=>{if(!nodes.has(id))nodes.set(id,{textContent:'stale',close(){this.closed=true;}});return nodes.get(id);};
const ctx={$,window:{},generation:0,sid:null,mode:'live',sample:{question:'Original sample question'},cancelSpeech(){},disconnect(){},setStep(){},state(t){ctx.lastState=t;},Promise};vm.createContext(ctx);
vm.runInContext(code.slice(code.indexOf('async function reset('),code.indexOf('async function textMode(')),ctx);
(async()=>{await ctx.reset();assert.equal($('question').textContent,'Original sample question');assert.equal($('question-label').textContent,'SAMPLE QUESTION');assert.equal($('coaching').hidden,true);assert.equal(ctx.mode,'sample');
console.log('PASS: reset restores question/state after mode change (mock DOM).');})().catch(e=>{console.error(e);process.exitCode=1;});
