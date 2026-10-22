"""Original authored scenario. Never presented as model-generated feedback."""
BRIEF = {
    'role': 'Software Engineering Intern',
    'company': 'A product engineering team',
    'resume': 'Computer science student. Built a campus events application in a three-person team. Owned the search endpoint and wrote API tests. Used Python, PostgreSQL, and React.',
    'job': 'Build reliable customer-facing features. Explain technical tradeoffs clearly, collaborate with teammates, and test your work.',
}
QUESTION = 'Tell me about a time you solved a technical problem in a team project. What did you personally contribute?'
FIRST = 'So, um, we built an events app for our campus. We had some issues with search being slow. We worked on the database and, like, made it better. We tested it and it worked well. I learned a lot about working in a team.'
RETRY = 'In a three-person team, I owned the search endpoint for our campus events app. Search was slow, so I inspected the database queries and found we were fetching more fields than we needed. I narrowed the query and wrote API tests to check that search results stayed correct. The endpoint felt faster in our testing, although we did not record a latency benchmark. Next time, I would measure before and after so I could quantify the improvement.'
SAMPLE = {
    'brief': BRIEF, 'question': QUESTION, 'first': FIRST, 'retry': RETRY,
    'followup': 'You mentioned the team improved search. Walk me through one change you personally made, and how you checked it worked.',
    'coaching': {
        'summary': 'The project is relevant. Your personal contribution is still hidden behind “we.”',
        'strength': 'You chose a concrete engineering project and named a real problem: slow search.',
        'evidence': [
            {'quote': 'We worked on the database', 'observation': 'This describes the team, but not your own action.', 'suggestion': 'Name the query you changed and explain why you chose that change.'},
            {'quote': 'it worked well', 'observation': 'The outcome is not supported by a check or observation.', 'suggestion': 'Explain how you tested it. If you did not measure latency, say that rather than inventing a number.'},
        ],
        'structure': 'Lead with the problem, spend most of the answer on your action, and finish with the result and a lesson.',
        'language': 'Replace “made it better” with the precise action: “narrowed the query” or the change you actually made.',
        'knowledge': 'There is not enough technical detail here to assess correctness. Explain the query and test strategy first.',
        'retry_focus': 'Make your own contribution and your verification clear.',
        'outline': ['Context: campus events app, three-person team.', 'Your action: what you inspected and changed.', 'Verification: what you tested and what you observed.', 'Reflection: what you would measure next time.'],
    },
    'comparison': {
        'summary': 'The retry explains your ownership, action, verification, and uncertainty.',
        'changes': [
            {'before': 'We worked on the database', 'after': 'I inspected the database queries', 'why': 'Your contribution is explicit.'},
            {'before': 'it worked well', 'after': 'wrote API tests to check that search results stayed correct', 'why': 'You explain how you checked the work.'},
            {'before': 'made it better', 'after': 'we did not record a latency benchmark', 'why': 'You avoid claiming a measurement you do not have.'},
        ],
        'next_step': 'Practice a follow-up about which API test cases you chose and why.',
    },
}
