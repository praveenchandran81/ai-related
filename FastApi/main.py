import os
import sys
import importlib.util

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.models import Product
from app.routers.products import router as products_router

MCP_FILE_PATH = "/Users/pc-mac-mini/Documents/MCPServer/server.py"
mcp = None

try:
    # Dynamically load the module directly from the file path.
    spec = importlib.util.spec_from_file_location("remote_mcp_module", MCP_FILE_PATH)
    remote_mcp_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(remote_mcp_module)

    # Extract the 'mcp' instance from the loaded file.
    mcp = getattr(remote_mcp_module, "mcp", None)
    if mcp is None:
        raise AttributeError

except FileNotFoundError:
    print(
        f"Warning: could not find your MCP file at '{MCP_FILE_PATH}'. "
        "The API will continue without MCP endpoints."
    )
except ModuleNotFoundError as exc:
    print(
        f"Warning: optional MCP dependency missing ({exc}). "
        "The API will continue without MCP endpoints."
    )
except AttributeError:
    print(
        f"Warning: the file at '{MCP_FILE_PATH}' does not define a valid 'mcp' object. "
        "The API will continue without MCP endpoints."
    )

app = FastAPI(title="Praveen FastAPI")

if mcp is not None and hasattr(mcp, "http_app"):
    print(f"MCP support enabled from '{MCP_FILE_PATH}'.")
    app.mount("/mcp", mcp.http_app())
else:
    print(
        "MCP support is disabled because the external server could not be loaded. "
        "Install the required package in that project before enabling /mcp."
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


app.include_router(products_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "FastAPI Product API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
