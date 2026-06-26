#!/usr/bin/env python3
"""Agent OS — single dashboard generator (ponytail: one generator, stdlib only).

source state JSON(situation-room/state/*.json) → agent-dashboard.json(통합 정본)
→ hq-dashboard.html 의 인라인 window.STATE 갱신.

이전의 agent_os_situation_room_snapshot.py(424줄) + agent_dashboard_snapshot.py(338줄)
두 generator를 대체한다. 의존성 없음(stdlib only).

usage:
  python3 build_dashboard.py --src 05-dashboard/situation-room/state \
      --out 05-dashboard/agent-dashboard.json --html 05-dashboard/hq-dashboard.html \
      [--cron live_cron.json]
"""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

def load(p):
    p = Path(p)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

def build_state(src, cron_override=None):
    status = load(src / "status.json")
    agents = load(src / "agents.json")
    kb = status.get("kanban", {})
    # cron: 라이브 점검 결과(--cron)가 있으면 우선, 없으면 source의 stale cron
    cron = cron_override or status.get("cron", {})
    jobs = cron.get("jobs", [])
    failed = sum(1 for j in jobs if j.get("status") not in ("ok", "scheduled"))
    state = {
        "schema_version": "0.1",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "generated_by": "build_dashboard.py",
        "freshness_note": status.get("freshness_note",
            "source snapshot %s 기준. cron/health는 최신 점검 반영." % status.get("generated_at", "")),
        "overall": status.get("overall", "UNKNOWN"),
        "overall_reason": status.get("overall_reason", ""),
        "mvp": status.get("mvp", {"version": "v0.1", "criteria": []}),
        "health": {},
        "cron": {"active": len(jobs) - failed, "failed": failed, "jobs": jobs},
        "kanban": {k: kb.get(k, 0) for k in ("todo", "running", "blocked", "done")},
        "next_actions": status.get("next_actions", [])[:6],
        "agents": [
            {"id": a.get("id"), "layer": a.get("layer"), "mission": a.get("mission"),
             "state": a.get("state"), "counts": a.get("task_counts", {})}
            for a in agents.get("agents", [])
        ],
        "projects": status.get("projects", []),
        "models": status.get("providers", []),
        "cost_guard": status.get("cost_guard", {}),
        "deferred": status.get("deferred", []),
    }
    h = status.get("healthcheck", {})
    if isinstance(h, dict):
        state["health"] = {"healthcheck": h.get("overall"), "checked_at": h.get("time")}
    else:
        state["health"] = {"healthcheck": h}
    return state

def inject_html(html_path, state):
    """window.STATE = ... 한 줄을 통째로 교체 (line-based, 견고)."""
    p = Path(html_path)
    if not p.exists():
        return False
    lines = p.read_text(encoding="utf-8").splitlines()
    blob = "window.STATE = " + json.dumps(state, ensure_ascii=False, separators=(",", ":")) + ";"
    out, hit = [], False
    for ln in lines:
        if ln.lstrip().startswith("window.STATE ="):
            out.append(blob); hit = True
        else:
            out.append(ln)
    if hit:
        p.write_text("\n".join(out) + "\n", encoding="utf-8")
    return hit

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="situation-room/state", help="source state JSON dir")
    ap.add_argument("--out", default="agent-dashboard.json")
    ap.add_argument("--html", default="hq-dashboard.html")
    ap.add_argument("--cron", help="optional live cron JSON to override stale source")
    a = ap.parse_args()
    cron_override = load(a.cron) if a.cron else None
    state = build_state(Path(a.src), cron_override)
    Path(a.out).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    injected = inject_html(a.html, state)
    print("OK  json=%s  cron(active/failed)=%d/%d  agents=%d  html_injected=%s"
          % (a.out, state["cron"]["active"], state["cron"]["failed"], len(state["agents"]), injected))

if __name__ == "__main__":
    main()
