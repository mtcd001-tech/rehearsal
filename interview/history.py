"""Opt-in practice history on this computer. Stores derived check signals only: never answer text or audio."""
import json
import os
import threading
import time
from collections import Counter
from pathlib import Path

from checks import check_answer, compare_answers

PATH = Path(os.getenv('INTERVIEW_HISTORY_FILE', Path(__file__).parent / 'data' / 'practice_history.json'))
MAX_ENTRIES = 200
_lock = threading.Lock()

def _load():
    try:
        data = json.loads(PATH.read_text(encoding='utf-8'))
        return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def _save(entries):
    PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = PATH.with_suffix('.tmp')
    tmp.write_text(json.dumps(entries[-MAX_ENTRIES:], indent=1), encoding='utf-8')
    tmp.replace(PATH)

def record(question, first, retry=''):
    """Run the checks and store only labels, statuses, counts, and the comparison summary."""
    first_check = check_answer(first, question)
    entry = {'at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'question': question[:300],
             'first': {'words': first_check['words'], 'priority': first_check['priority'] and first_check['priority']['id'],
                       'signals': {s['id']: {'status': s['status'], 'count': s['count']} for s in first_check['signals']}}}
    if retry.strip():
        result = compare_answers(first, retry)
        entry['retry'] = {'words': result['after_words'], 'moved_toward': [c['id'] for c in result['changes'] if c['direction'] == 'toward'],
                          'moved_away': [c['id'] for c in result['changes'] if c['direction'] == 'away'], 'summary': result['summary']}
    with _lock:
        entries = _load()
        entries.append(entry)
        _save(entries)
    return {'saved': entry, 'total_sessions': len(entries), 'stored': 'Signal labels and counts only. No answer text or audio is stored.'}

LABELS = {'ownership': 'your own role', 'actions': 'concrete actions', 'verification': 'how you checked the result', 'vague': 'vague outcome words',
          'fillers': 'filler words', 'claims': 'numbers to support', 'reflection': 'reflection or honest limits', 'length': 'answer length'}

def progress(limit=5):
    with _lock:
        entries = _load()
    if not entries:
        return {'sessions': 0, 'recent': [], 'recurring_priorities': [], 'suggested_focus': None,
                'note': 'No saved practice yet. Results are saved only when the candidate chooses to save them.'}
    priorities = Counter(e['first']['priority'] for e in entries if e['first'].get('priority'))
    improved = Counter(i for e in entries for i in e.get('retry', {}).get('moved_toward', []))
    recurring = [{'id': k, 'label': LABELS.get(k, k), 'times_priority': n, 'times_improved_on_retry': improved.get(k, 0)} for k, n in priorities.most_common(3)]
    last = entries[-1]
    # Suggest the most frequent priority; break ties toward the most recent session's priority.
    focus = max(priorities, key=lambda k: (priorities[k], k == last['first'].get('priority'))) if priorities else None
    return {'sessions': len(entries), 'recent': entries[-limit:][::-1], 'recurring_priorities': recurring,
            'suggested_focus': {'id': focus, 'label': LABELS.get(focus, focus)} if focus else None,
            'note': 'Derived from saved rule checks on this computer. Counts describe wording, not ability.'}

def clear():
    with _lock:
        existed = PATH.exists()
        if existed:
            PATH.unlink()
    return {'cleared': existed}
