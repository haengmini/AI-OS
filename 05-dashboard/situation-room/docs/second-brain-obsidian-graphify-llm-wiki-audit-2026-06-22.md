# Second Brain / Obsidian / Graphify / Karpathy LLM Wiki Audit

- 작성일: 2026-06-22
- 대상 vault/cache: `/opt/data/agent_os_archive/files`
- Drive 원칙: Google Drive `Agent OS`가 원본, local `/opt/data`는 cache/mirror/staging
- 점검 범위: Karpathy LLM Wiki 구조, Obsidian vault, Graphify 설치/출력, Claude/Gemini/Codex 공유성, 실시간/준실시간 동기화

## 1. 결론

현재 상태는 **Second Brain의 골격은 있으나, Karpathy식 LLM Wiki + Obsidian + Graphify가 완성된 상태는 아니다.**

요약 판정:

| 항목 | 상태 | 판정 |
|---|---|---|
| Drive-backed Obsidian vault | `.obsidian/` 존재, Obsidian core plugin 설정 있음 | 부분 구축 |
| Karpathy LLM Wiki 구조 | `SCHEMA.md`, `index.md`, `log.md`, `raw/`, `entities/`, `concepts/` 없음 | 미구축 |
| Graphify | setup 문서와 hooks는 있으나 `graphify` CLI와 `graphify-out/graph.json` 없음 | 미완료 |
| 다른 브랜드 모델 공유성 | `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, `.claude`, `.gemini`, `.codex` 존재 | 부분 구축 |
| 실시간 동기화 | Obsidian Sync core plugin은 enabled지만 서버에 `ob`/obsidian-headless/continuous process 없음 | 미검증/미구축 |
| Drive 동기화 | Google Drive archive script는 동작하나 기본은 daily/manual mirror | 준실시간 아님 |

핵심 문제:

1. **Obsidian vault는 있지만 LLM Wiki가 아니다.**
   - 현재는 Agent OS 문서 폴더에 가까우며, Karpathy식 `SCHEMA/index/log/raw/entities/concepts/comparisons/queries` 구조가 없다.

2. **Graphify 지시문은 있지만 실제 그래프가 없다.**
   - `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`는 `graphify-out/graph.json` 존재를 전제로 하지만 해당 output이 없다.
   - Hermes 서버에는 `graphify` 명령도 설치되어 있지 않다.

3. **실시간 동기화는 현재 확인되지 않았다.**
   - Drive archive는 동작하지만 cron/manual pull 방식이다.
   - Obsidian Sync plugin 설정은 보이나 headless sync process는 없다.
   - Claude/Gemini/Codex가 Drive를 읽을 수 있게 하는 문서 계약은 있으나, 자동 실시간 동기화/graph refresh는 없다.

## 2. 점검 근거

### 2.1 환경 변수

```text
WIKI_PATH=None
OBSIDIAN_VAULT_PATH=None
HERMES_HOME=/opt/data
HOME=/opt/data
```

판정:
- Hermes/agent가 명시적으로 wiki/vault 경로를 알도록 하는 `WIKI_PATH`, `OBSIDIAN_VAULT_PATH`가 설정되어 있지 않다.
- 현재는 관례적으로 `/opt/data/agent_os_archive/files`를 Drive-backed Obsidian vault로 사용한다.

### 2.2 Obsidian vault

확인된 파일:

```text
/opt/data/agent_os_archive/files/.obsidian/app.json
/opt/data/agent_os_archive/files/.obsidian/appearance.json
/opt/data/agent_os_archive/files/.obsidian/core-plugins.json
/opt/data/agent_os_archive/files/.obsidian/graph.json
/opt/data/agent_os_archive/files/.obsidian/workspace.json
```

`core-plugins.json`에서 확인:

```json
{
  "graph": true,
  "backlink": true,
  "canvas": true,
  "outgoing-link": true,
  "properties": true,
  "daily-notes": true,
  "templates": true,
  "sync": true
}
```

판정:
- Obsidian vault 자체는 존재한다.
- Obsidian graph/backlink/outgoing-link/sync core plugin은 켜져 있다.
- 그러나 서버에서 Obsidian Sync가 실제로 continuous sync 중인지는 확인되지 않는다.
- `ob`, `obsidian`, `obsidian-headless` 명령이 현재 서버 PATH에 없다.

### 2.3 Karpathy LLM Wiki 구조

현재 vault root에서 없음:

```text
SCHEMA.md: 없음
index.md: 없음
log.md: 없음
raw/: 없음
entities/: 없음
concepts/: 없음
comparisons/: 없음
queries/: 없음
```

Markdown/wiki metrics:

```json
{
  "markdown_files": 56,
  "frontmatter_pages": 5,
  "pages_with_wikilinks": 9,
  "total_wikilinks": 25,
  "broken_wikilinks_count": 9
}
```

판정:
- 문서와 노트는 있지만, Karpathy식 LLM Wiki의 핵심 backbone이 없다.
- index/log/schema가 없어서 agent가 매 세션 orientation하기 어렵다.
- frontmatter와 wikilink 사용률이 낮아 Obsidian/Dataview/LLM navigation 품질이 약하다.

### 2.4 Graphify 상태

존재:

```text
/opt/data/agent_os_archive/files/.graphifyignore
/opt/data/agent_os_archive/files/02-memory/graphify-setup.md
```

없음:

```text
/opt/data/agent_os_archive/files/graphify-out/
/opt/data/agent_os_archive/files/graphify-out/graph.json
/opt/data/agent_os_archive/files/graphify-out/GRAPH_REPORT.md
/opt/data/agent_os_archive/files/graphify-out/wiki/index.md
```

서버 명령:

```text
graphify: not found
```

Drive 검색 결과:
- `graphify-setup.md` 존재
- `.graphifyignore` 존재
- `graphify-out` 또는 `graph.json`은 검색/manifest에서 확인되지 않음

판정:
- Graphify는 setup 문서와 ignore 규칙만 있다.
- 실제 지식 그래프 output은 생성되지 않았다.
- `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`에 graphify 사용 규칙이 있지만, 전제 파일이 없어 현재 작동하지 않는다.

### 2.5 다른 브랜드 모델과의 공유성

존재하는 공유 지시 파일:

```text
CLAUDE.md
GEMINI.md
AGENTS.md
.codex/hooks.json
.claude/settings.json
.gemini/settings.json
```

좋은 점:
- Claude/Gemini/Codex가 Agent OS의 역할, 읽을 위치, 쓸 위치를 알 수 있게 되어 있다.
- 지시 파일들이 Karpathy 원칙처럼 “index이지 dump가 아니다”라는 방향을 따른다.
- `.claude`와 `.gemini` hook은 `graphify-out/graph.json`이 있으면 graphify를 먼저 보도록 유도한다.

문제:
- `graphify-out/graph.json`이 없어 hook의 핵심 조건이 충족되지 않는다.
- `.codex/hooks.json`은 Windows 경로 `C:\Users\user\...\graphify.EXE`를 가리켜 Linux Hermes 서버와 맞지 않는다.
- 외부 모델들이 Drive를 읽을 수는 있더라도, “실시간 동기화 + graph refresh + artifact registry update”까지 자동으로 묶여 있지는 않다.

## 3. Second Brain 성숙도 판정

현재는 다음 단계 중 **1.5단계**에 가깝다.

```text
0. 문서 흩어짐
1. Drive-backed vault 생성
1.5 Agent OS 문서 구조 + 모델 지시 파일 존재   ← 현재
2. Karpathy LLM Wiki backbone 완성
3. Graphify graph + Obsidian graph + artifact registry 연결
4. Claude/Gemini/Hermes/Codex가 같은 graph/index/artifact를 보고 작업
5. 실시간/준실시간 sync + automated lint/healthcheck
```

즉, **세컨드 브레인의 저장소와 운영 문서 골격은 있지만, 지식 컴파일/그래프/실시간 동기화 계층은 아직 완성되지 않았다.**

## 4. 실시간 동기화 판정

### 현재 동기화 경로

```text
Google Drive Agent OS
  -> /opt/data/agent_os_archive/files     # Hermes local archive/mirror
  -> Situation Room / summaries / manifest
```

현재 archive sync는 다음 방식이다.

- `agent_os_drive_archive.sh` 수동 실행 가능
- `agent-os-drive-daily-archive` cron으로 주기 실행
- Drive -> local mirror 중심
- report 작성 시 Hermes가 Drive upload/upsert를 수행하면 Drive 원본이 생김

### 실시간성 판정

| 방향 | 현재 상태 | 실시간 여부 |
|---|---|---|
| Hermes local -> Drive | 보고서/상태 파일은 upsert하면 즉시 반영 | 작업별 수동/스크립트 즉시 가능 |
| Drive -> Hermes local | archive script/cron 실행 시 반영 | daily/manual, 실시간 아님 |
| Obsidian desktop/mobile -> Drive | Google Drive/Obsidian Sync 클라이언트 상태에 의존 | 이 서버에서 확인 불가 |
| Drive -> Claude/Gemini/Codex | 모델이 Drive 또는 local vault를 직접 열 때 가능 | 자동 push 아님 |
| Graphify refresh | graphify-out 없음 | 미구축 |

판정:
- 현재는 **공유 Drive workspace**는 있다.
- 하지만 **실시간 multi-model sync system**은 아니다.
- 준실시간으로 만들려면 sync daemon 또는 짧은 주기의 no-agent sync job, graph refresh job, registry update job이 필요하다.

## 5. 권장 개선 순서

### P0 — LLM Wiki backbone 생성

Drive-backed vault root에 다음을 만든다.

```text
SCHEMA.md
index.md
log.md
raw/
  articles/
  papers/
  transcripts/
  assets/
entities/
concepts/
comparisons/
queries/
```

`SCHEMA.md`는 Agent OS/DFXISP/AI드론에 맞춰 다음 taxonomy를 정의해야 한다.

```text
agent-os, project, dfxisp, ai-drone, fpga, zcu104, ai-isp,
model-routing, workflow, verification, hardware, software,
paper, source, decision, glossary, dashboard, sync
```

### P0 — `WIKI_PATH` / `OBSIDIAN_VAULT_PATH` 설정

Hermes와 모든 role agent가 같은 vault를 보도록:

```text
WIKI_PATH=/opt/data/agent_os_archive/files
OBSIDIAN_VAULT_PATH=/opt/data/agent_os_archive/files
```

단, Hermes config/env 변경은 운영 설정 변경이므로 별도 명시 후 적용한다.

### P0 — Graphify 실제 생성

서버 또는 Windows Drive 클라이언트 쪽에서 graphify를 설치/실행해야 한다.

서버 후보:

```bash
uv tool install graphifyy
cd /opt/data/agent_os_archive/files
graphify .
```

예상 산출물:

```text
graphify-out/graph.json
graphify-out/GRAPH_REPORT.md
graphify-out/graph.html
graphify-out/wiki/index.md
```

주의:
- graphify가 Claude/Codex/Gemini 백엔드를 요구할 수 있으므로 API/외부 모델 호출 비용이 발생할 수 있다.
- 설치/모델 연결/토큰 사용 전 사용자 승인 권장.

### P1 — Graphify hook 수정

현재 `.codex/hooks.json`은 Windows graphify 경로를 가리킨다.

```text
C:\Users\user\AppData\Local\Programs\Python\Python313\Scripts\graphify.EXE
```

Linux/Hermes 서버에서는 작동하지 않는다. profile/OS별 hook 분리가 필요하다.

### P1 — Obsidian Sync/headless 확인

실시간 동기화를 원하면 둘 중 하나를 선택해야 한다.

1. Google Drive Desktop 기반 동기화
   - user devices에서 Drive app이 `Agent OS`를 sync
   - Hermes 서버는 Google Drive API archive cron으로 pull

2. Obsidian Sync/headless 기반 동기화
   - `obsidian-headless` 설치
   - `ob sync --continuous` systemd user service 실행

현재 서버에는 `ob` 명령과 continuous sync process가 없다.

### P1 — Wiki lint/healthcheck routine 추가

정기적으로 다음을 점검한다.

- broken wikilinks
- orphan pages
- frontmatter 누락
- index 누락
- stale pages
- graphify-out freshness
- Drive manifest freshness
- external model instruction drift

추천 output:

```text
05-dashboard/situation-room/state/second-brain-health.json
05-dashboard/situation-room/docs/second-brain-health.md
```

## 6. 즉시 실행 가능한 다음 작업

다음 단계는 안전한 문서 생성/Drive 저장 범위에서 바로 진행 가능하다.

1. `SCHEMA.md`, `index.md`, `log.md` 초안 생성
2. `raw/`, `entities/`, `concepts/`, `comparisons/`, `queries/` 폴더 생성
3. 기존 56개 Markdown을 index에 1차 등록
4. Second Brain healthcheck JSON/MD 생성
5. Graphify 설치/실행 계획을 `02-memory/graphify-runbook.md`로 정리

단, 실제 graphify 설치/실행은 모델 API/토큰/외부 호출 가능성이 있으므로 사용자 승인 후 진행하는 것이 안전하다.

## 7. 최종 판정

질문: “안드레 카파시의 LLM Wiki와 옵시디언, graphify가 잘 만나 Second Brain이 잘 구축되었는가?”

답:

**아직 아니다.**

정확히는:

```text
Drive-backed Obsidian vault: 있음
Agent OS 문서 체계: 있음
Claude/Gemini/Codex/Hermes 지시 파일: 있음
Karpathy LLM Wiki backbone: 없음
Graphify output: 없음
Realtime sync daemon: 없음
Multi-model shared artifact registry: 시작됨
```

따라서 현재는 “Second Brain의 토대”이며, 완성하려면 **LLM Wiki backbone + graphify-out 생성 + sync/healthcheck loop**를 추가해야 한다.
