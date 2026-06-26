# Claude Second Brain Work Review — 2026-06-22

- 대상: Claude/Cowork가 Google Drive `Agent OS`에 반영한 Second Brain / LLM Wiki 작업
- 검토자: Hermes Agent
- 검토 시각: 2026-06-22
- 원칙: Google Drive가 canonical source of truth, `/opt/data/agent_os_archive/files`는 local mirror/cache
- 검토 경로: `/opt/data/agent_os_archive/files`

## 1. 결론

Claude 작업은 **성공적인 1차 스캐폴딩**이다.

이전 상태와 비교하면 가장 큰 변화는 다음이다.

```text
이전: Obsidian vault + graphify-out은 있으나 LLM Wiki backbone 부재
현재: 02-memory 아래에 SCHEMA/index/log + concepts/entities/comparisons/queries/raw/templates 생성됨
```

즉, Second Brain은 다음 단계로 올라갔다.

```text
Before: 1.5단계 — Agent OS 문서 구조 + 모델 지시 파일 존재
After:  2.3단계 — 02-memory scoped LLM Wiki backbone + seed notes 존재
```

다만 아직 완성은 아니다. 핵심 남은 작업은 다음이다.

1. `02-memory`를 공식 wiki root로 쓸지, vault root를 wiki root로 쓸지 계약을 확정해야 한다.
2. root-level `SCHEMA.md/index.md/log.md`는 여전히 없다.
3. 새 Markdown 17개 이상이 `graphify-out/graph.json`보다 최신이라 Graphify는 현재 `STALE`이다.
4. 일부 wikilink가 아직 깨져 있다.
5. Second Brain healthcheck 산출물은 아직 없다.

## 2. Drive sync 결과

Hermes에서 Drive archive sync를 실행했다.

```text
Agent OS Drive archive sync complete
root_id=1xbqGeDdLerv8jd3eeHsR0IS-CHkI7kgz
folders=36 files=115 new=14 changed=14 removed=0
archive=/opt/data/agent_os_archive
daily_summary=/opt/data/agent_os_archive/summaries/daily/2026-06-22.md
```

Claude 작업분이 local mirror에 정상 동기화되었다.

## 3. Claude가 새로 만든 핵심 파일

최근 동기화된 핵심 파일:

```text
02-memory/SCHEMA.md
02-memory/index.md
02-memory/log.md
02-memory/templates/note-template.md
02-memory/raw/agent-os-backend-references.md
02-memory/queries/how-does-hermes-loop-work.md
02-memory/entities/hermes.md
02-memory/entities/graphify.md
02-memory/concepts/progressive-disclosure.md
02-memory/concepts/model-routing.md
02-memory/concepts/memory-promotion-filter.md
02-memory/concepts/drive-first-source-of-truth.md
02-memory/concepts/7-layer-architecture.md
02-memory/comparisons/postgres-vs-drive-as-agent-bus.md
```

Claude가 기록한 log:

```text
2026-06-22 — 백본 스캐폴딩 (by Claude/Cowork)
- SCHEMA.md, index.md, log.md 생성
- folders: concepts/ entities/ comparisons/ queries/ raw/ templates/
- seed atomic notes 작성
- graphify-out 연결 및 query-first 규칙 명시
- 기존 노트의 frontmatter/wikilink 소급 변환은 미완
```

## 4. 좋은 점

### 4.1 `02-memory` scoped wiki 구조가 명확하다

`02-memory/SCHEMA.md`가 다음 폴더 타입을 정의한다.

```text
concepts/     개념·원칙·메커니즘
entities/     사람·도구·모델·프로젝트·에이전트
comparisons/  A vs B 비교·의사결정
queries/      자주 묻는 질문 + 답
raw/          미증류 원본
templates/    노트 템플릿
```

Agent OS 7-layer 구조상 `02-memory`를 Second Brain의 중심으로 삼는 것은 설계적으로 타당하다.

### 4.2 Karpathy LLM Wiki 원칙을 반영했다

SCHEMA에 다음 원칙이 들어갔다.

```text
index이지 dump가 아니다
atomic notes
frontmatter
wikilinks
query-first
graphify first
promotion filter
append-only log
```

이전의 “문서 더미” 상태에서 “AI가 navigate 가능한 wiki”로 한 단계 전환되었다.

### 4.3 Seed notes 선택이 적절하다

초기 seed가 Agent OS 운영 핵심을 잘 잡고 있다.

```text
7-layer-architecture
model-routing
drive-first-source-of-truth
progressive-disclosure
memory-promotion-filter
hermes
graphify
postgres-vs-drive-as-agent-bus
how-does-hermes-loop-work
```

특히 `drive-first-source-of-truth`, `model-routing`, `hermes`, `graphify`는 여러 모델이 함께 일하는 Second Brain에서 우선적으로 있어야 하는 개념이다.

### 4.4 Claude가 자기 한계를 명시했다

`claude-sync-verification-2026-06-22.md`에서 Claude가 다음을 정확히 기록했다.

```text
Drive -> Claude read: 가능
Claude -> Drive create_file: 가능
Claude -> Drive existing file in-place update: 불가
```

이건 운영적으로 매우 중요하다. Claude/Cowork는 기존 `status.json` 같은 상태 파일을 patch/update하지 못하므로, dated status file을 추가하고 Hermes가 merge하는 구조가 맞다.

## 5. 문제점 / 리스크

### 5.1 Wiki root 계약 불일치

이전 Hermes 문서에서는 다음 root-level backbone을 권장했다.

```text
SCHEMA.md
index.md
log.md
raw/
entities/
concepts/
comparisons/
queries/
```

하지만 Claude는 다음 위치에 만들었다.

```text
02-memory/SCHEMA.md
02-memory/index.md
02-memory/log.md
02-memory/raw/
02-memory/entities/
02-memory/concepts/
02-memory/comparisons/
02-memory/queries/
```

검토 결과:

```text
vault root backbone: 없음
02-memory backbone: 있음
```

판정:

- `02-memory` scoped wiki는 Agent OS 7-layer 관점에서 타당하다.
- 하지만 `WIKI_PATH` 또는 root redirect가 없으면 Hermes/Claude/Gemini/Codex가 “wiki root가 어디인지” 헷갈릴 수 있다.

권장:

```text
공식 WIKI_PATH = /opt/data/agent_os_archive/files/02-memory
OBSIDIAN_VAULT_PATH = /opt/data/agent_os_archive/files
```

그리고 vault root에는 redirect 문서 또는 안내를 둔다.

```text
SCHEMA.md -> 02-memory/SCHEMA.md 참조
index.md  -> 02-memory/index.md 참조
log.md    -> 02-memory/log.md 참조
```

혹은 root-level backbone으로 통일한다. 둘 중 하나를 정해야 한다.

### 5.2 Graphify가 현재 STALE

staleness check 결과:

```text
graphify-staleness: STALE — graph.json보다 새 문서 17+개
```

새로 생긴 문서들이 `graphify-out/graph.json`보다 최신이므로, graphify query는 아직 Claude가 만든 02-memory seed notes를 완전히 반영하지 못할 수 있다.

권장:

```text
Claude/Codex/Gemini model session에서 semantic rebuild
→ graphify-out Drive upsert
→ Hermes archive sync
→ staleness FRESH 확인
```

### 5.3 Broken wikilinks 존재

02-memory scan 결과:

```text
wikilinks_total_in_02_memory: 94
broken_wikilinks_count: 13
```

주요 broken examples:

```text
[[07-loop]]
[[hardware-layer]]
[[memory-layer]]
[[models-layer]]
[[agents-layer]]
[[dashboard-layer]]
[[production-layer]]
[[loop-layer]]
[[원본노트]]
[[note-title]]
[[<관련-노트>]]
```

해석:

- 일부는 template placeholder라 심각하지 않다.
- `hardware-layer` 등 layer note는 의도적으로 “아직 미생성”이라고 Claude가 표시했다.
- 하지만 `[[07-loop]]`처럼 실제 폴더/문서가 있으나 alias가 없는 링크는 수정 필요하다.

권장:

1. layer note 7개를 실제로 생성하거나 링크를 plain text로 바꾼다.
2. template placeholder는 lint ignore 규칙에 넣는다.
3. `[[07-loop]]`는 실제 경로에 맞는 노트/alias를 만든다.

### 5.4 Orphan notes 존재

Scan 결과:

```text
orphan_notes_count: 2
orphan_notes:
- 02-memory/README.md
- 02-memory/queries/how-does-hermes-loop-work.md
```

`queries/how-does-hermes-loop-work.md`는 `index.md`에 “저장된 Q&A: queries/”라고만 있고 직접 wikilink가 없어 inbound가 잡히지 않았다.

권장:

```text
02-memory/index.md에 [[how-does-hermes-loop-work]] 직접 추가
02-memory/README.md는 index/SCHEMA에서 직접 링크하거나 archive/legacy 처리
```

### 5.5 기존 100여 개 문서의 소급 변환은 아직 안 됨

Claude도 log에 명시했다.

```text
기존 노트(MY/AGENT-OS/04-agents 등)의 frontmatter·wikilink 소급 변환은 in-place 수정 불가
```

현재 02-memory seed는 좋지만, 전체 vault의 기존 문서가 아직 LLM Wiki 규칙으로 통합된 것은 아니다.

권장:

```text
1차: root canonical docs만 frontmatter + links 추가
2차: 04-agents, 05-dashboard, 07-loop docs
3차: 06-production project docs
```

### 5.6 Second Brain healthcheck 없음

아직 다음 파일은 없다.

```text
05-dashboard/situation-room/state/second-brain-health.json
05-dashboard/situation-room/docs/second-brain-health.md
```

권장:

정기적으로 다음을 산출하게 한다.

```text
wiki_root
graphify_status
staleness_status
broken_wikilinks
orphan_notes
frontmatter_missing
index_completeness
pending_rebuild
human_attention_needed
```

## 6. 측정 결과

```json
{
  "wiki_path": "/opt/data/agent_os_archive/files/02-memory",
  "markdown_count_02_memory": 16,
  "note_count_excluding_meta_templates": 12,
  "root_missing_backbone": [
    "SCHEMA.md",
    "index.md",
    "log.md",
    "raw",
    "entities",
    "concepts",
    "comparisons",
    "queries"
  ],
  "02_memory_missing_backbone": [],
  "frontmatter_missing": [
    "02-memory/graphify-setup.md",
    "02-memory/README.md"
  ],
  "required_frontmatter_missing_count": 0,
  "wikilinks_total_in_02_memory": 94,
  "broken_wikilinks_count": 13,
  "orphan_notes_count": 2,
  "graphify_status": "STALE",
  "graphify_query_smoke": "PASS"
}
```

## 7. 판정표

| 항목 | 판정 | 설명 |
|---|---:|---|
| Drive sync | PASS | Claude 작업분 14 new / 14 changed 반영 |
| 02-memory wiki backbone | PASS | SCHEMA/index/log/folders 생성됨 |
| Seed atomic notes | PASS | 핵심 개념/엔터티/비교/Q&A 있음 |
| Frontmatter | PARTIAL | 새 seed는 양호, 기존 README/graphify-setup은 미변환 |
| Wikilinks | PARTIAL | 94 links 중 13 broken |
| Orphans | PARTIAL | 2개 |
| Graphify query | PASS | 기존 graph로 query 실행 가능 |
| Graph freshness | FAIL/STALE | 새 문서 17+개가 graph.json보다 최신 |
| Healthcheck artifacts | MISSING | second-brain-health.json/md 없음 |
| Multi-model sync contract | PARTIAL | Claude create는 가능, update는 Hermes merge 필요 |

## 8. 권장 다음 작업

우선순위 순서:

### P0 — Wiki root 계약 확정

둘 중 하나 선택:

A안: `02-memory`를 공식 LLM Wiki root로 채택

```text
WIKI_PATH=/opt/data/agent_os_archive/files/02-memory
OBSIDIAN_VAULT_PATH=/opt/data/agent_os_archive/files
```

B안: vault root에 SCHEMA/index/log/raw/entities/concepts를 둔다.

현재 구조상 A안이 더 자연스럽다. Agent OS 7-layer에서 memory layer가 Second Brain의 중심이기 때문이다.

### P0 — root redirect 추가

A안을 택한다면 root에 작은 redirect 문서를 둔다.

```text
SCHEMA.md -> 02-memory/SCHEMA.md
index.md -> 02-memory/index.md
log.md -> 02-memory/log.md
```

단, root-level 파일 추가는 Drive canonical artifact이므로 upsert와 registry 기록을 함께 해야 한다.

### P0 — Graphify semantic rebuild

현재 STALE이므로 다음 모델 세션이 수행해야 한다.

```bash
cd Agent OS vault root
graphify extract .  # 또는 Claude/Cowork graphify rebuild workflow
```

산출물:

```text
graphify-out/graph.json
graphify-out/GRAPH_REPORT.md
graphify-out/wiki/*
```

이후 Hermes가 확인:

```bash
graphify-staleness-check.sh  # FRESH 기대
```

### P1 — Broken links 정리

- 7-layer 하위 노트 생성 또는 링크 제거
- `[[07-loop]]` alias/노트 생성
- template placeholder는 lint ignore 처리
- `queries/how-does-hermes-loop-work`를 index에 직접 링크

### P1 — Second Brain healthcheck 생성

다음 파일 생성:

```text
05-dashboard/situation-room/state/second-brain-health.json
05-dashboard/situation-room/docs/second-brain-health.md
```

그리고 Situation Room dashboard에 연결한다.

## 9. 최종 평가

Claude 작업은 방향이 맞다. 특히 다음 세 가지가 좋다.

```text
1. 02-memory를 scoped LLM Wiki로 만들었다.
2. SCHEMA/index/log를 만들어 AI navigation backbone을 세웠다.
3. seed notes가 Agent OS 운영 핵심을 잘 잡았다.
```

하지만 “완료”는 아니다.

현재 상태를 정확히 표현하면:

```text
Second Brain backbone: 생성됨
Graphify integration: 이전 graph 기준 작동, 현재 STALE
Full vault integration: 미완
Healthcheck loop: 미완
Multi-model write/update protocol: 부분 완성
```

다음으로는 **WIKI_PATH 계약 확정 → root redirect 또는 root migration → graphify rebuild → second-brain-health 생성** 순서로 진행하면 된다.
