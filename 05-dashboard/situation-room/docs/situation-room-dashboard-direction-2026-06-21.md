# Agent OS Situation Room — Popular Dashboard Direction

Date: 2026-06-21 UTC
Task: t_9194d0ab
Role: researcher
Status: research recommendation, not final product decision

## Summary

Recommended familiar direction: a local-first “Mission Control” dashboard that combines GitHub Agent HQ’s assign / steer / track mental model with a Linear-style dark app shell and Vercel-style disciplined card system. Agent-specific panels should borrow from LangSmith, AutoGen Studio, and Agno/AgentOS: graph/debug views, agent roster, trace/session monitoring, HITL/audit cues, and task-to-artifact handoffs.

This should be treated as a design direction for analyst/owner approval, not a unilateral final decision. The strongest fit for Agent OS is not a workflow-builder-first canvas; it is a daily operations dashboard where humans and agents can both read the same state through HTML + Markdown + JSON.

## Inputs

Local archive files read first:

1. `/opt/data/agent_os_archive/.hermes/plans/2026-06-20_0100-agent-os-situation-room-popular-dashboard.md`
2. `/opt/data/agent_os_archive/files/05-dashboard/DASHBOARD-README.md`
3. `/opt/data/agent_os_archive/files/05-dashboard/README.md`
4. `/opt/data/agent_os_archive/files/05-dashboard/design/figma/design-spec.md`
5. `/opt/data/agent_os_archive/summaries/agent-team/agent-dashboard-sota-survey-2026-06-20.md`
6. `/opt/data/agent_os_archive/summaries/agent-team/multi-model-dashboard-strategy.md`
7. `/opt/data/agent_os_archive/summaries/agent-team/handoff-contract.md`

External/reference pages checked by HTTP fetch:

1. GitHub Agent HQ blog — https://github.blog/news-insights/company-news/welcome-home-agents/
2. GitHub Copilot cloud agent docs — https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent
3. LangSmith Studio docs — https://docs.langchain.com/langsmith/studio
4. LangSmith Observability — https://www.langchain.com/langsmith/observability
5. AutoGen Studio docs — https://microsoft.github.io/autogen/dev/user-guide/autogenstudio-user-guide/index.html
6. Agno homepage — https://www.agno.com/
7. Agno agent-ui GitHub — https://github.com/agno-agi/agent-ui
8. Linear and Vercel design-system templates from local `popular-web-designs` skill:
   - `templates/linear.app.md`
   - `templates/vercel.md`

## Output

Created this research handoff:

`/opt/data/agent_os_archive/summaries/agent-team/situation-room-dashboard-direction-2026-06-21.md`

## Decisions

### 1. Recommended top-level metaphor: Mission Control

Use GitHub Agent HQ as the strongest mental model.

Evidence:
- GitHub’s Agent HQ page describes “a mission control, a single command center to assign, steer, and track the work of multiple agents from anywhere.”
- GitHub Copilot cloud agent docs describe an agent that can research a repository, create an implementation plan, make branch changes, and allow review/iteration before PR creation.
- The existing Agent OS plan already names this pattern: “Mission Control” first screen with health, blockers, active agents, projects, tasks, and trace/artifact drill-down.

Interpretation:
- Agent OS should adapt this from repo/PR operations to Kanban/task/artifact operations.
- The first screen should answer: What is blocked? Who/what is running? What needs 형민’s decision? What artifacts changed? What can an agent safely do next?

### 2. Recommended visual language: Linear dark app shell + Vercel discipline

Use a Linear-like dark, technical operations shell, but apply Vercel-like restraint for cards, spacing, and hierarchy.

Evidence from local design templates:
- Linear pattern: dark-mode-native app surface, near-black backgrounds, subtle borders, compact data density, one restrained violet/indigo accent, excellent for developer dashboards.
- Vercel pattern: highly disciplined typography, cards, shadow-as-border, restrained monochrome hierarchy, developer-infrastructure familiarity.
- Existing Agent OS plan line 18 already proposes a “Linear/Vercel hybrid: dark technical shell with clean cards, high contrast, compact data density.”

Interpretation:
- Prefer dark mode for “situation room” feeling and long-running operations monitoring.
- Borrow Vercel’s restraint so the dashboard does not become a noisy sci-fi control panel.
- Avoid decorative gradients except very subtle status highlights.

### 3. Recommended information architecture

Use this hierarchy for MVP:

1. Overview / Mission Control
   - Overall status: PASS / WARN / BLOCKED
   - Human Attention Needed
   - Active blockers
   - Kanban counts and lane preview
   - Agent roster summary
   - Project cards
   - Governance/cost guard strip
   - Recent artifacts / handoffs

2. Agents
   - Role, provider family, execution mode, availability, current task, last artifact, cost risk

3. Kanban
   - triage / todo / ready / running / blocked / done lanes
   - task cards tied to assignee, blocker, artifact count, last updated

4. Graph / Flow
   - operator → pm → researcher/analyst/coder/admin → reviewer → reporter
   - governor/auditor/curator/sentinel as governance side-band

5. Traces / Runs
   - lightweight local trace summaries first
   - deeper LangSmith/Langfuse/Phoenix-style trace tree later

6. Artifacts / Handoffs
   - paths, summaries, verification state, next agent

7. Cost / Provider Guard
   - paid provider enabled yes/no
   - manual/offline mode available yes/no
   - no credential values

### 4. Agent UI references to include, but not copy wholesale

- GitHub Agent HQ: top-level command center; assign / steer / track; trusted developer workflow.
- LangSmith / LangGraph Studio: graph-based debug and observability drill-down; useful for run traces, not necessarily the home page.
- AutoGen Studio: agent/team prototyping and “low-code multi-agent workflow” vocabulary; useful for role/team pages.
- Agno / AgentOS / agent-ui: chat + trace + monitor/manage direction; useful for agent detail panels and runtime/session management.
- Linear/Vercel/SaaS dashboards: familiar app shell, sidebar, top status bar, cards, command palette/search, compact tables, clear badges.

### 5. Human + AI readability rule

Every visual state should have a paired machine-readable and prompt-readable representation:

- Human: `/opt/data/agent_os_archive/dashboard/index.html`
- Machine/agents: `/opt/data/agent_os_archive/dashboard/status.json`, `agents.json`, `tasks.json`, `artifacts.json`
- Human + AI prompt context: `/opt/data/agent_os_archive/summaries/agent-team/situation-board.md`
- Source of truth for work: Hermes Kanban DB
- Durable source/archive: `/opt/data/agent_os_archive/files` and summaries

This preserves the existing archive rule that `dashboard-state.json` is shared state and prevents the UI from becoming an opaque artifact only humans can inspect.

## Suggested dashboard direction in one sentence

Build Agent OS Situation Room as a local-first GitHub-Agent-HQ-like Mission Control: Linear dark operational shell, Vercel-clean card/grid discipline, LangSmith-style trace drill-down, AutoGen/Agno-style agent/team panels, and Markdown/JSON mirrors for every visible state.

## Concrete UI pattern spec

### Layout

```text
┌────────────────────────────────────────────────────────────┐
│ Top bar: Agent OS Situation Room | updated | cost | status │
├──────────────┬─────────────────────────────────────────────┤
│ Sidebar      │ Overview / Mission Control                  │
│ Overview     │                                             │
│ Agents       │ [Overall] [Needs Human] [Kanban] [Cost]     │
│ Kanban       │                                             │
│ Graph        │ [Agent roster cards] [Project cards]        │
│ Runs/Traces  │                                             │
│ Artifacts    │ [Active lanes] [Recent artifacts/handoffs]  │
│ Governance   │                                             │
└──────────────┴─────────────────────────────────────────────┘
```

### Visual tokens

- Background: near-black / deep slate.
- Panels: slightly lifted dark surfaces with subtle semi-transparent border.
- Primary accent: one violet/indigo accent for active nav, selected state, and key CTA.
- Status colors: green PASS, amber WARN, red BLOCKED, blue RUNNING, gray MANUAL/OFFLINE.
- Typography: Inter or Geist; monospace for task IDs, paths, run IDs, timestamps.
- Density: compact but not cramped; table/card hybrid for agent and task lists.
- Mobile: sidebar collapses; first screen becomes vertical cards with “Needs Human” near the top.

### Component priorities

1. Human Attention Needed card — should be visually dominant when non-empty.
2. Overall status strip — always visible.
3. Agent roster — role-first, model/provider second.
4. Kanban preview — counts plus latest blocked/running cards.
5. Artifact/handoff panel — path, source task, verification status.
6. Governance/cost guard — small but persistent; no secrets.

## Evidence Notes

Facts from archive:

- The local plan already specifies a static, local-first dashboard with `index.html`, `status.json`, `agents.json`, `tasks.json`, and `situation-board.md`.
- The dashboard layer README defines Dashboard as Visual Interface, Slack as Mobile Command Interface, and JSON as Shared State Layer.
- The existing design spec requires Korean/English hybrid UI, mobile responsive layout, card-based layout, clear status colors, JSON-driven data, and minimal manual editing.
- The multi-model strategy says the dashboard should be model-agnostic, using Provider/Model → Profile/Adapter → Agent Role → Kanban Task → Artifact/Handoff/Trace → Dashboard View.

Facts from external fetches:

- GitHub Agent HQ page fetched HTTP 200; title: “Introducing Agent HQ: Any agent, any way you work - The GitHub Blog.” Its page text includes the mission-control phrase and “assign, steer, and track” language.
- GitHub Copilot cloud agent docs fetched HTTP 200; description says Copilot can research a repository, create an implementation plan, make code changes on a branch, and support review/iteration.
- LangSmith Observability page fetched HTTP 200; description says it provides tracing, real-time monitoring, debugging, cost and latency tracking.
- AutoGen Studio docs fetched HTTP 200; page text says it lets users compose teams and interact with them for tasks, and describes a no-code developer tool for building/debugging multi-agent systems.
- Agno homepage fetched HTTP 200; description says it is an agent framework and high-performance runtime for multi-agent systems, with AgentOS for building/running/managing secure multi-agent systems.
- Agno agent-ui GitHub page fetched HTTP 200; description says it is a modern chat interface for AI agents built with Next.js, Tailwind CSS, and TypeScript.

Interpretations / recommendations:

- GitHub Agent HQ is the best top-level mental model because Agent OS is primarily an operations and task coordination system.
- LangSmith/AutoGen/Agno are better as secondary/detail screens than as the MVP home page because their strongest patterns are traces, graph/team prototyping, chat/session management, and runtime ops.
- Linear/Vercel conventions are familiar to developer/SaaS users and match the requested human + AI readability goal better than a highly custom visual canvas.

## Verification

Checks performed:

1. Read local archive/source files under `/opt/data/agent_os_archive/files` and `/opt/data/agent_os_archive/summaries`.
2. Loaded local `popular-web-designs` skill and inspected Linear and Vercel templates.
3. Fetched official/reference pages with Python `urllib.request`; all listed external references returned HTTP 200 except Linear title extraction was inconclusive due site rendering/minification, but the local Linear design template was available and used.
4. Created this handoff file in the required Agent OS handoff-contract style.

No browser visual implementation was produced in this task; this task is research/design-direction only.

## Open Questions

1. Final owner/analyst approval is still needed before treating this direction as binding product design.
2. Need a follow-up analyst or designer to translate this into a concrete `DESIGN.md` or wireframe spec.
3. Need a coder task only after data schema and visual priorities are accepted.
4. The dashboard should not expose credentials; provider status should remain `configured/not_configured/manual`, not raw secrets.

## Next Agent

Recommended next agent: `analyst` or `pm`.

Reason: convert this research direction into a scoped implementation spec: exact screen sections, JSON schema, MVP acceptance criteria, and handoff to `coder` for static dashboard implementation.
