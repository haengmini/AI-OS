#!/usr/bin/env bash
set -euo pipefail
exec /usr/bin/env python3 /opt/data/scripts/agent_dashboard_snapshot.py "$@"
