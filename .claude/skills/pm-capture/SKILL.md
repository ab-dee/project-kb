---
name: pm-capture
description: Capture project management knowledge from the current Claude Code session into a structured daily log. Invoke when the user says /pm-capture, "capture what we did", "save this session", "log this to the knowledge base", "save our decisions", or "what should I remember from today". Also invoke when wrapping up a session where significant work, decisions, or discoveries happened — even if the user doesn't explicitly ask. Extracts decisions made, features built, patterns established, bugs found, and open action items from the current conversation and recent git history, then writes a structured entry to knowledge/logs/YYYY-MM-DD.md in the project root.
allowed-tools: [Read, Write, Bash, Glob]
---

# PM Knowledge Capture

Save what happened in this session so it isn't lost when the conversation ends.

## Why this matters

The real value of a working session isn't just the output — it's the reasoning, the tradeoffs weighed, the alternatives rejected, and the gotchas discovered. Version control captures *what* changed; this skill captures *why* and *what we learned*.

## What to look for

Work through the current conversation and recent git history to find:

- **Context**: What problem or goal triggered this session
- **Changes Made**: What was actually built or modified (specific files, modules, configs, scripts)
- **Decisions**: Architectural or design choices with their reasoning. If alternatives were considered and rejected, note that too — it prevents relitigating the same decision later.
- **Patterns**: Any new code conventions, naming idioms, or structural approaches established in this session
- **Bugs & Gotchas**: Issues encountered or fixed, with root cause if known
- **Action Items**: Open TODOs, deferred work, follow-ups the user mentioned

If a section has nothing to report, omit it rather than writing "N/A". A shorter, accurate entry beats a padded one.

## Steps

1. If the project uses git, run `git log --oneline -10` and `git diff HEAD~1 --stat` to see recent changes
2. Review the current conversation for PM-relevant content
3. If nothing meaningful happened (purely exploratory chat, no code or decisions), say so and don't write an entry
4. Determine today's date for the filename
5. Create `knowledge/logs/` if it doesn't exist
6. Append the entry to `knowledge/logs/YYYY-MM-DD.md`

## Entry format

Append this to the log file (create the file with the header if it's the first entry today):

```
### Session (HH:MM) - [One-line title of what was accomplished]

**Context:** [One sentence: what triggered this work]

**Changes Made:**
- [Each meaningful change, referencing specific files, modules, or scripts]

**Decisions:**
- [Decision with reasoning]
- [Rejected alternative and why it was ruled out]

**Patterns:**
- [New convention established, if any]

**Bugs & Gotchas:**
- [Issue found or fixed, with root cause]

**Action Items:**
- [ ] [Open item]
```

## File structure

If `knowledge/logs/YYYY-MM-DD.md` doesn't exist yet:

```markdown
# Daily Log: YYYY-MM-DD

## Sessions

[entry goes here]
```

If it already exists, just append the new session entry under `## Sessions`.
