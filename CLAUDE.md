# CLAUDE.md — 에이전트 진입점

> 이 폴더에서 작업할 때 가장 먼저 읽는 라우팅 파일. **짧게 유지한다.**
> 규칙·정체성·구조의 정본은 `README.md` 하나다. 여기엔 라우팅만.

## 먼저 읽을 것
```text
README.md  → 정체성·사명·운영규칙·구조 (단일 정본). 세션 시작 시 필수.
```

## 어디서 읽고 어디에 쓰는가
```text
재사용 지식(위키)        → 02-memory/  (진입점: 02-memory/index.md)   READ + WRITE(승격분만)
실제 프로젝트·산출물      → 06-production/<project>/                    READ + WRITE
라이브 상태·UI           → 05-dashboard/ (state JSON, situation-room)  READ + WRITE
옛 메타 문서·중복·로그    → _archive/                                  (구조에서 제외)
Codex 계약              → AGENTS.md                                   READ
```

## 핵심 규칙 (정본: README §5)
```text
1. 미검증을 "완료"로 처리하지 않는다. 검증 수단을 함께 설계한다.
2. Ponytail: 만들 필요 없음 → 재사용 → stdlib → native → one-line → 최소 구현.
3. 위험 작업(삭제·대량이동·git push·external upload·API key·sudo)은 사용자 승인 후.
4. 언어: 설명·보고는 한국어, 코드·명령·파일명은 영어.
5. 모든 작업 완료 후에는 반드시 GitHub, Google Drive, Notion 에 관련 기록을 커밋 및 업데이트하여 동기화한다.
```
