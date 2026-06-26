#!/usr/bin/env python3
"""
Agent OS Cockpit — 자체 호스팅 통합 GUI (관제 + 제어).

- stdlib http.server (웹 프레임워크 의존성 없음)
- 데이터: dashboard-state.json (Drive 우선, 로컬 미러 fallback) + substrate Postgres(tasks)
- 명령창 = substrate 큐에 task 투입(ready) → 담당 에이전트가 claim/handoff. LLM 챗봇 아님, 명령·소통 채널.
- 127.0.0.1 바인딩(로컬 전용). 외부 접근은 SSH 터널.

실행: PG_PW=... python3 server.py   (기본 포트 8787, COCKPIT_PORT로 변경)
"""
import os, sys, json, datetime, urllib.parse, http.server, socketserver
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOST = os.environ.get("COCKPIT_HOST", "127.0.0.1")   # Docker 컨테이너면 0.0.0.0
PORT = int(os.environ.get("COCKPIT_PORT", "8787"))
LOCAL_STATE = Path("/opt/data/agent_os_archive/files/05-dashboard/dashboard-state.json")
PG_DSN = os.environ.get("AGENTOS_DSN",
    "postgresql://postgres:%s@127.0.0.1:5432/agentos" % os.environ.get("PG_PW", ""))

def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_state():
    """Drive(신선) 우선 → 로컬 미러 fallback."""
    try:
        sys.path.insert(0, "/opt/data/scripts")
        import sync_ai_drone_obsidian_to_drive as d
        svc = d.build_service("drive", "v3")
        dash = d.find_child_folder(svc, d.ROOT_ID, "05-dashboard")
        f = d.list_children_by_name(svc, dash["id"]).get("dashboard-state.json")
        raw = svc.files().get_media(fileId=f["id"]).execute()
        return json.loads(raw.decode("utf-8") if isinstance(raw, (bytes, bytearray)) else raw), "drive"
    except Exception:
        try:
            return json.loads(LOCAL_STATE.read_text("utf-8")), "local"
        except Exception as e:
            return {"_error": str(e)}, "none"

def _pg():
    import psycopg2  # lazy: substrate 미배포여도 콕핏은 뜬다
    return psycopg2.connect(PG_DSN)

def load_tasks():
    try:
        c = _pg(); cur = c.cursor()
        cur.execute("SELECT task_id,board,title,status,owner_agent,priority,approval,"
                    "to_char(updated_at,'MM-DD HH24:MI') FROM tasks "
                    "ORDER BY priority, updated_at DESC LIMIT 200;")
        cols = ["task_id","board","title","status","owner_agent","priority","approval","updated"]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        c.close()
        return {"ok": True, "tasks": rows}
    except Exception as e:
        return {"ok": False, "error": str(e), "tasks": []}

def enqueue_command(agent, text):
    tid = "CMD-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        c = _pg(); cur = c.cursor()
        cur.execute("INSERT INTO tasks(task_id,board,title,status,owner_agent,priority) "
                    "VALUES(%s,'agent-os',%s,'ready',%s,0)", (tid, text[:200], agent))
        c.commit(); c.close()
        return {"ok": True, "task_id": tid, "routed_to": agent}
    except Exception as e:
        (HERE / "commands.jsonl").open("a", encoding="utf-8").write(
            json.dumps({"ts": now(), "agent": agent, "text": text}, ensure_ascii=False) + "\n")
        return {"ok": True, "task_id": tid, "routed_to": agent,
                "note": "substrate 미연결 → commands.jsonl 폴백 (" + str(e)[:80] + ")"}

class H(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers(); self.wfile.write(b)
    def log_message(self, *a):  # 조용히
        pass
    def do_GET(self):
        p = urllib.parse.urlparse(self.path).path
        if p in ("/", "/index.html"):
            self._send(200, (HERE / "index.html").read_bytes(), "text/html; charset=utf-8")
        elif p == "/api/state":
            st, src = load_state()
            self._send(200, json.dumps({"source": src, "state": st, "served_at": now()}, ensure_ascii=False))
        elif p == "/api/tasks":
            self._send(200, json.dumps(load_tasks(), ensure_ascii=False))
        else:
            self._send(404, '{"error":"not found"}')
    def do_POST(self):
        if urllib.parse.urlparse(self.path).path == "/api/command":
            n = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(n) or b"{}")
            self._send(200, json.dumps(enqueue_command(data.get("agent", "Hermes"),
                                                        data.get("text", "")), ensure_ascii=False))
        else:
            self._send(404, '{"error":"not found"}')

if __name__ == "__main__":
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer((HOST, PORT), H) as srv:
        print(f"Agent OS Cockpit → http://{HOST}:{PORT}  (Ctrl-C 종료)")
        srv.serve_forever()
