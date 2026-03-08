# Debug 與測試

本文件說明自訂 MCP Server（天氣查詢）的四種除錯與測試方式。

---

## 建立 Python 的虛擬環境

進行本機測試前，建議先建立虛擬環境以隔離依賴。

### 使用 uv（推薦）

```bash
cd 範例檔/mcpo-custom
uv venv
uv pip install -r requirements.txt
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

> 詳細步驟請參考 [uv 開發環境](./uv開發環境.md)

### 使用 venv + pip

```bash
cd 範例檔/mcpo-custom
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 方法一：直接呼叫工具函式（最簡單）

在開發時，可先獨立測試工具邏輯，不透過 MCP 層。建立 `test_tools.py`：

```python
# test_tools.py - 直接呼叫工具函式測試（不透過 MCP 層）
from server import get_weather

print(get_weather("台北"))   # 應輸出台北目前氣溫約 XX°C,天氣代碼 XX
print(get_weather("高雄"))   # 應輸出高雄目前氣溫約 XX°C,天氣代碼 XX
```

執行：

```bash
cd mcpo-custom
python test_tools.py
```

> **注意：** 此方式會實際呼叫 Open-Meteo API，需有網路連線。

---

## 方法二：透過 mcpo + Swagger UI（推薦）

在虛擬環境內使用 mcpo 指令啟動 MCP Server，透過 Swagger 介面測試：

```bash
cd 範例檔/mcpo-custom
source .venv/bin/activate   # Windows: .venv\Scripts\activate
mcpo --port 8000 -- python server.py
```

用瀏覽器開啟：`http://localhost:8000/docs`
可看到所有已註冊的工具（如 `get_weather`），並直接呼叫測試，無需透過 Open-WebUI。

---

## 方法三：加入 print 或 logging

在工具內加入 log，方便追蹤執行流程與 API 回應：

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mcp.tool()
def get_weather(city: str) -> str:
    """查詢指定城市的天氣概況。"""
    logger.info(f"get_weather 被呼叫: city={city}")
    # ... 呼叫 API ...
    logger.info(f"回傳: {result}")
    return result
```

使用 mcpo 本機執行時，透過 Swagger UI 呼叫工具後，log 會直接輸出在執行 mcpo 的終端機。

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
            result = await session.call_tool("get_weather", arguments={"city": "台北"})
            print("get_weather(台北) 結果:", result)

asyncio.run(test_tools())
```

執行：`python test_client.py`（需在 `mcpo-custom` 目錄且 server.py 在同一目錄）

---

[← 回 README](./README.md)
