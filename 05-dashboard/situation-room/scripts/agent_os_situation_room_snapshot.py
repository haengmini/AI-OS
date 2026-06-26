#!/usr/bin/env python3
"""Generate Agent OS Situation Room static dashboard.

Local-first, no external APIs. Reads Kanban SQLite DBs and local JSON/Markdown
state, then writes machine-readable JSON, human/AI-readable Markdown, and a
self-contained HTML dashboard.
"""
from __future__ import annotations

import html
import json
import os
import sqlite3
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path("/opt/data")
ARCHIVE = ROOT / "agent_os_archive"
DASHBOARD = ARCHIVE / "dashboard"
SUMMARIES = ARCHIVE / "summaries" / "agent-team"
KANBAN_ROOT = ROOT / "kanban" / "boards"
PROFILES_DIR = ROOT / "profiles"
CRON_JOBS = ROOT / "cron" / "jobs.json"
HEALTH_JSON = SUMMARIES / "status.json"
MANIFEST_JSON = ARCHIVE / "manifest.json"

BOARD_SLUGS = ["agent-os", "dfxisp", "ai-drone"]
STATUSES = ["triage", "todo", "scheduled", "ready", "running", "blocked", "done", "archived"]
ROLES = [
    ("operator", "Control", "요청 접수·맥락 보존·라우팅"),
    ("pm", "Control", "목표 분해·완료 기준·의존성 설계"),
    ("admin", "Ops", "Drive·Slack·Cron·인증·운영 설정"),
    ("researcher", "Specialist", "근거 수집·자료 조사·출처 정리"),
    ("analyst", "Specialist", "분석·tradeoff·설계 판단"),
    ("coder", "Specialist", "구현·스크립트·테스트"),
    ("reviewer", "Governance", "산출물 검증·품질 게이트"),
    ("reporter", "Specialist", "Slack/Drive/문서 보고"),
    ("governor", "Management", "팀 구조·라우팅 무결성"),
    ("auditor", "Management", "상태/준수 감사"),
    ("curator", "Management", "지식 위생·문서 정리"),
    ("sentinel", "Management", "지연/실패/이상 감시"),
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime | None = None) -> str:
    return (dt or utc_now()).isoformat(timespec="seconds")


def epoch_to_iso(value: Any) -> str | None:
    if value in (None, ""):
        return None
    try:
        return datetime.fromtimestamp(int(value), timezone.utc).isoformat(timespec="seconds")
    except Exception:
        return None


def read_json(path: Path, default: Any) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n")


def read_board(slug: str) -> dict[str, Any]:
    board_dir = KANBAN_ROOT / slug
    meta = read_json(board_dir / "board.json", {})
    db = board_dir / "kanban.db"
    tasks: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    assignee_counts: dict[str, Counter[str]] = defaultdict(Counter)
    if db.exists():
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
        comments = {r["task_id"]: r["n"] for r in con.execute("SELECT task_id, COUNT(*) n FROM task_comments GROUP BY task_id")}
        attachments = {r["task_id"]: r["n"] for r in con.execute("SELECT task_id, COUNT(*) n FROM task_attachments GROUP BY task_id")}
        events = {r["task_id"]: r["last_event_at"] for r in con.execute("SELECT task_id, MAX(created_at) last_event_at FROM task_events GROUP BY task_id")}
        link_parents: dict[str, list[str]] = defaultdict(list)
        link_children: dict[str, list[str]] = defaultdict(list)
        for r in con.execute("SELECT parent_id, child_id FROM task_links"):
            link_children[r["parent_id"]].append(r["child_id"])
            link_parents[r["child_id"]].append(r["parent_id"])
        sql = """
        SELECT id,title,body,assignee,status,priority,created_by,created_at,started_at,completed_at,
               workspace_kind,workspace_path,branch_name,tenant,result,consecutive_failures,
               worker_pid,last_failure_error,max_runtime_seconds,last_heartbeat_at,current_run_id,
               skills,model_override,max_retries,goal_mode,session_id
        FROM tasks
        ORDER BY CASE status
          WHEN 'triage' THEN 1 WHEN 'todo' THEN 2 WHEN 'scheduled' THEN 3 WHEN 'ready' THEN 4
          WHEN 'running' THEN 5 WHEN 'blocked' THEN 6 WHEN 'done' THEN 7 WHEN 'archived' THEN 8 ELSE 99 END,
          priority DESC, created_at ASC
        """
        for r in con.execute(sql):
            d = dict(r)
            status = d.get("status") or "unknown"
            assignee = d.get("assignee") or "unassigned"
            counts[status] += 1
            assignee_counts[assignee][status] += 1
            d["board"] = slug
            d["created_at_iso"] = epoch_to_iso(d.get("created_at"))
            d["started_at_iso"] = epoch_to_iso(d.get("started_at"))
            d["completed_at_iso"] = epoch_to_iso(d.get("completed_at"))
            d["last_heartbeat_at_iso"] = epoch_to_iso(d.get("last_heartbeat_at"))
            d["last_event_at"] = events.get(d["id"])
            d["last_event_at_iso"] = epoch_to_iso(events.get(d["id"]))
            d["comment_count"] = comments.get(d["id"], 0)
            d["attachment_count"] = attachments.get(d["id"], 0)
            d["parents"] = link_parents.get(d["id"], [])
            d["children"] = link_children.get(d["id"], [])
            tasks.append(d)
        con.close()
    return {
        "slug": slug,
        "name": meta.get("name") or slug,
        "default_workdir": meta.get("default_workdir") or meta.get("workdir"),
        "counts": {s: counts.get(s, 0) for s in STATUSES if counts.get(s, 0)},
        "assignee_counts": {k: dict(v) for k, v in sorted(assignee_counts.items())},
        "tasks": tasks,
    }


def build_agents(boards: list[dict[str, Any]]) -> dict[str, Any]:
    by_assignee: dict[str, Counter[str]] = defaultdict(Counter)
    current_tasks: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for board in boards:
        for task in board["tasks"]:
            assignee = task.get("assignee") or "unassigned"
            by_assignee[assignee][task.get("status") or "unknown"] += 1
            if task.get("status") in {"triage", "todo", "ready", "running", "blocked", "scheduled"}:
                current_tasks[assignee].append({
                    "id": task["id"],
                    "board": board["slug"],
                    "title": task["title"],
                    "status": task["status"],
                })
    agents = []
    for role, layer, mission in ROLES:
        profile = PROFILES_DIR / role
        soul = profile / "SOUL.md"
        counts = dict(by_assignee.get(role, Counter()))
        status = "available" if profile.exists() and soul.exists() else "missing_contract"
        if counts.get("running"):
            state = "running"
        elif counts.get("blocked"):
            state = "blocked"
        elif counts.get("todo") or counts.get("ready") or counts.get("scheduled"):
            state = "queued"
        else:
            state = "idle"
        agents.append({
            "id": role,
            "display_name": role,
            "layer": layer,
            "mission": mission,
            "provider_family": "hermes",
            "model_label": "profile default",
            "execution_mode": "hermes-profile",
            "cost_mode": "local/current-subscription",
            "status": status,
            "state": state,
            "profile_present": profile.exists(),
            "soul_present": soul.exists(),
            "task_counts": counts,
            "current_tasks": current_tasks.get(role, [])[:5],
        })
    external_models = [
        {"id": "hermes", "label": "Hermes", "status": "active", "execution_mode": "native", "cost_mode": "current", "best_for": "orchestration, files, cron, Kanban"},
        {"id": "codex", "label": "Codex", "status": "candidate", "execution_mode": "profile/cli/manual", "cost_mode": "managed/auth-present", "best_for": "coding, scripts, tests"},
        {"id": "claude", "label": "Claude", "status": "manual/not_configured", "execution_mode": "manual artifact ingest", "cost_mode": "paid if API enabled", "best_for": "analysis, review, design critique"},
        {"id": "gemini", "label": "Gemini", "status": "manual/not_configured", "execution_mode": "manual artifact ingest", "cost_mode": "paid if API enabled", "best_for": "long context, research, documents"},
        {"id": "gpt", "label": "GPT", "status": "current/default or not_configured", "execution_mode": "profile/manual", "cost_mode": "depends", "best_for": "synthesis, reporting"},
    ]
    return {"generated_at": iso(), "agents": agents, "external_models": external_models}


def project_cards() -> list[dict[str, Any]]:
    return [
        {"slug": "dfxisp", "name": "DFXISP", "status": "Active", "priority": "P0", "board": "dfxisp", "path": "/opt/data/projects/dfxisp", "focus": "머신 비전을 위한 DFX AI-ISP 설계 / ZCU104 FPGA 구현"},
        {"slug": "ai-drone", "name": "AI드론", "status": "Exploration", "priority": "P1", "board": "ai-drone", "path": "/opt/data/projects/ai-drone", "focus": "문제/가설/PoC/go-no-go 기준 탐색"},
        {"slug": "agent-os", "name": "Agent OS Ops", "status": "Operating", "priority": "P0", "board": "agent-os", "path": "/opt/data/agent_os_archive", "focus": "상황실, Drive/Slack archive, team governance"},
    ]


def build_status(boards: list[dict[str, Any]], agents_blob: dict[str, Any]) -> dict[str, Any]:
    health = read_json(HEALTH_JSON, {})
    manifest = read_json(MANIFEST_JSON, {})
    cron = read_json(CRON_JOBS, {"jobs": []})
    total_counts: Counter[str] = Counter()
    for board in boards:
        total_counts.update(board["counts"])
    failed_jobs = [j for j in cron.get("jobs", []) if j.get("last_status") not in (None, "ok")]
    enabled_jobs = [j for j in cron.get("jobs", []) if j.get("enabled")]
    attention = []
    for board in boards:
        for t in board["tasks"]:
            if t.get("status") == "blocked":
                attention.append({"severity": "warn", "kind": "blocker", "summary": t["title"], "related_board": board["slug"], "related_task_id": t["id"], "required_user_action": "검토 또는 차단 해제 조건 확인"})
    for j in failed_jobs:
        attention.append({"severity": "critical", "kind": "cron", "summary": f"Cron failed: {j.get('name')}", "related_task_id": j.get("id"), "required_user_action": "로그 확인"})
    health_overall = (health.get("overall") or health.get("status") or "unknown").upper()
    if failed_jobs or health_overall == "FAIL":
        overall = "FAIL"
    elif total_counts.get("blocked", 0) > 0:
        overall = "BLOCKED"
    elif health_overall not in {"PASS", "OK", "UNKNOWN"}:
        overall = "WARN"
    else:
        overall = "PASS"
    next_actions = []
    for board in boards:
        for t in board["tasks"]:
            if t.get("status") in {"running", "blocked", "ready", "todo"}:
                next_actions.append({"board": board["slug"], "task_id": t["id"], "owner": t.get("assignee") or "unassigned", "status": t.get("status"), "action": t.get("title")})
    next_actions = next_actions[:8]
    return {
        "generated_at": iso(),
        "overall": overall,
        "healthcheck": {"overall": health_overall, "time": health.get("time") or health.get("generated_at"), "source": str(HEALTH_JSON)},
        "kanban": {s: total_counts.get(s, 0) for s in STATUSES if total_counts.get(s, 0)},
        "attention": attention,
        "next_actions": next_actions,
        "cron": {"active": len(enabled_jobs), "failed": len(failed_jobs), "jobs": [{"id": j.get("id"), "name": j.get("name"), "enabled": j.get("enabled"), "state": j.get("state"), "last_status": j.get("last_status"), "next_run_at": j.get("next_run_at"), "no_agent": j.get("no_agent"), "script": j.get("script")} for j in cron.get("jobs", [])]},
        "archive": {"manifest_exists": MANIFEST_JSON.exists(), "files": len(manifest.get("files", [])) if isinstance(manifest.get("files"), list) else manifest.get("file_count"), "updated_at": manifest.get("updated_at") or manifest.get("last_sync_at")},
        "projects": project_cards(),
        "providers": agents_blob["external_models"],
        "cost_guard": {"external_api_enabled": False, "manual_mode_available": True, "paid_run_pending": False, "default_policy": "외부 paid provider는 명시 승인 전 manual/not_configured로 표시"},
        "source_files": {"dashboard": str(DASHBOARD), "situation_board": str(SUMMARIES / "situation-board.md"), "kanban_root": str(KANBAN_ROOT)},
    }


def render_markdown(status: dict[str, Any], boards: list[dict[str, Any]], agents_blob: dict[str, Any]) -> str:
    lines = [
        "# Agent OS Situation Board",
        "",
        f"- Generated at: `{status['generated_at']}`",
        f"- Overall: **{status['overall']}**",
        f"- Healthcheck: `{status['healthcheck']['overall']}`",
        f"- Cost mode: `{status['cost_guard']['default_policy']}`",
        "",
        "## Human Attention Needed",
    ]
    if status["attention"]:
        for a in status["attention"]:
            lines.append(f"- **{a['severity']} / {a['kind']}** — `{a.get('related_board','')}` `{a.get('related_task_id','')}`: {a['summary']} → {a.get('required_user_action','')}")
    else:
        lines.append("- 현재 즉시 필요한 사용자 개입 없음.")
    lines += ["", "## Next Actions"]
    for n in status["next_actions"]:
        lines.append(f"- `{n['board']}` `{n['task_id']}` [{n['status']}] {n['owner']}: {n['action']}")
    lines += ["", "## Boards"]
    for b in boards:
        counts = ", ".join(f"{k}={v}" for k, v in b["counts"].items()) or "empty"
        lines.append(f"- `{b['slug']}` — {b['name']}: {counts}")
    lines += ["", "## Agent Team", "", "| Agent | State | Model | Current Tasks |", "|---|---|---|---|"]
    for ag in agents_blob["agents"]:
        cur = "; ".join(f"{t['board']}:{t['id']} {t['status']}" for t in ag.get("current_tasks", [])) or "-"
        lines.append(f"| `{ag['id']}` | {ag['state']} | {ag['provider_family']} / {ag['model_label']} | {cur} |")
    lines += ["", "## Projects"]
    for p in status["projects"]:
        lines.append(f"- **{p['name']}** `{p['priority']}` `{p['status']}` — board `{p['board']}`, path `{p['path']}` — {p['focus']}")
    lines += ["", "## Providers & Cost Guard"]
    for p in status["providers"]:
        lines.append(f"- `{p['label']}`: {p['status']} / {p['execution_mode']} / {p['cost_mode']} — {p['best_for']}")
    lines += ["", "## Governance"]
    lines.append(f"- Cron active={status['cron']['active']}, failed={status['cron']['failed']}")
    lines.append(f"- Archive manifest exists={status['archive']['manifest_exists']}, updated_at={status['archive']['updated_at']}")
    lines += ["", "## Source Files"]
    for k, v in status["source_files"].items():
        lines.append(f"- `{k}`: `{v}`")
    lines.append("")
    return "\n".join(lines)


def esc(s: Any) -> str:
    return html.escape("" if s is None else str(s))


def render_html(status: dict[str, Any], boards: list[dict[str, Any]], agents_blob: dict[str, Any]) -> str:
    data = {"status": status, "boards": boards, "agents": agents_blob}
    # Valid JSON embedded for agent/browser reuse. Only escape literal closing
    # script tags; do not HTML-escape quotes because application/json content
    # should remain machine-readable JSON.
    data_json = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    status_class = status["overall"].lower()
    kpis = [
        ("Overall", status["overall"], "Current operational state"),
        ("Attention", len(status["attention"]), "Human decisions/blockers"),
        ("Running", status["kanban"].get("running", 0), "Active worker tasks"),
        ("Done", status["kanban"].get("done", 0), "Completed tasks"),
    ]
    kpi_html = "\n".join(f'<article class="metric"><span>{esc(label)}</span><strong>{esc(value)}</strong><small>{esc(sub)}</small></article>' for label, value, sub in kpis)
    attention_html = "\n".join(
        f'<li><b>{esc(a["kind"])}</b><span>{esc(a["summary"])}</span><code>{esc(a.get("related_board"))}/{esc(a.get("related_task_id"))}</code></li>' for a in status["attention"][:6]
    ) or '<li><b>clear</b><span>현재 사용자 개입 필요 항목 없음</span><code>PASS</code></li>'
    boards_html = "\n".join(render_board_card(b) for b in boards)
    agents_html = "\n".join(render_agent_card(a) for a in agents_blob["agents"])
    providers_html = "\n".join(f'<div class="provider"><b>{esc(p["label"])}</b><span>{esc(p["status"])}</span><small>{esc(p["best_for"])}</small></div>' for p in status["providers"])
    project_html = "\n".join(f'<article class="project"><div><b>{esc(p["name"])}</b><span>{esc(p["priority"])} · {esc(p["status"])}</span></div><p>{esc(p["focus"])}</p><code>{esc(p["path"])}</code></article>' for p in status["projects"])
    next_html = "\n".join(f'<tr><td><code>{esc(n["task_id"])}</code></td><td>{esc(n["board"])}</td><td>{esc(n["owner"])}</td><td><span class="badge {esc(n["status"])}">{esc(n["status"])}</span></td><td>{esc(n["action"])}</td></tr>' for n in status["next_actions"])
    task_rows = []
    for b in boards:
        for t in b["tasks"][:50]:
            task_rows.append(f'<tr data-status="{esc(t.get("status"))}" data-assignee="{esc(t.get("assignee"))}"><td><code>{esc(t["id"])}</code></td><td>{esc(b["slug"])}</td><td>{esc(t.get("title"))}</td><td>{esc(t.get("assignee"))}</td><td><span class="badge {esc(t.get("status"))}">{esc(t.get("status"))}</span></td><td>{esc(t.get("priority"))}</td></tr>')
    tasks_html = "\n".join(task_rows)
    artifact_paths = {
        "index.html": str(DASHBOARD / "index.html"),
        "status.json": str(DASHBOARD / "status.json"),
        "agents.json": str(DASHBOARD / "agents.json"),
        "tasks.json": str(DASHBOARD / "tasks.json"),
        "situation-board.md": str(SUMMARIES / "situation-board.md"),
        **status.get("source_files", {}),
    }
    artifact_html = "\n".join(
        f'<div class="artifact"><b>{esc(k)}</b><code>{esc(v)}</code><button type="button" onclick="copyPath(this)" data-copy="{esc(v)}">Copy path</button></div>'
        for k, v in artifact_paths.items()
    )
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Agent OS Situation Room</title>
<style>
:root {{ --bg:#070a12; --muted:#0b1020; --surface:#111827; --text:#e5edf7; --sub:#9ca3af; --faint:#64748b; --border:rgba(148,163,184,.18); --blue:#38bdf8; --violet:#8b5cf6; --pink:#f472b6; --green:#22c55e; --amber:#f59e0b; --red:#ef4444; --shadow:0 0 0 1px rgba(148,163,184,.16),0 12px 34px -24px rgba(0,0,0,.9); }}
*{{box-sizing:border-box}} body{{margin:0;font-family:Inter,ui-sans-serif,system-ui,sans-serif;background:radial-gradient(circle at top left,rgba(109,93,252,.20),transparent 32rem),var(--muted);color:var(--text);font-size:14px}} code,.mono{{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,monospace;font-size:12px}} a{{color:inherit}} .app{{display:grid;grid-template-columns:260px 1fr;min-height:100vh}} aside{{background:rgba(7,10,18,.92);border-right:1px solid var(--border);padding:22px 18px;position:sticky;top:0;height:100vh}} .brand{{font-weight:600;font-size:18px;letter-spacing:-.5px;margin-bottom:24px}} nav a{{display:flex;gap:10px;padding:9px 10px;border-radius:8px;color:#444;text-decoration:none;margin:2px 0}} nav a:hover,nav a.active{{background:#f2f5ff;color:#0a43a6}} .side-foot{{position:absolute;bottom:20px;left:18px;right:18px;color:var(--sub);font-size:12px}} main{{padding:24px 28px 60px;max-width:1500px;width:100%}} .top{{display:flex;justify-content:space-between;gap:16px;align-items:flex-start;margin-bottom:22px}} h1{{font-size:34px;line-height:1.05;letter-spacing:-1.5px;margin:0 0 7px}} .lede{{color:var(--sub);margin:0}} .pill{{display:inline-flex;align-items:center;gap:7px;border-radius:999px;padding:5px 10px;background:#fff;box-shadow:0 0 0 1px var(--border);font-size:12px;white-space:nowrap}} .dot{{width:8px;height:8px;border-radius:50%;background:var(--green)}} .dot.blocked{{background:var(--amber)}} .dot.fail{{background:var(--red)}} .metrics{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:18px 0}} .metric,.card,.project,.panel{{background:var(--surface);border-radius:12px;box-shadow:var(--shadow)}} .metric{{padding:17px}} .metric span,.label{{font-size:12px;color:var(--sub);text-transform:uppercase;letter-spacing:.04em}} .metric strong{{display:block;font-size:32px;letter-spacing:-1.3px;margin:7px 0}} .metric small{{color:var(--sub)}} .grid{{display:grid;grid-template-columns:1.4fr .8fr;gap:16px;margin-top:16px}} .card,.panel{{padding:18px}} .card h2,.panel h2{{font-size:16px;margin:0 0 14px;letter-spacing:-.3px}} .attention{{list-style:none;margin:0;padding:0;display:grid;gap:9px}} .attention li{{display:grid;grid-template-columns:90px 1fr auto;gap:10px;align-items:center;padding:10px;border-radius:9px;background:#fafafa;box-shadow:0 0 0 1px #eee}} .attention b{{color:var(--amber)}} .boards{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}} .board h3{{margin:0 0 8px}} .lanes{{display:flex;gap:6px;flex-wrap:wrap}} .badge{{display:inline-flex;border-radius:999px;padding:3px 8px;font-size:12px;background:#f1f1f1;color:#444;font-weight:500}} .badge.running{{background:#ebf5ff;color:#0068d6}} .badge.blocked{{background:#fff7ed;color:#c2410c}} .badge.done{{background:#ecfdf5;color:#047857}} .badge.ready,.badge.todo{{background:#f5f3ff;color:#6d28d9}} .agents{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}} .agent{{padding:13px;border-radius:11px;background:#fff;box-shadow:0 0 0 1px var(--border)}} .agent-top{{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}} .agent b{{font-size:14px}} .agent p{{margin:0;color:var(--sub);font-size:12px;line-height:1.35}} .agent .state{{font-size:11px;border-radius:999px;padding:2px 7px;background:#f1f1f1}} .agent .state.running{{background:#ebf5ff;color:#0068d6}} .agent .state.blocked{{background:#fff7ed;color:#c2410c}} .providers{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}} .provider{{padding:12px;border-radius:10px;background:#fafafa;box-shadow:0 0 0 1px #eee}} .provider b{{display:block}} .provider span{{display:block;color:var(--blue);font-size:12px;margin:4px 0}} .provider small{{color:var(--sub)}} .projects{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}} .project{{padding:15px}} .project div{{display:flex;justify-content:space-between;gap:8px}} .project span{{color:var(--blue);font-size:12px}} .project p{{color:var(--sub);min-height:34px}} table{{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:var(--shadow)}} th,td{{text-align:left;padding:10px 12px;border-bottom:1px solid #eee;vertical-align:top}} th{{font-size:12px;color:var(--sub);text-transform:uppercase;letter-spacing:.04em;background:#fafafa}} tr:hover td{{background:#fcfcff}} .toolbar{{display:flex;gap:10px;margin:12px 0}} input{{border:0;box-shadow:0 0 0 1px var(--border);border-radius:8px;padding:10px 12px;min-width:260px;font:inherit;background:#fff}} .section{{scroll-margin-top:20px;margin-top:20px}} .status-{status_class}{{color:var(--amber)}} @media(max-width:1000px){{.app{{grid-template-columns:1fr}} aside{{position:relative;height:auto}} .side-foot{{position:static;margin-top:20px}} .metrics,.agents,.providers,.projects,.boards,.artifacts{{grid-template-columns:1fr 1fr}} .grid{{grid-template-columns:1fr}}}} @media(max-width:640px){{main{{padding:18px}} .metrics,.agents,.providers,.projects,.boards,.artifacts{{grid-template-columns:1fr}} .top{{display:block}}}}
body, aside, main{{background-color:var(--muted)}} nav a{{color:#cbd5e1}} nav a:hover,nav a.active{{background:rgba(56,189,248,.12);color:#e0f2fe}} .pill,.metric,.card,.project,.panel,.agent,.provider,table,input,.attention li,.artifact{{background:var(--surface);color:var(--text);border:1px solid var(--border)}} th,td{{border-bottom:1px solid var(--border)}} th,tr:hover td{{background:rgba(15,23,42,.8)}} .artifacts{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:14px}} .artifact{{border-radius:10px;padding:12px;display:grid;gap:8px}} .artifact code{{word-break:break-all;color:#cbd5e1}} .artifact button{{justify-self:start;border:1px solid var(--border);border-radius:999px;padding:5px 10px;background:rgba(56,189,248,.12);color:#dff7ff;cursor:pointer}} .agent{{cursor:pointer}}
</style>
</head>
<body>
<div class="app">
<aside>
  <div class="brand">Agent OS<br><span style="color:#666;font-weight:400">Situation Room</span></div>
  <nav>
    <a class="active" href="#overview">⌘ Overview</a>
    <a href="#attention">● Attention</a>
    <a href="#boards">▦ Boards</a>
    <a href="#agents">◎ Agents</a>
    <a href="#projects">◇ Projects</a>
    <a href="#providers">◐ Providers & Cost</a>
    <a href="#tasks">≡ Tasks</a>
    <a href="#artifacts">□ Artifacts</a>
  </nav>
  <div class="side-foot"><div class="pill"><span class="dot"></span> Local-first · no paid API by default</div><p><code>{esc(str(DASHBOARD))}</code></p></div>
</aside>
<main id="overview">
  <div class="top">
    <div><h1>Mission Control for Human + AI Agents</h1><p class="lede">가장 보편적인 SaaS 대시보드 형식: Vercel식 clean app shell + Sentry식 운영 밀도.</p></div>
    <div class="pill"><span class="dot {'' if status['overall']=='PASS' else status_class}"></span><b>{esc(status['overall'])}</b> · {esc(status['generated_at'])}</div>
  </div>
  <section class="metrics">{kpi_html}</section>
  <section class="grid">
    <div class="card" id="attention"><h2>Human Attention Needed</h2><ul class="attention">{attention_html}</ul></div>
    <div class="card"><h2>Next Actions</h2><table><thead><tr><th>Task</th><th>Board</th><th>Owner</th><th>Status</th><th>Action</th></tr></thead><tbody>{next_html}</tbody></table></div>
  </section>
  <section class="section card" id="boards"><h2>Board Health</h2><div class="boards">{boards_html}</div></section>
  <section class="section card" id="agents"><h2>Agent Roster</h2><div class="agents">{agents_html}</div></section>
  <section class="section panel" id="providers"><h2>Model Control Plane / Cost Guard</h2><div class="providers">{providers_html}</div><p class="lede" style="margin-top:12px">외부 Claude/Gemini/GPT API는 기본 비활성. 결과물은 manual artifact ingest로 수용 가능.</p></section>
  <section class="section" id="projects"><div class="projects">{project_html}</div></section>
  <section class="section" id="tasks"><h2>Task Inventory</h2><div class="toolbar"><input id="q" placeholder="Search tasks, assignees, status..."><button class="pill" onclick="toggleCompact()">Toggle compact</button></div><table id="taskTable"><thead><tr><th>ID</th><th>Board</th><th>Title</th><th>Assignee</th><th>Status</th><th>Priority</th></tr></thead><tbody>{tasks_html}</tbody></table></section>
  <section class="section card" id="artifacts"><h2>Artifacts / Path Copy</h2><p class="lede">Generated static files and source paths. Buttons use the browser clipboard when available.</p><div class="artifacts">{artifact_html}</div></section>
</main>
</div>
<script type="application/json" id="dashboard-data">{data_json}</script>
<script>
const q=document.getElementById('q');
q?.addEventListener('input',()=>{{const v=q.value.toLowerCase();document.querySelectorAll('#taskTable tbody tr').forEach(tr=>{{tr.style.display=tr.innerText.toLowerCase().includes(v)?'':'none'}})}});
function toggleCompact(){{document.body.classList.toggle('compact');document.querySelectorAll('.agent p,.project p').forEach(e=>e.style.display=document.body.classList.contains('compact')?'none':'');}}
function showAgent(raw){{try{{const a=JSON.parse(raw); alert(`${{a.id}}\n${{a.state}} · ${{a.layer}}\n${{a.mission}}\nCurrent tasks: ${{(a.current_tasks||[]).map(t=>t.board+':'+t.id+' '+t.status).join(', ')||'-'}}`);}}catch(e){{alert(raw)}}}}
async function copyPath(btn){{const value=btn.dataset.copy||''; try{{await navigator.clipboard.writeText(value); btn.textContent='Copied'; setTimeout(()=>btn.textContent='Copy path',1100);}}catch(e){{prompt('Copy path', value);}}}}
</script>
</body>
</html>"""


def render_board_card(b: dict[str, Any]) -> str:
    lanes = "".join(f'<span class="badge {esc(k)}">{esc(k)} {esc(v)}</span>' for k, v in b["counts"].items()) or '<span class="badge">empty</span>'
    return f'<div class="board"><h3>{esc(b["name"])}</h3><code>{esc(b["slug"])}</code><div class="lanes">{lanes}</div></div>'


def render_agent_card(a: dict[str, Any]) -> str:
    agent_json = html.escape(json.dumps(a, ensure_ascii=False), quote=True)
    return f'<div class="agent" onclick="showAgent(this.dataset.agent)" data-agent="{agent_json}"><div class="agent-top"><b>{esc(a["id"])}</b><span class="state {esc(a["state"])}">{esc(a["state"])}</span></div><p>{esc(a["mission"])}</p><p><code>{esc(a["provider_family"])} · {esc(a["execution_mode"])}</code></p></div>'


def main() -> None:
    DASHBOARD.mkdir(parents=True, exist_ok=True)
    SUMMARIES.mkdir(parents=True, exist_ok=True)
    boards = [read_board(slug) for slug in BOARD_SLUGS]
    tasks_blob = {"generated_at": iso(), "boards": boards}
    agents_blob = build_agents(boards)
    status = build_status(boards, agents_blob)
    # Keep all generated files on the same top-level timestamp.
    generated_at = iso()
    for blob in (tasks_blob, agents_blob, status):
        blob["generated_at"] = generated_at
    atomic_write_json(DASHBOARD / "tasks.json", tasks_blob)
    atomic_write_json(DASHBOARD / "agents.json", agents_blob)
    atomic_write_json(DASHBOARD / "status.json", status)
    atomic_write(SUMMARIES / "situation-board.md", render_markdown(status, boards, agents_blob))
    atomic_write(DASHBOARD / "index.html", render_html(status, boards, agents_blob))
    print(f"Agent OS Situation Room generated: {DASHBOARD / 'index.html'}")
    print(f"Overall={status['overall']} boards={len(boards)} agents={len(agents_blob['agents'])} tasks={sum(len(b['tasks']) for b in boards)}")


if __name__ == "__main__":
    main()
