#!/usr/bin/env python3
"""
Background worker: reads JSONL transcript, calls `claude -p` to extract
PM knowledge, appends structured entry to knowledge/logs/YYYY-MM-DD.md.

Runs detached after session_hook.py spawns it. Uses `claude -p` (Claude Code
CLI print mode) — no separate API key required.
"""
import json
import os
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path


MAX_CHARS = 10_000  # truncate conversation to this before sending to Claude
MAX_TURNS = 40


def extract_conversation(transcript_path: str) -> str:
    turns = []
    try:
        with open(transcript_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    msg = entry.get("message", {})
                    role = msg.get("role", "")
                    content = msg.get("content", "")
                    if not role:
                        continue
                    if isinstance(content, list):
                        parts = [
                            b.get("text", "")
                            for b in content
                            if isinstance(b, dict) and b.get("type") == "text"
                        ]
                        content = " ".join(parts)
                    if content and isinstance(content, str):
                        turns.append(f"{role.upper()}: {content.strip()}")
                except Exception:
                    continue
    except Exception:
        return ""

    recent = turns[-MAX_TURNS:]
    text = "\n\n".join(recent)
    if len(text) > MAX_CHARS:
        text = text[-MAX_CHARS:]
    return text


def call_claude(conversation: str, cwd: str) -> str:
    time_str = datetime.now().strftime("%H:%M")
    prompt = f"""You are a project management analyst reviewing a Claude Code session.
Extract PM-relevant knowledge from the conversation below.

Output exactly these sections. Omit any section that has nothing to report.

### Session ({time_str}) - [one-line title of what was accomplished]

**Context:** [one sentence: what triggered this work]

**Changes Made:**
- [specific files or components changed]

**Decisions:**
- [decision with reasoning; note rejected alternatives if discussed]

**Patterns:**
- [new code conventions established, if any]

**Bugs & Gotchas:**
- [issues found or fixed, with root cause]

**Action Items:**
- [ ] [open item]

If nothing PM-relevant happened (purely exploratory chat, no code or decisions), output exactly:
NOTHING_TO_CAPTURE

CONVERSATION:
{conversation}"""

    env = os.environ.copy()
    env["CLAUDE_INVOKED_BY"] = "pm_capture"

    try:
        result = subprocess.run(
            ["claude", "-p", prompt],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=cwd,
            env=env,
        )
        return result.stdout.strip()
    except FileNotFoundError:
        # claude CLI not on PATH
        return ""
    except Exception:
        return ""


def append_to_log(entry: str, cwd: str):
    log_dir = Path(cwd) / "knowledge" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / f"{date.today().isoformat()}.md"

    if not log_file.exists():
        log_file.write_text(
            f"# Daily Log: {date.today().isoformat()}\n\n## Sessions\n\n"
        )

    with open(log_file, "a") as f:
        f.write(entry + "\n\n")


def main():
    transcript_path = os.environ.get("PM_TRANSCRIPT_PATH", "")
    cwd = os.environ.get("PM_PROJECT_CWD", ".")

    if not transcript_path:
        sys.exit(0)

    conversation = extract_conversation(transcript_path)
    if not conversation:
        sys.exit(0)

    entry = call_claude(conversation, cwd)

    if not entry or entry == "NOTHING_TO_CAPTURE":
        sys.exit(0)

    append_to_log(entry, cwd)


if __name__ == "__main__":
    main()
