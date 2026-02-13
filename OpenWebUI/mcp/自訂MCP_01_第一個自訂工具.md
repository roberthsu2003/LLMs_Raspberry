# 自訂 MCP Server（一）：撰寫第一個自訂工具

## 📋 目錄

- [前言](#前言)
- [一、環境準備](#一環境準備)
- [二、建立專案結構](#二建立專案結構)
- [三、撰寫 server.py](#三撰寫-serverpy)
- [四、本機測試](#四本機測試)
- [五、Debug 與測試](#五debug-與測試)
- [六、驗證與練習](#六驗證與練習)
- [七、整合 mcpo 部署](#七整合-mcpo-部署)

---

## 範例目錄: [mcp-custom1](./實作範例/mcp-custom)


## 前言

本階段目標：使用 **FastMCP** 撰寫最簡單的自訂工具，無需呼叫外部 API 或資料庫。

學習重點：

- FastMCP 基本用法
- `@mcp.tool()` 裝飾器
- 參數型別與回傳值

---

## 一、環境準備

確認已安裝：

- Python 3.11 以上
- pip

```bash
python --version
pip --version
```

---

## 二、建立專案結構

建立目錄 `mcp-custom`，結構如下：

```
mcp-custom/
├── requirements.txt
└── server.py
```

---

## 三、撰寫 server.py

### 3.1 requirements.txt

```
mcp
```

### 3.2 server.py（最小可用版本）

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Custom Tools")

@mcp.tool()
def hello(name: str) -> str:
    """向指定對象打招呼。"""
    return f"Hello {name}, 這是自訂 MCP Server"

@mcp.tool()
def add(a: int, b: int) -> int:
    """將兩個整數相加。"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

### 3.3 說明

| 項目 | 說明 |
|------|------|
| `FastMCP("Custom Tools")` | 建立 MCP Server 實例，名稱會顯示在工具列表中 |
| `@mcp.tool()` | 將函式註冊為 MCP 工具，LLM 可呼叫 |
| 型別標註 | `name: str`、`a: int` 會自動轉成 tool schema，供 LLM 理解 |
| `mcp.run()` | 預設使用 stdio transport，可被 mcpo 橋接 |

---

## 四、本機測試

安裝依賴並執行：

```bash
cd mcp-custom
pip install -r requirements.txt
python server.py
```

程式會以 stdio 模式運行，等待輸入。若要完整測試，需搭配 mcpo 或下方「Debug 與測試」的方式。

---

## 五、Debug 與測試

### 5.1 方法一：直接呼叫工具函式（最簡單）

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



### 5.2 方法二：透過 mcpo + Swagger UI（推薦）

部署 mcpo 後，透過 Swagger 介面測試：

```bash
docker compose up -d --build
```

開啟：`http://localhost:8003/docs`

可看到所有已註冊的工具，並直接呼叫測試，無需透過 Open-WebUI。

### 5.3 方法三：加入 print 或 logging

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

### 5.4 方法四：用 MCP Client 寫測試腳本

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

## 六、驗證與練習

完成本階段後，在 Open-WebUI 中測試（需先完成下方「整合 mcpo 部署」）：

- 「請幫我用工具加總 3 + 5」
- 「用 hello 工具跟小明打招呼」

### 練習題

1. 新增 `multiply(a: int, b: int)` 工具，回傳兩數相乘結果。
2. 新增 `greet(name: str, language: str)` 工具，依 `language` 參數回傳不同語言的問候語。

---

## 七、整合 mcpo 部署

將自訂 MCP Server 整合至 Docker 環境，讓 Open-WebUI 能呼叫。

### 7.1 專案結構

```
Docker_compose快速部署open-webui/
├── docker-compose.yml
├── mcpo-tools/
    |── Dockerfile
    |── server.py
    ├── requirements.txt

```

### 7.2 mcpo/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY tools.py .

RUN pip install --no-cache-dir \
  mcpo \
  requests

EXPOSE 8000

```

### 7.3 docker-compose.yml 新增服務

```yaml
services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: always
    networks:
      - webui-net
    ports:
      - "8080:8080"
    volumes:
      - open-webui:/app/backend/data
    environment:
      OLLAMA_BASE_URL: http://host.docker.internal:11434
      MCP_ENABLE: "true"
    extra_hosts:
      - "host.docker.internal:host-gateway"

  mcpo-weather:
    build: ./mcpo-tools
    container_name: mcpo-weather
    restart: always
    networks:
      - webui-net
    ports:
      - "8001:8000"
    command: >
      mcpo --port 8000 --
      python tools.py

  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared
    restart: unless-stopped
    networks:
      - webui-net
    command: tunnel run --token ${CLOUDFLARE_TOKEN}

volumes:
  open-webui:
    external: true

networks:
  webui-net:
    name: webui-net
    driver: bridge

```

### 7.4 啟動與連線

```bash
docker compose up -d --build
```

**Open-WebUI 設定**：管理員控制台 → 設定 → 外部工具 → 新增 `http://mcpo-custom:8000`

> 完整說明與常見問題請參考 [自訂MCP_04_整合mcpo部署](./自訂MCP_04_整合mcpo部署.md)。

---

上一篇：[自訂MCP_00_認識FastMCP](./自訂MCP_00_認識FastMCP.md)  
下一篇：[自訂MCP_02_呼叫外部API](./自訂MCP_02_呼叫外部API.md)
