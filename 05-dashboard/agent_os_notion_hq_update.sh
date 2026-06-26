#!/usr/bin/env bash
set -euo pipefail
exec /opt/data/.venvs/google-workspace/bin/python /opt/data/scripts/agent_os_notion_hq_update.py "$@"
