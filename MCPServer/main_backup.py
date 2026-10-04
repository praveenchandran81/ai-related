#!/usr/bin/env python3
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE_DIR = str(Path(__file__).resolve().parent)
for bad in ["", ".", WORKSPACE_DIR, os.getcwd(), str(Path.cwd())]:
    while bad in sys.path:
        sys.path.remove(bad)

import httpx
from mcp.server import MCPServer

BASE_URL = os.getenv("FASTAPI_BASE_URL", "http://localhost:8000")
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "mcp_server.log"

logger = logging.getLogger("mcp_server")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(file_handler)

    stderr_handler = logging.StreamHandler(sys.__stderr__)
    stderr_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(stderr_handler)

mcp = MCPServer("fastapi-products")


def _log_request(tool_name: str, payload: dict | None = None, status: str = "start") -> None:
    payload = payload or {}
    logger.info("tool=%s action=%s payload=%s", tool_name, status, payload)


@mcp.tool()
def getproducts() -> dict:
    """Fetch all products from the local FastAPI app."""
    _log_request("getproducts")
    try:
        response = httpx.get(f"{BASE_URL}/products", timeout=20.0)
        response.raise_for_status()
        result = {
            "status_code": response.status_code,
            "url": f"{BASE_URL}/products",
            "data": response.json(),
        }
        _log_request("getproducts", {"status_code": response.status_code}, "success")
        return result
    except Exception as exc:
        logger.exception("getproducts failed")
        raise


@mcp.tool()
def create_product(
    product: dict | None = None,
    name: str | None = None,
    description: str = "",
    price: str | int | float | None = None,
) -> dict:
    """Create a product using the local FastAPI app."""
    payload = product.copy() if isinstance(product, dict) else {}
    if name is not None:
        payload["name"] = name
    if description:
        payload["description"] = description
    if price is not None:
        payload["price"] = price

    _log_request("create_product", payload)
    try:
        response = httpx.post(f"{BASE_URL}/products", json=payload, timeout=20.0)
        response.raise_for_status()
        result = {
            "status_code": response.status_code,
            "url": f"{BASE_URL}/products",
            "request": payload,
            "response": response.json(),
        }
        _log_request("create_product", {"status_code": response.status_code, "request": payload}, "success")
        return result
    except Exception:
        logger.exception("create_product failed")
        raise


if __name__ == "__main__":
    banner = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] mcp server is listening on stdio"
    print(banner, file=sys.__stderr__, flush=True)
    logger.info("mcp server is listening on stdio")
    mcp.run()
