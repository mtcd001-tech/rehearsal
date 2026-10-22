# User test pass (about 10 minutes)

Restart the existing server, then open http://127.0.0.1:8766 and refresh. No paid API needed.

1. Setup: enter role/company/JD, choose Technical and 5 minutes, enter Clear explanations as your goal. Save and reopen. All values should remain; the page summary should show Technical and 5 minutes.
2. Resume: select PDF/DOCX/TXT, review extracted text, Apply, Save and reopen. Experience should match. Selecting another file alone must not replace it.
3. Demo: play sample, see coaching, retry and compare. Reopen setup: your personal details must remain. The demo itself stays fictional.
4. Microphone: Practice my own answer, record 20 seconds, stop and play back. Confirm sound and duration. Leave captions off. Type what you said, Check my words, add a second take and compare. Recording alone does not transcribe.
5. Readability: narrow the window; check labels, dropdowns and Save button. Try keyboard Tab through setup and Escape to close.
6. Research disabled state: with company/JD present, Build my tailored interview should show API setup needed, without inventing a report or erasing fields.

Report step number, clicked control, expected result, actual result and exact error. Screenshots help with layout; hide private details.

Setup lives in page memory. Full reload clears it; close/reopen and mode changes should preserve it. Live AI quality and selected voice time limits need a later API-enabled test.

## Gemini pass (API now configured)

After restarting, save a fictional setup and open Practice my own answer. Click Ask a question from my setup, then Hear the question. Enable automatic Gemini analysis, record 20 seconds, stop and wait for transcript/feedback. Practice this answer again should restore that exact question; Ask me a follow-up should prepare a question based on your answer. A follow-up must not be compared as a retry of a different question. Confirm Reset clears takes and late results do not reappear. These actions send disclosed context/audio to Google.
