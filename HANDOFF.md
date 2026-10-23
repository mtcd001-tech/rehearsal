# Rehearsal handoff

Updated October22,2026: Feature scope frozen; preparing submission. Pressure Replay implemented and verified with synthetic live speech. Read AGENTS.md, interview/README.md and latest WORK_LOG.md before editing. This is the current snapshot; the log preserves history.

## Objective, scope and authorization

Active project is Rehearsal in interview/, Amazon Alexa+ hackathon entry. Trace in trace/ is paused. User wants most work done autonomously and frequent resumable checkpoints. Never add AI/tool authorship credits. Commits use user's identity. No delegation authorization. No remote publication/submission authorization; publishing/video/Devpost remain pending.

User confirmed the FIVE-MINUTE interview and physical webcam work well. They explicitly said full30-minute perfection is unnecessary for this short demo. Do not require or repeatedly ask for those tests again. Longer-session stability is unverified and must not be claimed. The latest approved feature is Pressure Replay, now implemented; planning-only status is superseded. Latest user direction: ask before adding ANY new feature. Focus on existing-flow fixes and submission preparation; do not expand scope.

Gemini key is in ignored interview/.env. User authorized Gemini development/live testing; never print keys. OpenAI calls remain deferred and have been removed from runtime. Company Google Search research returned429 repeatedly; do not loop retries. Research is optional and not needed for replay or interviews based on supplied setup.

## Launch and server ownership

Windows D:/hackamazon, Python3.11 .venv, Node22. Run .venv/Scripts/python interview/server.py (or interview/start.ps1), then http://127.0.0.1:8766. Install interview/requirements.txt when needed. .env overrides inherited environment values. App is single-user/loopback only, not ready for public hosting.

The user runs the server in their own terminal. Do not restart it as a hidden process or kill it for routine testing. It has NOT been restarted for Pressure Replay: user must preserve any current transcript, Ctrl+C/relaunch, and refresh. Backend changes require restart; refreshing alone is insufficient. Tests use an owned ephemeral loopback server with scratch history and terminate its process tree afterward.

## Implemented core

- Setup: company/role/JD, local resume PDF/DOCX/TXT extraction (5MB,10sec, PDF15pages, max10k text), review/apply, learning goals, round and5/15/30-minute length. Setup is page-memory only. Research sends company/role to Google Search, then resume/JD to synthesis; unavailable research must not be fabricated.
- Gemini Live room: automatic spoken turns, timed ending, no coaching during interview, compression/resumption, transcript capture. Native audio via local websocket; mono16kHz microphone worklet,24kHz playback. Explicit stream disclosure, no raw audio saved. End stops mic. Optional video-only self-view stays local; output analyser animates Maya's mouth and mic energy drives listening behavior. User confirmed short session/webcam.
- Final debrief: transcript-based Gemini review, exact quote filtering, no scores/pronunciation/hiring verdicts. Suggested drafts need fact-checking. Transient500/502/503/504/network errors retry up to3 attempts with bounded delay, never429. Final debrief max12288 tokens. Old503 occurred on user run before retries; fictional final-review calls subsequently succeeded.
- Single-answer practice: max2min/four takes, optional Gemini audio analysis/transcription, goals/setup-generated questions and selected-answer followups; same-question retry grouping. Browser captions separate opt-in; audio stays local unless analysis/captions selected.
- Authored demo and deterministic MCP wording checks remain no-key. Seven MCP tools: check_answer_text, compare_answer_texts, save_practice_result, get_practice_progress, get_interview_brief, coach_latest_answer, compare_retry. MCP2025-11-25 Streamable HTTP. History stores only derived counts, not text/audio. MCP App reference host at /mcp-app-preview; no third-party host verification. agent_sim.py is scripted, not Alexa. No actual Alexa device integration claimed.

## Pressure Replay (new)

After the full debrief, choose one evidence-backed moment. Options require a quote unique to one candidate turn and its immediately preceding interviewer turn; the actual original question is used, not the review's paraphrase. Long original answers (>6000 chars), ambiguous or missing anchors are excluded. No eligible evidence means no replay card.

Start90-second replay reuses the room/audio/camera. It creates a separate child session containing a copy of the original answer/context. Maya repeats the original question, then asks ONE changed-condition followup. Exchange tracker collects transcription fragments, handles interruption boundaries and closes after two completed answer exchanges; a90-second deadline also applies. Early/manual end retains partial answers.

Comparison only after end: exact before/retry quote pairs, qualitative verdict, remaining gap, and separate followup evidence. Followup words cannot be used as proof of an improved retry. Identical/partial/unsupported retries cannot receive an improvement verdict. AI reasoning is still fallible. Existing compare_answer_texts is called through real MCP as an optional expandable wording panel; failure of that panel does not discard the AI comparison. Seven-tool set unchanged.

Original debrief/transcript stays intact on permission, connection and comparison failures. Try replay comparison again retries analysis only. Download includes original and latest replay. Back to practice clears parent and children; up to3 saved child sessions per parent in memory. No disk persistence/audio recording added.

Files: pressure_replay.py for anchors/state/comparison; live_interview.py for Live setup/turn tracking; server.py routes /api/interview/replay and /api/interview/replay-review plus existing /api/interview/live; static/interview.js for UI/state restoration; index.html/style.css for card. Tests: test_pressure_replay.py and .cjs.

## Verification and exact next action

- Full regression:73 Python tests PASS (provider mocks, real local MCP integration, isolated history). Eleven JS mock suites PASS; all JS syntax PASS. New tests cover ambiguous anchoring, parent preservation, two-answer ending, interruption/partial handling, review gating/evidence filtering, original/replay export and permission/provider failure recovery.
- Actual live synthetic replay: exact original question, spoken retry, changed requirement to empirical evidence, second spoken answer, automatic ending after54.5sec, no errors. Actual Gemini comparison succeeded with one verified before/retry pair and followup quote. Only fictional/generated speech sent. Fixtures in ignored interview/data/replay-*.wav.
- Earlier browser QA by another session used synthetic media/mocked transport for full room/mobile flows. User confirmed base five-minute session and physical webcam. CURRENT replay UI and physical-mic replay are not browser-verified: current computer-use inventory has no surfaces. Do not imply mocked tests are browser/live model quality tests.
- Next: user restarts their own server and tests only new Pressure Replay from a fresh short interview/debrief, then downloads original+replay. Fix actual findings, rehearse the concise demo and freeze features. Do not make30-minute stability a blocker.

## Submission and known limits

README.md overview, interview/README.md detailed behavior, DEMO.md primary replay script plus fallback, SUBMISSION.md draft, docs/SUBMIT_CHECKLIST.md remaining actions. Screenshots01-10 predate Pressure Replay; do not claim they show the new card. Old silent AVI is outdated.

Earlier official-rules check recorded deadline Oct23,2026 noon PT/3pm ET, Alexa+ simulation or self-hosted MCP track, repo/license, text, public video under3min and product feedback; optional friction log. Source https://amazonappdev2026.devpost.com/rules . Recheck rules if changing submission assumptions. No remote/publication created by this milestone.

Risks: model transcripts/advice/drafts may be wrong; exact quote checks are not factual validation. Word-list MCP checks can misclassify. Async revision/generation guards protect reset and late results; preserve them. PowerShell can display UTF-8 mojibake; inspect actual bytes before fixing encoding.
