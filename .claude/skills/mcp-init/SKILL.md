---
name: mcp-init
description: Install the MCP wrapper script and regenerate the git-ignored .mcp.json and .claude/settings.local.json for the current project. Invoke when the user says /mcp-init, "mcp", "setup mcp", "install mcp", "configure mcp", "mcp servers", or anything mentioning MCP setup or configuration. Also invoke automatically at the end of pm-init.
allowed-tools: [Bash, Read, Write, Edit]
---

# MCP Setup

Sets up MCP servers for the current project. Works in any repo.

## Steps

### 1. Install `~/.claude/start-memory.sh` (idempotent)

Check if `$HOME/.claude/start-memory.sh` exists. If not, write it:

```sh
#!/bin/sh
MEMORY_FILE_PATH="$(dirname "$0")/memory.jsonl" \
  npx -y @modelcontextprotocol/server-memory
```

Then `chmod +x "$HOME/.claude/start-memory.sh"`.

### 2. Resolve paths

Run `pwd` to get the absolute project path. Use `$HOME` for the memory script path. Never use `~` inside JSON values — it won't be expanded by all launchers.

### 3. Write `.mcp.json` in the current directory

Always overwrite with all 10 servers. Substitute real resolved values for HOME and PWD — do not write placeholders:

```json
{
  "mcpServers": {
    "sequential-thinking": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"] },
    "deepWiki":            { "command": "npx", "args": ["-y", "mcp-remote", "https://mcp.deepwiki.com/mcp"] },
    "fetch":               { "command": "uvx", "args": ["mcp-server-fetch"] },
    "git":                 { "command": "uvx", "args": ["mcp-server-git"] },
    "filesystem":          { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "<resolved-pwd>"] },
    "memory":              { "command": "sh",  "args": ["<resolved-home>/.claude/start-memory.sh"] },
    "time":                { "command": "uvx", "args": ["mcp-server-time"] },
    "context7":            { "command": "npx", "args": ["-y", "@upstash/context7-mcp"] },
    "playwright":          { "command": "npx", "args": ["@playwright/mcp@latest"] },
    "duckduckgo":          { "command": "uvx", "args": ["duckduckgo-mcp-server"] }
  }
}
```

### 4. Update `.claude/settings.local.json`

Read the file if it exists. Set or replace `enabledMcpjsonServers` with all 10 server names. Preserve all other existing keys (hooks, permissions, etc).

If the file does not exist, create `.claude/settings.local.json`:

```json
{
  "enabledMcpjsonServers": [
    "sequential-thinking", "deepWiki", "fetch", "git",
    "filesystem", "memory", "time", "context7", "playwright", "duckduckgo"
  ]
}
```

### 5. Report

Tell the user:
- Whether the memory script was freshly installed or already existed
- That `.mcp.json` was written with 10 servers, with filesystem pointing to the resolved project path
- That `settings.local.json` was updated
- To **restart Claude Code** to pick up the changes
