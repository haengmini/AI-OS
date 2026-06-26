---
type: redirect
title: Agent OS Wiki Log Redirect
tags: [meta, wiki, redirect, log]
created: 2026-06-22
updated: 2026-06-22
status: stable
source: "[[02-memory/log]]"
---

# Wiki Log Redirect

The official Agent OS LLM Wiki append-only log lives at:

```text
02-memory/log.md
```

All Second Brain ingest/update/query/lint operations should append to that file.

Operational contract:

```text
WIKI_PATH=/opt/data/agent_os_archive/files/02-memory
OBSIDIAN_VAULT_PATH=/opt/data/agent_os_archive/files
```
