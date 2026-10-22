# Rehearsal handoff

Updated October 22, 2026: Gemini-only migration completed. Read AGENTS.md and interview/README.md, then latest WORK_LOG.md before editing. Historical decisions/tests remain in WORK_LOG.md; this snapshot supersedes earlier provider plans.

## Objective and authorization

Active project: Rehearsal in interview/, Amazon Alexa+ hackathon mock interview app. Trace in trace/ is paused. User expects autonomous development, resumable checkpoints after small milestones, and commits using only their git identity (no AI credits). No remote publication/submission authorization; no remote configured at last check. User supplied Gemini key in ignored interview/.env and authorized Gemini testing. OpenAI paid calls remain deferred and are now removed from runtime. Never print secrets. Do not delegate merely because this is a handoff protocol.

## Current behavior

All active AI features use the same GEMINI_API_KEY: audio transcript/review/draft, tailored question/follow-up, text interview, MCP coaching/retry comparison, company research and plan synthesis. Shared generateContent helper in audio_review.py; model GEMINI_MODEL (legacy GEMINI_AUDIO_MODEL fallback), default gemini-3.5-flash. Research may override GEMINI_RESEARCH_MODEL. NEW: continuous Gemini Live interview implemented in live_interview.py + static/interview.js/interview-pcm.js. Defaults to gemini-3.8-live (separate GEMINI_LIVE_MODEL), same key. User changed objective to full uninterrupted timed interview, no coaching until end. Removed old OpenAI voice UI/runtime; legacy /api/token returns 410 without a provider call.

Interview setup accepts company, role, JD, resume upload/paste, skills goals, round and 5/15/30-minute target. Upload PDF/DOCX/TXT <=5 MB; local subprocess extraction <=10 seconds, PDF <=15 pages, preview/apply <=10k characters, no OCR. Setup is page-memory only. Authored demo preserves personal setup.

Company research is enabled by default; ignored local .env flag changed to 1 at user request. Button: Research this company & build my plan. Search sends company/role only to Gemini Google Search grounding. Synthesis receives resume/JD/goals to tailor the simulated interview (not resume editing). research.py rejects incomplete/uncited grounding; citations use UTF-8 segment offsets and original part indexes; Google's rendered search suggestions appear in a sandboxed iframe. User reviews/applies/saves plan. Changing inputs invalidates it. Not verified company questions.

Recorded practice: built-in or Gemini question -> browser Hear the question -> Record -> Stop -> explicit Gemini analysis or opt-in automatic analysis. Browser converts to mono 16kHz WAV, server caps at12 MB in memory. Audio request includes question/skills, not resume. Feedback includes transcript, quotes, estimated delivery, retry focus, suggested draft and missing details. Corrected transcript informs follow-up; retry restores same question. Two-minute takes, four takes per page. Comparisons/history group only matching questions. No validated fluency/pronunciation/hiring scores; drafts can infer unsupported facts.

Authored sample remains no-key. Deterministic checks use English word lists and exact text evidence, no scores. Seven real MCP tools (Streamable HTTP2025-11-25): check_answer_text, compare_answer_texts, save_practice_result, get_practice_progress, get_interview_brief, coach_latest_answer, compare_retry. Last two use Gemini. Audio/research/question endpoints are separate HTTP integrations. MCP App at /mcp-app-preview is a reference host, not tested third-party. agent_sim.py is a scripted tool loop, not actual Alexa. History stores derived counts only in ignored interview/data; audio is page-local unless selected for analysis/captions.

## Launch and verification

Windows D:/hackamazon; .venv Python3.11. Run .venv/Scripts/python interview/server.py; http://127.0.0.1:8766. Restart existing server and refresh browser for latest code. User reported disabled research after migration. Identified stale server on8766 and restarted it on Oct22; /api/status now confirms provider gemini, key configured and research enabled. No provider call used for this check. .env overrides inherited settings; never overwrite it from example. Local single-user loopback app, not public-hosting ready.

Previous migration regression: 50 Python tests passed, including real local MCP integration, with provider calls mocked and scratch history on an owned temporary server. Eight JS mock suites and all JS syntax passed. Test runner cleanup hit Windows file-lock on temporary server.log after successful tests; owned child termination was issued/waited. No user server killed. This is a harness cleanup issue, not failed assertions.

Separate live checks: earlier synthetic audio review and fictional follow-up succeeded. THIS migration: Gemini text HTTP503 and company search HTTP429. Stopped live retries; no personal data sent. Newly migrated text/research not verified end to end. No OpenAI calls. Physical microphone/browser WAV conversion, current UI/mobile layout and Search iframe still need browser QA. Earlier overnight fake-mic/headless and sample UI tests predate latest changes; do not imply coverage.

## Files and next steps

server.py routes/MCP/sessions; audio_review.py shared Gemini JSON/audio; gemini_questions.py questions; research.py grounding/synthesis; resume_import.py extraction; static/app.js sample/text, practice.js recording, audio-review.js analysis, practice-questions.js followups, research.js plan UI. Tests: test_*.py and eight test_*.cjs. README.md overview, interview/README.md details, DEMO.md and SUBMISSION.md drafts, docs/USER_TEST.md manual checks.

1. Restart and browser-test: save fictional company/JD/experience/goals, question -> real mic recording -> analysis -> retry/followup. Check plan loading/error/source frame. Gemini quota may block; avoid repeated paid retries.
2. Fix user findings, checkpoint log/handoff after each milestone. Browser APIs must be tested with approved computer-use tooling; no direct CDP fallback.
3. Review submission/demo claims against actual behavior. Publishing repo, uploading demo and Devpost submission remain pending. Deadline from earlier official-rule verification: Oct23,2026 noon PT /3pm ET. Alexa+ track accepts simulation or self-hosted MCP; required repo/license, description, public video <3min, product feedback, track; optional friction log up to10% bonus. Recheck official rules if needed: https://amazonappdev2026.devpost.com/rules .
4. docs/SUBMIT_CHECKLIST.md has publication steps; gh unavailable at last check. Existing ignored demo-video/rehearsal-demo-captioned.avi is old silent1:43 fallback, structurally checked but not played; it predates migration and needs review before use. Source capture scripts were session-local, may be unavailable.

Known risks: qualitative model advice/transcripts can be wrong; English rule lists misclassify; generated drafts need factual review. Browser speech may use OS online services. Setup resets on reload. Async generation/requestVersion guards protect resets; preserve those. PowerShell may display UTF-8 mojibake; inspect bytes before changing encoding.


## Update: Oct 22, evening ET (Claude session)

**Browser QA.** Done in real Chrome via the Claude-in-Chrome extension, against an isolated no-key copy on port 8767. It covered home, setup, consent, the room (desktop and 390 px), the debrief, the sample and the practice panel. The full room → End → debrief → Back flow was exercised with a mocked transport and synthetic oscillator microphone (all mock text prefixed [MOCK]; UI only).

**Fixed (commit fa7f7d2):**
- glyph corruption (`?` in place of ·, →, ×, …);
- the room ignored the saved setup length;
- the stage clock showed inside the room;
- the mobile room overflowed horizontally;
- Maya's caption was not restored after an interview.

**Live check.** Gemini text generation succeeded with a fictional brief. Company research is still HTTP 429; do not loop.

**Docs.**
- `SUBMISSION.md` rewritten around the interview room, with a verification-status table, Gemini Live product feedback, the 7 friction entries, and test counts of 59 Python tests and 9 JS suites.
- README lead, status table and quickstart updated.
- `DEMO.md` is now a single primary script (excerpt labelling rules, plus a no-key fallback). The old AVI is marked outdated.
- `docs/SUBMIT_CHECKLIST.md` has the user's 5-minute mic test as step 1.
- The gallery was renamed to `docs/screenshots/01–10`, with new real captures for home, setup, consent, room and mobile.

**The single most important remaining verification:** the user's own 5-minute interview with a physical microphone. After that come publishing, the video and Devpost (user actions).

## Current milestone: focused full interview room

User rejected cluttered per-answer coaching UI and explicitly requested 30 minutes of hands-free interviewing with analysis only at end. New primary Enter interview room CTA, 5/15/30-minute selector (room default30), consent, microphone worklet, continuous native audio, automatic turn detection, audio interruption handling, countdown and end button. Single-answer/demo moved into expandable section; feedback redesigned as summary/priority with expandable analysis/draft/transcript. Stage is moved into a focused overlay and restored afterward.

Backend live_interview.py proxies Gemini WebSocket, validates local origin, bounds audio packets/transcript, enforces deadline and end-only review, captures transcripts, enables compression and resumption. GoAway waits for resumable handle; no quota retry loops. Final review is transcript-based, exact candidate-quote filtering, no scores or pronunciation claims. Empty transcript produces no assessment. Requires newly installed websockets15.0.1. New session is separate from existing sample/text state; no raw audio saved.

Verification checkpoint: 59 Python tests PASS on isolated temporary server (provider mocks, real MCP); nine JS suites PASS including worklet resampling, timed ending, mic cleanup, late permission, and no review before ending. HTML nesting/IDs/scripts pass. Live setup accepted and spoken model audio received. First synthetic turn test timed out because the fixture was22050Hz while the harness required16000Hz. Corrected conversion test SUCCESS: actual model audio, two completed model turns, synthetic candidate transcript received, clean end, no errors. No browser surface available, so visual QA and real mic/full 30-minute verification pending. Do not call this end-to-end verified yet. Next: user refresh/test5-minute session first, then full 30-minute stability/interruptions. Earlier text/search503/429 still limits final analysis/research independently of Live access.

Final review live check SUCCESS on fictional completed transcript: one answer review/two priorities. Earlier generic-text503 is historical; company search429 remains unresolved. Physical mic/visual/full30-minute QA remains pending. Server8766 restarted with new websocket implementation after checks.
