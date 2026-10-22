/* Rule-based answer checks from the local MCP tools. Only answer text is sent, and only to this app's loopback server. */
(()=>{
const STATUS={missing:'Missing',watch:'Worth a look',ok:'Clear'},MOVE={toward:'Moved toward the suggestion',same:'No change',away:'Moved away'};
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!==undefined)e.textContent=text;return e;}
function head(box,title,out){const top=el('div','rule-head');const left=el('div');left.append(el('span','eyebrow',title),el('p','rule-tool',`${out.tool}${out.protocol?' · MCP '+out.protocol+' · Streamable HTTP':''} · deterministic, no AI model`));top.append(left);box.append(top);}
function quotes(list,cls){const wrap=el('div','rule-quotes');list.forEach(q=>wrap.append(el('q',cls,q)));return wrap;}
function renderCheck(box,out,title='RULE CHECK ON THE WORDS ALONE'){const r=out.result;box.replaceChildren();box.hidden=false;head(box,title,out);
 if(r.priority)box.append(el('p','rule-priority',`Start here: ${r.priority.label}. ${r.priority.suggestion}`));else box.append(el('p','rule-priority','Every checked signal is present. Next, practice a likely follow-up question.'));
 const list=el('div','rule-list');r.signals.forEach(s=>{const row=el('div','rule-row');const status=el('span','pill '+s.status,STATUS[s.status]||s.status);const body=el('div');body.append(el('strong','',s.label),el('p','',s.note));if(s.quotes.length)body.append(quotes(s.quotes,s.status==='ok'?'good':'flag'));if(s.status!=='ok')body.append(el('p','rule-suggestion',s.suggestion));row.append(status,body);list.append(row);});
 box.append(list,el('p','privacy',r.source));}
function renderCompare(box,out,title='RULE CHECK · FIRST TAKE VS RETRY'){const r=out.result;box.replaceChildren();box.hidden=false;head(box,title,out);box.append(el('p','rule-priority',r.summary));
 const list=el('div','rule-list');r.changes.forEach(c=>{const row=el('div','rule-row');const body=el('div');body.append(el('strong','',`${c.label}: ${c.before_count} → ${c.after_count}`));if(c.before_quotes.length)body.append(quotes(c.before_quotes,'flag'));if(c.after_quotes.length)body.append(quotes(c.after_quotes,'good'));row.append(el('span','pill '+(c.direction==='toward'?'ok':c.direction==='away'?'missing':'same'),MOVE[c.direction]),body);list.append(row);});
 box.append(list,el('p','rule-priority',`Next: ${r.next_step}`),el('p','privacy',`${r.note} ${r.before_words} → ${r.after_words} words. ${r.source}`));}
function renderError(box,e){box.replaceChildren(el('p','privacy','Rule check unavailable: '+e.message));box.hidden=false;}
window.answerChecks={check:(text,question='')=>api('/api/check',{text,question}),compare:(before,after)=>api('/api/compare-text',{before,after}),renderCheck,renderCompare,renderError};
})();
