#!/usr/bin/env python3
"""
SessionEnd hook — fires when a Claude Code session closes.
Spawns flush.py as a detached background process so the session
can close immediately without waiting for the Claude CLI call.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

# Recursion guard: flush.py calls `claude -p`, which would re-fire this hook.
# CLAUDE_INVOKED_BY being set means we're inside that sub-invocation — skip.
if os.environ.get("CLAUDE_INVOKED_BY"):
    sys.exit(0)

try:
    data = json.loads(sys.stdin.read())
except Exception:
    sys.exit(0)

transcript_path = data.get("transcript_path", "")
cwd = data.get("cwd", ".")
session_id = data.get("session_id", "")

if not transcript_path or not Path(transcript_path).exists():
    sys.exit(0)

env = os.environ.copy()
env["CLAUDE_INVOKED_BY"] = "pm_capture"
env["PM_TRANSCRIPT_PATH"] = transcript_path
env["PM_PROJECT_CWD"] = cwd
env["PM_SESSION_ID"] = session_id

flush_script = Path(__file__).parent / "flush.py"

subprocess.Popen(
    [sys.executable, str(flush_script)],
    env=env,
    stdin=subprocess.DEVNULL,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    start_new_session=True,  # detach fully (POSIX); Windows: use creationflags
)
