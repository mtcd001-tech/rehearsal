> **Continuing agent:** Read [HANDOFF.md](../HANDOFF.md), [AGENTS.md](../AGENTS.md), and [WORK_LOG.md](../WORK_LOG.md) before editing. Update the handoff and log after each meaningful milestone.

# Rehearsal — interview practice

A sample-first prototype for practicing behavioral interviews, with an illustrated AI interviewer, spoken dialogue, transcript-linked feedback, and a retry comparison. Trace remains in the parent directory and is unchanged.

## Try it now

From D:\hackamazon:

```powershell
.venv\Scripts\python interview\server.py
```

Open **http://127.0.0.1:8766**. Click **Experience the sample**, then **Play sample answer**, **See the coaching**, **Try that answer again**, and **Play improved answer**. Skip narration advances the current spoken segment. Download practice notes exports only the displayed session as JSON.

Alternatively run `interview/start.ps1` from PowerShell. For a fresh checkout: create a Python 3.11+ virtual environment, install this directory's `requirements.txt`, then run `server.py`.

## What sample mode does

- Plays an original, authored engineering-internship scenario using browser speech synthesis when supported.
- Displays an original SVG interviewer with breathing, blinking, and speaking animation. This is an illustration, not generated human video or photorealistic lip sync.
- Shows a first answer, an interviewer follow-up, feedback tied to exact phrases, and a clearer retry.
- Separates structure, language clarity, and technical depth.
- Keeps the sample in browser memory. No microphone or model API is used in this mode. Browser voice availability varies; text remains readable if speech fails. Some OS/browser voices may use their own online speech service.
- The sample always uses its own fictional context. Editing Your brief affects subsequent live/text sessions, not the authored sample.

## Live implementation and current blocker

The app includes WebRTC Realtime voice, a server-side ephemeral-token endpoint, typed AI practice, and MCP tools for context, coaching, and retry comparison. **These AI paths are not verified end to end.** The configured API credential returned `429 insufficient_quota` for a minimal text request, and Realtime token setup returned HTTP 500. Work on provider access was deferred at the user's request. No further provider calls were made after that decision.

When ready, copy `.env.example` to `.env` in this directory and set a working key locally. Do not put it in a chat, browser source, screenshot, or Git commit. Restart the server. Explicit values in `.env` override inherited environment values.

Click Start live interview to read the data-use explanation and opt into microphone access. The standard API key stays on the server; the browser receives a short-lived client secret. Live sessions stop after ten minutes. End conversation closes the WebRTC connection and microphone tracks. Reset clears this app's in-memory session. This does not erase provider-side records.

Live voice sends audio and context to OpenAI; text practice and coaching send the brief and transcript. Raw audio is not stored by this app. Live session state is in server memory, cleaned approximately two hours after creation (30-second cleanup interval), on Reset, or at server shutdown. The local service is single-user, loopback-only, and not prepared for public hosting. No analytics or webcam capture is included.

## MCP and hackathon positioning

Streamable HTTP endpoint: **http://127.0.0.1:8766/mcp**

Tools:

- `get_interview_brief(session_id)` — retrieve the supplied context and recorded transcript.
- `coach_latest_answer(session_id)` — call the model, verify quoted evidence exists in the actual answer, store the baseline and retry focus.
- `compare_retry(session_id)` — compare a new answer with the coached baseline and filter unsupported quotes.

The web tool gateway invokes the real MCP endpoint. Realtime function calls are bridged through the same gateway. Protocol **2025-11-25** was verified locally. Coaching model calls were tested with mocks, not a functioning paid API.

This is an **Alexa+ experience simulation**, not an Alexa device integration. The sample alone is not a competitive demonstration of the live integration; validate an actual AI interview before submitting.

## Boundaries

This is practice feedback, not a hiring decision, clinical assessment, or validated skill score. No numeric confidence, personality, accent, or employability scores are produced. Transcript-only feedback cannot assess pronunciation or audio fluency. The coach is instructed not to invent experience or performance metrics. Quote filtering prevents invented evidence snippets but does not guarantee that all generated advice is correct.

Prior art: [Yoodli](https://yoodli.ai/use-cases/interview-preparation) already provides interview roleplay and feedback. Rehearsal does not claim that category as novel. The intended focus is a transparent, evidence-based retry loop for technical internship communication; distinctiveness and learner impact remain to be validated.

## Verification

Keep the server running, then from this directory:

```powershell
..\.venv\Scripts\python -m unittest test_interview -v
node --check static/app.js
```

Eight tests passed: evidence quote filtering, retry requirements, empty-answer handling, transcript deduplication, failed-provider behavior, response schema checks, session deletion, and local HTTP/MCP integration. No provider request is needed for these tests.

Browser QA (October 22, 2026, desktop Chrome on Windows): the full sample flow, browser speech with skip, coaching, retry comparison, and reset/restart were exercised with no console errors, and a 390px-wide layout showed no horizontal overflow. Physical microphone recording, file downloads, real mobile devices, and the live AI paths have not been verified.

## Sources used for implementation

- https://developers.openai.com/api/docs/guides/voice-webrtc
- https://developers.openai.com/api/reference/resources/realtime/subresources/client_secrets/methods/create
- https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create

## Still required before hackathon submission

Working API billing/access; actual live voice validation; browser QA; stronger differentiation/customer validation; public GitHub repository; accurate demo video; updated submission copy and tool feedback. Existing Trace submission drafts in the parent directory do not describe this project and must not be submitted as Rehearsal's materials.

## Local microphone rehearsal (no API key)

Choose **Practice my own answer**. Pick one of five original behavioral questions, optionally hear it, then select **Record my answer** and grant microphone permission. A live activity meter and timer indicate recording. Stop saves the take in the current browser tab; two minutes stops it automatically. Listen, add your own transcript/notes, pick a focus, and record a retry. Up to four takes can be compared by listening to their players. Download audio and notes separately if you want to keep them.

This mode does not upload recordings, call an AI provider, or automatically transcribe. Its prompts are self-review, not generated feedback. Reset, switching modes, or closing the tab discards undownloaded recordings. Microphone tracks are released on stop/reset and on leaving the page. Browser recording support and permission are required.

Local recording logic tests: `node test_practice.cjs` from this directory. These use mocked browser APIs to check capture/stop, cleanup, delayed permission, and permission-denial recovery. They do not replace a physical microphone/browser check.
