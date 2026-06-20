---
name: pm-query
description: Query the project knowledge base to recall decisions, patterns, bugs, or backlog items. Invoke when the user says /pm-query, "what do we know about X", "what did we decide about Y", "what patterns do we use for Z", "what's on the backlog", "remind me why we did X", or asks a question that sounds like it might be answered by accumulated project knowledge. Also invoke proactively when the user asks about a past decision or convention and the knowledge/index.md file exists in the project — don't make up an answer when the knowledge base might have the real one. Requires knowledge/index.md to exist; suggest /pm-compile if it doesn't.
allowed-tools: [Read, Glob]
---

# PM Knowledge Query

Answer questions using the project knowledge base in `knowledge/`.

## The approach

Don't search by keyword — read the index to understand what knowledge exists, then read the articles most likely to contain the answer in full. This produces synthesized answers rather than grep matches.

## Steps

1. Check that `knowledge/index.md` exists
   - If not: tell the user to run `/pm-compile` first (and `/pm-capture` if there are no logs yet)
2. Read `knowledge/index.md` — scan the summaries for what's relevant to the question
3. Pick 2-6 articles whose summaries suggest they cover the topic; read them in full
4. Synthesize a direct answer, noting which articles informed it
5. If the knowledge base genuinely doesn't have enough to answer the question, say so clearly — don't invent. Suggest running `/pm-capture` during the session where this was originally discussed, then `/pm-compile`.

## Category shortcuts

- "what's on the backlog?" → read all files in `knowledge/articles/backlog/`
- "what patterns do we use?" → start with `knowledge/articles/patterns/`
- "why did we do X?" / "what was the decision about Y?" → start with `knowledge/articles/architecture/`
- "what did we build?" → start with `knowledge/articles/features/`
- "what bugs should I know about?" → start with `knowledge/articles/bugs/`

## Answer format

Lead with the direct answer. Then cite sources:

> **From [article-title](articles/architecture/article-title.md):** [key quote or paraphrase]

If the question spans multiple articles, synthesize across them rather than quoting each in isolation. The user asked a question, not for a reading list.
