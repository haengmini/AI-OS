#!/usr/bin/env python3
"""Drive-first Agent OS loop watchdog.

Checks the Google Drive canonical dashboard and DFXISP HLS C-sim scaffold,
then upserts loop-status-latest.{json,md} into Drive 05-dashboard.
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, "/opt/data/skills/productivity/google-workspace/scripts")
from google_api import build_service  # noqa: E402
from googleapiclient.http import MediaFileUpload  # noqa: E402

DASHBOARD_ID = "1AjhJOMeSnmMtrnMeRDIDH1v9VoK_RwT0"
DASHBOARD_PARENT = "1eUjXgSTbqdkbx2myeV7APWLkYQgnQGhH"  # Agent OS / 05-dashboard
DFXISP_HLS_FOLDER = "1LbQkwIckkJpWBbR4c4ip2l5f_X3M-DML"
DFXISP_REPO = Path("/opt/data/dfxisp_md")
OUT_DIR = Path("/opt/data/agent_os_loop_status")


def run(cmd: list[str], cwd: Path | None = None, timeout: int = 120) -> dict:
    p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    return {"cmd": cmd, "returncode": p.returncode, "output": p.stdout[-4000:]}


def download_file(service, file_id: str, path: Path) -> None:
    request = service.files().get_media(fileId=file_id)
    data = request.execute()
    path.write_bytes(data)


def upsert(service, local_path: Path, name: str, parent: str, mime: str) -> dict:
    q = f"'{parent}' in parents and name = '{name}' and trashed=false"
    found = service.files().list(q=q, spaces="drive", fields="files(id,name)", pageSize=10).execute().get("files", [])
    media = MediaFileUpload(str(local_path), mimetype=mime, resumable=False)
    if found:
        return service.files().update(fileId=found[0]["id"], media_body=media,
                                      fields="id,name,modifiedTime,webViewLink").execute()
    return service.files().create(body={"name": name, "parents": [parent]}, media_body=media,
                                  fields="id,name,modifiedTime,webViewLink").execute()


def main() -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    service = build_service("drive", "v3")
    checks: list[dict] = []

    with TemporaryDirectory() as td:
        tmp = Path(td)
        html = tmp / "hq-dashboard.html"
        download_file(service, DASHBOARD_ID, html)
        script = "\n".join(part.split("</script>", 1)[0] for part in html.read_text(encoding="utf-8").split("<script>")[1:])
        js = tmp / "hq-dashboard.js"
        js.write_text(script, encoding="utf-8")
        node_check = run(["node", "--check", str(js)], timeout=60)
        checks.append({"name": "drive_hq_dashboard_js", "ok": node_check["returncode"] == 0, "detail": node_check})

    expected = {"README.md", "Makefile", "include/dfxisp_accel.hpp", "src/dfxisp_accel.cpp", "tests/test_dfxisp_csim.cpp"}
    files = service.files().list(q=f"'{DFXISP_HLS_FOLDER}' in parents and trashed=false", spaces="drive",
                                 fields="files(id,name,modifiedTime,webViewLink)", pageSize=100).execute().get("files", [])
    names = {f["name"] for f in files}
    checks.append({"name": "drive_dfxisp_hls_files", "ok": expected.issubset(names), "missing": sorted(expected - names), "files": files})

    if (DFXISP_REPO / "isppipeline/hls/Makefile").exists():
        csim = run(["make", "csim"], cwd=DFXISP_REPO / "isppipeline/hls", timeout=120)
        checks.append({"name": "dfxisp_local_csim", "ok": csim["returncode"] == 0, "detail": csim})
    else:
        checks.append({"name": "dfxisp_local_csim", "ok": False, "detail": "missing local hls Makefile"})

    ok = all(c.get("ok") for c in checks)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    status = {"generated_at": now, "overall": "PASS" if ok else "FAIL", "checks": checks}
    json_path = OUT_DIR / "loop-status-latest.json"
    md_path = OUT_DIR / "loop-status-latest.md"
    json_path.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md = ["# Agent OS Drive-first Loop Status", "", f"- Generated: `{now}`", f"- Overall: **{status['overall']}**", "", "## Checks"]
    for c in checks:
        md.append(f"- {'✅' if c.get('ok') else '❌'} `{c['name']}`")
        if not c.get("ok"):
            md.append(f"  - detail: `{str(c.get('missing') or c.get('detail'))[:500]}`")
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    json_meta = upsert(service, json_path, "loop-status-latest.json", DASHBOARD_PARENT, "application/json")
    md_meta = upsert(service, md_path, "loop-status-latest.md", DASHBOARD_PARENT, "text/markdown")
    if ok:
        print(f"Agent OS loop PASS — Drive status updated: {md_meta['webViewLink']}")
        return 0
    print(f"Agent OS loop FAIL — Drive status updated: {md_meta['webViewLink']}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
