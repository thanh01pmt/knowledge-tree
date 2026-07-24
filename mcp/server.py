#!/usr/bin/env python3
"""
Backward compatibility proxy for mcp/main.py
"""
from mcp.main import hub as mcp

if __name__ == "__main__":
    mcp.run()
