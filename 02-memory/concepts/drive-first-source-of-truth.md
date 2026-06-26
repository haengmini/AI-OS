---
type: concept
title: Drive-first Source of Truth
tags: [storage, sync, contract]
created: 2026-06-22
source: "[[agent-routing-contract]] §1"
status: stable
---

# Drive-first Source of Truth

## 한 줄 정의
**Google Drive가 정본(source of truth)**, 로컬 `/opt/data`는 캐시·미러·스테이징.

## 핵심
```
Google Drive = canonical workspace / document store
Kanban       = task state / ownership
Local /opt/data = execution cache, mirror, staging, scripts
Slack        = command/update surface (durable store 아님)
```
- 모든 산출물은 완료 전 Drive에 반영. 로컬 경로는 "cache/staging"으로 라벨.
- **운영상 주의**(2026-06-22 확인): Cowork Drive 커넥터는 기존 파일 *in-place 수정 불가*(새 파일 생성만). 공유 상태는 단일 JSON 덮어쓰기 대신 **append/태스크별 파일**로 두고 머지. → [[postgres-vs-drive-as-agent-bus]] 참고.

## 근거 / 출처
- `04-agents/routing/agent-routing-contract.md` §1, §3.

## 관련
- [[index]]
- [[hermes]]
- [[postgres-vs-drive-as-agent-bus]]
