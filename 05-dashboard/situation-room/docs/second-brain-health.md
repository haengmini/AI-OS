# Second Brain Health — 2026-06-22

- Generated: 2026-06-22T06:47:35+00:00
- Overall status: **attention_needed**
- Official WIKI_PATH: `/opt/data/agent_os_archive/files/02-memory`
- Obsidian vault: `/opt/data/agent_os_archive/files`
- Google Drive canonical: yes

## Summary

| Check | Result |
|---|---:|
| 02-memory backbone | PASS |
| Markdown files in 02-memory | 24 |
| Wiki notes excluding meta/templates | 20 |
| Wikilinks in 02-memory | 153 |
| Missing frontmatter | 0 |
| Missing required fields | 0 |
| Broken wikilinks | 0 |
| Orphan notes | 0 |
| Graphify status | STALE |

## Quality details

### Broken wikilinks

None

### Orphan notes

None

### Frontmatter issues

None

## Graphify

```text
graphify-staleness: STALE — graph.json보다 새 문서 20+개 2026-06-22T06:47:35Z
  - /opt/data/agent_os_archive/files/index.md
  - /opt/data/agent_os_archive/files/log.md
  - /opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/graphify-hermes-local-setup-run-2026-06-22.md
  - /opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/graphify-sync-query-run-2026-06-22.md
  - /opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/second-brain-build-method-2026-06-22.md
  - /opt/data/agent_os_archive/files/05-dashboard/situation-room/docs/claude-second-brain-work-review-2026-06-22.md
  - /opt/data/agent_os_archive/files/02-memory/queries/how-does-hermes-loop-work.md
  - /opt/data/agent_os_archive/files/02-memory/index.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/drive-first-source-of-truth.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/07-loop.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/production-layer.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/hardware-layer.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/7-layer-architecture.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/dashboard-layer.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/memory-promotion-filter.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/model-routing.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/models-layer.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/memory-layer.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/agents-layer.md
  - /opt/data/agent_os_archive/files/02-memory/concepts/loop-layer.md
→ 모델 세션에서 semantic 재빌드 후 graphify-out을 Drive에 upsert
```

## Required next action

- semantic_rebuild_graphify_out
- upsert_graphify_out_to_drive
- rerun_staleness_until_fresh
- add_second_brain_card_to_situation_room

## Interpretation

The LLM Wiki backbone is now healthy at the Markdown/link/frontmatter layer. The remaining blocker is graph freshness: `graphify-out/graph.json` is older than the newly created Second Brain notes and reports. A semantic Graphify rebuild should be run by a model session, then the rebuilt `graphify-out` should be upserted to Drive and re-synced by Hermes until this report shows `Graphify status = FRESH`.
