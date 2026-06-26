# Claude (Cowork) Sync Verification & Hermes Audit Review

- 작성일: 2026-06-22
- 작성자: Claude (Cowork mode)
- 목적: (1) Hermes audit 설계 검토, (2) Cowork Claude의 Drive vault 동기화 가능 여부 검증 및 적용
- 원본 위치: Google Drive `Agent OS/05-dashboard/situation-room/docs/`

## 1. 결론 (Sync 판정)

| 방향 | 메커니즘 | 상태 |
|---|---|---|
| Drive -> Claude (읽기) | Google Drive MCP connector (search/read/download) | 작동함 (지금 검증 완료) |
| Claude -> Drive (새 파일 생성) | connector `create_file` | 작동함 (이 파일이 증거) |
| Claude -> Drive (기존 파일 in-place 수정) | connector에 update/patch 툴 없음 | 불가 — 새 파일만 생성 가능 |
| 로컬 파일시스템 `G:\내 드라이브\Agent OS` | Cowork 워크스페이스 마운트 | 비어 있음 — 이 경로로는 vault 접근 불가 |

핵심: **Cowork Claude는 "Drive 파일시스템 마운트"가 아니라 "Drive MCP 커넥터"로 동기화된다.** 읽기와 새 파일 쓰기는 즉시 가능하다. 단, 공유 상태 JSON(dashboard-state.json) 같은 기존 파일의 in-place 갱신은 이 커넥터로는 불가능하므로, 덮어쓰기 대신 "새 dated 파일 추가" 방식으로만 기여해야 한다.

## 2. Hermes audit 검토

정확한 부분:
- Linux 서버(`/opt/data/agent_os_archive/files`) 기준 상태 진단은 사실에 부합. Drive 커넥터로 교차 확인 시 `graphify-out/`, `SCHEMA.md`, `index.md`, `log.md`는 실제로 Drive에도 없음.
- "Obsidian vault 외형은 있으나 LLM Wiki backbone은 없다", "graphify 지시문은 있으나 output이 없다"는 판정은 타당.
- "1.5단계" 진단은 합리적.

설계상 약점 (Hermes가 일부만 지적):
1. **죽은 규칙**: CLAUDE.md / GEMINI.md / AGENTS.md가 `graphify-out/graph.json` 존재를 전제로 "graphify query first"를 지시하지만 해당 산출물이 없어 규칙 전체가 무효. 전제 없는 규칙은 에이전트 혼란을 유발하므로 조건부(`if exists`) 명시 또는 산출물 생성 중 하나로 정리 필요.
2. **경로 정체성 불일치 (가장 중요)**: 같은 vault가 세 가지 경로로 존재 — Drive(정본), Windows `G:/내 드라이브/Agent OS`(graphify-setup.md 기준), Linux `/opt/data/...`(Hermes 기준). 이를 묶는 단일 계약(env/manifest)이 없음. graphify-setup.md는 Windows 경로를, audit는 Linux 경로를 vault root로 부름.
3. **`.codex/hooks.json`이 Windows 경로(`C:\\Users\\user\\...\\graphify.EXE`)를 가리킴** — Linux Hermes 서버에서 작동 불가.
4. **"실시간 동기화" 목표의 과설계**: 정본=Drive + 주기적 pull/mirror 구조는 second brain 용도에 충분. 실시간 daemon은 현재 우선순위 대비 과투자. Hermes도 이를 P0가 아닌 후순위로 둔 점은 적절.

문서 계약 레이어(CLAUDE.md/AGENT-OS.md/Routing Table, "index이지 dump가 아니다")는 Karpathy 원칙에 잘 부합하며 설계의 강점.

## 3. 적용한 것 / 권고

적용 (이번 세션):
- Claude read-sync 라이브 검증 (audit, CLAUDE.md, dashboard-state.json 등 실제 파일 읽기 확인).
- Claude write-sync 검증: 이 파일을 Drive에 직접 생성 — Cowork Claude가 vault에 쓸 수 있음을 증명.

권고 (승인 필요 / 다음 단계):
- dashboard-state.json은 in-place 수정 불가 → 갱신이 필요하면 (a) update를 지원하는 Drive 연동으로 교체하거나, (b) 각 에이전트가 dated status 파일을 append하고 Hermes가 머지하는 구조로 변경.
- `.codex/hooks.json`의 Windows 경로를 환경 분기 처리.
- graphify: 실제 빌드는 토큰/API 비용 발생 → 형민 승인 후 진행. 그 전까지 graphify 규칙은 `if graphify-out exists` 조건부로 명시.
- 경로 정체성 통일: vault 정본은 Drive, 각 환경의 로컬 경로는 mirror임을 manifest 한 곳에 박기.

---
*이 문서 자체가 Cowork Claude -> Drive 쓰기 동기화의 증거다.*
