# Devpost submission draft — Trace

Status: local working prototype; not submitted. Review this copy against the final recorded demo before publishing.

## Tagline

See where your reasoning and your Python code diverge.

## Inspiration

Backtracking can be difficult to understand from source code alone. A beginner can follow every line and still miss that several results point to the same mutable list. We wanted to make the invisible execution state visible and let learners navigate directly to the evidence behind their confusion.

## What it does

Trace runs short Python programs locally and records actual execution events. The interface pairs source code with a call stack, collection contents, stable object references, a call journey, and output. Learners can step, rewind, or play through execution.

A conversational command panel can jump to the first exception, repeated references, the next variable change, or a function return. These commands invoke a real MCP tool over Streamable HTTP. Two original examples provide an authored correction and a rerun against an explicit expected output: an off-by-one index error and backtracking that saves references instead of snapshots.

## How we built it

CPython's sys.settrace captures call, line, return, and exception events in a child process. A graph serializer preserves shared object identities and cycles. FastAPI serves the interface and trace APIs. The official MCP Python SDK exposes trace_python, inspect_step, and navigate_trace through Streamable HTTP, with protocol 2025-11-25 verified by integration tests.

The frontend is plain JavaScript, HTML, and CSS. Execution state comes from Python, not from a generated explanation.

## Alexa+ track fit

We built a simulated Alexa+ conversational debugging experience backed by a working MCP server. Its visual surface changes in response to tool calls, while run IDs and current-step context carry the investigation across questions. We do not claim access to Amazon's private Alexa+ tools or a connection to an Alexa device.

The current web demo uses a deterministic command router, not an LLM. External MCP-compatible agents can use the same tools. We deliberately expose the boundary between observed runtime facts and explanatory guidance.

## Challenges

- Preserving aliasing instead of serializing each reference as an independent list.
- Explaining that a line event captures state before execution, while return and exception events have different meanings.
- Separating an actual exception from an incorrect result: the latter needs an explicit expectation.
- Keeping the local prototype bounded without claiming that filtering Python syntax makes a secure sandbox.

## Accomplishments

The tests verify shared-list identity and independent copies, exact failed index access, recursive parent/child calls, cyclic references, and end-to-end MCP navigation. The demo requires no cloud credentials or device.

## What's next

Validate the experience with learners; improve evidence-based explanations; add a genuine model-driven MCP client and optional voice interaction; build a hardened execution service before offering public code execution. More languages and subject domains are out of this prototype's scope.

## Built with

Python, CPython tracing, MCP Python SDK, Streamable HTTP, FastAPI, Uvicorn, JavaScript, HTML, CSS.

## Product feedback draft (observations from this build)

### MCP Python SDK

Purpose: expose the trace as tools and call navigation tools from the web application.

Worked well: typed tool definitions made discoverable input schemas straightforward; the SDK supplied both server and HTTP client pieces. Integration testing verified protocol 2025-11-25 and actual tool execution.

Needs work: the older streamablehttp_client helper still ran but emitted a deprecation warning, making the similarly named client helpers easy to confuse. We changed to streamable_http_client.

Onboarding: successful tool discovery and navigation were reached during this build; no precise timing benchmark was recorded.

Would use again: yes, because the same runtime evidence can be exposed to multiple agent clients without reimplementing the trace engine.

### FastAPI and Uvicorn

Purpose: serve the local interface, validation endpoints, and mounted MCP application.

Worked well: typed request bodies and ASGI lifecycle support allowed the trace API and MCP session manager to share one local service.

Needs work: no library defect established during this build. Mounting and lifecycle ownership require care and deserve a small complete example.

Onboarding: local service and endpoint tests passed.

Would use again: yes, for local tools and API prototypes.

### CPython sys.settrace

Purpose: capture actual execution events.

Worked well: frames expose local state and events distinguish calls, lines, returns, and exceptions.

Needs work: line events happen before the source statement executes, which needs explicit UI labeling; object identity must be preserved by the application serializer. These are design constraints, not reported Python defects.

Onboarding: small controlled examples were useful for confirming event semantics.

Would use again: yes for an educational tracer, with tighter runtime isolation for public deployment.

### Browser platform

Purpose: render the interactive trace with standard HTML, CSS, and JavaScript.

Worked well: no frontend build toolchain is needed.

Needs work / onboarding: browser visual verification is pending because no browser surface was available in the build environment. Do not describe the interface as visually verified until that check is done.

Would use again: yes, subject to completing responsive and accessibility checks.

## Optional friction log

1. Task: connect an MCP HTTP client. Steps: imported the older streamablehttp_client helper and ran the integration test. Expected: clean client setup. Actual: working connection plus deprecation warning. Severity: low. Workaround: use streamable_http_client. Suggestion: emphasize the renamed helper in migration examples. Retest after the change passed.

Do not claim a guaranteed judging bonus. Do not invent additional friction entries.

## Remaining submission fields

- GitHub repository URL: pending.
- Public YouTube/Vimeo URL, under three minutes: pending.
- Primary track: Alexa+.
- Mini challenges: none claimed.
- Team members / eligibility / final terms: user review required.
- Final code and video must be frozen by October 23, 2026 at 3 p.m. EDT.
