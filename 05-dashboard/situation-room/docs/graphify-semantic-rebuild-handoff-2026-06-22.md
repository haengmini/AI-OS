# Graphify Semantic Rebuild Handoff — 2026-06-22

- Owner: next model session with Graphify semantic extraction capability (Claude/Codex/Gemini)
- Prepared by: Hermes Agent
- Vault root: `/opt/data/agent_os_archive/files`
- Official wiki root: `/opt/data/agent_os_archive/files/02-memory`
- Reason: Second Brain P0 cleanup created/updated Markdown files after the last `graphify-out/graph.json` build.

## Current status

```text
Graphify CLI: PASS
Graphify query: PASS
Graphify freshness: STALE
```

Hermes check:

```bash
cd /opt/data/agent_os_archive/files
graphify-staleness-check.sh
graphify check-update .
```

Observed:

```text
graphify-staleness: STALE — graph.json보다 새 문서 20+개
[graphify check-update] Pending non-code changes in /opt/data/agent_os_archive/files.
[graphify check-update] Run `/graphify --update` to apply semantic re-extraction.
```

## Why rebuild is needed

The current `graphify-out/graph.json` predates:

- root redirect docs: `/SCHEMA.md`, `/index.md`, `/log.md`
- official `02-memory` wiki root contract
- new seed layer notes: `hardware-layer`, `memory-layer`, `models-layer`, `agents-layer`, `dashboard-layer`, `production-layer`, `loop-layer`, `07-loop`
- updated `02-memory/index.md` and `02-memory/log.md`
- `second-brain-health.json/md`

Therefore Graphify queries work, but the graph does not fully represent the latest Second Brain state.

## Expected rebuild action

Use the model/session's Graphify semantic update workflow. In Graphify's own wording:

```bash
cd /opt/data/agent_os_archive/files
/graphify --update
```

If using the local CLI directly, inspect Graphify's current command semantics first. The installed CLI says:

```bash
graphify check-update .
graphify extract .
graphify cluster-only .
graphify label .
```

Avoid destructive options. Do not delete `graphify-out/`. Preserve:

```text
graphify-out/graph.json
graphify-out/GRAPH_REPORT.md
graphify-out/STATUS.md
graphify-out/wiki/*
```

## Completion criteria

1. Rebuilt `graphify-out` is uploaded/upserted to Google Drive.
2. Hermes archive sync pulls the new graph output.
3. Hermes runs:

```bash
cd /opt/data/agent_os_archive/files
graphify-staleness-check.sh
graphify query "What is the Agent OS memory layer?"
graphify explain "7-Layer Architecture"
```

4. `second-brain-health.json` changes `graphify.status` from `STALE` to `FRESH`.

## Current health files

```text
05-dashboard/situation-room/state/second-brain-health.json
05-dashboard/situation-room/docs/second-brain-health.md
```

These currently show that Markdown/frontmatter/wikilink health is clean, while Graphify freshness is the remaining blocker.
