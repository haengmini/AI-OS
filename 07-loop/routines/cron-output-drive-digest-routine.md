# Cron Output Drive Digest Routine

- Canonical location: Google Drive `Agent OS/07-loop/routines/cron-output-drive-digest-routine.md`
- Local cache: `/opt/data/agent_os_archive/files/07-loop/routines/cron-output-drive-digest-routine.md`
- Owner: `admin` + `sentinel`
- Status: design v0.1, ready for implementation
- Updated: 2026-06-22

## 1. Problem

Hermes cron jobs currently write useful operational evidence under local paths such as:

```text
/opt/data/cron/output/<job_id>/<timestamp>.md
/opt/data/agent_os_archive/summaries/daily/YYYY-MM-DD.md
/opt/data/slack_channel_archive/C0BA8DR4VV1.md
```

These files are useful but local-first. 이형민's Agent OS rule is Drive-first:

```text
Google Drive = canonical/original store
Local /opt/data = cache/staging/mirror
```

Therefore cron outputs need a Drive digest/index so Claude, Gemini, Hermes, and other devices can inspect operational history from the shared workspace.

## 2. Goal

Create a deterministic no-agent routine that:

1. scans recent `/opt/data/cron/output` files,
2. summarizes metadata without invoking an LLM,
3. writes a daily Markdown digest locally,
4. uploads/upserts the digest into Drive,
5. records the Drive ID/link in `artifact-registry.json`,
6. optionally posts a short Slack alert only on failures or notable blockers.

## 3. Canonical Drive placement

Recommended Drive locations:

```text
Agent OS/07-loop/routines/cron-output-drive-digest-routine.md   # this design/runbook
Agent OS/07-loop/reports/cron-output-digest/YYYY-MM-DD.md       # daily digest output, create folder if approved/available
Agent OS/05-dashboard/situation-room/state/artifact-registry.json
Agent OS/05-dashboard/situation-room/docs/situation-board.md
```

If `07-loop/reports/` does not yet exist, use one of these options:

- Preferred: create `07-loop/reports/cron-output-digest/` in Drive.
- Conservative fallback: place daily digest files under `05-dashboard/situation-room/docs/cron-output-digest-YYYY-MM-DD.md` until the reports folder exists.

## 4. Input sources

```text
/opt/data/cron/jobs.json
/opt/data/cron/output/*/*.md
/opt/data/agent_os_archive/summaries/agent-team/status.json
/opt/data/agent_os_archive/summaries/daily/YYYY-MM-DD.md
/opt/data/agent_os_archive/manifest.json
```

## 5. Output schema

Daily digest Markdown:

```md
# Cron Output Digest — YYYY-MM-DD

## Summary
- jobs_checked:
- outputs_found:
- failures:
- stale_jobs:
- drive_sync_status:

## Job outputs
| job_id | name | last_status | output_file | modified_at | drive_link |
|---|---|---|---|---|---|

## Notable changes

## Blockers / human attention

## Verification
- generated_at:
- local_cache:
- drive_file_id:
```

Optional machine state JSON:

```json
{
  "date": "YYYY-MM-DD",
  "generated_at": "ISO-8601",
  "jobs_checked": 4,
  "outputs_found": 4,
  "failures": [],
  "stale_jobs": [],
  "digest_drive_file_id": "...",
  "digest_drive_link": "..."
}
```

## 6. Script design

Script path:

```text
/opt/data/scripts/cron_output_drive_digest.py
/opt/data/scripts/cron_output_drive_digest.sh
```

Behavior:

1. Load `cron/jobs.json`.
2. For each job, find the newest file in `/opt/data/cron/output/<job_id>/`.
3. Extract first heading and first 10-20 non-empty lines as preview.
4. Detect failure words: `ERROR`, `Traceback`, `failed`, `non-zero`, `blocked`.
5. Write local digest to:

```text
/opt/data/agent_os_archive/files/07-loop/reports/cron-output-digest/YYYY-MM-DD.md
```

6. Upsert digest to Drive.
7. Update `artifact-registry.json` with:
   - artifact_id: `cron-output-digest-YYYY-MM-DD`
   - owner_agent: `sentinel`
   - type: `cron_digest`
   - Drive ID/link
   - local cache path
8. Print concise one-line stdout:

```text
Cron output digest complete date=YYYY-MM-DD jobs=4 failures=0 drive_file_id=...
```

## 7. Cron schedule

Recommended order:

```text
23:50 Drive archive sync
00:00 Slack/session archive
00:05 Cron output Drive digest
09:10 Agent team healthcheck
```

Proposed Hermes cron job:

```yaml
name: cron-output-drive-digest
schedule: 5 0 * * *
script: cron_output_drive_digest.sh
no_agent: true
deliver: local
```

Rationale:
- script-only/no_agent avoids model cost
- local delivery prevents Slack noise
- stdout can remain concise
- non-zero exit still alerts via cron failure handling

## 8. Approval and safety

Allowed without extra approval when user has asked to proceed:

- read local cron outputs
- create/update Drive Markdown digest under Agent OS
- create/update local cache files
- create/update artifact registry
- create/modify this cron job under default profile

Still requires explicit approval:

- deleting local cron outputs
- deleting/moving existing Drive files/folders
- changing Drive sharing/permissions
- changing credentials/tokens/API scopes
- publishing outside the private Drive/Slack workspace

## 9. Implementation checklist

- [ ] Ensure Drive folder `07-loop/reports/cron-output-digest` exists or choose fallback.
- [ ] Create deterministic Python script.
- [ ] Create shell wrapper.
- [ ] Test one foreground run.
- [ ] Verify Drive file ID/link.
- [ ] Register artifact.
- [ ] Create no_agent cron job at `5 0 * * *`.
- [ ] Add digest link to Situation Room.

## 10. Current baseline jobs

Observed default-profile cron jobs:

| name | schedule | role |
|---|---|---|
| agent-os-drive-daily-archive | `50 23 * * *` | Drive archive sync |
| slack-channel-C0BA8DR4VV1-daily-archive | `0 0 * * *` | Slack/session archive |
| agent-team-healthcheck | `10 9 * * *` | team/system health |
| project-weekly-review | every `2880m` | portfolio review |
