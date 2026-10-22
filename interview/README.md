# Rehearsal - Gemini interview practice

Continuing agents: read ../AGENTS.md, ../HANDOFF.md and latest ../WORK_LOG.md before editing. Keep the log and snapshot current after each milestone.

## Run

From the repository root, install interview/requirements.txt into the Python 3.11+ virtual environment, then run:

    .venv\Scripts\python interview\server.py

Open http://127.0.0.1:8766. Restart the server after configuration/backend changes; refresh the browser after UI changes. The local service is single-user and loopback-only, not ready for public hosting.

Copy .env.example to interview/.env if no .env exists, and set GEMINI_API_KEY locally. Never paste or commit the key. All active AI features use this Gemini key. GEMINI_MODEL defaults to gemini-3.5-flash; GEMINI_RESEARCH_MODEL defaults to the same. Older GEMINI_AUDIO_MODEL is a fallback only when GEMINI_MODEL is unset. INTERVIEW_PORT defaults to 8766. Explicit .env values override inherited environment values.

Company research is enabled by default and only runs after a click. Set INTERVIEW_RESEARCH_ENABLED=0 to disable it. API quotas, search access and availability depend on the Google account. A key does not guarantee available quota. No automatic retry loops.

## Set up your interview

Open Interview setup or Edit setup:

1. Enter company, target role and job description.
2. Upload a resume (PDF/DOCX/UTF-8 TXT, maximum 5 MB), review the extracted text and explicitly Apply it, or paste your experience.
3. Choose recruiter, behavioral, technical or hiring-manager round; 5/15/30-minute target; and optional Skills I want to improve.
4. Optionally choose Research this company & build my plan. Review sources and the proposed questions, then Use this interview plan.
5. Save interview setup. Reopening or trying the authored demo preserves it within the current page. Full reload discards setup; no browser persistence has been added.

Resume extraction runs locally in memory with a 10-second subprocess timeout. Original files are not saved. PDFs must have selectable text, be unlocked and have at most 15 pages; there is no OCR or legacy DOC support. Text is capped at 10,000 characters with a notice. Columns/tables can extract in the wrong order; review the preview.

Research uses Gemini Google Search grounding with company/role only. Resume/JD/goals do not enter the search stage. The subsequent Gemini synthesis receives them to tailor the simulation. Sources are linked inline; Google's search suggestions are shown in a sandboxed frame. Official information, anecdotes and inferred practice format are distinguished by the prompt. Uncited or incomplete results are rejected. Links/evidence checks do not prove all claims accurate. Changing setup inputs clears a stale plan. This is simulated preparation, not confirmed company questions.

## Full mock interview

Enter interview room is now the primary mode. Choose 5, 15 or 30 minutes (room defaults to 30), allow the microphone once, and speak naturally. Gemini Live asks spoken questions and follow-ups using saved setup. There are no per-answer Record/Next buttons and no coaching panels during the interview. Use headphones. Automatic speech detection handles turns; interruptions stop queued interviewer audio. End interview is always available, and the countdown ends the session automatically.

The focused room shows Maya, connection/microphone state and a countdown. The server separately enforces duration. Context compression and session resumption are enabled for longer sessions. A connection rollover may briefly pause the audio; the UI asks you to hold your thought. Network/access failures end the session honestly, retaining received transcripts for review. The app does not silently retry quota failures or pretend to complete the requested duration.

When it ends, the microphone stops and the app requests a transcript-based review: summary, strengths, priority improvements, and expandable question-by-question analysis with quoted evidence and suggested rewrites. Feedback is unavailable through the review endpoint while the session is active. No transcript means no invented assessment. This final review cannot measure vocal fluency/pronunciation; generated transcripts/drafts need checking. Download the transcript/review before returning to practice; returning clears the server session.

GEMINI_LIVE_MODEL defaults to gemini-3.8-live and is independent of GEMINI_MODEL. The same server-side key is used. Install updated requirements (websockets==15.0.1). Microphone PCM streams through a same-origin local WebSocket to Google; no raw audio file is stored. Saved setup is sent to Google on start. The browser uses AudioWorklet with mono16kHz input and 24kHz model playback. The session's input/output transcripts are held in server memory. Closing the page stops the mic/connection.

The single-answer practice/demo now live in an expandable section. Recording feedback uses a concise summary and next-step card, with analysis, draft and transcript in expandable sections instead of a long wall of text.

Live setup, native interviewer audio, synthetic candidate answer/follow-up and a separate fictional final review verified; the complete 30-minute physical-microphone experience and current visual layout still require browser testing. Automated tests use mocked audio/transport, including timer, reconnect, cancellation, review gating and PCM conversion. Official protocol references: https://ai.google.dev/api/live and https://ai.google.dev/gemini-api/docs/live-api/session-management .

## Recorded interview - no typing required

Choose Practice my own answer. Select a built-in question or Ask a question from my setup. The latter explicitly sends your saved brief, including resume/JD if supplied, to Gemini. Hear the question reads it with browser speech.

Enable Analyze after I stop recording (Gemini) before recording, or click Analyze my recording with Gemini on a saved take. Record -> Stop -> automatic transcript and review. This uploads the recording, question and skills to Google. The audio-review request itself does not include the resume. Browser speech voices may use an operating-system online service.

Feedback covers the answer's structure, language and technical reasoning, quotes from the generated transcript, qualitative delivery observations, one retry focus and a suggested draft. Drafts can add unsupported inferences; verify facts and fill placeholders truthfully. Delivery observations are AI estimates, not validated pronunciation, fluency, personality or hiring scores. Transcription can be wrong; correct it if needed. User edits are not overwritten by late model/caption results.

Practice this answer again restores the question and focus. Ask me a follow-up sends the selected answer transcript (including corrections) and setup to Gemini. It generates a related question without claiming to search the web. Record another answer when ready. This is turn-based recording, not continuous Gemini Live voice.

Recordings stop at two minutes; up to four takes stay in page memory. The chosen 5/15/30 minutes is a target session length, not a hard recording-session cutoff. Download before Reset or closing the page. WAV conversion is mono 16 kHz; upload limit is 12 MB. Server uploads are not written to disk. Failures preserve the browser recording.

Optional browser captions are separate: in Chrome they send audio to Google's speech-recognition service. They are off by default. They are not needed for Gemini review.

## Text interview and coaching

Gemini text interview sends setup and typed answers to Google. Review my answer uses the same Gemini key through the MCP coaching tool; it returns analysis, quoted evidence, a suggested draft and missing-detail questions. Try that answer again and Compare my retry support the revision loop. Text practice shows a reminder at the selected duration and lets you finish. Transcript-only feedback cannot assess pronunciation or spoken fluency.

The retired OpenAI voice path remains removed. Legacy /api/token returns 410; the new Gemini Live path is /api/interview/live. No OpenAI key or calls are required.

## Local tools and authored demo

Experience the sample is a fictional authored scenario, not model-generated feedback about the user. It uses browser speech and the deterministic MCP rule panels. The demo exports its own fictional brief and does not overwrite personal setup.

Check my words uses local wording rules, exact text quotes and a revision checklist. Compare first and latest take compares the first/latest eligible takes answering the same question, never unrelated follow-ups. These counts are prompts for revision, not answer-quality scores. English word lists can miss or misclassify phrasing.

Optional practice history stores only derived signal labels/counts on this computer, not answer text or audio. It is gitignored at interview/data/practice_history.json; INTERVIEW_HISTORY_FILE overrides it. Saved history persists until cleared; recordings and transcripts do not. Downloads may include transcripts and AI feedback, so review before sharing.

## MCP and simulation

Endpoint: http://127.0.0.1:8766/mcp (Streamable HTTP, protocol 2025-11-25).

- check_answer_text and compare_answer_texts: deterministic; no key.
- save_practice_result and get_practice_progress: opt-in local history; no key.
- get_interview_brief: session context.
- coach_latest_answer and compare_retry: Gemini analysis; exact transcript-quote filtering.

Web check/coaching endpoints call the real MCP server. Gemini research/audio/question endpoints are separate HTTP integrations, not additional MCP tools. The seven-tool set is unchanged. Model session context/transcripts are kept in server memory for up to two hours and cleared on Reset/server shutdown; this does not erase provider records.

The MCP Apps card ui://rehearsal/answer-check is served with text/html;profile=mcp-app and tested in the included /mcp-app-preview reference host. It has not been verified in a third-party host. agent_sim.py is a scripted tool loop, not an LLM or actual Alexa connection. This remains an Alexa-style simulation; no Alexa device integration is claimed.

## Verification and remaining limits

Authorized live tests succeeded earlier for synthetic audio and a fictional Gemini follow-up. During the Gemini-only migration, text returned HTTP 503 and company search HTTP 429; those live paths could not be confirmed. No repeated quota retries. Mocked responses are not evidence of model quality.

Python tests cover provider payloads/schema validation, grounding citations and UTF-8 offsets, resume subprocess parsing, session/history/rule behavior and real local MCP integration. JS tests mock browser/media APIs, including recording, transcription updates, stale results, question changes and retry grouping. Physical microphone, browser WAV decoding/rendering, latest mobile layout and search-suggestion frame still need browser testing.

For Python integration tests, run a separate local server with isolated history, then from interview run python -m unittest discover -p test_*.py. Set its port in the environment consistently; .env values override environment settings. Individual unit modules can run without a server. JS tests run from interview using node test_practice.cjs, test_audio_review.cjs, test_gemini_questions.cjs, test_research.cjs, test_resume.cjs, test_setup.cjs, test_timer.cjs and test_recovery.cjs.

Manual checklist: ../docs/USER_TEST.md. Demo/submission drafts: ../DEMO.md and ../SUBMISSION.md. Publication and submission are still pending.

Implementation references: https://ai.google.dev/gemini-api/docs/audio , https://ai.google.dev/gemini-api/docs/google-search , https://ai.google.dev/api/generate-content .
