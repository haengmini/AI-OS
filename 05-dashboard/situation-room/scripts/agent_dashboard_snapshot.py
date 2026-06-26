#!/usr/bin/env python3
"""Generate the Agent OS dashboard program outputs.

Inputs are Drive-backed local mirror JSON files. Outputs are a machine-readable
snapshot, a human Markdown board, and a self-contained HTML UI that works from
file:// without a server.
"""
from __future__ import annotations

import html
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("AGENT_OS_VAULT", "/opt/data/agent_os_archive/files"))
SR = ROOT / "05-dashboard" / "situation-room"
STATE_DIR = SR / "state"
DOCS_DIR = SR / "docs"
UI_DIR = SR / "ui"
OUT_JSON = STATE_DIR / "agent-dashboard.json"
OUT_MD = DOCS_DIR / "agent-dashboard.md"
OUT_HTML = UI_DIR / "agent-dashboard.html"

STATUS_PATH = STATE_DIR / "status.json"
AGENTS_PATH = STATE_DIR / "agents.json"
TASKS_PATH = STATE_DIR / "tasks.json"
ARTIFACTS_PATH = STATE_DIR / "artifact-registry.json"
SECOND_BRAIN_PATH = STATE_DIR / "second-brain-health.json"
CRON_PATH = Path("/opt/data/cron/jobs.json")
MANIFEST_PATH = Path("/opt/data/agent_os_archive/manifest.json")

ROLE_ORDER = [
    "operator", "pm", "admin", "researcher", "analyst", "coder", "reviewer", "reporter",
    "governor", "auditor", "curator", "sentinel",
]


def read_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def atomic_write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def flatten_tasks(tasks_data):
    rows = []
    for board in tasks_data.get("boards", []):
        for task in board.get("tasks", []):
            item = dict(task)
            item.setdefault("board", board.get("slug"))
            rows.append(item)
    return rows


def summarize_artifacts(registry):
    artifacts = registry.get("artifacts", []) if isinstance(registry, dict) else []
    return sorted(artifacts, key=lambda a: a.get("created_at", ""), reverse=True)[:12]


def build_snapshot():
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    status = read_json(STATUS_PATH, {})
    agents_data = read_json(AGENTS_PATH, {"agents": []})
    tasks_data = read_json(TASKS_PATH, {"boards": []})
    artifacts = read_json(ARTIFACTS_PATH, {"artifacts": []})
    second_brain = read_json(SECOND_BRAIN_PATH, {})
    cron = read_json(CRON_PATH, {})
    manifest = read_json(MANIFEST_PATH, {})

    tasks = flatten_tasks(tasks_data)
    task_counts = Counter(t.get("status") or "unknown" for t in tasks)
    board_summaries = []
    for board in tasks_data.get("boards", []):
        board_summaries.append({
            "slug": board.get("slug"),
            "name": board.get("name"),
            "default_workdir": board.get("default_workdir"),
            "counts": board.get("counts", {}),
            "assignee_counts": board.get("assignee_counts", {}),
            "task_count": len(board.get("tasks", [])),
        })

    agent_rows = agents_data.get("agents", [])
    agent_rows.sort(key=lambda a: ROLE_ORDER.index(a.get("id")) if a.get("id") in ROLE_ORDER else 999)

    attention = list(status.get("attention", []))
    if second_brain.get("overall_status") == "attention_needed":
        attention.append({
            "severity": "warn",
            "kind": "second-brain",
            "summary": "Graphify semantic rebuild needed; Second Brain wiki health is clean but graph is STALE.",
            "required_user_action": "Claude/Codex/Gemini model session should rebuild graphify-out, then Hermes verifies FRESH.",
        })

    overall = status.get("overall", "UNKNOWN")
    if any(a.get("severity") in {"fail", "critical"} for a in attention):
        overall = "FAIL"
    elif attention and overall == "PASS":
        overall = "WARN"

    cron_jobs = []
    if isinstance(cron, dict):
        jobs = cron.get("jobs", cron if isinstance(cron, dict) else {})
        if isinstance(jobs, dict):
            for jid, job in jobs.items():
                if isinstance(job, dict):
                    cron_jobs.append({
                        "job_id": jid,
                        "name": job.get("name") or jid,
                        "schedule": job.get("schedule"),
                        "enabled": job.get("enabled", True),
                        "deliver": job.get("deliver"),
                        "script": job.get("script"),
                    })

    snapshot = {
        "generated_at": now,
        "program": {
            "name": "Agent OS Dashboard",
            "version": "0.1.0",
            "source_script": "/opt/data/scripts/agent_dashboard_snapshot.py",
            "outputs": {
                "json": str(OUT_JSON),
                "markdown": str(OUT_MD),
                "html": str(OUT_HTML),
            },
        },
        "overall": overall,
        "attention": attention,
        "next_actions": status.get("next_actions", [])[:12],
        "boards": board_summaries,
        "tasks": {
            "counts": dict(task_counts),
            "total": len(tasks),
            "items": tasks,
        },
        "agents": agent_rows,
        "second_brain": second_brain,
        "artifacts": summarize_artifacts(artifacts),
        "cron": cron_jobs,
        "archive": {
            "drive_root_id": manifest.get("drive_root_id"),
            "last_sync_at": manifest.get("last_sync_at"),
            "file_count": len(manifest.get("files", {})) if isinstance(manifest.get("files"), dict) else None,
            "folder_count": len(manifest.get("folders", {})) if isinstance(manifest.get("folders"), dict) else None,
        },
        "source_files": [
            str(STATUS_PATH), str(AGENTS_PATH), str(TASKS_PATH), str(ARTIFACTS_PATH),
            str(SECOND_BRAIN_PATH), str(CRON_PATH), str(MANIFEST_PATH),
        ],
    }
    return snapshot


def badge_class(value: str) -> str:
    value = (value or "").lower()
    if value in {"pass", "healthy", "fresh", "available", "done"}:
        return "ok"
    if value in {"warn", "blocked", "stale", "attention_needed", "running", "todo"}:
        return "warn"
    if value in {"fail", "critical", "missing"}:
        return "bad"
    return "muted"


def render_markdown(data):
    lines = [
        "# Agent OS Dashboard",
        "",
        f"- Generated: `{data['generated_at']}`",
        f"- Overall: **{data['overall']}**",
        f"- HTML: `{OUT_HTML}`",
        f"- JSON: `{OUT_JSON}`",
        "",
        "## Human Attention Needed",
    ]
    if data["attention"]:
        for a in data["attention"]:
            lines.append(f"- **{a.get('severity','warn')} / {a.get('kind','attention')}** — {a.get('summary')} ({a.get('required_user_action','')})")
    else:
        lines.append("- None")
    lines += ["", "## Boards"]
    for b in data["boards"]:
        counts = ", ".join(f"{k}: {v}" for k, v in b.get("counts", {}).items())
        lines.append(f"- `{b.get('slug')}` — {counts or 'no tasks'}")
    lines += ["", "## Agents"]
    for a in data["agents"]:
        lines.append(f"- `{a.get('id')}` — {a.get('state')} / {a.get('mission')}")
    sb = data.get("second_brain", {})
    lines += [
        "", "## Second Brain",
        f"- Status: `{sb.get('overall_status')}`",
        f"- Wiki root: `{sb.get('wiki_root')}`",
        f"- Graphify: `{sb.get('graphify', {}).get('status')}`",
        f"- Broken links: `{sb.get('quality', {}).get('broken_wikilinks_count')}`",
        f"- Orphans: `{sb.get('quality', {}).get('orphan_notes_count')}`",
        "", "## Next Actions",
    ]
    for n in data.get("next_actions", []):
        lines.append(f"- `{n.get('board')}/{n.get('task_id')}` {n.get('owner')} — {n.get('action')}")
    return "\n".join(lines) + "\n"


def render_html(data):
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    overall = html.escape(str(data.get("overall", "UNKNOWN")))
    generated = html.escape(str(data.get("generated_at", "")))
    total_tasks = data.get("tasks", {}).get("total", 0)
    running = data.get("tasks", {}).get("counts", {}).get("running", 0)
    blocked = data.get("tasks", {}).get("counts", {}).get("blocked", 0)
    agent_running = sum(1 for a in data.get("agents", []) if a.get("state") == "running")
    sb_status = data.get("second_brain", {}).get("overall_status", "unknown")
    graph_status = data.get("second_brain", {}).get("graphify", {}).get("status", "unknown")

    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Agent OS Dashboard</title>
<style>
:root {{
  --bg:#f7f8fb; --panel:#ffffff; --panel2:#f2f4f8; --text:#111827; --muted:#6b7280;
  --line:#e5e7eb; --blue:#2563eb; --green:#16a34a; --amber:#d97706; --red:#dc2626;
  --purple:#7c3aed; --shadow:0 14px 35px rgba(15,23,42,.07); --radius:18px;
}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.45 Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif}}
.app{{display:grid;grid-template-columns:270px 1fr;min-height:100vh}}
aside{{position:sticky;top:0;height:100vh;background:#0b1020;color:#e5e7eb;padding:24px;border-right:1px solid #111827}}
.brand{{font-weight:780;font-size:18px;letter-spacing:-.03em;margin-bottom:6px}} .sub{{color:#94a3b8;font-size:12px;margin-bottom:28px}}
.nav button{{display:block;width:100%;text-align:left;padding:10px 12px;border:0;border-radius:12px;background:transparent;color:#cbd5e1;cursor:pointer;margin:4px 0}}
.nav button.active,.nav button:hover{{background:#172033;color:white}}
main{{padding:26px 32px 60px;max-width:1500px;width:100%}}
.top{{display:flex;align-items:center;justify-content:space-between;gap:18px;margin-bottom:22px}}
h1{{font-size:30px;margin:0;letter-spacing:-.04em}} .meta{{color:var(--muted);font-size:12px}}
.actions{{display:flex;gap:10px;align-items:center}} input,select{{border:1px solid var(--line);border-radius:11px;padding:10px 12px;background:white;min-width:210px}}
.grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;margin:18px 0 22px}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:18px}}
.kpi-label{{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.06em}} .kpi{{font-size:30px;font-weight:760;letter-spacing:-.04em;margin-top:8px}}
.badge{{display:inline-flex;align-items:center;border-radius:999px;padding:4px 9px;font-size:12px;font-weight:650;border:1px solid var(--line);background:var(--panel2)}}
.badge.ok{{color:var(--green);background:#ecfdf5;border-color:#bbf7d0}} .badge.warn{{color:var(--amber);background:#fffbeb;border-color:#fde68a}} .badge.bad{{color:var(--red);background:#fef2f2;border-color:#fecaca}} .badge.muted{{color:var(--muted)}}
.section{{display:none}} .section.active{{display:block}} .two{{display:grid;grid-template-columns:1.1fr .9fr;gap:16px}} .three{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.list{{display:flex;flex-direction:column;gap:10px}} .row{{display:flex;align-items:center;justify-content:space-between;gap:12px;border:1px solid var(--line);border-radius:14px;padding:12px;background:#fff}}
.row-title{{font-weight:650}} .row-sub{{color:var(--muted);font-size:12px;margin-top:3px}} .mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px}}
table{{width:100%;border-collapse:separate;border-spacing:0 8px}} th{{text-align:left;color:var(--muted);font-size:12px;font-weight:650;padding:0 10px}} td{{background:white;border-top:1px solid var(--line);border-bottom:1px solid var(--line);padding:12px 10px;vertical-align:top}} td:first-child{{border-left:1px solid var(--line);border-radius:12px 0 0 12px}} td:last-child{{border-right:1px solid var(--line);border-radius:0 12px 12px 0}}
.progress{{height:8px;background:#edf2f7;border-radius:999px;overflow:hidden;margin-top:10px}} .bar{{height:100%;background:linear-gradient(90deg,var(--blue),var(--purple));border-radius:999px}}
.code{{background:#0b1020;color:#d1e7ff;border-radius:14px;padding:14px;overflow:auto;white-space:pre-wrap;font-size:12px}}
@media (max-width: 1000px){{.app{{grid-template-columns:1fr}} aside{{position:relative;height:auto}} .grid,.two,.three{{grid-template-columns:1fr}} .top{{flex-direction:column;align-items:flex-start}}}}
</style>
</head>
<body>
<script type="application/json" id="dashboard-data">{data_json}</script>
<div class="app">
  <aside>
    <div class="brand">Agent OS Dashboard</div>
    <div class="sub">Mission Control · Drive-backed · Generated {generated}</div>
    <div class="nav">
      <button class="active" data-tab="overview">Overview</button>
      <button data-tab="agents">Agents</button>
      <button data-tab="tasks">Tasks</button>
      <button data-tab="brain">Second Brain</button>
      <button data-tab="artifacts">Artifacts</button>
      <button data-tab="ops">Ops</button>
    </div>
  </aside>
  <main>
    <div class="top">
      <div><h1>Mission Control</h1><div class="meta">Overall <span class="badge {badge_class(overall)}">{overall}</span> · generated {generated}</div></div>
      <div class="actions"><input id="search" placeholder="Search tasks, agents, artifacts…"/><select id="statusFilter"><option value="">All statuses</option><option>running</option><option>blocked</option><option>todo</option><option>done</option></select></div>
    </div>
    <div class="grid">
      <div class="card"><div class="kpi-label">Total tasks</div><div class="kpi">{total_tasks}</div><div class="meta">All boards</div></div>
      <div class="card"><div class="kpi-label">Running</div><div class="kpi">{running}</div><div class="meta">Active work items</div></div>
      <div class="card"><div class="kpi-label">Blocked</div><div class="kpi">{blocked}</div><div class="meta">Human attention</div></div>
      <div class="card"><div class="kpi-label">Active agents</div><div class="kpi">{agent_running}</div><div class="meta">Profiles running tasks</div></div>
    </div>
    <section id="overview" class="section active"></section>
    <section id="agents" class="section"></section>
    <section id="tasks" class="section"></section>
    <section id="brain" class="section"></section>
    <section id="artifacts" class="section"></section>
    <section id="ops" class="section"></section>
  </main>
</div>
<script>
const data = JSON.parse(document.getElementById('dashboard-data').textContent);
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, m => ({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}}[m]));
const badge = (v) => `<span class="badge ${{['pass','healthy','fresh','available','done'].includes(String(v).toLowerCase())?'ok':['warn','blocked','stale','attention_needed','running','todo'].includes(String(v).toLowerCase())?'warn':['fail','critical','missing'].includes(String(v).toLowerCase())?'bad':'muted'}}">${{esc(v)}}</span>`;
function row(title, sub, right='') {{ return `<div class="row"><div><div class="row-title">${{esc(title)}}</div><div class="row-sub">${{esc(sub)}}</div></div><div>${{right}}</div></div>`; }}
function renderOverview() {{
  const att = data.attention?.length ? data.attention.map(a => row(a.summary, a.required_user_action || a.kind, badge(a.severity))).join('') : row('No attention items', 'System has no human blockers', badge('PASS'));
  const boards = (data.boards||[]).map(b => row(b.slug, Object.entries(b.counts||{{}}).map(([k,v])=>`${{k}}: ${{v}}`).join(' · '), `<span class="mono">${{b.task_count}} tasks</span>`)).join('');
  const next = (data.next_actions||[]).slice(0,8).map(n => row(n.action, `${{n.board}} / ${{n.task_id}} / ${{n.owner}}`, badge(n.status))).join('');
  $('#overview').innerHTML = `<div class="two"><div class="card"><h2>Human Attention Needed</h2><div class="list">${{att}}</div></div><div class="card"><h2>Boards</h2><div class="list">${{boards}}</div></div></div><div class="card" style="margin-top:16px"><h2>Next Actions</h2><div class="list">${{next}}</div></div>`;
}}
function renderAgents() {{
  $('#agents').innerHTML = `<div class="three">${{(data.agents||[]).map(a => `<div class="card"><div style="display:flex;justify-content:space-between;gap:8px"><h3>${{esc(a.display_name||a.id)}}</h3>${{badge(a.state)}}</div><p class="meta">${{esc(a.layer)}} · ${{esc(a.provider_family)}} · ${{esc(a.execution_mode)}}</p><p>${{esc(a.mission)}}</p><div class="progress"><div class="bar" style="width:${{Math.min(100, Object.values(a.task_counts||{{}}).reduce((x,y)=>x+y,0)*18)}}%"></div></div><p class="mono">${{esc(JSON.stringify(a.task_counts||{{}}))}}</p></div>`).join('')}}</div>`;
}}
function filteredTasks() {{ const q=$('#search').value.toLowerCase(); const st=$('#statusFilter').value; return (data.tasks?.items||[]).filter(t => (!st || t.status===st) && JSON.stringify(t).toLowerCase().includes(q)); }}
function renderTasks() {{
  const rows = filteredTasks().slice(0,200).map(t => `<tr><td class="mono">${{esc(t.board)}}<br>${{esc(t.id)}}</td><td><b>${{esc(t.title)}}</b><div class="row-sub">${{esc((t.body||'').slice(0,180))}}</div></td><td>${{badge(t.status)}}</td><td>${{esc(t.assignee)}}</td><td class="mono">${{esc(t.created_at_iso||'')}}</td></tr>`).join('');
  $('#tasks').innerHTML = `<div class="card"><h2>Task Inventory</h2><table><thead><tr><th>ID</th><th>Task</th><th>Status</th><th>Owner</th><th>Created</th></tr></thead><tbody>${{rows}}</tbody></table></div>`;
}}
function renderBrain() {{
  const sb=data.second_brain||{{}}; const q=sb.quality||{{}}; const g=sb.graphify||{{}};
  $('#brain').innerHTML = `<div class="two"><div class="card"><h2>Second Brain</h2>${{row('Overall', sb.wiki_root||'', badge(sb.overall_status))}}${{row('Graphify', g.staleness_stdout||'', badge(g.status))}}${{row('Broken links', 'Wikilink health', badge(q.broken_wikilinks_count||0))}}${{row('Orphans', 'Inbound link coverage', badge(q.orphan_notes_count||0))}}</div><div class="card"><h2>Contract</h2><div class="code">${{esc(JSON.stringify(sb.official_contract||{{}}, null, 2))}}</div></div></div>`;
}}
function renderArtifacts() {{ $('#artifacts').innerHTML = `<div class="card"><h2>Recent Artifacts</h2><div class="list">${{(data.artifacts||[]).map(a => row(a.title||a.artifact_id, a.drive_path||a.local_cache, `<a href="${{esc(a.drive_link)}}">Drive</a>`)).join('')}}</div></div>`; }}
function renderOps() {{ $('#ops').innerHTML = `<div class="two"><div class="card"><h2>Cron</h2><div class="list">${{(data.cron||[]).map(c => row(c.name, `${{c.schedule||''}} · ${{c.script||''}}`, badge(c.enabled?'enabled':'disabled'))).join('')}}</div></div><div class="card"><h2>Archive</h2><div class="code">${{esc(JSON.stringify(data.archive||{{}}, null, 2))}}</div><h3>Source files</h3><div class="code">${{esc((data.source_files||[]).join('\n'))}}</div></div></div>`; }}
function renderAll() {{ renderOverview(); renderAgents(); renderTasks(); renderBrain(); renderArtifacts(); renderOps(); }}
renderAll();
document.querySelectorAll('.nav button').forEach(b => b.onclick = () => {{ document.querySelectorAll('.nav button,.section').forEach(x=>x.classList.remove('active')); b.classList.add('active'); document.getElementById(b.dataset.tab).classList.add('active'); }});
$('#search').addEventListener('input', renderTasks); $('#statusFilter').addEventListener('change', renderTasks);
</script>
</body>
</html>"""


def main():
    data = build_snapshot()
    atomic_write(OUT_JSON, json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    atomic_write(OUT_MD, render_markdown(data))
    atomic_write(OUT_HTML, render_html(data))
    print(json.dumps({"ok": True, "outputs": data["program"]["outputs"], "overall": data["overall"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
