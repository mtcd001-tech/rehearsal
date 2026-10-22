# Rehearsal — demo video script (target 2:40, hard limit under 3:00)

Record at 1440×900 or larger in Chrome. Start the server first (`.venv\Scripts\python interview\server.py`) and open `http://127.0.0.1:8766`. Turn system volume up so the browser speech is audible. Use no copyrighted music.

The original no-key script below remains a fallback. See the Gemini route at the end before making a new recording.

Only show what works today: the authored sample, the live rule checks, local practice, and the MCP server. **Do not show or imply a live AI conversation** — continuous voice is not implemented.

| Time | On screen | Say (paraphrase in your own voice) |
|---|---|---|
| 0:00–0:15 | Practice room with Maya | "Behavioral interviews are hard for internship candidates, especially in a second language. The usual feedback is a score or 'use STAR.' Rehearsal shows you the exact words to change." |
| 0:15–0:45 | Click **Experience the sample** → **Play sample answer**. Let the first answer play, then the follow-up; use *Skip narration* if needed. | "This is an authored sample, clearly labelled. The candidate says 'we worked on the database' and 'it worked well.' Maya asks the follow-up a real interviewer would: what did *you* do, and how did you check it?" |
| 0:45–1:15 | **See the coaching**. Scroll to the panel "Computed now by the check_answer_text MCP tool." | "Above is the authored coaching. Below is computed live by our MCP server: it quotes 'we built an events app,' finds no 'I + action' phrase, flags 'made it better' and 'worked well,' and gives one priority. Every quote is an exact substring — evidence can't be invented. No scores." |
| 1:15–1:40 | **Try that answer again** → **Play improved answer** → scroll to the comparison and the `compare_answer_texts` panel. | "Same story, told clearly. The comparison tool shows what actually moved: 'I' statements from 1 to 5, vague outcomes from 4 to 0, and an honest limit — 'we did not record a latency benchmark.'" |
| 1:40–2:10 | **Practice my own answer**. Record a short take (or type one), write what you said, press **Check my words**. Add a second, improved take and press **Compare first and latest take**. | "Now it's my turn. Audio stays in this browser tab. I check my words, fix the one priority, and the comparison tells me honestly whether my retry changed." |
| 2:10–2:15 | Press **Save results to my progress**; point at the history panel ("Most frequent priority: your own role"). | "If I choose, it remembers my focus across sessions — counts only, never my words." |
| 2:15–2:40 | Open `http://127.0.0.1:8766/mcp-app-preview` (footer link *MCP App preview*), click **Call check_answer_text**; point at the card and the JSON-RPC log (`ui/initialize` → `tool-result`). Optionally run `.venv\Scripts\python interview\agent_sim.py --demo` to show an assistant-style turn order with real tool calls. | "It's a self-hosted MCP server — spec 2025-11-25 over Streamable HTTP, with instructions and read-only annotations for agents. The web app is an MCP client of the same tools, so Alexa+ or any agent can run this loop by voice." |
| 2:40–2:50 | Back to the app; README "What works today" table. | "Gemini practice is turn-based; continuous voice is not implemented. Rehearsal: one change at a time, with proof." |

## Fallback: silent captioned walkthrough

If there is no time to record, use `demo-video/rehearsal-demo-captioned.avi`:

- 1:43 long, 1280×720, 15 fps, Motion-JPEG, 126 MB, **no audio**.
- A captioned capture of the real app following this flow, with an intro card and an honest end card.
- Rendered in headless Chrome from screencast frames.
- The file structure was validated, but the agent could not play it in a video player. **Play it once before uploading** (for example in VLC or Windows Media Player). YouTube accepts AVI.
- It is git-ignored, so it is not in the repository.

A narrated recording of your own is stronger. Judges respond to a real voice, and the browser speech is not audible in the capture.

## Recording checklist

- [ ] Server started from a fresh terminal; page reloaded before recording.
- [ ] Microphone permission granted in Chrome before recording (or use the typed take).
- [ ] The words "authored sample" and "computed now by the … MCP tool" are visible on screen.
- [ ] No API key, `.env`, or personal data visible in the terminal or editor.
- [ ] Video under 3:00, uploaded publicly to YouTube or Vimeo; link pasted into `SUBMISSION.md` and Devpost.

## Suggested typed takes for the practice segment (or say your own)

First take:

> So we, um, built a dashboard for our club. We had some problems with loading and we made it better. It worked well.

Retry:

> I owned the loading problem on our club dashboard. I profiled the page and found we fetched every event at once, so I added pagination and tested it on a slow connection. It loaded noticeably faster, but I did not measure it, so next time I would record load times before and after.

These were used in automated browser QA; the comparison reports that all six tracked signals moved toward the suggestion.

## Updated Gemini route (target under 3 minutes; browser-check before recording)

Use fictional resume/JD and answers, never your key or personal contact details. Gemini audio and follow-up calls passed live synthetic/fictional tests, but rehearse the full browser flow first. If it fails, use the no-key script above and label the limitation.

- 0:00-0:20: explain the problem; show setup with role, interview round and development goal.
- 0:20-0:45: Practice my own answer -> Ask a question from my setup -> Hear the question. Explain that this is a simulated question, not company-confirmed research.
- 0:45-1:15: enable Gemini analysis, record a short fictional answer and stop. Explain that audio is sent to Google only after opting in. Do not present synthetic or prerecorded speech as a live user response.
- 1:15-1:50: show actual transcript, a quoted finding, one retry focus and the suggested draft. Mention that draft facts need review.
- 1:50-2:15: Practice this answer again; record a clearer retry, then show deterministic same-question comparison if time permits.
- 2:15-2:35: Ask me a follow-up; explain the distinction between Gemini contextual questions and MCP rule checks.
- 2:35-2:55: show MCP App preview or terminal simulation and the real tool result. Close with the limitation: turn-based Gemini practice, no verified continuous voice or Alexa device integration.

API wait times count toward the recording length; rehearse timing. If editing out waits, label the cut rather than claiming instantaneous processing.

Migration check: all active AI features now use Gemini. Text and company research returned HTTP 503/429 during live verification. Rehearse availability before recording; do not show mocked research as live.
