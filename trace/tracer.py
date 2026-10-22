"""Small educational Python tracer. Local trusted code only, not a security sandbox."""
import ast
import builtins
import contextlib
import io
import json
import sys

MAX_STEPS = 600
ALLOWED_BUILTINS = ('range', 'len', 'enumerate', 'zip', 'min', 'max', 'sum', 'abs', 'sorted', 'reversed', 'list', 'dict', 'set', 'tuple', 'int', 'float', 'str', 'bool', 'print', 'all', 'any')
ALLOWED_METHODS = {'append', 'pop', 'copy', 'extend', 'insert', 'remove', 'clear', 'reverse', 'sort', 'count', 'index', 'get', 'items', 'keys', 'values', 'add', 'discard'}

def validate(source):
    if len(source) > 12000:
        raise ValueError('Keep programs under 12,000 characters.')
    tree = ast.parse(source, filename='<trace>')
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.ClassDef, ast.With, ast.AsyncFunctionDef, ast.Await, ast.Yield, ast.YieldFrom, ast.Try, ast.Global, ast.Nonlocal)):
            raise ValueError(f'{type(node).__name__} is outside this learning prototype. Use functions, loops, and lists.')
        if isinstance(node, ast.Name) and node.id.startswith('__'):
            raise ValueError('Private Python internals are not supported.')
        if isinstance(node, ast.Attribute) and node.attr not in ALLOWED_METHODS:
            raise ValueError(f'Method .{node.attr} is not supported in this prototype.')
    return tree

def trace(source):
    try:
        tree = validate(source)
    except (ValueError, SyntaxError) as exc:
        return {'steps': [], 'error': {'type': type(exc).__name__, 'message': str(exc), 'line': getattr(exc, 'lineno', None)}, 'source': source}
    steps, calls, object_ids, retained = [], [], {}, []
    active = []
    frames = {}
    output = io.StringIO()
    failure = None

    def encode(value, heap, depth=0):
        if value is None or type(value) in (bool, int, float, str):
            return value if not isinstance(value, str) else value[:500]
        if isinstance(value, (list, tuple, dict, set)):
            identity = id(value)
            if identity not in object_ids:
                object_ids[identity] = f'obj{len(object_ids) + 1}'
                retained.append(value)  # Prevent CPython from recycling object identities.
            label = object_ids[identity]
            if label not in heap:
                heap[label] = {'type': type(value).__name__, 'items': [], 'length': len(value)}
                if depth < 7:
                    values = list(value.items()) if isinstance(value, dict) else list(value)
                    heap[label]['items'] = [encode(x, heap, depth + 1) for x in values[:60]]
            return {'ref': label}
        return {'display': f'<{type(value).__name__}>'}

    def callback(frame, event, arg):
        if frame.f_code.co_filename != '<trace>':
            return callback
        if event not in ('call', 'line', 'return', 'exception'):
            return callback
        if len(steps) >= MAX_STEPS:
            raise RuntimeError(f'Trace stopped at {MAX_STEPS} events. Try a smaller input.')
        key = id(frame)
        if event == 'call':
            cid = len(calls)
            frames[key] = cid
            calls.append({'id': cid, 'name': frame.f_code.co_name, 'parent': active[-1][1] if active else None, 'start': len(steps), 'end': None})
            active.append((frame, cid))
        heap = {}
        stack = []
        for f, cid in active:
            variables = {k: encode(v, heap) for k, v in f.f_locals.items() if not k.startswith('__') and not callable(v)}
            stack.append({'id': cid, 'name': f.f_code.co_name, 'line': f.f_lineno, 'variables': variables})
        step = {'index': len(steps), 'event': event, 'line': frame.f_lineno, 'stack': stack, 'heap': heap, 'stdout': output.getvalue()[:4000]}
        if event == 'return':
            step['return'] = encode(arg, heap)
        if event == 'exception':
            step['exception'] = {'type': arg[0].__name__, 'message': str(arg[1])}
            # Capture the attempted index without re-evaluating arbitrary expressions.
            for node in ast.walk(tree):
                if isinstance(node, ast.Subscript) and node.lineno == frame.f_lineno and isinstance(node.value, ast.Name):
                    obj = frame.f_locals.get(node.value.id, frame.f_globals.get(node.value.id))
                    index = None
                    if isinstance(node.slice, ast.Name):
                        index = frame.f_locals.get(node.slice.id, frame.f_globals.get(node.slice.id))
                    elif isinstance(node.slice, ast.Constant):
                        index = node.slice.value
                    if isinstance(obj, (list, tuple, str)) and type(index) is int:
                        step['access'] = {'name': node.value.id, 'index': index, 'length': len(obj), 'valid': -len(obj) <= index < len(obj)}
                        if not step['access']['valid']:
                            break
        steps.append(step)
        if event == 'return' and active and active[-1][0] is frame:
            calls[active[-1][1]]['end'] = len(steps) - 1
            active.pop()
        return callback

    namespace = {'__builtins__': {name: getattr(builtins, name) for name in ALLOWED_BUILTINS}}
    try:
        with contextlib.redirect_stdout(output):
            sys.settrace(callback)
            exec(compile(tree, '<trace>', 'exec'), namespace, namespace)
    except BaseException as exc:
        failure = {'type': type(exc).__name__, 'message': str(exc)}
    finally:
        sys.settrace(None)
    return {'source': source, 'steps': steps, 'calls': calls, 'error': failure, 'stdout': output.getvalue()[:4000]}

if __name__ == '__main__':
    request = json.load(sys.stdin)
    json.dump(trace(request['source']), sys.stdout)
