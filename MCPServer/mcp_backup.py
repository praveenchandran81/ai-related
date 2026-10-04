#!/usr/bin/env python3
import importlib.util
import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE_DIR = Path(__file__).resolve().parent
for bad in ["", ".", str(WORKSPACE_DIR), os.getcwd(), str(Path.cwd())]:
    while bad in sys.path:
        sys.path.remove(bad)

spec = importlib.util.spec_from_file_location("mcp_server_main", WORKSPACE_DIR / "main.py")
if spec is None or spec.loader is None:
    raise RuntimeError("Could not load main.py")

module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

mcp = module.mcp

if __name__ == "__main__":
    log_dir = WORKSPACE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    banner = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] mcp server is listening"
    print(banner, file=sys.__stderr__, flush=True)
    with (log_dir / "mcp_server.log").open("a", encoding="utf-8") as log_file:
        log_file.write(banner + "\n")
    mcp.run()
