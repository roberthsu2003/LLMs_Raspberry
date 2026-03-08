# Debug 與測試

本文件說明自訂 MCP Server 的四種除錯與測試方式。

---

## 方法一：直接呼叫工具函式（最簡單）

在開發時，可先獨立測試工具邏輯，不透過 MCP 層。建立 `test_tools.py`：

```python
# test_tools.py
from server import add, hello

print(add(3, 5))        # 應輸出 8
print(hello("小明"))    # 應輸出 Hello 小明, 這是自訂 MCP Server
```

執行：

```bash
cd mcp-custom
python test_tools.py
```

---

## 方法二：透過 mcpo + Swagger UI（推薦）

部署 mcpo 後，透過 Swagger 介面測試：

```bash
docker compose up -d --build
```

開啟：`http://localhost:8003/docs`

可看到所有已註冊的工具，並直接呼叫測試，無需透過 Open-WebUI。

---

## 方法三：加入 print 或 logging

在工具內加入 log，方便追蹤執行流程：

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
def add(a: int, b: int) -> int:
    """將兩個整數相加。"""
    logger.info(f"add 被呼叫: a={a}, b={b}")
    result = a + b
    logger.info(f"回傳: {result}")
    return result
```

容器內執行時，用 `docker compose logs -f mcpo-custom` 查看輸出。

---

## 方法四：用 MCP Client 寫測試腳本

以 Python MCP Client 連到 stdio 模式的 server，程式化測試：

```python
# test_client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_tools():
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("工具列表:", [t.name for t in tools.tools])
            result = await session.call_tool("add", arguments={"a": 3, "b": 5})
            print("add(3, 5) 結果:", result)

asyncio.run(test_tools())
```

執行：`python test_client.py`（需在 `mcp-custom` 目錄且 server.py 在同一目錄）

---

[← 回 README](./README.md)
