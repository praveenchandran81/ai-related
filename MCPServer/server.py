import logging
from typing import Annotated
import httpx
from pydantic import Field
from fastmcp import FastMCP
import uvicorn




logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_worker")

mcp = FastMCP("MCP Server with products and addition tools")

FASTAPI_BASE_URL = "http://localhost:8000"

@mcp.tool()
async def list_all_products() -> str:
    """
    List all products from the FastAPI server.
    
    Returns:
        string: A formatted string containing the list of products.
    """
    logger.info("Fetching all products from FastAPI server")
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{FASTAPI_BASE_URL}/products",timeout=10.0)
        response.raise_for_status()
        products = response.json()
        product_list = "\n".join([f"ID: {product['id']}, Name: {product['name']}, Price: {product['price']}" for product in products])
        return f"List of Products:\n{product_list}"

@mcp.tool()
async def create_product(name: str, description: str, price: float) -> str:
    """
    Create a new product on the FastAPI server.
    
    Args:
        name (str): The name of the product.
        description (str): The description of the product.
        price (float): The price of the product.
    
    Returns:
        string: A message indicating the result of the operation.
    """
    logger.info(f"Creating product with name: {name}, description: {description}, price: {price}")
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{FASTAPI_BASE_URL}/products", json={"name": name, "description": description, "price": price},timeout=10.0)
        response.raise_for_status()
        product = response.json()
        return f"Product created successfully: ID: {product['id']}, Name: {product['name']}, Price: {product['price']}"

@mcp.tool()
async def add_numbers(a:int, b:int)->int:
    """
    Add two numbers together.
    
    Args:
        a (int): The first number.
        b (int): The second number.
    
    Returns:
        int: The sum of the two numbers.
    """

    logger.info(f"Adding numbers: {a} + {b}")
    return a + b

@mcp.tool()
async def check_status() -> str:
    """
    Check the status of the server.
    
    Returns:
        str: The status message.
    """
    logger.info("Checking server status")
    return "Server is running"

if __name__ == "__main__":
    # Create the HTTP app container on the fly
    app = mcp.http_app()
    # Run this server on a completely separate port (e.g., 8001)
    uvicorn.run(app, host="0.0.0.0", port=8001)
 

 # for running , in the terminal run the following command
 # in one terminal, python server.py
 # in the another terminal, run the following command to start the MCP Inspector:
 # npx @modelcontextprotocol/inspector --server-url http://localhost:8001/mcp --transport http
 # it will open the mcp inspector in the browser, where you can test the tools and see the logs.
 # MCP Inspector is now available at http://127.0.0.1:6274



