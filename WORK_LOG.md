# Rehearsal work log

Append meaningful milestones here. Keep `HANDOFF.md` as the current snapshot. Dates use America/New_York. Earlier entries below are reconstructed from completed work and tool results; no exact clock times are claimed.

### 2026-10-22 — Hackathon research and initial Trace prototype
- Purpose: assess feasibility before October 23, 3 p.m. EDT deadline.
- Changes: researched official rules/FAQ/resources; built Trace at repository root with actual Python tracing, visual state, sample corrections, and MCP navigation. Added Trace README, submission draft, demo script, tests, and ZIP.
- Verification: seven Trace tests passed, including actual local MCP protocol 2025-11-25 handshake. Browser unavailable.
- Decision: Trace lacked strong Amazon fit and differentiation; paused after user proposed interview coaching. Preserve it; do not use its submission materials for Rehearsal.

### 2026-10-22 — Rehearsal sample and API architecture
- Purpose: test user's mock-interview concept with voice, an interviewer presence, and evidence-based coaching/retry.
- Changes: created `interview/` with FastAPI/MCP server, original sample scenario, animated SVG interviewer, speech synthesis, transcript, coaching tabs, retry comparison, editable brief, download, live WebRTC and typed AI paths, setup docs.
- Research: Yoodli already offers similar interview roleplay; novelty not established. Used official OpenAI WebRTC/client-secret/Chat Completions docs.
- Verification: eight Python tests passed; actual local MCP handshake/tool context worked at 2025-11-25. Coaching/comparison provider outputs tested with mocks. JS syntax and initial DOM-ID checks passed.
- Blocker: minimal real text call returned 429 insufficient_quota; Realtime token call returned 500 server_error. User chose sample-first and deferred API access. No further paid calls after this choice.
- Limitations: no browser/audio/WebRTC end-to-end QA available. Sample is explicitly authored, not live AI.

### 2026-10-22 — Local microphone rehearsal
- Purpose: let user practice their own answers while API access is deferred; user liked the sample and requested continued work.
- Changes: added `interview/static/practice.js`, local practice panel/styles, reset cleanup hook in `app.js`, `test_practice.cjs`, README instructions. Five curated questions, two-minute recording limit, activity meter, up to four takes, playback/audio download, manual notes/transcript, retry focus, notes export.
- Verification: `node test_practice.cjs` passed mocked recording/save, reset cleanup, late permission cleanup, and permission-denial recovery. `node --check static/app.js` and `node --check static/practice.js` passed.
- Limitations: no automatic transcription or AI evaluation; no audio uploads. Physical microphone and browser behavior unverified. Switching modes/reset discards undownloaded takes.
- Next action: browser/local recording QA if possible; continue improving the active Rehearsal project without paid API retries.

### 2026-10-22 — Persistent agent handoff established
- Purpose: user explicitly requested documentation sufficient for a brand-new agent and mandatory ongoing updates.
- Changes: added root `AGENTS.md` continuity instructions, detailed `HANDOFF.md` state snapshot, this `WORK_LOG.md`, and entry links in project READMEs.
- Verification: inspected workspace/file inventory and `git status`; all source remains untracked, no established commit/remote. Checked that handoff references match actual project paths.
- Limitations: documentation does not itself publish, back up, or complete the project. API and browser verification blockers remain as recorded above.
- Next action: read `HANDOFF.md` next-priority list, continue Rehearsal, append a milestone entry and refresh snapshot after meaningful changes.

### 2026-10-22 — First real-browser QA (Claude in Chrome) and sample-flow fixes
- Purpose: HANDOFF priority 1, browser verification. Chrome automation became available this session.
- Changes:
  - `interview/static/index.html`: fixed literal `?` corruption in three labels ("Skip narration →", "LOCAL RECORDING · NO AI", "Ready to record · maximum 2 minutes per take").
  - `interview/static/app.js`: in sample mode, "Review my answer" no longer desynchronizes the flow (it advances via the same step as the primary button, else stays disabled); `addTurn` no longer re-enables it for sample turns; `reset()` restores the "Play sample answer →" label (previously stuck on "Sample complete ✓").
  - `.claude/settings.local.json` (gitignored): user asked that Chrome automation run without per-action prompts; allow rule added for `mcp__claude-in-chrome`.
- Verification (real Chrome on Windows, against the user-started Rehearsal server on 8766, PID observed, not restarted):
  - Desktop: full sample flow start → answer → coaching → retry → improved answer → comparison → download button visible; reset returns to 0 turns with correct labels; restart works. Browser speech synthesis did play (skip button appeared and advanced segments). No console errors. No duplicate DOM IDs.
  - Local practice panel opens with question select, Hear question, Record, focus field.
  - Mobile: 390px-wide same-origin iframe (window resize was not applied by the browser) — no horizontal overflow before or after the full sample flow; comparison stacks cleanly.
  - `python -m unittest test_interview` 8/8 OK; `node test_practice.cjs` PASS; `node --check` on app.js/practice.js OK.
- Open issues / unverified: did NOT click Record (Chrome mic permission prompt would block automation) — physical microphone capture/playback/download still unverified. Download click not exercised (would trigger a file download). Speech audio quality/voice not heard by agent. Live/text AI modes untouched (API deferral still in effect). Mobile check via iframe, not a real device.
- Next action: user does a 2-minute manual mic test in Local practice; then Rehearsal-specific submission materials (README/SUBMISSION/DEMO) and a first git commit + GitHub repo when user approves.

### 2026-10-22 (night) — Direction set by user; first commits
- Decision: user asked the agent to commit, write submission materials, and keep developing autonomously overnight. User rule: never credit Claude/Codex/AI as co-author anywhere (recorded in AGENTS.md; agent memory; local settings attribution disabled).
- Commits: `e7edb0e` snapshot of all prior work (trace-submission.zip and `.claude/` are gitignored).
- No remote/GitHub repository created; publishing still needs the user.

### 2026-10-22 (night) — Deterministic answer checks as MCP tools (works with no API key)
- Purpose: the core coach→retry→compare loop had no real computation without a paid key. Added transparent, deterministic wording checks so the loop and MCP tools work offline and are demonstrable.
- Changes: `interview/checks.py` (ownership "I" vs "we", I+action phrases, verification terms, vague outcomes, fillers, numeric claims to support, reflection/limits, length; exact-substring quotes; compare = per-signal count deltas with honest "no change" wording; no scores). `server.py`: MCP tools `check_answer_text`, `compare_answer_texts`; endpoints `/api/check`, `/api/compare-text` (go through the real MCP client); `coach_latest_answer` also attaches `rule_checks`. Fixed pre-existing bug: MCP tool errors were raised inside the anyio task group and surfaced as HTTP 500 "Internal Server Error"; now 400 with readable message. `test_checks.py` (8 tests), integration test extended and port-parametrized (`INTERVIEW_PORT`).
- Frontend: `static/checks.js` renderer; sample coaching/comparison show panels computed live by the MCP tools (labelled as such next to the authored feedback); local practice adds typed takes, "Check my words" per take, first-vs-latest comparison, notes export includes checks; WebM duration=Infinity player fix.
- Verification: Python 16/16 OK against agent-owned server on port 8767 (user's 8766 server left untouched, still running old code); `node test_practice.cjs` PASS (new mocked tests: typed takes, check gating, compare args, stale result after reset, 4-take limit). Headless Chrome (CDP driver in agent scratchpad, `--use-fake-device-for-media-stream`): sample panels render real MCP output (protocol 2025-11-25); local flow recorded a real 3 s MediaRecorder WebM from Chrome's FAKE mic device, playable, duration 3.36 s after fix; check/typed take/compare/reset work; 390px has no horizontal overflow; no console errors. Screenshots reviewed by agent.
- Open issues: physical microphone still not tested (fake device only). Heuristics are English-only word lists; can misfire (e.g. "profiled" counted as verification). Claude-in-Chrome extension disconnected mid-session; headless Chrome used instead.
- Next action: Rehearsal submission docs (root README, SUBMISSION, DEMO), then optional browser speech captions.

### 2026-10-22 (night) — Repo restructure and submission materials
- Purpose: make the repository judge-ready and draft all Devpost text.
- Changes: moved Trace into `trace/` (imports verified from new location; its README marked paused). New root `README.md` (status table, setup for Windows/macOS/Linux, MCP usage with a verified Python example, privacy, tests, layout, prior art). `SUBMISSION.md` (all Devpost fields, product feedback per tool, 5 friction-log entries, feature requests). `DEMO.md` (timed script <3 min, checklist, sample typed takes). `interview/README.md` updated. LICENSE holder set to Minh Dau. MCP server now publishes `instructions`, tool titles, and annotations (check tools read-only/idempotent/closed-world). Pluralization fix in check notes.
- Verification: re-read official rules via curl (WebFetch 403). Each friction entry was reproduced: tool error text prefix "Error executing tool <name>:"; exception inside client contexts → ExceptionGroup; `FastMCP.__init__` has no version parameter and serverInfo.version = 1.30.0. README Python example executed against port 8767 and printed 2025-11-25 plus JSON. Python 16/16 OK (test now asserts instructions and annotations).
- Open: GitHub repo, video, Devpost submission are user actions; `[fill in]` markers remain in SUBMISSION.md. The user's 8766 server still runs pre-overnight code.
- Next action: optional features (practice history across sessions via MCP; captions), keeping docs in sync.

### 2026-10-22 (night) — Opt-in practice history across sessions
- Purpose: judges list "context-aware add-on that maintains state across sessions" as creative for Alexa+. Lets an assistant open a session with last time's focus.
- Changes: `interview/history.py` (atomic JSON writes, lock, 200-entry cap, derived signals only — never answer text/audio; `INTERVIEW_HISTORY_FILE` override). MCP tools `save_practice_result`, `get_practice_progress` (+ server instructions updated); `GET/POST/DELETE /api/progress` (DELETE deliberately not an MCP tool). UI: history panel, "Use this as my focus", "Clear my history", "Save results to my progress" (disabled again until the text changes). `interview/data/` git-ignored. `test_history.py` (6 tests). Docs updated (READMEs, SUBMISSION, DEMO).
- Verification: Python 22/22 OK (integration test writes history only when `INTERVIEW_HISTORY_FILE` is set; agent server used a scratchpad file; repo `interview/data` never created). JS mocked tests PASS (progress loads on entry, save args, dedupe). Headless Chrome: save → reload → panel shows "1 saved session… your own role", focus button fills focus, clear → 0 sessions; screenshot reviewed; no console errors.
- Note: tool-call shell escapes collapse backslashes (a NUL byte and a dropped declaration slipped into practice.js once; caught by grep/node --check and fixed). Prefer Edit tool or no-backslash replacements.
- Next action: research MCP Apps spec before implementing a UI resource; else captions.

### 2026-10-22 (night) — MCP Apps view for the check tools
- Purpose: judges name "MCP Apps" as creative for Alexa+; renders check results as a card in MCP Apps hosts.
- Research: SEP-1865 (Final) and full spec `modelcontextprotocol/ext-apps/specification/draft/apps.mdx` — `ui://` resource, mimeType `text/html;profile=mcp-app`, tool `_meta.ui.resourceUri` (flat key deprecated), `ui/initialize` with `appInfo`/`appCapabilities` → `ui/notifications/initialized`, host sends `ui/notifications/tool-input` then `tool-result` (CallToolResult), view sends `size-changed`; default CSP forbids network so view is self-contained.
- Changes: `interview/mcp_app/answer_check.html` (view; theme via hostContext; renders check or compare from structuredContent, falls back to text JSON); `server.py` resource registration, tool meta, `structured_output=True` with `dict[str, Any]` returns, `/api/app-resource`, `/api/app-call` (restricted to the two linked tools), `/mcp-app-preview`; `static/mcp-app-host.html` reference host (sandbox="allow-scripts", JSON-RPC log); footer link. Docs + friction entries 6–7.
- Verification: Python 22/22 OK (asserts tool→resource linkage, resource mimeType/content, structuredContent, 422 for non-linked tool). Headless Chrome: preview host completed handshake for both tools, card rendered (screenshots reviewed), iframe resized from size-changed; sample + local QA re-run clean.
- Open: not tested in a third-party MCP Apps host (none available). Host advertises `hostCapabilities: {}`; view does not call tools back.
- Next action: commit; then optional speech captions or polish; keep docs in sync.

### 2026-10-22 (night) — Opt-in browser captions for recorded takes
- Purpose: let a spoken answer become checkable text without typing (voice-first loop).
- Changes: `static/practice.js` (SpeechRecognition opt-in, en-US, continuous/interim, restart on end while recording, final results fill the take until the user edits, abort on reset, graceful errors), checkbox + disclosure in `index.html` (hidden when unsupported), styles, docs.
- Verification: `node test_practice.cjs` PASS with new mocked-recognizer tests (opt-in only, hidden without API, fill/late results/user edits win, restart on end, abort on reset). Headless Chrome: API present, recording with captions enabled still produces a take; no console errors; recognizer returned no text in headless (expected) — real recognition unverified.
- Next action: commit; final consistency pass of docs; keep handoff current.

### 2026-10-22 (night) — Clone check, gallery, spoken tips, honest badge
- Fresh `git clone` of HEAD into scratchpad, run on port 8768 with existing venv python: Python 22/22 OK, JS PASS, `/mcp-app-preview` 200 — repo contains everything needed (pip install itself not re-run; packages already match pins).
- `docs/screenshots/` — 7 real headless-Chrome captures + captions README; SUBMISSION lists gallery order.
- Badge under Maya changed from "AI interviewer" to "Virtual interviewer" (sample/local modes use no AI). aria-label updated.
- Local practice: "Hear Maya say the tip" / "Hear Maya sum it up" buttons speak the priority with the user's own quoted phrase (verified in Chrome by intercepting speechSynthesis.speak).

### 2026-10-22 (night) — Broader action rule, more questions, agent simulation
- `checks.py`: I+action rule now accepts lowercase "i", regular past tense, present tense, "I'm …ing"; excludes learned/wanted/"used to"/"need" etc. (fairness for non-native speakers). New test.
- Five more practice questions (debugging, explaining a project, feedback, deadlines, ambiguity); rule-check regions `aria-live="polite"`.
- `interview/agent_sim.py`: scripted terminal agent (not an LLM, not Alexa) running the loop via real MCP calls per server instructions; `--demo`, `--save`; integration test runs it as a subprocess.
- Verification: Python 24/24 OK (8767 server), JS PASS, `agent_sim.py --demo` output reviewed. Repo scanned for control characters after a shell escape turned `\a` into BEL in README (fixed).

### 2026-10-22 (night) — AI text-practice UI exercised against a local mock provider; cache fix
- Added `INTERVIEW_PROVIDER_BASE_URL` (default `https://api.openai.com/v1`) so the UI can be tested against a local mock without paid calls. Mock lives only in the agent scratchpad (`mock_provider.py`, every reply prefixed `[MOCK]`); servers for this used a fake key so the real inherited key was never sent.
- Headless Chrome, AI text practice against the mock: start → answer → Review my answer (coach_latest_answer via MCP; the invented quote was filtered; rule checks rendered inside AI coaching) → retry → Compare my retry (compare_retry) and new deterministic "RULE CHECK · SAME TWO ANSWERS" panel. No console errors. This verifies UI/MCP glue only — **not** real AI quality or the provider.
- Found stale-JS caching (Chrome reused an older app.js). Server now sends `Cache-Control: no-cache` for `/`, `/static/*`, `/mcp-app-preview` (ETag revalidation).
- Tests: Python 24/24 OK; JS PASS. Live WebRTC voice path still untested (needs the real Realtime service).

### 2026-10-22 (night) — Silent captioned fallback demo video
- Produced `demo-video/rehearsal-demo-captioned.avi` (git-ignored): 1:43, 1280×720, 15 fps MJPEG, 126 MB, no audio. Pipeline (agent scratchpad): CDP `Page.startScreencast` while driving the real app on 8767 (sample → live rule check → retry comparison → typed takes → check → compare → save progress → MCP App preview), then deterministic per-frame composition in Chrome canvas (captions + intro/outro cards) and a hand-written MJPEG AVI muxer in Node (no ffmpeg available).
- First attempt (canvas MediaRecorder WebM) failed: headless timer throttling produced a 12 s file after ~1 h; deleted.
- Verification: parsed AVI (RIFF/avih/strh/strf, 1542 idx1 entries all point to JPEG SOI), extracted and viewed frames at 3 s/20 s/73 s/end — captions readable, end card states live AI unverified. **Not played in an actual video player** — user must play before uploading.
- Docs: DEMO.md fallback section, SUBMIT_CHECKLIST mention.

### 2026-10-22 (early morning) — Contrast, review, final regression; end of overnight session
- Small-text contrast raised to WCAG AA (≥4.5:1, computed) for rule checks, privacy/caption disclosures, evidence notes, and the MCP App view; screenshots refreshed. server.py import tidy after a read-through review (no logic issues found; origin/host checks, size limits, error paths reviewed).
- README/SUBMISSION wording tightened: Alexa+ "could" call the tools (not tested with Alexa+), recording verified with fake mic only, AI typed practice exercised only against a mock, OS voices may use online speech.
- Final regression against final code (agent server 8767, then stopped): Python 24/24 OK; JS PASS; headless Chrome sample, local recording (fake mic) + check + typed take + compare + mobile 390px + reset, progress save/reload/clear, MCP App preview both tools, spoken tip — all pass, no console errors.
- State: everything committed on `main`; no remote. User's own 8766 server (PID 29460) still running pre-overnight code — restart needed to see changes.
- Next action (user): follow `docs/SUBMIT_CHECKLIST.md`.

### 2026-10-22 — IN PROGRESS: resume upload and interruption checkpoints
- Request: inspect overnight changes; add resume upload; keep work resumable even if stopped suddenly.
- Reviewed: full HANDOFF, project README, latest work log and clean git status at a00a655. Preserving deterministic checks, history, captions, MCP Apps, and submission assets.
- Plan: local extraction for PDF/DOCX/TXT into editable brief, bounded file handling, no original-file storage or paid API calls; tests and docs afterwards.
- Current checkpoint: implementation about to start. Next: add parser/endpoint, then file picker + preview/apply, then tests. This entry is not a completion claim.

### 2026-10-22 — Resume upload checkpoint: implementation written, tests pending
- Added `resume_import.py` (in-memory PDF/DOCX/TXT extraction), `/api/resume` with 5 MB bound and 10-second worker timeout; pinned pypdf; file picker, editable preview and explicit Apply in brief dialog.
- Original files are not saved; no provider calls. Existing experience is replaced only on Apply, and saved brief changes only on Save.
- Next action: run parser/endpoint tests and frontend syntax/lifecycle checks; document results. Browser QA not yet performed for this feature.


### 2026-10-22 ? COMPLETE: resume upload and durable checkpoints
- Changes: parser/endpoint, PDF/DOCX/TXT picker and editable preview, explicit Apply/Save, no original-file storage; pypdf pinned; READMEs/HANDOFF updated. AGENTS now requires pre-edit IN PROGRESS checkpoints and updates after small batches.
- Verification: `python -m unittest discover -s interview -p test_resume.py -v` 7/7 passed (synthetic PDF/Word/text, encryption/blank/bad/oversize/XML rejection, actual extraction subprocess via ASGI endpoint); `node test_resume.cjs` PASS (mocked preview/apply/stale close); existing `node test_practice.cjs` PASS; new JS syntax check and git diff check passed.
- No paid API calls. Original user server left alone. File picker/rendering unverified in browser this turn; prior overnight UI verification does not cover new controls.
- Next action: update dependencies and restart server, try Your brief -> Upload -> review -> Apply -> Save; then remaining submission actions. Earlier IN PROGRESS entries are completed by this milestone. Commit this bounded change using existing user identity only.

### 2026-10-22 — IN PROGRESS: company/JD research and resume alignment
- User request: paste company and JD, search public information about interviews, tailor preparation and resume.
- Plan: cited web research (company/role only in search), separate synthesis against JD/resume, faithful evidence-backed suggestions, optional apply to interview context. Keep public facts separate from anecdotes/inferences.
- Paid API deferral remains: implement gated provider integration, mock tests only. Next: research module + endpoint, brief UI, validation/tests/docs. No live research claim.

### 2026-10-22 — Research checkpoint: implementation written, validation pending
- Added Responses web-search integration and evidence-checked synthesis. Search stage receives company/role only; JD/resume used only in subsequent model synthesis. API feature is off unless INTERVIEW_RESEARCH_ENABLED=1.
- Brief UI shows inline linked citations, inferred questions, exact resume/JD evidence pairs, gaps, and explicit apply-to-interview-notes. No automatic resume rewrite.
- Next: mocked parser/provider/endpoint tests, existing frontend regression, docs, commit. No paid calls or live verification performed.

### 2026-10-22 ? COMPLETE: company research and resume alignment
- Purpose: tailor interview preparation and suggest truthful resume improvements from company, JD and experience.
- Changes: `interview/research.py`, `/api/research`, brief schema/UI/research.js, resume Apply input notification, styles, tests, `.env.example`, README and HANDOFF. Search gets company/role only; synthesis gets resume/JD. Inline sources, inferred questions and paired exact quotes; explicit apply to context, no automatic resume rewrite. Default-off feature gate preserves API deferral.
- Verification: 7 research Python tests PASS (mocked provider/search); 22 checks/history/resume Python tests PASS (real resume extraction subprocess); `node test_research.cjs`, `node test_resume.cjs`, `node test_practice.cjs` PASS (browser mocks); JS syntax checks passed. No paid calls.
- Open issues / unverified: actual browser controls/rendering and live research/provider quality; exact quotes and citations do not prove advice is correct. Existing server not restarted; full running-server MCP suite not rerun this milestone.
- Next action: restart server and browser-check new controls; live research only after user resolves API access and lifts deferral. Finish submission actions. Earlier research IN PROGRESS checkpoints are now complete.

### 2026-10-22 - IN PROGRESS: tailor the simulated interview
- User clarified the goal is interview personalization, not resume editing. Previous resume-edit plan is superseded.
- Baseline a7ca06f clean. Next: replace edit suggestions with evidence-grounded interview probes, apply full plan to context, align interviewer prompts, test and update docs. Paid API deferral remains.

### 2026-10-22 - Interview tailoring checkpoint
- Replaced resume edits with evidence-grounded follow-ups/listen-for criteria; Apply now includes the full simulation plan and deep dives. Text/voice/coach prompts use the plan. Tests being updated; no paid calls.
- Next: run targeted tests and update current documentation.

### 2026-10-22 - COMPLETE: personalize the simulated interview
- Purpose: implement user's clarification; supersedes resume-edit suggestions from a7ca06f.
- Changes: research plan now supplies format/sequence/difficulty, questions and evidence-grounded experience probes with follow-ups/listen-for criteria. UI applies the entire plan. Text/voice/coach prompts use it. README and HANDOFF updated.
- Verification: 8 research Python tests PASS with mocked providers, including saved plan propagation to text interviewer; research/resume JS mocks PASS; research JS syntax and git diff checks PASS.
- Limitations: no paid calls, live model quality/voice and new browser rendering unverified. Fixed sample/local question bank unchanged.
- Next: browser-check after restart; verify personalized AI interviews only when user resolves API access and lifts deferral.

### 2026-10-22 - IN PROGRESS: readability and setup UX
- Baseline c94fa1b clean; read handoff/README and inspected UI. Small 8-12px text and dense setup form are main issues.
- Next: improve typography/contrast, group setup into three labeled sections, simplify copy while preserving IDs/behavior; run regressions. Browser inventory empty, visual QA unavailable.

### 2026-10-22 - COMPLETE: readable UI and guided setup
- Purpose: make the app easier to read and understand.
- Changes: `interview/static/index.html` and `style.css`: larger body/control/transcript text, darker labels, 44px controls, simpler navigation/copy, numbered setup sections (job, experience, plan), two-column role/company on desktop, stacked mobile fields, expandable saved-plan editor, explicit save footer. Existing IDs and behavior preserved.
- Verification: HTML parser confirms balanced elements and unique IDs. Research/resume/practice JS mocked regressions PASS from interview directory. Initial research test invocation from repo root failed due to its relative fixture path; rerun from correct directory passed. No paid calls or server restart.
- Limits: browser inventory empty; visual layout, keyboard traversal and phone rendering not verified. No new behavior tests added for styling-only changes.
- Next: open/reload app, inspect desktop/mobile layout and setup dialog; continue pending API/submission work.

### 2026-10-22 - IN PROGRESS: skills development goal
- Baseline 0a181ec clean. Add optional skills field to setup, saved brief, research synthesis and interview/coaching prompts. Preserve API deferral. Next: implement field and propagation, run targeted mocks, update docs.

### 2026-10-22 - COMPLETE: skills development goals
- Purpose: let users specify skills they want to practice.
- Changes: setup textarea/help, Brief.skills optional max 1000, save/reopen field mapping, research payload/invalidation, synthesis and interviewer/coach prompts, tests and continuity docs.
- Verification: 8 research Python tests PASS with mocked providers, including goals reaching synthesis/session/text interviewer but not search; research JS mock PASS for goal-change invalidation; app/research JS syntax PASS.
- Limitations: fixed sample/local checks unchanged; live personalization and browser UI unverified. No paid calls or server restart.
- Next: restart app and inspect setup save/reopen; real AI validation awaits user API access.

### 2026-10-22 - IN PROGRESS: interview round and duration
- Baseline 3414690 clean. Add validated round and 5/15/30-minute choices, pass to research/session prompts, update voice cutoff and text time reminder. No paid calls. Next: implementation and targeted tests.

### 2026-10-22 - COMPLETE: interview round and duration
- Changes: validated Brief fields, setup selectors and defaults, research payload/invalidation, round/pacing prompts, selected voice cutoff and nonblocking text reminder; docs and test_timer.cjs.
- Verification: 9 Python research tests PASS (mocked provider; includes validation and propagation); research/practice JS mocks PASS; app syntax PASS; timer boundary mocks PASS for all three lengths/modes, single notification and sample exclusion. Initial timer-file write used a duplicated interview path and failed; corrected path and test passed.
- Limits: live/browser behavior and AI pacing unverified; browser timer can be delayed in background tabs. No paid calls or server restart.
- Next: restart and browser-check setup save/reopen; working API access needed for real interview validation.

### 2026-10-22 - IN PROGRESS: setup continuity and user test pass
- Baseline 0c69781 clean. Found startSample replaces personal brief with sample data. Next: preserve saved setup, show round/duration summary, keep demo export fictional, add regression and practical test checklist. No paid calls.

### 2026-10-22 - COMPLETE: setup continuity and user test pass
- Fixed demo replacing personal brief; added round/duration summary; demo export uses sample brief. Added test_setup.cjs and docs/USER_TEST.md.
- Setup/timer/research/resume JS mocks and app syntax PASS. Browser/audio unverified; no paid calls or restart. Full reload still clears setup.
- Combined documentation command was blocked by execution policy; used patch tool and simpler documentation commands instead.
- Next: user runs checklist; fix reported issues.
- Follow-up integration check caught missing setup-summary DOM element (Unicode-sensitive replacement missed). Added element and asserted presence before finishing.

### 2026-10-22 - IN PROGRESS: failure recovery and answer improvement
- User requests analysis and improved answer after interview. Implement explicit AI suggested rewrite/missing details in existing coaching; add local no-API revision checklist; fix failed voice/reset stale question. Baseline 819d4b7. Next: code, mocked tests, docs. No paid calls.

### 2026-10-22 - COMPLETE: answer improvement and failure recovery
- Changes: server coach prompt/output for improved draft and missing questions; coaching UI text rendering; local revision checklist; reset/failed connection cleanup and 429 recovery wording; tests/docs.
- Verification: 17 CoachTests/checks Python tests PASS with mocked provider; setup/practice/recovery JS mocks PASS; app/checks syntax PASS. Initial test-edit command used wrong venv path, corrected before running. No paid calls.
- Limits: draft facts are prompt-constrained, not independently verified; local checks are deterministic, not semantic analysis. Browser rendering and actual model quality unverified.
- Next: user tests local revision checklist; verify real AI coaching once API access is available.

### 2026-10-22 - IN PROGRESS: Gemini recorded-answer review
- User supplied Gemini key locally and explicitly authorized implementation/testing. Gemini synthetic-audio tests now authorized; OpenAI deferral remains. Never log credentials.
- Next: bounded audio endpoint, Gemini transcript/analysis/rewrite, recording review UI with upload disclosure, synthetic live check and mocks.

### 2026-10-22 - Gemini implementation checkpoint
- Model list authenticated. Live synthetic WAV: 2.5 Flash 404, 3.1 Flash Lite 503, 3.5 Flash SUCCESS with matching transcript/3 evidence quotes and feedback. Default set to successful model. Draft added an unsupported inference; prompt tightened and UI explicitly labels draft for fact checking.
- Audio endpoint/validation mocks 4 PASS; practice JS regression/syntax PASS. Next: audio frontend lifecycle mocks, docs and handoff. No personal data used in tests.

### 2026-10-22 - COMPLETE: Gemini recorded-answer review
- Changes: audio_review.py and bounded /api/audio-review; browser WAV conversion/upload consent; per-recording and opt-in automatic review, transcript fill with edit protection, analysis/evidence/delivery/draft/missing details; example config, tests, README/HANDOFF.
- Verification: actual Gemini model listing 200; synthetic WAV review 200 using gemini-3.5-flash, matching transcript and 3 exact evidence quotes. Earlier model attempts 404/503. Final prompt tightened against inferred facts. Initial fixture generation failed because data directory did not exist; created it and generated synthetic WAV (gitignored).
- Tests: 12 Python audio/coach tests PASS (mocked); audio JS WAV/lifecycle tests PASS; existing practice mocks PASS and JS syntax PASS. No secret printed or personal data sent.
- Limits: physical mic/browser decoding/rendering unverified; qualitative AI delivery feedback and rewrites may be incorrect. OpenAI flows unchanged/deferred. User server not restarted.
- Next: user tests recording -> automatic Gemini review -> spoken retry after restarting server. Default model is configured in code/example, key stays in ignored .env.

### 2026-10-22 - IN PROGRESS: tailored Gemini questions and follow-ups
- User authorized continued development. Baseline c5c44f9 clean. Next: shared Gemini JSON call, tailored-question endpoint using saved setup, per-answer follow-up, retry same question, same-question comparison, lifecycle tests and synthetic live check. Only fictional context in provider tests.

### 2026-10-22 - Question flow checkpoint
- Added Gemini question/follow-up endpoint and explicit setup-data disclosure, per-recording follow-up and same-question retry actions. Comparisons now group takes by question.
- Live fictional follow-up request HTTP 200; response probed benchmarking/index tradeoffs grounded in the answer. 6 Python questions/audio tests and question/audio/practice JS mocks passed. Next: full regression, docs and commit.

### 2026-10-22 - COMPLETE: tailored Gemini question and follow-up loop
- Changes: shared Gemini JSON helper, question schema/service/API, explicit setup-sharing question button, selected-answer follow-ups, same-question retry/focus action, comparison grouping. Updated eight UI/server/docs files plus question tests and demo/submission docs.
- Live verification: fictional follow-up HTTP 200; model asked about benchmarking and index tradeoffs grounded in supplied answer. No personal data sent, no OpenAI calls.
- Regression: ALL 47 Python tests PASS on temporary owned loopback server with scratch history and real MCP calls (model calls mocked); all eight JS test files PASS. HTML nesting, unique IDs, script existence checked. Temp server stopped; user's server untouched.
- Limits: real browser/mic/audio conversion/rendering still pending; Gemini is turn-based, company web search still OpenAI and deferred. Four-take limit; downloaded notes may contain personal transcripts, setup is page-memory only.
- Next: user browser-check, then resolve any failures and remaining submission tasks. See updated DEMO route. All changes ready for checkpoint commit.

### 2026-10-22 - IN PROGRESS: Gemini-only migration
- User explicitly requested all active AI features use Gemini. Baseline 0a54a79 clean. Next: text/coaching provider migration, Google-grounded company research and citations, remove OpenAI live path from UI/runtime, update configuration/tests/docs and live fictional checks. Continuous Gemini Live remains out of scope, recorded turn-based flow stays explicit.

### 2026-10-22 - Gemini-only implementation checkpoint
- Active text/coaching/comparison now shared Gemini JSON helper. Research now Google Search grounding with UTF-8/part-aware linked citations and sandboxed Search suggestions; synthesis uses Gemini. Old OpenAI calls/control path removed; legacy token endpoint returns 410.
- Research enabled in local ignored .env at user's migration request. No keys printed. Live checks: text 503, search 429; stopped retries. Mocked migration tests pass; full regression/docs next.

### 2026-10-22 - COMPLETE: Gemini-only migration
- Purpose: one Gemini key for every active AI feature.
- Changes: shared JSON generation for text/coaching/retry; Google Search grounded research and citations/Search suggestions; removed legacy voice controls/provider calls; token endpoint 410; config and README/submission/demo/handoff updated.
- Verification: 50 Python tests PASS (mocked providers, real temporary local MCP integration and isolated history); all eight JS mock suites PASS; all JS syntax PASS. Test harness temporary-directory cleanup hit a Windows server.log file lock after all assertions passed; child terminate/wait completed. User server untouched.
- Live limits: text HTTP503, search HTTP429; no retries after these failures. Earlier audio/followup successes remain distinct. No secrets printed, no personal data sent, no OpenAI calls.
- Next: restart user app and browser/microphone-check latest controls; verify research when quota permits. Continuous Gemini Live is not implemented. Publication/submission pending.

### 2026-10-22 - IN PROGRESS: stale research configuration
- User reported disabled research. Verified local key present/flag1 without exposing key; running port8766 status is old sample-first/research false. Identified Python interview/server.py PID24520. Next: restart this app and verify status without provider calls.

### 2026-10-22 - COMPLETE: restarted stale backend
- Purpose: resolve research-disabled message despite correct .env.
- Changes: restarted identified interview/server.py on8766 with workspace venv, hidden window; updated HANDOFF. No credentials/config changed.
- Verification: GET /api/status now gemini-recorded/provider gemini/key_configured true/research_enabled true. No AI requests or quota retries.
- Limits: actual research availability still subject to prior429; restarting cleared server sessions. Browser page-memory data remains until refresh.
- Next: user can retry research from current page; preserve setup/recordings before refreshing.

### 2026-10-22 - IN PROGRESS: focused interview room and uninterrupted mock interview
- User changes priority: cleaner UI, continuous timed interview with feedback only at end. Previous recorded practice remains optional. Next: concise review cards, Gemini Live audio bridge with automatic turn detection/timed end, final session review, lifecycle tests. Live quota/browser limits will be explicit.

### 2026-10-22 - Interview implementation checkpoint
- Added live_interview.py Gemini websocket bridge with automatic speech detection, context compression, resumption, bounded audio/transcripts and timed ending; final review endpoint rejects active sessions. New focused full-screen room with microphone worklet/playback, countdown and end-only analysis; feedback now summary/priority plus expandable sections. Added websockets15.0.1 dependency.
- Syntax checks passed. Browser inventory empty; no visual/microphone QA yet. Next: lifecycle/mock tests, one fictional Live handshake if available, fix issues, docs.

### 2026-10-22 - Interview regression checkpoint
- Changes: focused room/consent, continuous PCM input/native output, timed end and final review UI; concise expandable single-answer report; no background-page interaction during live mode.
- Verification: 59 Python tests PASS, nine JS suites PASS and all JS syntax. HTML balanced/IDs unique/scripts present. Provider mocked in regression; owned test process tree stopped. Initial commands with wrong working-directory paths were corrected.
- Live: setup accepted, actual Maya audio received. First synthetic-input harness timed out because22050Hz fixture did not meet its16000Hz assertion; corrected conversion test underway. No personal data used. Browser inventory empty; visual/real mic30-minute test pending.
- Next: finish synthetic test, reconcile docs, restart app, commit. New objective supersedes earlier decision to keep continuous Live out of scope.

### 2026-10-22 - Live synthetic interview verified
- Actual Gemini Live setup accepted. Corrected22050Hz fixture conversion to16kHz PCM; synthetic answer streamed in100ms packets. Received native interviewer audio, two completed model turns, candidate transcript and clean end with no error. No personal data sent. First fixture harness timeout was not an application failure; no quota loop used.
- Voice resumption/timer are mocked-test verified only; real browser audio/UI/full30-minute behavior remain unverified. Final review fictional provider check pending. Next: update final result, restart user app with websocket dependency and commit.

### 2026-10-22 - COMPLETE: focused full-interview implementation
- Purpose: user requested realistic hands-free timed interview, with analysis only after completion, and cleaner UI.
- Changes: full-screen interview mode/native Gemini audio, safe mic/playback cleanup, automatic turns/deadline, context compression/resumption, post-interview debrief/export; compact expandable recording reviews; README/demo/submission/HANDOFF updated. Historical single-answer mode retained in expandable section.
- Verification:59 Python tests and nine JS mock suites passed; syntax/HTML IDs/nesting/script paths/diff checks passed. Live synthetic exchange succeeded with two model turns and candidate transcription. Separate live fictional final review succeeded (one answer review/two priorities). No personal data used. Provider success does not validate all advice.
- Limits: no available browser surface; current visual layout, physical mic/echo/interruptions and full30-minute session remain unverified. Resumption/timer tested with mocks. Prior company research429 remains independent. No publication performed.
- Next: restart8766 with current code; user refresh after preserving recordings, test5-minute interview first and then30-minute stability. Save transcript/review before returning to practice.

- Restart verification: current8766 serves new room and microphone worklet; invalid WebSocket session rejected before provider access. Final focused regression15 Python tests plus Live JS lifecycle/PCM test and JS syntax passed after cleanup fixes. No user recordings were sent by these checks.

### 2026-10-22 (16:30 ET) - IN PROGRESS: browser QA of Gemini build + submission doc review
- Resumed after Codex work; HEAD c50688d, tree clean. Task: run regression, browser-check current UI (setup, interview room, single-answer practice, sample, mobile) with the Claude-in-Chrome extension if connected (no CDP fallback per HANDOFF), fix findings, then reconcile README/SUBMISSION/DEMO with Gemini behavior.
- Intended files: interview/static/*, docs; no provider-config changes. Gemini calls only if needed and minimal (user authorized Gemini testing; no retry loops on 429/503).
- Next action: check server on 8766 and run test suites.

### 2026-10-22 (17:15 ET) - Browser QA fixes, batch 1
- Real Chrome (Claude-in-Chrome extension) against an isolated no-key copy of the repo on 8767 (git-tracked files only, no .env, scratch history): home, setup dialog, consent dialog, interview room (desktop + 390px iframe), debrief/results, sample flow, practice panel. No console errors.
- Fixed: (1) 12 more literal `?` glyph corruptions (`·`, `→`, `×`, `…`) in index.html, app.js setup summary, audio-review.js; (2) room length ignored saved setup (always 30) — now preselects setup duration (or the setup form's default); (3) stage's own 00:00 clock showed inside the room next to the countdown — hidden there; (4) mobile room overflowed horizontally (stage 90vw > padded width) — stage slot stretches to the column; (5) after an interview, Maya's card kept "Listen. Think. Answer." / "Conversation ended" — original caption restored.
- Mocked in-browser flow (synthetic oscillator mic, fake WebSocket, mocked transcript/review endpoints; all text prefixed [MOCK]): room start → countdown → End interview → debrief rendering (summary, keep/work-on, expandable dimensions/answer/transcript) → Back to practice restores page; empty transcript shows "no assessment". UI-only; not Gemini.
- Tests: all 9 JS suites PASS, all static JS syntax OK. Python unaffected (59 OK earlier this session).
- Not done: real Gemini Live session with a physical mic (needs the user's voice); research/text quota paths.
- Next: commit; docs review for Gemini-era claims.

### 2026-10-22 (17:30 ET) - One live Gemini check each (fictional/public data, no retries)
- Text path (`gemini_questions.practice_question`, fictional brief): SUCCESS in 4.6 s, returned a tailored question. Earlier 503 appears transient.
- Company research (`research.search_company('Amazon','Software Development Engineer Intern')`): HTTP 429 again. Not retried. Likely Search-grounding quota on this key; research stays unverified live.
- No personal data sent; key not printed.

### 2026-10-22 (17:35 ET) - IN PROGRESS: refresh screenshots + coherent submission docs
- Plan: real (non-mock) screenshots of redesigned UI via Chrome extension into docs/screenshots (replace outdated 1-practice-room, 7-mobile; add setup, consent, room); rewrite SUBMISSION.md around the interview room with accurate verification status; update README lead/status/quickstart; restructure DEMO.md. Never screenshot [MOCK] debrief as real.
- Next action: capture screenshots from isolated 8767 server.

### 2026-10-22 (18:10 ET) - COMPLETE: screenshots + coherent submission docs
- Gallery: new real captures via Chrome extension (01-home, 02-setup, 03-consent, 04-interview-room connecting state, 08-mobile); kept still-accurate sample/MCP captures renamed 05-07, 09, 10; removed old-UI 1-practice-room/7-mobile. No mock data in any image.
- SUBMISSION.md rewritten (interview room first, verification-status table, Gemini Live feedback, friction log intact). README lead/images/status/quickstart, DEMO.md single script with honesty rules + no-key fallback, SUBMIT_CHECKLIST step 1 = user's 5-minute real-mic interview. HANDOFF updated.
- Checks: control-char scan clean; .env.example key empty; .env/data untracked.
- Next: commit; then remaining improvements only if low-risk. User must do real-mic test, publish, record, submit.

### 2026-10-22 (evening) - IN PROGRESS: post-interview review returned HTTP 503
- User ran a real interview room session (first physical-mic run). Session ended and results page shown; final review failed: "Gemini request failed (HTTP 503)". Transcript section present (contents not yet confirmed).
- Plan: inspect gemini_json + /api/interview/review; add bounded retry for transient 503/500 only (never 429), optionally a fallback model; keep transcript safe; tests. Next: read code.

### 2026-10-22 (evening) - COMPLETE: resilient Gemini calls after user's review 503
- User's first real interview-room run reached the results page; final review failed with Gemini HTTP 503 (provider overload). Whether Maya spoke/heard the user and transcript contents: not yet confirmed by user.
- Changes: `audio_review.gemini_json` retries transient 500/502/503/504 and network errors up to 3 attempts (2 s, 5 s; Retry-After honored, capped 10 s); 429 never retried; clearer messages ("temporarily unavailable ... nothing was lost"). New `max_tokens` arg; post-interview review uses 12288 (was 4096) to avoid truncated debriefs on long interviews. Applies to all Gemini generateContent features.
- Tests: 3 new unit tests (503→success, bounded give-up, network retry) + quota not retried; full regression on isolated no-key copy: 62 Python OK, 9 JS suites PASS.
- User's 8766 server still runs pre-fix backend; restarting it clears in-memory interview sessions — user should download the transcript first (or press Try analysis again on the current server).
