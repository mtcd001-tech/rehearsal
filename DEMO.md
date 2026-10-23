# Rehearsal demo video (target 2:45, under 3:00)

## Prepare once

Preserve any current transcript, then restart the server in your terminal:

```powershell
.venv\Scripts\python interview\server.py
```

Refresh http://127.0.0.1:8766 and use headphones. The five-minute interview and webcam are already user-confirmed. Check the new Pressure Replay flow once: finish a short interview, select a quoted moment, answer the original question and changed-condition follow-up, then confirm the comparison and original debrief remain available. Download both. No full 30-minute test is required.

Use fictional experience and job details. Keep keys, `.env`, personal contact details and private browser tabs off screen. Company research is optional and quota-blocked; use the supplied brief. Do not depend on research for the recording.

## Primary script: interview, feedback, replay

Record the real flow first, then edit excerpts to these timings. Do not speed up speech to fit. Narration can be recorded afterward.

| Time | Show | Suggested narration |
|---|---|---|
| 0:00–0:15 | Setup: role, experience and skill focus | "Rehearsal helps me practice the difficult part of an interview: explaining my own contribution, then answering a follow-up." |
| 0:15–0:55 | Live room: one answer and follow-up; show End interview | "Maya uses my interview brief. I speak naturally, without clicking between answers. Coaching waits until the end. This is an excerpt." |
| 0:55–1:15 | Debrief: exact quoted line, improvement focus, Pressure Replay selector | "The feedback points to my words. Instead of just reading advice, I can retry this specific moment." |
| 1:15–2:10 | Replay: original question, spoken retry, changed-condition follow-up, reply and ending | "Maya repeats the question, then changes one condition. That gives me a chance to apply the feedback and explain my reasoning under pressure." |
| 2:10–2:35 | Actual before/retry quotes, separate follow-up feedback; expand Wording comparison | "The comparison shows evidence of what changed, including remaining gaps. The wording panel calls our self-hosted MCP tool. It can also report no improvement." |
| 2:35–2:45 | Comparison card or home page | "Interview, reflect, then retry the hard moment. This is a web simulation backed by MCP tools; it has not been connected to Alexa+ itself." |

Let the actual result determine the narration. Do not claim improvement if the comparison reports mixed or insufficient evidence. Exact quote matching does not prove the model's reasoning correct. Suggested answer drafts still need fact-checking.

Caption edits such as "interview excerpt", "cut: debrief generating" and "replay excerpt". Show whether replay ended automatically or manually. Never imply an edited clip is a complete 30-minute session.

## Fallback if replay or the provider fails

If the main interview works but replay does not, show the actual interview and debrief, then demonstrate the deterministic MCP comparison through single-answer practice or the authored sample. Describe replay as implemented but not demonstrated; do not splice a synthetic test into a claimed user session.

If live voice is unavailable, show the no-key authored sample: answer, follow-up, live `check_answer_text` output, retry, `compare_answer_texts`, and the footer's MCP App preview. Clearly say "authored sample" and distinguish the authored answers from tool output computed now. State why live voice could not be shown. Do not use mocked results as live output.

## Before uploading

- [ ] Real flow rehearsed; original debrief and replay download checked if replay is featured.
- [ ] No secrets or personal information visible; no copyrighted music.
- [ ] Cuts/excerpts labelled; actual Alexa integration and full 30-minute stability not claimed.
- [ ] Any authored sample is identified on screen.
- [ ] Video under 3:00; public upload link added to SUBMISSION.md and Devpost.

The silent AVI in `demo-video/` predates the redesign and must not be submitted. Existing gallery screenshots also predate Pressure Replay; capture a fresh comparison screenshot only after checking the new flow.
