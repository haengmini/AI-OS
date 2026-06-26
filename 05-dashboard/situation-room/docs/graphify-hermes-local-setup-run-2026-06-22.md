# Graphify Hermes Local Setup Run — 2026-06-22

- 목적: Hermes Linux 환경에서 `graphify` wrapper, PATH, staleness 감지 스크립트, daily 09:05 감지 cron을 설치/검증한다.
- Canonical Drive location: `Agent OS/05-dashboard/situation-room/docs/graphify-hermes-local-setup-run-2026-06-22.md`
- Local setup script: `/opt/data/setup-graphify-hermes.sh`
- Local wrapper: `/opt/data/scripts/graphify`
- Local staleness checker: `/opt/data/scripts/graphify-staleness-check.sh`
- Vault: `/opt/data/agent_os_archive/files`

## 1. Work list

1. Create/review `setup-graphify-hermes.sh`.
2. Run setup script.
3. Source `~/.bashrc` and verify `which graphify`.
4. Verify graphify works from the vault root.
5. Run staleness checker.
6. Register daily 09:05 staleness check cron.
7. Save Drive-first execution log.

## 2. Idempotence note

The pasted script was implemented with one small safety improvement:

```text
If PATH already points `graphify` to /opt/data/scripts/graphify, the resolver skips that wrapper so it does not rewrite the wrapper to exec itself.
```

This preserves the intended behavior while avoiding self-recursion on repeated runs after PATH is active.

## 3. Setup script output

```text
[1] graphify = /opt/data/.local/bin/graphify
[2] wrapper = /opt/data/scripts/graphify -> /opt/data/.local/bin/graphify
[3] PATH 등록(.bashrc/.profile). 현재 셸 반영: source ~/.bashrc
[4] staleness = /opt/data/scripts/graphify-staleness-check.sh
[5] self-test
    wrapper OK
graphify-staleness: STALE — graph.json보다 새 문서 1+개 2026-06-22T05:40:05Z
  - /opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/graphify-sync-query-run-2026-06-22.md
→ 모델 세션에서 semantic 재빌드 후 graphify-out을 Drive에 upsert
```

## 4. PATH verification

After `source /opt/data/.bashrc`:

```text
PATH=/opt/data/scripts:/opt/data/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
which graphify: /opt/data/scripts/graphify
graphify realpath: /opt/data/scripts/graphify
```

Result:

```text
PASS — graphify resolves to /opt/data/scripts/graphify
```

## 5. Graphify smoke test

Command:

```bash
cd /opt/data/agent_os_archive/files
graphify explain "7-Layer Architecture"
```

Result excerpt:

```text
Node: 7-Layer Architecture
  ID:        c_seven_layer
  Source:    AGENT-OS.md None
  Type:      concept
  Community: OS Constitution & Architecture
  Degree:    10
```

Result:

```text
PASS — wrapper can run Graphify from vault root.
```

## 6. Staleness check result

Command:

```bash
/opt/data/scripts/graphify-staleness-check.sh
```

Result:

```text
graphify-staleness: STALE — graph.json보다 새 문서 1+개 2026-06-22T05:40:05Z
  - /opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/graphify-sync-query-run-2026-06-22.md
→ 모델 세션에서 semantic 재빌드 후 graphify-out을 Drive에 upsert
```

Interpretation:

```text
Detection layer works. It correctly noticed at least one Markdown file newer than graphify-out/graph.json and set the need for a semantic rebuild.
```

This is expected because Hermes created a new graphify query run log after the last semantic graph build.

## 7. Cron registration

System `crontab` is not available in the Hermes container/runtime:

```text
crontab command not available
```

Therefore the daily check was registered with Hermes cron instead.

Hermes cron job:

```text
job_id: c0f632683bd8
name: graphify-staleness-check
schedule: 5 9 * * *
script: graphify-staleness-check.sh
mode: no_agent / script-only
deliver: local
```

The script was also run immediately once and wrote to local log:

```text
/opt/data/cron/output/graphify-staleness/YYYY-MM-DD.log
```

## 8. Slack integration note

Current cron delivery is `local` to avoid daily Slack noise. Recommended Slack integration:

```text
FRESH -> stay local/silent or local-only log
STALE -> post a concise Slack alert with the changed file list and next action: semantic rebuild by Claude/Codex/Gemini model session
```

This preserves the intended separation:

```text
Detection = Hermes/free/script-only
Semantic rebuild = model session / possible cost
```

## 9. Final status

```text
setup script: PASS
wrapper: PASS
PATH: PASS
graphify smoke test: PASS
staleness detection: PASS, currently STALE
cron: PASS via Hermes cron, not system crontab
Drive-first log: created
```
