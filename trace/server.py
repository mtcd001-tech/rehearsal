import asyncio
import json
import os
import re
import sys
import uuid
from collections import OrderedDict
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from mcp.server.fastmcp import FastMCP
from mcp.client.streamable_http import streamable_http_client
from mcp import ClientSession
from pydantic import BaseModel, Field

from examples import EXAMPLES

ROOT = Path(__file__).parent
PORT = int(os.environ.get('PORT', '8765'))
mcp = FastMCP('Trace visual debugger', stateless_http=True, json_response=True)
runs = OrderedDict()
limit = asyncio.Semaphore(2)

class Program(BaseModel):
    source: str = Field(max_length=12000)

class Question(BaseModel):
    run_id: str
    question: str = Field(max_length=1000)
    step: int = 0

async def execute(source):
    async with limit:
        process = await asyncio.create_subprocess_exec(sys.executable, '-I', str(ROOT / 'tracer.py'), stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, cwd=str(ROOT))
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(json.dumps({'source': source}).encode()), timeout=4)
        except asyncio.TimeoutError:
            process.kill()
            await process.communicate()
            return {'source': source, 'steps': [], 'calls': [], 'error': {'type': 'ExecutionLimit', 'message': 'Execution exceeded four seconds. Reduce the input or simplify the program.'}, 'stdout': ''}
        if process.returncode:
            return {'source': source, 'steps': [], 'calls': [], 'error': {'type': 'WorkerError', 'message': 'The execution worker stopped. Simplify the input.'}, 'stdout': ''}
        return json.loads(stdout)

def get_run(run_id):
    if run_id not in runs:
        raise ValueError('This trace expired. Run the program again.')
    return runs[run_id]

@mcp.tool()
async def trace_python(source: str) -> dict:
    """Execute a small, trusted educational Python program and record its real trace. Returns an ID for inspection/navigation."""
    result = await execute(source)
    result['id'] = uuid.uuid4().hex
    runs[result['id']] = result
    while len(runs) > 24:
        runs.popitem(last=False)
    return {'run_id': result['id'], 'events': len(result['steps']), 'error': result['error'], 'stdout': result.get('stdout', '')}

@mcp.tool()
def inspect_step(run_id: str, step: int) -> dict:
    """Inspect a recorded execution event: source line, frames, object identities, output, and exception. Never infer values."""
    run = get_run(run_id)
    if not run['steps']:
        return {'error': run['error']}
    index = max(0, min(step, len(run['steps']) - 1))
    return run['steps'][index]

@mcp.tool()
def navigate_trace(run_id: str, target: str, current_step: int = 0, variable: str = '') -> dict:
    """Move the visual debugger to error, alias, change, return, start, end, next, or previous. Supply variable for change. Returns evidence and a selected step."""
    run = get_run(run_id)
    steps = run['steps']
    if not steps:
        return {'step': 0, 'message': str(run['error']), 'evidence': None}
    chosen = max(0, min(current_step, len(steps) - 1))
    message = 'Showing the recorded state at this execution event.'
    if target in ('start', 'end', 'next', 'previous'):
        chosen = {'start': 0, 'end': len(steps)-1, 'next': min(chosen+1, len(steps)-1), 'previous': max(0, chosen-1)}[target]
        message = f'Moved to event {chosen + 1}. Line events show state before the highlighted line executes.'
    elif target == 'error':
        found = next((s for s in steps if 'exception' in s), None)
        if found:
            chosen = found['index']
            message = f"{found['exception']['type']}: {found['exception']['message']}. This is the first recorded exception."
            a = found.get('access')
            if a and not a['valid']:
                message += f" {a['name']} has {a['length']} elements. Index {a['index']} does not refer to an element; valid nonnegative indices are 0 through {a['length']-1}."
        else:
            message = 'This run raised no exception. A wrong answer still needs an expected result to establish a logical bug.'
    elif target == 'alias':
        found = None
        for s in steps:
            for label, obj in s['heap'].items():
                refs = [v['ref'] for v in obj['items'] if isinstance(v, dict) and 'ref' in v]
                shared = next((v for v in refs if refs.count(v) > 1), None)
                if shared:
                    found = (s, label, shared, refs.count(shared))
                    break
            if found:
                break
        if found:
            s, label, shared, count = found
            chosen = s['index']
            message = f'{label} contains {count} references to the same object, {shared}. These are not independent snapshots. Mutating {shared} changes what every reference sees. Sharing is legal Python; whether it is a bug depends on your intended output.'
        else:
            message = 'No collection containing repeated references was recorded in this run.'
    elif target == 'return':
        found = next((s for s in steps if s['index'] > chosen and s['event'] == 'return'), None)
        if found:
            chosen = found['index']
            message = 'This frame is returning. Its recorded return value is shown above the call stack.'
        else:
            message = 'There is no later return event in this trace.'
    elif target == 'change':
        previous = None
        seen = False
        found = None
        for s in steps:
            for frame in reversed(s['stack']):
                if variable in frame['variables']:
                    value = frame['variables'][variable]
                    expanded = s['heap'].get(value.get('ref')) if isinstance(value, dict) and 'ref' in value else value
                    signature = json.dumps(expanded, sort_keys=True)
                    if seen and signature != previous and s['index'] > chosen:
                        found = s
                    previous, seen = signature, True
                    break
            if found:
                break
        if found:
            chosen = found['index']
            message = f'This is the next recorded change to {variable}. Inspect the preceding event to see the operation that ran.'
        else:
            message = f'No later recorded change to {variable or "that variable"} was found. Try a variable name from the stack.'
    return {'step': chosen, 'message': message, 'evidence': steps[chosen]}

@asynccontextmanager
async def lifespan(app):
    async with mcp.session_manager.run():
        yield

app = FastAPI(title='Trace', lifespan=lifespan)

@app.middleware('http')
async def local_only(request: Request, call_next):
    # This prototype executes trusted local snippets; it must not become a public code runner.
    host = request.headers.get('host', '').split(':')[0]
    origin = request.headers.get('origin')
    if host not in ('localhost', '127.0.0.1', 'testserver'):
        return JSONResponse({'detail': 'Local access only.'}, status_code=403)
    if origin and origin not in (f'http://localhost:{PORT}', f'http://127.0.0.1:{PORT}'):
        return JSONResponse({'detail': 'Cross-origin requests are not allowed.'}, status_code=403)
    return await call_next(request)

@app.get('/')
def home():
    return FileResponse(ROOT / 'static' / 'index.html')

@app.get('/api/examples')
def examples():
    return EXAMPLES

@app.post('/api/run')
async def run_program(body: Program):
    result = await trace_python(body.source)
    return get_run(result['run_id'])

@app.post('/api/ask')
async def ask(body: Question):
    """Transparent deterministic command router; the actual tool invocation uses Streamable HTTP MCP."""
    text = body.question.lower()
    variable = ''
    if any(x in text for x in ('alias', 'shared', 'same list', 'disappear', 'reference')):
        target = 'alias'
    elif any(x in text for x in ('error', 'fail', 'invalid', 'bounds', 'wrong')):
        target = 'error'
    elif 'return' in text:
        target = 'return'
    elif 'change' in text:
        target = 'change'
        match = re.search(r'(?:when (?:did|does)|change (?:to|of))\s+([a-zA-Z_]\w*)', text)
        variable = match.group(1) if match else 'path'
    elif any(x in text for x in ('start', 'begin', 'first')):
        target = 'start'
    elif any(x in text for x in ('end', 'last', 'finish')):
        target = 'end'
    elif any(x in text for x in ('back', 'previous')):
        target = 'previous'
    elif 'next' in text:
        target = 'next'
    else:
        return {'step': body.step, 'message': 'I support trace navigation: show the error, find shared references, when did path change, next return, start, end, next, or previous. This demo uses a deterministic command router, not a language model.', 'tool': None}
    try:
        async with streamable_http_client(f'http://127.0.0.1:{PORT}/mcp') as (read, write, _):
            async with ClientSession(read, write) as session:
                initialized = await session.initialize()
                result = await session.call_tool('navigate_trace', {'run_id': body.run_id, 'target': target, 'current_step': body.step, 'variable': variable})
                if result.isError:
                    raise ValueError(result.content[0].text)
                data = json.loads(result.content[0].text)
                data.update({'tool': 'navigate_trace', 'transport': 'Streamable HTTP', 'protocol': initialized.protocolVersion, 'target': target})
                return data
    except Exception as exc:
        raise HTTPException(400, 'MCP navigation failed. Rerun the program and try again.') from exc

app.mount('/static', StaticFiles(directory=ROOT / 'static'), name='static')
app.mount('/', mcp.streamable_http_app())

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=PORT)

