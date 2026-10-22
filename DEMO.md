# Rehearsal — demo video script (target 2:40, hard limit under 3:00)

Record at 1440×900 or larger in Chrome. Start the server first (`.venv\Scripts\python interview\server.py`) and open `http://127.0.0.1:8766`. Turn system volume up so the browser speech is audible. Use no copyrighted music.

Only show what works today: the authored sample, the live rule checks, local practice, and the MCP server. **Do not show or imply a live AI conversation** — that path is unverified.

| Time | On screen | Say (paraphrase in your own voice) |
|---|---|---|
| 0:00–0:15 | Practice room with Maya | "Behavioral interviews are hard for internship candidates, especially in a second language. The usual feedback is a score or 'use STAR.' Rehearsal shows you the exact words to change." |
| 0:15–0:45 | Click **Experience the sample** → **Play sample answer**. Let the first answer play, then the follow-up; use *Skip narration* if needed. | "This is an authored sample, clearly labelled. The candidate says 'we worked on the database' and 'it worked well.' Maya asks the follow-up a real interviewer would: what did *you* do, and how did you check it?" |
| 0:45–1:15 | **See the coaching**. Scroll to the panel "Computed now by the check_answer_text MCP tool." | "Above is the authored coaching. Below is computed live by our MCP server: it quotes 'we built an events app,' finds no 'I + action' phrase, flags 'made it better' and 'worked well,' and gives one priority. Every quote is an exact substring — evidence can't be invented. No scores." |
| 1:15–1:40 | **Try that answer again** → **Play improved answer** → scroll to the comparison and the `compare_answer_texts` panel. | "Same story, told clearly. The comparison tool shows what actually moved: 'I' statements from 1 to 5, vague outcomes from 4 to 0, and an honest limit — 'we did not record a latency benchmark.'" |
| 1:40–2:10 | **Practice my own answer**. Record a short take (or type one), write what you said, press **Check my words**. Add a second, improved take and press **Compare first and latest take**. | "Now it's my turn. Audio stays in this browser tab. I check my words, fix the one priority, and the comparison tells me honestly whether my retry changed." |
| 2:10–2:15 | Press **Save results to my progress**; point at the history panel ("Most frequent priority: your own role"). | "If I choose, it remembers my focus across sessions — counts only, never my words." |
| 2:15–2:40 | Open `http://127.0.0.1:8766/mcp-app-preview` (footer link *MCP App preview*), click **Call check_answer_text**; point at the card and the JSON-RPC log (`ui/initialize` → `tool-result`). Optionally run the README Python snippet to show `2025-11-25`. | "It's a self-hosted MCP server — spec 2025-11-25 over Streamable HTTP, with instructions and read-only annotations for agents. The web app is an MCP client of the same tools, so Alexa+ or any agent can run this loop by voice." |
| 2:40–2:50 | Back to the app; README "What works today" table. | "Live AI voice is built but unverified, and we say so. Rehearsal: one change at a time, with proof." |

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
