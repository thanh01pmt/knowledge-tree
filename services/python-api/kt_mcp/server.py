#!/usr/bin/env python3
"""
Backward compatibility proxy for kt_mcp/main.py.

Note: The package was renamed from mcp/ to kt_mcp/ to avoid namespace
collision with the `mcp` PyPI SDK. This proxy keeps `python mcp/server.py`
working for legacy callers by importing from the new location.
"""
import sys
from pathlib import Path

PKG_DIR = Path(__file__).parent.resolve()
if str(PKG_DIR) not in sys.path:
    sys.path.insert(0, str(PKG_DIR))

from main import hub as mcp

if __name__ == "__main__":
    mcp.run()