#!/usr/bin/env python3
"""
Multi-MCP Hub Entrypoint for Knowledge Tree System
"""
import os
import sys
from pathlib import Path

# Add project root to sys.path
MCP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = MCP_DIR.parent
if str(MCP_DIR) not in sys.path:
    sys.path.insert(0, str(MCP_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from servers.kt_server import kt_mcp
from servers.system_server import sys_mcp

# 1. Main Hub Instance
hub = FastMCP("KnowledgeTreeHub")

# 2. Mount Sub-MCP Servers with Namespaces
hub.mount(kt_mcp, namespace="kt")
hub.mount(sys_mcp, namespace="sys")

# 3. Custom Health Endpoint
@hub.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    return JSONResponse({
        "status": "healthy",
        "service": "Multi-MCP Hub Server",
        "version": "0.2.0",
        "mounted_servers": ["kt", "sys"]
    })

# 4. Entrypoint
if __name__ == "__main__":
    transport = os.getenv("FASTMCP_TRANSPORT", "stdio").lower()
    host = os.getenv("FASTMCP_HOST", "0.0.0.0")
    port = int(os.getenv("FASTMCP_PORT", "8000"))
    
    if transport in ("http", "sse", "streamable-http"):
        print(f"🚀 Running Multi-MCP Hub Server via {transport.upper()} on {host}:{port}")
        hub.run(transport="http", host=host, port=port)
    else:
        hub.run()
