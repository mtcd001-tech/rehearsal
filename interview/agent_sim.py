"""Terminal simulation of a voice assistant running Rehearsal's practice loop over MCP.

A scripted, deterministic agent: it is not an LLM and not Alexa. It follows the turn order in the server's
MCP instructions and makes real tool calls (get_practice_progress, check_answer_text, compare_answer_texts,
save_practice_result) against a running Rehearsal server, printing what an assistant would say.

    python interview/agent_sim.py              # answer in the terminal
    python interview/agent_sim.py --demo       # use the authored sample answers
"""
import argparse
import asyncio
import json
import logging
import os
import random

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from sample import SAMPLE

QUESTIONS = [
    SAMPLE['question'],
    'Walk me through a bug that was hard to find. How did you narrow it down, and how did you confirm the fix?',
    'Tell me about a time you had more work than time. How did you decide what to do first?',
]

def say(text):
    print(f'\n  Maya: {text}')

def tool_line(name, detail):
    print(f'    [MCP tools/call {name}] {detail}')

async def call(session, name, arguments):
    result = await session.call_tool(name, arguments)
    if result.isError:
        raise SystemExit(f'{name} failed: {result.content[0].text}')
    return result.structuredContent or json.loads(result.content[0].text)

def tip(check):
    if not check['priority']:
        return 'Every signal I check is there. Next, try a follow-up question about the same story.'
    signal = next(s for s in check['signals'] if s['id'] == check['priority']['id'])
    quote = f' For example, you said: "{signal["quotes"][0]}".' if signal['quotes'] else ''
    return f'Start here: {check["priority"]["label"].lower()}. {check["priority"]["suggestion"]}{quote}'

def ask(prompt, demo_value, demo):
    if demo:
        print(f'\n  You: {demo_value}')
        return demo_value
    text = ''
    while not text.strip():
        text = input(f'\n  {prompt}\n  You: ')
    return text

async def run(url, demo, save):
    async with streamable_http_client(url) as (read, write, _):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            print(f'Connected to {init.serverInfo.name} · MCP {init.protocolVersion} · scripted agent (not an LLM)')
            progress = await call(session, 'get_practice_progress', {})
            tool_line('get_practice_progress', f'sessions={progress["sessions"]}')
            focus = progress.get('suggested_focus')
            say(f'Welcome back. Last time, your recurring focus was {focus["label"]}. Keep that in mind.' if focus
                else "Let's practice one behavioral question. Answer the way you would out loud.")
            question = SAMPLE['question'] if demo else random.choice(QUESTIONS)
            say(question)
            first = ask('(type your answer, then Enter)', SAMPLE['first'], demo)
            check = await call(session, 'check_answer_text', {'answer': first, 'question': question})
            tool_line('check_answer_text', f'priority={check["priority"]["id"] if check["priority"] else None}, words={check["words"]}')
            say(tip(check))
            say('Try the same question again with that one change. Keep your real experience; change how you tell it.')
            retry = ask('(type your retry, then Enter)', SAMPLE['retry'], demo)
            if retry.strip() == first.strip():
                say('That is the same answer as before, so there is nothing to compare yet.')
                return
            compared = await call(session, 'compare_answer_texts', {'before': first, 'after': retry})
            moved = [c['id'] for c in compared['changes'] if c['direction'] == 'toward']
            tool_line('compare_answer_texts', f'moved_toward={moved}')
            say(f'{compared["summary"]} Next: {compared["next_step"]}')
            if save:
                saved = await call(session, 'save_practice_result', {'question': question, 'first_answer': first, 'retry_answer': retry})
                tool_line('save_practice_result', f'total_sessions={saved["total_sessions"]} (signals only, no answer text)')
                say('Saved your progress on this computer. Only the signal counts, not your words.')

def main():
    logging.getLogger('httpx').setLevel(logging.WARNING)
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    port = os.getenv('INTERVIEW_PORT', '8766')
    parser.add_argument('--url', default=f'http://127.0.0.1:{port}/mcp')
    parser.add_argument('--demo', action='store_true', help='use the authored sample answers instead of typing')
    parser.add_argument('--save', action='store_true', help='save the result to local practice history (signals only)')
    args = parser.parse_args()
    asyncio.run(run(args.url, args.demo, args.save))

if __name__ == '__main__':
    main()
