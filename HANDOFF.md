# Rehearsal handoff

Updated October 22, 2026: Gemini-only migration completed. Read AGENTS.md and interview/README.md, then latest WORK_LOG.md before editing. Historical decisions/tests remain in WORK_LOG.md; this snapshot supersedes earlier provider plans.

## Objective and authorization

Active project: Rehearsal in interview/, Amazon Alexa+ hackathon mock interview app. Trace in trace/ is paused. User expects autonomous development, resumable checkpoints after small milestones, and commits using only their git identity (no AI credits). No remote publication/submission authorization; no remote configured at last check. User supplied Gemini key in ignored interview/.env and authorized Gemini testing. OpenAI paid calls remain deferred and are now removed from runtime. Never print secrets. Do not delegate merely because this is a handoff protocol.

## Current behavior

All active AI features use the same GEMINI_API_KEY: audio transcript/review/draft, tailored question/follow-up, text interview, MCP coaching/retry comparison, company research and plan synthesis. Shared generateContent helper in audio_review.py; model GEMINI_MODEL (legacy GEMINI_AUDIO_MODEL fallback), default gemini-3.5-flash. Research may override GEMINI_RESEARCH_MODEL. No continuous Gemini Live implementation. Removed old OpenAI voice UI/runtime; legacy /api/token returns 410 without a provider call.

Interview setup accepts company, role, JD, resume upload/paste, skills goals, round and 5/15/30-minute target. Upload PDF/DOCX/TXT <=5 MB; local subprocess extraction <=10 seconds, PDF <=15 pages, preview/apply <=10k characters, no OCR. Setup is page-memory only. Authored demo preserves personal setup.

Company research is enabled by default; ignored local .env flag changed to 1 at user request. Button: Research this company & build my plan. Search sends company/role only to Gemini Google Search grounding. Synthesis receives resume/JD/goals to tailor the simulated interview (not resume editing). research.py rejects incomplete/uncited grounding; citations use UTF-8 segment offsets and original part indexes; Google's rendered search suggestions appear in a sandboxed iframe. User reviews/applies/saves plan. Changing inputs invalidates it. Not verified company questions.

Recorded practice: built-in or Gemini question -> browser Hear the question -> Record -> Stop -> explicit Gemini analysis or opt-in automatic analysis. Browser converts to mono 16kHz WAV, server caps at12 MB in memory. Audio request includes question/skills, not resume. Feedback includes transcript, quotes, estimated delivery, retry focus, suggested draft and missing details. Corrected transcript informs follow-up; retry restores same question. Two-minute takes, four takes per page. Comparisons/history group only matching questions. No validated fluency/pronunciation/hiring scores; drafts can infer unsupported facts.

Authored sample remains no-key. Deterministic checks use English word lists and exact text evidence, no scores. Seven real MCP tools (Streamable HTTP2025-11-25): check_answer_text, compare_answer_texts, save_practice_result, get_practice_progress, get_interview_brief, coach_latest_answer, compare_retry. Last two use Gemini. Audio/research/question endpoints are separate HTTP integrations. MCP App at /mcp-app-preview is a reference host, not tested third-party. agent_sim.py is a scripted tool loop, not actual Alexa. History stores derived counts only in ignored interview/data; audio is page-local unless selected for analysis/captions.

## Launch and verification

Windows D:/hackamazon; .venv Python3.11. Run .venv/Scripts/python interview/server.py; http://127.0.0.1:8766. Restart existing server and refresh browser for latest code. User reported disabled research after migration. Identified stale server on8766 and restarted it on Oct22; /api/status now confirms provider gemini, key configured and research enabled. No provider call used for this check. .env overrides inherited settings; never overwrite it from example. Local single-user loopback app, not public-hosting ready.

Current regression: 50 Python tests passed, including real local MCP integration, with provider calls mocked and scratch history on an owned temporary server. Eight JS mock suites and all JS syntax passed. Test runner cleanup hit Windows file-lock on temporary server.log after successful tests; owned child termination was issued/waited. No user server killed. This is a harness cleanup issue, not failed assertions.

Separate live checks: earlier synthetic audio review and fictional follow-up succeeded. THIS migration: Gemini text HTTP503 and company search HTTP429. Stopped live retries; no personal data sent. Newly migrated text/research not verified end to end. No OpenAI calls. Physical microphone/browser WAV conversion, current UI/mobile layout and Search iframe still need browser QA. Earlier overnight fake-mic/headless and sample UI tests predate latest changes; do not imply coverage.

## Files and next steps

server.py routes/MCP/sessions; audio_review.py shared Gemini JSON/audio; gemini_questions.py questions; research.py grounding/synthesis; resume_import.py extraction; static/app.js sample/text, practice.js recording, audio-review.js analysis, practice-questions.js followups, research.js plan UI. Tests: test_*.py and eight test_*.cjs. README.md overview, interview/README.md details, DEMO.md and SUBMISSION.md drafts, docs/USER_TEST.md manual checks.

1. Restart and browser-test: save fictional company/JD/experience/goals, question -> real mic recording -> analysis -> retry/followup. Check plan loading/error/source frame. Gemini quota may block; avoid repeated paid retries.
2. Fix user findings, checkpoint log/handoff after each milestone. Browser APIs must be tested with approved computer-use tooling; no direct CDP fallback.
3. Review submission/demo claims against actual behavior. Publishing repo, uploading demo and Devpost submission remain pending. Deadline from earlier official-rule verification: Oct23,2026 noon PT /3pm ET. Alexa+ track accepts simulation or self-hosted MCP; required repo/license, description, public video <3min, product feedback, track; optional friction log up to10% bonus. Recheck official rules if needed: https://amazonappdev2026.devpost.com/rules .
4. docs/SUBMIT_CHECKLIST.md has publication steps; gh unavailable at last check. Existing ignored demo-video/rehearsal-demo-captioned.avi is old silent1:43 fallback, structurally checked but not played; it predates migration and needs review before use. Source capture scripts were session-local, may be unavailable.

Known risks: qualitative model advice/transcripts can be wrong; English rule lists misclassify; generated drafts need factual review. Browser speech may use OS online services. Setup resets on reload. Async generation/requestVersion guards protect resets; preserve those. PowerShell may display UTF-8 mojibake; inspect bytes before changing encoding.
