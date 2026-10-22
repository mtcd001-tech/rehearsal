"""Deterministic answer checks. No model calls, no audio analysis, no scores.

Every quote returned is sliced from the submitted text, so evidence cannot be invented.
Signals describe wording patterns only; they are prompts for a retry, not a judgment of quality.
"""
import re

SOURCE = 'Rule-based text checks: deterministic pattern matching on your words. No AI model, no audio analysis, no scores.'
ACTION_VERBS = ('added', 'analyzed', 'automated', 'built', 'cached', 'changed', 'cleaned', 'compared', 'configured', 'coordinated', 'created',
                'debugged', 'deployed', 'designed', 'documented', 'drafted', 'fixed', 'found', 'implemented', 'improved', 'indexed', 'inspected',
                'investigated', 'led', 'measured', 'migrated', 'narrowed', 'optimized', 'organized', 'owned', 'paired', 'planned', 'profiled',
                'proposed', 'prototyped', 'rebuilt', 'refactored', 'removed', 'replaced', 'reproduced', 'researched', 'reviewed', 'rewrote',
                'scheduled', 'set', 'simplified', 'split', 'suggested', 'tested', 'traced', 'tracked', 'trained', 'updated', 'validated',
                'wrote', 'asked', 'explained', 'presented', 'talked', 'decided', 'chose', 'taught', 'mentored', 'volunteered')
VERIFY = r"\b(?:tests?|tested|testing|measured?|measuring|benchmark(?:s|ed)?|verif(?:y|ied)|checked|check|confirmed|monitored|logged|profiled|reproduced|metrics?|latency|before and after|a/b|feedback from|user testing|code review)\b"
VAGUE = r"\b(?:worked (?:really |very |pretty )?well|made (?:it|things) (?:much |a lot |way )?better|a lot(?! of)|really good|very good|pretty good|went (?:really |pretty )?well|and stuff|things like that|it was good|improved things|some issues|some problems|kind of worked|it helped)\b"
FILLER = r"\b(?:um+|uh+|erm|you know|i mean|basically|sort of|kind of)\b|(?<=,\s)like(?=,)"
REFLECT = r"\b(?:learned|next time|in hindsight|i would|i'd|differently|if i did it again|lesson|did not measure|didn't measure|did not record|didn't record|not sure|i was wrong)\b"
CLAIM = r"\b\d+(?:\.\d+)?\s?(?:%|percent\b|x\b|times\b|ms\b|milliseconds\b|seconds\b|users\b|hours\b|requests\b)"
TEAM = r"\b(?:we|we're|we've|we'd|our|us|the team)\b"
SELF = r"\b(?:i|i'm|i've|i'd|i'll|my|me|myself)\b"
# Broad on purpose: non-native speakers often use present tense ("I write the tests") or type a lowercase "i".
NOT_ACTIONS = ('learned', 'liked', 'loved', 'wanted', 'needed', 'enjoyed', 'hoped', 'worried', 'assumed', 'believed', 'guessed', 'failed', 'noticed', 'realized', 'seemed')
IRREGULAR = ('built', 'wrote', 'found', 'led', 'set', 'split', 'chose', 'taught', 'ran', 'rewrote', 'rebuilt', 'made', 'took', 'sent', 'spent', 'brought', 'drew', 'kept')
PRESENT = ('add', 'build', 'write', 'fix', 'test', 'check', 'debug', 'design', 'implement', 'change', 'create', 'measure', 'review', 'use', 'profile',
           'refactor', 'deploy', 'inspect', 'compare', 'lead', 'own', 'plan', 'research', 'explain', 'ask', 'choose', 'decide', 'clean', 'update',
           'remove', 'replace', 'reproduce', 'trace', 'track', 'run', 'automate', 'document', 'optimize', 'organize', 'present', 'mentor')
ADVERB = r"(?:(?:also|then|first|finally|personally|quickly|actually|just|carefully)\s+)?"
SELF_ACTION = (r"\b[Ii]\s+" + ADVERB + r"(?:(?!(?:" + '|'.join(NOT_ACTIONS) + r")\b)[a-z]{2,}(?<!e)ed\b(?!\s+to\b)|(?:" + '|'.join(ACTION_VERBS + IRREGULAR + PRESENT) + r")\b)"
               r"|\b[Ii](?:'m| am)\s+" + ADVERB + r"[a-z]{3,}ing\b")
STOP = re.compile(r'[.!?;\n]')
TRAILING = {'a', 'an', 'the', 'and', 'or', 'but', 'for', 'our', 'my', 'to', 'of', 'in', 'on', 'with', 'at', 'by', 'that', 'being', 'is', 'was', 'we', 'i', 'it', 'so'}

def phrase(text, start, max_words=7):
    """Exact substring from start up to max_words words, ending before sentence punctuation."""
    end = STOP.search(text, start)
    chunk = text[start:end.start() if end else len(text)]
    words = list(re.finditer(r'\S+', chunk))[:max_words]
    while len(words) > 2 and words[-1].group().lower().strip(',:') in TRAILING:
        words.pop()
    return chunk[:words[-1].end()].rstrip(',:') if words else ''

def quotes(text, pattern, limit=3, flags=re.I, max_words=7):
    out, covered = [], -1
    for m in re.finditer(pattern, text, flags):
        if m.start() < covered:
            continue
        q = phrase(text, m.start(), max_words)
        if q and q not in out:
            out.append(q)
            covered = m.start() + len(q)
        if len(out) >= limit:
            break
    return out

def plural(n, word):
    return f'{n} {word}' + ('' if n == 1 else 's')

def count(text, pattern, flags=re.I):
    return len(re.findall(pattern, text, flags))

def check_answer(text, question=''):
    text = (text or '').strip()
    if not text:
        raise ValueError('Add the words of your answer before running the check.')
    words = len(re.findall(r"\b[\w'-]+\b", text))
    team, me = count(text, TEAM), count(text, SELF)
    actions = count(text, SELF_ACTION, 0)
    verify, vague, filler = count(text, VERIFY), count(text, VAGUE), count(text, FILLER)
    reflect, claims = count(text, REFLECT), count(text, CLAIM)
    signals = []

    if team and (me == 0 or actions == 0):
        status, note = 'missing', f'"We/our" appears {plural(team, "time")}, but no phrase says what you did ("I" followed by an action). A listener cannot tell your part.'
    elif team >= 2 * max(me, 1) and team >= 3:
        status, note = 'watch', f'"We/our" appears {plural(team, "time")} and "I/my" {plural(me, "time")}. Make sure your own part is clear.'
    else:
        status, note = 'ok', f'"I/my" appears {plural(me, "time")} and "we/our" {plural(team, "time")}.'
    signals.append({'id': 'ownership', 'label': 'Your own role', 'status': status, 'count': me, 'other_count': team, 'note': note,
                    'quotes': quotes(text, r'\b(?:we|the team|our team)\b', 3) if status != 'ok' else quotes(text, SELF_ACTION, 3, 0),
                    'suggestion': 'Say "I" for the parts you did: what you inspected, chose, built, or tested.'})

    signals.append({'id': 'actions', 'label': 'Concrete actions', 'status': 'ok' if actions >= 2 else 'watch' if actions == 1 else 'missing', 'count': actions,
                    'note': f'{actions} phrase(s) where "I" is followed by a concrete action verb.', 'quotes': quotes(text, SELF_ACTION, 3, 0),
                    'suggestion': 'Name two or three specific steps you took, in order.'})

    signals.append({'id': 'verification', 'label': 'How you checked it', 'status': 'ok' if verify else 'missing', 'count': verify,
                    'note': f'{verify} mention(s) of testing, measuring, or checking the result.' if verify else 'No mention of how the result was tested, measured, or checked.',
                    'quotes': quotes(text, VERIFY, 3), 'suggestion': 'Explain how you knew it worked. If you did not measure it, say so honestly.'})

    signals.append({'id': 'vague', 'label': 'Vague outcome words', 'status': 'watch' if vague else 'ok', 'count': vague,
                    'note': f'{vague} vague outcome phrase(s).' if vague else 'No common vague outcome phrases found.',
                    'quotes': quotes(text, VAGUE, 3, max_words=5), 'suggestion': 'Replace vague outcomes with what actually changed or what you observed.'})

    signals.append({'id': 'fillers', 'label': 'Filler words', 'status': 'watch' if filler >= 3 else 'ok', 'count': filler,
                    'note': f'{filler} filler word(s) in the text. Text only, not an audio fluency measurement.',
                    'quotes': quotes(text, FILLER, 3, max_words=1), 'suggestion': 'A short pause is fine. Fillers matter less than clear content.'})

    if claims:
        signals.append({'id': 'claims', 'label': 'Numbers to support', 'status': 'watch', 'count': claims,
                        'note': f'{claims} number(s) describing results. Good when real; interviewers often ask how they were measured.',
                        'quotes': quotes(text, CLAIM, 3, max_words=4), 'suggestion': 'Be ready to explain how each number was measured.'})

    signals.append({'id': 'reflection', 'label': 'Reflection or honest limits', 'status': 'ok' if reflect else 'missing', 'count': reflect,
                    'note': f'{reflect} reflection or limitation phrase(s).' if reflect else 'No lesson, limitation, or "next time" found.',
                    'quotes': quotes(text, REFLECT, 2), 'suggestion': 'End with what you learned or what you would do differently.'})

    length_status = 'watch' if words < 60 or words > 320 else 'ok'
    signals.append({'id': 'length', 'label': 'Length', 'status': length_status, 'count': words,
                    'note': f'{words} words, about {round(words / 130 * 60)} seconds at a typical speaking pace (estimate).'
                            + (' Short answers often leave out the action and result.' if words < 60 else ' Long answers can lose the listener.' if words > 320 else ''),
                    'quotes': [], 'suggestion': 'Aim for roughly one to two minutes when spoken.'})

    order = ['ownership', 'verification', 'actions', 'vague', 'reflection', 'length', 'fillers', 'claims']
    flagged = sorted((s for s in signals if s['status'] != 'ok'), key=lambda s: (s['status'] != 'missing', order.index(s['id'])))
    priority = flagged[0] if flagged else None
    return {'words': words, 'signals': signals,
            'priority': {'id': priority['id'], 'label': priority['label'], 'suggestion': priority['suggestion']} if priority else None,
            'question': question[:500], 'source': SOURCE}

# Direction in which a count moves when the retry follows the suggestion.
DIRECTION = {'ownership': 1, 'actions': 1, 'verification': 1, 'reflection': 1, 'vague': -1, 'fillers': -1}

def compare_answers(before, after):
    if not (before or '').strip() or not (after or '').strip():
        raise ValueError('Both a first take and a retry are needed to compare.')
    if before.strip() == after.strip():
        raise ValueError('The retry is identical to the first take. Record or write a different version first.')
    a, b = check_answer(before), check_answer(after)
    old = {s['id']: s for s in a['signals']}
    changes = []
    for s in b['signals']:
        prev = old.get(s['id'])
        if s['id'] not in DIRECTION or not prev:
            continue
        diff = (s['count'] - prev['count']) * DIRECTION[s['id']]
        direction = 'toward' if diff > 0 else 'away' if diff < 0 else 'same'
        changes.append({'id': s['id'], 'label': s['label'], 'before_count': prev['count'], 'after_count': s['count'], 'direction': direction,
                        'before_quotes': prev['quotes'][:2], 'after_quotes': s['quotes'][:2]})
    moved = [c['label'].lower() for c in changes if c['direction'] == 'toward']
    worse = [c['label'].lower() for c in changes if c['direction'] == 'away']
    if moved:
        summary = 'Moved in the suggested direction: ' + ', '.join(moved) + '.'
    else:
        summary = 'No checked signal moved in the suggested direction yet. That is normal on a first retry.'
    if worse:
        summary += ' Watch: ' + ', '.join(worse) + '.'
    return {'summary': summary, 'changes': changes, 'before_words': a['words'], 'after_words': b['words'],
            'next_step': b['priority']['suggestion'] if b['priority'] else 'Practice a likely follow-up question about the same story.',
            'note': 'Counts describe wording patterns, not answer quality. A good retry can keep some counts the same.', 'source': SOURCE}
