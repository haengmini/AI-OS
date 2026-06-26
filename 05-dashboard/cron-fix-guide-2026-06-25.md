# cron 실패 3건 — 진단·수정 가이드 (WSL에서 실행)

> 이 세션의 Claude는 WSL(`/opt/data/...`)에 접근하지 못한다. 아래는 **원인을 단정하지 않고**,
> 가능 원인별로 재현→확인→수정 커맨드를 정리한 것. 당신 또는 Codex가 WSL에서 실행한다.
> 원칙(README §5): 미검증 수정 금지 — **로그로 원인을 먼저 확인한 뒤** 고친다.

## 공통 1단계 — 진짜 에러부터 본다
```bash
# 각 작업의 마지막 실행 로그를 직접 본다 (cron 요약 말고 원문)
ls -la /opt/data/logs 2>/dev/null
journalctl --user -u '*' --since "1 day ago" 2>/dev/null | tail -50
# 또는 cron 래퍼가 로그를 남기는 위치
grep -rl "Permission denied\|429" /opt/data/logs 2>/dev/null
```
"Permission denied"가 **어느 경로**에서 났는지가 핵심이다. 그 경로를 P로 두고 아래로.

---

## [P0] agent-os-drive-daily-archive — Permission denied
가능 원인 순서대로:

1. **cron 실행 유저 ≠ 파일 소유자** (가장 흔함). cron이 root나 다른 유저로 도는데 대상이 사용자 소유.
```bash
# 스크립트가 어떤 유저로 도는지 / 대상 권한
stat -c '%U %G %a %n' /opt/data/agent_os_archive /opt/data/scripts/agent_os_drive_archive.sh
crontab -l | grep -i drive          # 사용자 crontab
sudo crontab -l | grep -i drive     # root crontab
# 수동으로 사용자 권한에서 재현
bash -x /opt/data/scripts/agent_os_drive_archive.sh 2>&1 | tail -30
```
→ 유저 불일치면: cron을 **사용자 crontab으로 이동**하거나, 대상 디렉터리에 그룹 권한 부여
   (`chmod -R g+rw`, 같은 그룹 편입). rclone/gdrive 토큰이 특정 홈(`~/.config/rclone`)에 있으면
   그 홈을 쓰는 유저로 실행해야 한다.

2. **Drive remote(rclone/gdrive) 토큰 만료/스코프**. "Permission denied"가 로컬 fs가 아니라 원격에서 났을 수도.
```bash
rclone listremotes 2>/dev/null && rclone about <remote>: 2>&1 | tail
# 토큰 만료면 재인증 (브라우저 필요)
rclone config reconnect <remote>:
```

3. **마운트 미존재**. 대상 마운트가 cron 환경엔 없을 때.
```bash
mountpoint -q /opt/data/agent_os_archive && echo mounted || echo "NOT mounted"
```

---

## [P0] graphify-staleness-check — Permission denied
graphify 산출물 경로 불일치가 같이 의심된다 (문서마다 `/opt/data/...` vs `graphify-out/` 으로 다름).
```bash
# graph 산출물이 실제 어디 있는지부터
find /opt/data -name graph.json 2>/dev/null
find /opt/data -path '*graphify-out*' -maxdepth 4 2>/dev/null | head
stat -c '%U %G %a %n' $(find /opt/data -name graph.json 2>/dev/null | head -1)
# 수동 재현
bash -x /opt/data/scripts/*graphify*staleness* 2>&1 | tail -30
```
→ 원인이 권한이면 위 drive-archive와 동일 처방(유저/그룹 일치).
→ 원인이 "파일 없음"이면 staleness check 대상 경로를 실제 graph.json 위치로 **한 곳으로 통일**.
  (정본 경로를 하나 정하고 README/CLAUDE의 graphify 언급을 그 경로로 맞춘다.)

---

## [P1] slack-channel-daily-archive — HTTP 429
429 = rate/usage 초과. **출처를 먼저 특정**한다 (Slack API인지, LLM(Anthropic) 사용량 cap인지).
```bash
grep -i "429\|rate limit\|Retry-After\|usage" /opt/data/logs/*slack* 2>/dev/null | tail
```
- **Slack API 429**: `Retry-After` 헤더 존중 + 페이지네이션 backoff. 채널 전체를 한 번에 긁지 말고 분할.
- **LLM 사용량 429**: 매일 채널 전체 요약이 과한 호출. 처방:
  - 빈도 낮추기 (daily → weekly), 또는
  - 요약 범위 축소 (신규 메시지 delta만), 또는
  - 임시 비활성 후 v0.2로 미룸 (현재 deferred 처리됨).
```bash
# 임시 저빈도화 예: daily → weekly (월요일 0시)
crontab -l | sed 's#.*slack-channel.*daily.*#0 0 * * 1 /opt/data/scripts/slack_archive.sh weekly#' | crontab -
# 또는 임시 비활성 (라인 주석)
crontab -l | sed '/slack-channel.*daily-archive/s/^/#/' | crontab -
```

---

## 완료 판정 (검증 수단)
```text
[ ] drive-archive: 수동 실행이 0 exit + Drive에 오늘자 아카이브 생성됨
[ ] graphify-staleness: 수동 실행이 0 exit + graph.json mtime 확인 출력
[ ] slack: 다음 실행에서 429 미발생(또는 비활성 확정)
[ ] 위 3개 반영 후 build_dashboard.py 재실행 → hq-dashboard.html cron 카드가 녹색으로
```
> 수정은 한 번에 하나씩(small diff), 각 단계 후 수동 재현으로 검증. 권한·토큰 변경은 위험작업이므로
> 실제 적용 전 무엇을 바꾸는지 먼저 확인.
