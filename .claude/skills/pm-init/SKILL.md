---
name: pm-init
description: Initialize a project's knowledge base scaffold and generate a CLAUDE.md. Invoke when the user says /pm-init, "initialize knowledge base", "set up the knowledge base", "init this project", "scaffold pm", or "bootstrap pm". Scans the current project to understand its purpose, tech stack, and structure, then creates the knowledge/ directory tree and writes (or updates) CLAUDE.md at the project root so the pm-capture, pm-compile, and pm-query skills have somewhere to work.
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# PM Init

Bootstrap the knowledge base for a project that doesn't have one yet.

## Why this exists

The other pm-* skills assume `knowledge/` exists and `CLAUDE.md` is present. Without them, pm-capture has nowhere to write and Claude starts each session cold with no project context. Run pm-init once per project to eliminate that cold-start problem.

## Steps

### 1. Understand the project

Gather context by reading whatever exists:

- `README.md` or `README` — primary source for project purpose and setup instructions
- Package manifest — `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile`, `composer.json`, or `*.csproj` — reveals language, framework, dependencies
- Run `git log --oneline -10` to get a sense of recent work and project maturity
- Run `ls -1` (or `find . -maxdepth 2 -not -path './.git/*' -not -path './node_modules/*'`) to see top-level structure
- Spot check 1-2 key source files if the stack isn't clear from the manifest

Don't over-read — enough to write accurate CLAUDE.md sections, not a full audit.

### 2. Check what already exists

- If `knowledge/` already exists: note it, skip creation for directories that exist, still create any missing subdirectories
- If `CLAUDE.md` already exists: read it, then add a `## Knowledge Base` section if one isn't already there — do not overwrite existing content

### 3. Create the knowledge directory tree

Create these directories (use `mkdir -p`):

```
knowledge/logs/
knowledge/articles/features/
knowledge/articles/architecture/
knowledge/articles/patterns/
knowledge/articles/bugs/
knowledge/articles/backlog/
```

Write a `.gitkeep` file in each leaf directory so the structure is tracked by git even when empty.

### 4. Write or update CLAUDE.md

**If CLAUDE.md does not exist**, create it with this structure:

```markdown
# CLAUDE.md

## Project

[1-2 sentences describing what this project does and who it's for]

## Stack

- [language and runtime version if known]
- [framework]
- [key libraries worth knowing]

## Entry Points

- **Run:** `[command to start/run the app]`
- **Test:** `[test command]`
- **Build:** `[build command if applicable]`

## Conventions

- [Any patterns visible in the code or README — naming, file structure, testing approach]
- If nothing is established yet, omit this section rather than padding it

## Knowledge Base

This project uses the pm-* skill suite for session knowledge management:
- `/pm-capture` — run at the end of any session with meaningful changes to log decisions and context
- `/pm-compile` — run periodically to synthesize logs into searchable articles
- `/pm-query` — ask questions about past decisions, patterns, or backlog items
```

**If CLAUDE.md already exists**, append only the `## Knowledge Base` section above (if it isn't there already). Do not touch any existing content.

Fill each section with what you actually found — don't write placeholder text like "[framework]" into the file. If a section genuinely has nothing (e.g. no build step), omit it.

### 5. Report

Tell the user:
- What was created (list directories, confirm CLAUDE.md written/updated)
- What to do next: "Run `/pm-capture` at the end of sessions, `/pm-compile` after a few sessions to build the index, then `/pm-query` to recall decisions."
- If anything was skipped (e.g. knowledge/ already existed), say so

Keep the report brief — one short paragraph or a small list.
