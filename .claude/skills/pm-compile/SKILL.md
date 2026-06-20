---
name: pm-compile
description: Compile knowledge logs into structured PM articles for a project. Invoke when the user says /pm-compile, "compile the knowledge base", "update project knowledge", "organize what we've learned", "turn logs into articles", or "build the knowledge base". Also invoke when the user asks about patterns, decisions, or history and there are uncompiled logs but no index yet. Reads raw session logs from knowledge/logs/ and synthesizes them into organized concept articles covering features built, architecture decisions, patterns, bugs, and backlog items. Rebuilds knowledge/index.md so future sessions can query the knowledge base.
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# PM Knowledge Compile

Turn raw session logs into structured, cross-referenced knowledge articles.

## Why compile separately from capture

Capture is lightweight and happens often. Compile is a synthesis step — it looks across multiple sessions, spots patterns, merges related information, and produces articles that are useful to read in isolation. Running it after a few sessions gives Claude enough material to see recurring themes and write richer articles.

## Knowledge categories

Articles live in `knowledge/articles/{category}/`:

| Category | What goes here |
|----------|----------------|
| `features/` | Capabilities, modules, and functionality added to the project |
| `architecture/` | System-level decisions that constrain future work (tech stack, integrations, structure, tooling, config) |
| `patterns/` | Repeating conventions established in this project — naming, workflows, structural idioms, data flow |
| `bugs/` | Issues encountered, root causes, and fixes. Gotchas worth remembering. |
| `backlog/` | Open items, deferred work, ideas not yet started |

## Steps

1. Read `knowledge/index.md` if it exists — understand what's already been compiled so you don't duplicate it
2. List and read all files in `knowledge/logs/`
3. List and read all existing articles in `knowledge/articles/` (they may need updating)
4. For each distinct piece of knowledge found across the logs:
   - If an existing article already covers this topic → update it (add new information under `## Updates`)
   - If it's genuinely new → create a new article in the right category
5. Rebuild `knowledge/index.md` from scratch, listing every article with its one-line summary
6. Report what was created and what was updated

The goal is one article per concept, not one article per session. Prefer updating existing articles over creating near-duplicates.

## Article format

```markdown
---
title: "Descriptive Title"
category: architecture
slug: descriptive-title-kebab
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [relevant, tags]
summary: "One sentence that will appear in the index."
---

## Overview

[2-4 sentence explanation of this concept in this project's context]

## Key Points

- [Self-contained bullet per important fact]

## Details

[Deeper explanation when warranted — skip if Key Points is sufficient]

## Updates

### YYYY-MM-DD
[New information added in this compilation — keep earlier updates visible]
```

## Index format

`knowledge/index.md` is the master catalog — write it to be skimmable:

```markdown
# Project Knowledge Index
_Last compiled: YYYY-MM-DD_

## features
| Article | Summary | Updated |
|---------|---------|---------|
| [auth-flow](articles/features/auth-flow.md) | OAuth login flow with refresh token handling | 2026-06-09 |

## architecture
| Article | Summary | Updated |
|---------|---------|---------|
| [database-schema-decisions](articles/architecture/database-schema-decisions.md) | Chose denormalized schema for read performance over write simplicity | 2026-06-11 |

## patterns
...

## bugs
...

## backlog
...
```

Include all five category sections even if some are empty (just an empty table).
