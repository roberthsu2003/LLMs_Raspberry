from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Custom Tools")


@mcp.tool()
def hello(name: str) -> str:
    """向指定對象打招呼。"""
    return f"Hello, {name}!"


@mcp.tool()
def add(a: int, b: int) -> int:
    """將兩個整數相加。"""
    return a + b


if __name__ == "__main__":
    mcp.run()
