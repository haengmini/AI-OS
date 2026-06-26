# Agent OS Situation Room Popular Dashboard Implementation Plan

> **For Hermes:** Use delegated design/research/implementation workers, then implement and verify a static local-first dashboard artifact.

**Goal:** Build a popular, familiar web dashboard style for Agent OS that can be used by 이형민, Hermes, Claude/Gemini/Codex artifacts, and role agents.

**Architecture:** Use a local-first static dashboard generated from JSON/Markdown/Kanban state. The first implementation will be a single self-contained `index.html` with embedded CSS/JS and companion `status.json`, `agents.json`, `tasks.json`, and `situation-board.md`. Design follows the most widely adopted SaaS/developer-dashboard conventions: Linear/GitHub/Vercel style sidebar, top status bar, card grid, Kanban lanes, agent roster, project cards, and trace/artifact drill-down.

**Tech Stack:** Static HTML, CSS custom properties, vanilla JavaScript, local JSON files, Hermes Kanban CLI snapshots, Markdown companion docs.

---

## Design Decision

Select the most popular and broadly accepted pattern for agent dashboards:

- **Layout:** GitHub/Linear/Notion-style app shell: left sidebar + top bar + card grid.
- **Aesthetic:** Linear/Vercel hybrid: dark technical shell with clean cards, high contrast, compact data density.
- **Primary interaction:** user opens Mission Control and immediately sees health, blockers, active agents, projects, and tasks.
- **Agent compatibility:** every visual state is mirrored into JSON and Markdown.

## Work Allocation

1. `researcher`: survey popular agent/dashboard UI references and recommend the most familiar pattern.
2. `analyst`: map references into Agent OS information architecture and screen hierarchy.
3. `coder`: inspect available data files and propose low-risk implementation steps.
4. `reviewer`: after implementation, verify visual/readability/security requirements.
5. `reporter`: summarize results for Slack/thread.

## Files to Create or Modify

- Create: `/opt/data/agent_os_archive/dashboard/index.html`
- Create: `/opt/data/agent_os_archive/dashboard/status.json`
- Create: `/opt/data/agent_os_archive/dashboard/agents.json`
- Create: `/opt/data/agent_os_archive/dashboard/tasks.json`
- Create: `/opt/data/agent_os_archive/summaries/agent-team/situation-board.md`
- Create: `/opt/data/scripts/agent_os_situation_room_snapshot.py`
- Create: `/opt/data/scripts/agent_os_situation_room_snapshot.sh`

## Step-by-step Plan

### Task 1: Confirm source data

**Objective:** Gather live Agent OS data without using paid external model APIs.

**Commands:**

```bash
hermes kanban --board agent-os stats
hermes kanban --board agent-os list
hermes kanban --board dfxisp stats
hermes kanban --board ai-drone stats
hermes profile list
hermes cron list
```

**Expected:** Current board/profile/cron state is available.

### Task 2: Generate JSON snapshot

**Objective:** Create machine-readable dashboard state.

**Implementation:** Write a Python script that shells out to Hermes CLI and emits:

- `status.json`: overall status, timestamps, health, cost guard
- `agents.json`: roles, model family, execution mode, availability
- `tasks.json`: task cards from Kanban list output

### Task 3: Generate Markdown situation board

**Objective:** Create AI/human readable situation-board.md.

**Sections:**

```md
# Agent OS Situation Board
## Overall
## Human Attention Needed
## Agent Team
## Active Tasks
## Projects
## Governance
## Cost Guard
## Next Actions
```

### Task 4: Build self-contained web UI

**Objective:** Create static HTML following the selected popular dashboard design.

**UI Sections:**

- Sidebar: Overview, Agents, Kanban, Projects, Artifacts, Governance
- Top bar: last updated, cost mode, overall status
- Hero row: PASS/WARN/BLOCKED, blockers, todo, done
- Agent roster: 12 role cards with model badges
- Kanban lanes: triage/todo/ready/running/blocked/done
- Projects: DFXISP and AI드론 cards
- Model control plane: Hermes/Codex/Claude/Gemini/GPT availability
- Artifact/handoff panel

### Task 5: Add interactivity

**Objective:** Make the UI usable, not just static.

**Features:**

- Search/filter tasks
- Toggle compact/detailed cards
- Click agent cards to show details
- Tabs or side nav section jumping
- Copy artifact/path buttons

### Task 6: Verify locally

**Objective:** Ensure artifact renders and can be used.

**Verification:**

```bash
python3 /opt/data/scripts/agent_os_situation_room_snapshot.py
python3 -m http.server 8123 --directory /opt/data/agent_os_archive/dashboard
```

Then inspect in browser:

```text
http://127.0.0.1:8123/index.html
```

Use browser visual verification for layout issues.

### Task 7: Report

**Objective:** Provide final links/paths and explain how to choose/iterate.

**Deliverables:**

- Local path to dashboard HTML
- JSON/Markdown companion paths
- Summary of design choices
- Suggested next iteration

## Risks and Controls

- **Risk:** HTML-only state becomes opaque to agents.  
  **Control:** Mirror everything to JSON and Markdown.
- **Risk:** UI becomes too complex.  
  **Control:** Mission Control first, trace/workflow as secondary panels.
- **Risk:** Paid APIs accidentally used.  
  **Control:** API agents are shown as `manual/not_configured` unless explicitly enabled.
- **Risk:** Dashboard exposes secrets.  
  **Control:** Show only configured/not_configured, never key values.

## Validation Criteria

- Dashboard loads in browser without build step.
- `status.json`, `agents.json`, `tasks.json`, `situation-board.md` exist.
- UI shows current agent roster, Kanban status, projects, cost guard, and governance status.
- Browser visual inspection reports no obvious overlap/broken layout.
- No external API credential values are printed or embedded.
