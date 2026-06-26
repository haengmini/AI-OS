#!/usr/bin/env python3
"""Update the Notion Agent OS HQ page as the human-facing dashboard.

HTML dashboards are deprecated; this script mirrors current Agent OS loop,
DFXISP HLS, GitHub, and cron status into Notion HQ.
"""
from __future__ import annotations

import json
import os
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

NOTION_VERSION = "2025-09-03"
HQ_PAGE_ID = os.environ.get("AGENT_OS_NOTION_HQ_PAGE_ID", "3885871b-3d1c-8188-b8dd-feb80492f1fb")
REPO = Path("/opt/data/dfxisp_md")
HLS = REPO / "isppipeline/hls"
LOOP_JSON = Path("/opt/data/agent_os_loop_status/loop-status-latest.json")
MARKER = "## Hermes 운영 업데이트"


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 90) -> dict:
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    return {"returncode": p.returncode, "output": p.stdout.strip()}


def notion_request(path: str, method: str = "GET", body: dict | None = None) -> dict:
    key = os.environ["NOTION_API_KEY"]
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode()
    req = urllib.request.Request("https://api.notion.com/v1/" + path, data=data, method=method)
    req.add_header("Authorization", f"Bearer {key}")
    req.add_header("Notion-Version", NOTION_VERSION)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def get_page_markdown() -> str:
    return notion_request(f"pages/{HQ_PAGE_ID}/markdown").get("markdown", "")


def patch_page_markdown(markdown: str) -> dict:
    # Notion Markdown PATCH API (2025-09-03) requires typed operations.
    # Use append-only insert_content for the HQ page to preserve embedded databases/views.
    return notion_request(
        f"pages/{HQ_PAGE_ID}/markdown",
        method="PATCH",
        body={"type": "insert_content", "insert_content": {"content": markdown}},
    )


def collect_status() -> dict:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    verify = run(["make", "verify"], cwd=HLS, timeout=180)
    report = run(["make", "report"], cwd=HLS, timeout=180)
    hls_report = run(["make", "hls-report"], cwd=HLS, timeout=90)
    git_status = run(["git", "status", "-sb"], cwd=REPO)
    git_log = run(["git", "log", "--oneline", "-3"], cwd=REPO)
    loop = {}
    if LOOP_JSON.exists():
        try:
            loop = json.loads(LOOP_JSON.read_text(encoding="utf-8"))
        except Exception as exc:
            loop = {"error": str(exc)}
    return {
        "generated_at": now,
        "verify_ok": verify["returncode"] == 0,
        "report_ok": report["returncode"] == 0,
        "hls_report_ok": hls_report["returncode"] == 0,
        "verify_output": verify["output"][-1200:],
        "report_output": report["output"][-800:],
        "hls_report_output": hls_report["output"][-1200:],
        "git_status": git_status["output"],
        "git_log": git_log["output"],
        "loop": loop,
    }


def render_update(s: dict) -> str:
    ok = s["verify_ok"] and s["report_ok"] and s["hls_report_ok"]
    loop_overall = s.get("loop", {}).get("overall", "UNKNOWN")
    return f"""{MARKER}

<callout icon="🏢" color="blue_bg">
	**Dashboard policy changed:** Notion HQ is now the human-facing Agent OS dashboard. Legacy static HTML dashboards are deprecated/frozen and should not be used as the operating surface.
</callout>

### 현재 운영 상태

| Area | Status | Notes |
|---|---:|---|
| Notion HQ dashboard | ACTIVE | 이 페이지가 HQ 대시보드 정본/관제면 |
| Legacy HTML dashboard | FROZEN | `hq-dashboard.html` / `agent-dashboard.html` 사용 중지 |
| DFXISP HLS verify | {'PASS' if s['verify_ok'] else 'FAIL'} | `make verify` |
| HLS verification report | {'PASS' if s['report_ok'] else 'FAIL'} | `make report` → `isppipeline/hls/reports/latest.md` |
| HLS dry-run report | {'PASS' if s['hls_report_ok'] else 'FAIL'} | `make hls-report` |
| Loop status snapshot | {loop_overall} | Notion으로 미러링 중 |

### DFXISP / GitHub

```text
{s['git_status']}
```

최근 commit:

```text
{s['git_log']}
```

### Verification output

```text
{s['verify_output']}
```

### HLS dry-run summary

```text
{s['hls_report_output']}
```

### 다음 운영 규칙

- 사람 관제/대시보드는 **Notion HQ**에서 한다.
- Drive는 문서/산출물 정본 저장소로 유지한다.
- 로컬 `/opt/data`는 실행/검증 cache다.
- HTML 대시보드 갱신 cron은 중지 상태로 유지한다.
- 자동 루프는 Notion HQ / Drive 산출물 / GitHub 상태를 갱신하는 방향으로 전환한다.

_Last updated by Hermes: `{s['generated_at']}`_
"""


def merge_markdown(existing: str, update: str) -> str:
    if MARKER in existing:
        return existing.split(MARKER, 1)[0].rstrip() + "\n\n" + update
    return existing.rstrip() + "\n\n" + update


def main() -> int:
    status = collect_status()
    # Append the latest Notion HQ dashboard update. We intentionally avoid
    # replacing the whole HQ page because it contains embedded Notion databases/views.
    result = patch_page_markdown("\n\n" + render_update(status))
    print(json.dumps({
        "ok": True,
        "page_id": HQ_PAGE_ID,
        "url": result.get("url") or f"https://app.notion.com/p/Agent-OS-HQ-3885871b3d1c8188b8ddfeb80492f1fb",
        "verify_ok": status["verify_ok"],
        "report_ok": status["report_ok"],
        "hls_report_ok": status["hls_report_ok"],
    }, ensure_ascii=False, indent=2))
    return 0 if status["verify_ok"] and status["report_ok"] and status["hls_report_ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
