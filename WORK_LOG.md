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
