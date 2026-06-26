#!/usr/bin/env python3
"""
loop_status.py — Agent OS 공용 루프 상태 기록기 (Hermes / Claude / Gemini / GPT)

05-dashboard/dashboard-state.json 의 agent_status[<agent>] 블록만 갱신하고
Drive 정본 파일을 제자리(in-place)로 업데이트한다. 다른 에이전트 블록은 건드리지 않는다.

사용 예:
  loop_status.py --agent Hermes --status running --task "daily-status loop"
  loop_status.py --agent Hermes --status idle   --output "daily-status 완료: 3 tasks, 0 blockers" --log "..."
  loop_status.py --agent Claude --status running --task "DFXISP C1 설계"
  loop_status.py --agent Gemini --status idle   --output "레퍼런스 12건 정제"

배포: Hermes 서버 /opt/data/scripts/loop_status.py 로 두고 실행.
정본 보관: Agent OS/05-dashboard/loop_status.py (이 파일)
"""
from __future__ import annotations
import sys, io, json, argparse
from datetime import datetime, timezone

sys.path.insert(0, "/opt/data/scripts")
import sync_ai_drone_obsidian_to_drive as d   # build_service, ROOT_ID, find_child_folder, list_children_by_name
from googleapiclient.http import MediaIoBaseUpload

DASH_DIR  = "05-dashboard"
STATE_NAME = "dashboard-state.json"

def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent",  required=True, choices=["Hermes", "Claude", "Gemini", "GPT"])
    ap.add_argument("--status", required=True, choices=["idle","running","blocked","review","waiting","done"])
    ap.add_argument("--task",        default=None, help="current_task (생략 시 유지, idle/done이면 비움)")
    ap.add_argument("--output",      default=None, help="last_output")
    ap.add_argument("--waiting-for", default=None, dest="waiting_for")
    ap.add_argument("--note",        default=None)
    ap.add_argument("--log",         default=None, help="memory_log 한 줄 요약(옵션)")
    a = ap.parse_args()

    svc = d.build_service("drive", "v3")

    dash = d.find_child_folder(svc, d.ROOT_ID, DASH_DIR)
    if not dash:
        sys.exit("ERROR: Drive에서 05-dashboard 폴더를 못 찾음")
    fmeta = d.list_children_by_name(svc, dash["id"]).get(STATE_NAME)
    if not fmeta:
        sys.exit("ERROR: dashboard-state.json 없음")

    raw = svc.files().get_media(fileId=fmeta["id"]).execute()
    state = json.loads(raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw)

    ag = state.setdefault("agent_status", {}).setdefault(a.agent, {})
    ag["status"] = a.status
    if a.task is not None:
        ag["current_task"] = a.task
    elif a.status in ("idle", "done"):
        ag["current_task"] = None
    if a.output is not None:
        ag["last_output"] = a.output
    ag["last_active"] = now()
    ag["waiting_for"] = a.waiting_for           # 명시 안 하면 None으로 클리어
    if a.note is not None:
        ag["notes"] = a.note

    meta = state.setdefault("_meta", {})
    meta["last_updated_by"] = a.agent
    meta["last_updated_at"] = now()

    if a.log:
        state.setdefault("memory_log", []).append(
            {"date": now()[:10], "by": a.agent, "type": "loop", "summary": a.log})
        state["memory_log"] = state["memory_log"][-50:]

    body = json.dumps(state, ensure_ascii=False, indent=2).encode("utf-8")
    media = MediaIoBaseUpload(io.BytesIO(body), mimetype="application/json", resumable=True)
    svc.files().update(fileId=fmeta["id"], media_body=media,
                       fields="id,modifiedTime", supportsAllDrives=True).execute()

    print(f"[ok] {a.agent} -> {a.status} @ {now()}")

if __name__ == "__main__":
    main()
