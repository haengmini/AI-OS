#!/usr/bin/env python3
"""
claim_worker.py — 에이전트용 레퍼런스 워커.
LISTEN agent_<name> 로 상시 대기 → push 받으면 즉시 claim (폴링 없음).
NOTIFY는 연결된 리스너에만 가므로 5분 sweep 안전망 포함.

사용: PG_PW=... python3 claim_worker.py <agent>   (예: codex / Claude / Gemini / Hermes)
의존: pip install psycopg2-binary
"""
import os, sys, select
import psycopg2, psycopg2.extensions

AGENT = sys.argv[1] if len(sys.argv) > 1 else "codex"
DSN = os.environ.get(
    "AGENTOS_DSN",
    "postgresql://postgres:%s@127.0.0.1:5432/agentos" % os.environ.get("PG_PW", ""),
)

def drain_claims(cur):
    """ready 작업을 더 없을 때까지 점유."""
    while True:
        cur.execute("SELECT task_id, title FROM claim_task(%s);", (AGENT,))
        row = cur.fetchone()
        if not row:
            return
        task_id, title = row
        print(f"[{AGENT}] claimed {task_id} · {title}")
        # ── 실제 작업 핸들러 연결 지점 ───────────────────────────
        # 작업 수행 → outputs에 drive_file_id 기록 →
        #   SELECT handoff('{task_id}', '<next_task_id|NULL>');
        cur.execute("UPDATE tasks SET status='review' WHERE task_id=%s;", (task_id,))
        print(f"[{AGENT}] {task_id} → review (핸들러 미연결: TODO)")

def main():
    conn = psycopg2.connect(DSN)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(f"LISTEN agent_{AGENT};")
    print(f"[{AGENT}] listening on agent_{AGENT} … (Ctrl-C 종료)")
    drain_claims(cur)                       # 시작 시 밀린 작업 먼저
    while True:
        # 이벤트 대기, 최대 300초(안전망 sweep)
        if select.select([conn], [], [], 300) == ([], [], []):
            print(f"[{AGENT}] sweep")        # 놓친 ready 재확인
        conn.poll()
        while conn.notifies:
            conn.notifies.pop(0)
        drain_claims(cur)

if __name__ == "__main__":
    main()
