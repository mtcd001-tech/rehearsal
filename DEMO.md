# Demo recording script — target 2 minutes 35 seconds

Record the actual app at http://127.0.0.1:8765. Use your own narration; no third-party music or footage is necessary. This is a script, not a completed video.

## 0:00–0:18 — The problem

Screen: The disappearing subsets example, then jump to the end.

Say: “This backtracking program finishes without an exception. But all eight answers are empty. Reading the source does not make the mistake obvious. Trace lets you see what your code actually did.”

## 0:18–0:58 — Find the evidence

Click “Find shared references.” Show the response, the selected timeline event, and the object memory. Step forward several times or play slowly.

Say: “Find shared references. That question calls our MCP navigation tool and moves the canvas to recorded evidence. These result entries point to one object. As backtracking changes path, every saved reference sees the change. The animation is driven by real Python execution, not an invented model response.”

## 0:58–1:25 — Compare a correction

Click “Compare with a correction.” Show before and after outputs. Inspect result references if time permits.

Say: “This example's correction stores a copy instead. We rerun the program and compare its actual output with an explicit expected answer. Each subset now owns its snapshot. This is an authored example patch, not a claim to automatically fix arbitrary code.”

## 1:25–1:55 — Watch an error happen

Choose “One step too far.” Click “Show the error.” Highlight the attempted access panel, i = 4, and the four-element list. Step back once, then forward.

Say: “For an index error, Trace jumps to the exact failing event. The list has four slots, zero through three. The loop asks for slot four. There is no element to reach.”

## 1:55–2:18 — Platform integration

Show the MCP status below the command panel. Optionally briefly show README endpoint and tool names without losing the app demonstration.

Say: “This is our Alexa+ experience simulation. The working server uses Streamable HTTP and MCP protocol 2025-11-25. Our web demo uses deterministic commands; an MCP agent can call the same trace, inspection, and navigation tools. We are not connected to an Alexa device.”

## 2:18–2:35 — Close

Choose the recursion example and use “Next return.”

Say: “Trace turns a confusing execution into something you can inspect and ask about. The prototype supports short local Python programs. Our next step is testing with learners and adding a model-driven assistant while keeping every runtime claim grounded in the trace.”

## Recording checks

- Keep all claims consistent with what is working on screen.
- Check readable browser zoom and clear narration.
- Keep the finished video below three minutes.
- Upload as public to YouTube or Vimeo and test the link signed out.
- Do not include credentials or unrelated personal tabs.
