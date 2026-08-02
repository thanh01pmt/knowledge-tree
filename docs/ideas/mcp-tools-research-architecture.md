# Architecture Ideas: MCP Tools & Research Collection

*Captured: 2026-08-02*

## Core Problem
How to expose granular research capabilities (SearXNG, Crawl4AI, last30days, crosswalk) as MCP tools while supporting both:
- **Scheduled cron collectors** (deterministic, write to `.work/` on source of truth)
- **Agent-driven research** (adaptive, may run on any machine)

## Key Architectural Decisions

### 1. MCP Server in Repo = Zero-Config Agent Tooling
```
Any machine: git clone → python kt_mcp/main.py (stdio) → gets tools
```
- Works for Claude Desktop, Cursor, Pi, custom agents
- No hosted MCP server needed for local agents
- Agent's clone has its own `.work/` → commits back

### 2. Three Deployment Modes
| Mode | Transport | Filesystem | Use Case |
|------|-----------|------------|----------|
| Local Agent | stdio (subprocess) | Agent's clone | Ad-hoc research |
| Cron/Collectors | Direct script + subprocess | Source of truth | Scheduled collection |
| Remote Agent | HTTP (container) | Shared volume | Team/remote access |

### 3. Tool Design: Return Data, Not Files
```python
@research_mcp.tool
def last30days_trends(query: str) -> dict:
    # Run research
    # Return structured data + file content for caller to persist
    return {"trends": [...], "files": [{"path": "...", "content": "..."}]}
```
- **Cron**: Writes returned files to source of truth
- **Local Agent**: Writes to its clone → commits
- **Remote Agent**: Gets data → writes via its own tools

### 4. Current kt_mcp Structure (services/python-api/kt_mcp/)
```
kt_mcp/
├── main.py                    # Multi-MCP Hub (FastMCP)
├── servers/
│   ├── kt_server.py           # Namespace: kt (tree ops)
│   ├── system_server.py       # Namespace: sys
│   └── research_server.py     # Namespace: research (CURRENT: 2 tools)
```

**Current research_server.py tools:**
- `audit_curriculum(framework)` → runs `audit_curriculum.py`
- `watch_trends(query)` → runs `auto_stem_discovery.py`

**Needed granular tools:**
- `searxng_search(query)` → direct HTTP to SearXNG
- `crawl4ai_extract(url)` → direct HTTP to Crawl4AI
- `last30days_trends(query)` → subprocess `last30days.py` → returns queue
- `crosswalk_analyze(reference, compare)` → subprocess `curriculum_crosswalk.py`

### 5. Cron Collectors Stay As-Is (Subprocess Pattern)
```python
# run_collectors.py → auto_stem_discovery.py (subprocess, cwd=ROOT_DIR)
# Writes directly to .work/research/ on source of truth
# No MCP involvement for scheduled runs
```

### 6. MCP Tools for Agent Use Only
- Agents call granular tools for adaptive research
- Cron uses full scripts for deterministic collection
- Both use same underlying services/scripts

## Implementation Plan

1. **Extend `research_server.py`** with 4 granular tools
2. **Tools return structured data** (not write files)
3. **Keep cron collectors unchanged** (they work)
4. **Test agent tool access** via stdio

## Questions for Later

- [ ] Should crosswalk tools expose convergence CSV as downloadable artifact?
- [ ] How to handle auth headers (CF_ACCESS) in MCP tool context?
- [ ] Rate limiting for SearXNG/Crawl4AI when multiple agents call?
- [ ] Should we add a `research_deep_dive` tool that chains search→crawl→analyze?

## Related Files
- `/services/python-api/kt_mcp/servers/research_server.py` (to extend)
- `/services/python-api/kt_mcp/main.py` (hub entrypoint)
- `/.agents/cron/collectors/` (cron collectors - unchanged)
- `/.agents/skills/knowledge-researcher/scripts/auto_stem_discovery.py` (underlying script)
- `/.agents/skills/knowledge-researcher/scripts/curriculum_crosswalk.py` (underlying script)