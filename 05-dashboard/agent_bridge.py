#!/usr/bin/env python3
"""Agent OS — minimal chat+task bridge (stdlib only, no deps).

hq-dashboard.html(Command Center)가 POST 하는 엔드포인트.
대시보드 ⚙ 에 http://localhost:8765 (base) 를 넣으면 라이브 모드로 연결된다.
  POST /chat  {message, history}      → 상태 질문 즉답 / Hermes 대화 훅
  POST /task  {board,owner,model,priority,title,detail} → 작업 디스패치

설계(ponytail): 의존성 0, 로컬 전용 바인드. 실제 Hermes 연동은 훅 2개만 채우면 됨.
작업은 tasks_outbox.jsonl 에 안전 append → Hermes/Codex가 소비(부작용 없는 기본 동작).

usage:
  python3 agent_bridge.py --state agent-dashboard.json --outbox tasks_outbox.jsonl --port 8765
"""
import argparse, json, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

STATE_PATH=None; OUTBOX=None

def load_state():
    try: return json.loads(Path(STATE_PATH).read_text(encoding="utf-8"))
    except Exception: return {}

def local_answer(q,S):
    t=q.lower(); has=lambda *k: any(x in t for x in k)
    cron=S.get("cron",{}); jobs=cron.get("jobs",[])
    if has("상태","status","전체","요약"):
        mvp=S.get("mvp",{}).get("criteria",[]); p=sum(1 for c in mvp if c.get("state")=="pass"); kb=S.get("kanban",{})
        return "전체: %s — %s\nMVP %s/%s · healthcheck %s · cron %s ok/%s fail · kanban run %s/blocked %s/done %s"%(
            S.get("overall"),S.get("overall_reason",""),p,len(mvp),(S.get("health") or {}).get("healthcheck"),
            cron.get("active"),cron.get("failed"),kb.get("running"),kb.get("blocked"),kb.get("done"))
    if has("cron","크론","실패","fail","error"):
        bad=[j for j in jobs if j.get("status")!="ok"]
        return "cron 전부 정상." if not bad else "실패 cron %d건:\n"%len(bad)+"\n".join("• %s — %s → %s"%(j["name"],j.get("detail",j["status"]),j.get("judgment","")) for j in bad)
    if has("dfxisp"):
        n=[x for x in S.get("next_actions",[]) if x.get("board")=="dfxisp"]
        return "DFXISP 다음:\n"+"\n".join("• [%s] %s (%s)"%(x["status"],x["action"],x["owner"]) for x in n)
    if has("막힌","blocked","차단"):
        n=[x for x in S.get("next_actions",[]) if x.get("status")=="blocked"]
        return ("막힌 것:\n"+"\n".join("• %s (%s)"%(x["action"],x["owner"]) for x in n)) if n else "차단 없음."
    if has("다음","next","행동"):
        return "다음 행동:\n"+"\n".join("• [%s/%s] %s"%(x["board"],x["status"],x["action"]) for x in S.get("next_actions",[]))
    if has("에이전트","agent","누가"):
        a=S.get("agents",[]); r=[x for x in a if x.get("state")=="running"]
        return "에이전트 %d명, running %d:\n"%(len(a),len(r))+"\n".join("• %s — %s"%(x["id"],x["mission"]) for x in r)
    return None

def route_to_hermes_chat(msg,S):
    """TODO(연동): hermes 프로파일/CLI 호출. 미연결 시 status로 폴백."""
    return "(Hermes 대화 미연결 — route_to_hermes_chat() 훅을 채우면 자유 대화가 됩니다.)\n메시지: %r\n\n"%msg+(local_answer("상태",S) or "")

def route_to_hermes_task(task,S):
    """실제 Kanban 카드 생성 훅.
    TODO(연동): 예) subprocess.run(["kanban","add","--board",task["board"],
                 "--assignee",task["owner"],"--title",task["title"],"--body",task["detail"]])
    기본: tasks_outbox.jsonl 에 append → Hermes/Codex가 소비(부작용 없음, 안전).
    """
    rec=dict(task); rec["queued_at"]=time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(OUTBOX,"a",encoding="utf-8") as f: f.write(json.dumps(rec,ensure_ascii=False)+"\n")
    return "outbox에 queued: %s → %s/%s (Hermes가 소비). 실연동은 route_to_hermes_task() 훅."%(
        task.get("title"),task.get("board"),task.get("owner"))

class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*"); self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.send_header("Access-Control-Allow-Methods","POST, OPTIONS")
    def do_OPTIONS(self): self.send_response(204); self._cors(); self.end_headers()
    def _json(self,obj):
        b=json.dumps(obj,ensure_ascii=False).encode("utf-8")
        self.send_response(200); self.send_header("Content-Type","application/json; charset=utf-8"); self._cors(); self.end_headers(); self.wfile.write(b)
    def do_POST(self):
        n=int(self.headers.get("Content-Length",0))
        try: body=json.loads(self.rfile.read(n) or b"{}")
        except Exception: body={}
        S=load_state(); path=self.path.rstrip("/")
        if path.endswith("/task"):
            reply=route_to_hermes_task(body,S); self._json({"reply":reply,"agent":"dispatch","status":"queued"})
        else:
            msg=(body.get("message") or "").strip(); reply=local_answer(msg,S); agent="hq (local)"
            if reply is None: reply=route_to_hermes_chat(msg,S); agent="hermes (hook)"
            self._json({"reply":reply,"agent":agent})
    def log_message(self,*a): pass

def main():
    global STATE_PATH,OUTBOX
    ap=argparse.ArgumentParser()
    ap.add_argument("--state",default="agent-dashboard.json")
    ap.add_argument("--outbox",default="tasks_outbox.jsonl")
    ap.add_argument("--port",type=int,default=8765); ap.add_argument("--host",default="127.0.0.1")
    a=ap.parse_args(); STATE_PATH=a.state; OUTBOX=a.outbox
    print("Agent OS bridge → http://%s:%d  (POST /chat, /task)  state=%s outbox=%s"%(a.host,a.port,a.state,a.outbox))
    ThreadingHTTPServer((a.host,a.port),H).serve_forever()

if __name__=="__main__": main()
