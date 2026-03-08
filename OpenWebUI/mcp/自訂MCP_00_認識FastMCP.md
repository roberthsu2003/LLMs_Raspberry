# 自訂 MCP Server（第 0 章）：認識 FastMCP

## 📋 目錄

- [FastMCP 是什麼？](#fastmcp-是什麼)
- [先理解：什麼是 MCP？](#先理解什麼是-mcp)
- [為什麼 MCP 需要 WebSocket？](#為什麼-mcp-需要-websocket)
- [FastMCP 在做什麼？](#fastmcp-在做什麼)
- [沒有 FastMCP 會怎樣？](#沒有-fastmcp-會怎樣)
- [FastMCP 幫你做了什麼？](#fastmcp-幫你做了什麼)
- [使用 FastMCP 的好處](#使用-fastmcp-的好處)
- [範例：最小 FastMCP Server](#範例最小-fastmcp-server)
- [FastMCP 與 Pipeline 的差異](#fastmcp-與-pipeline-的差異)
- [FastMCP 適合什麼場景？](#fastmcp-適合什麼場景)
- [一句話總結](#一句話總結)

---

## FastMCP 是什麼？

**FastMCP** 是一個用來快速建立 MCP Server（Model Context Protocol Server）的 Python 套件。

簡單說：

> 它讓你可以用很少的程式碼，就建立一個可以被 LLM（例如 Open-WebUI、Claude、Cursor 等）呼叫的工具伺服器。

---

## 先理解：什麼是 MCP？

**MCP（Model Context Protocol）** 是由 Anthropic 推出的標準協定。

它的目的是：

讓「大型語言模型」可以標準化地呼叫外部工具或資料來源。

也就是讓 AI 可以：

- 查資料庫
- 存取本地檔案
- 呼叫 API
- 執行程式

---

## 為什麼 MCP 需要 WebSocket？

MCP 是**即時雙向通訊協定**。

Client（例如 Open-WebUI、Claude Desktop）與 Server（你的 MCP Server）之間，不是「一次請求一次回應」而已，而是會**長時間保持連線，隨時雙向傳訊息**。這種模式最適合用 **WebSocket**。

### HTTP 與 WebSocket 的差異

| 模式 | 特性 |
|------|------|
| **HTTP** | Client → Request → Server → Response → 連線結束 |
| **WebSocket** | Client ↔ Server 持續連線，可隨時互傳訊息，支援串流 |

### MCP 實際需要的場景

當模型決定呼叫工具、工具正在執行、或需要串流結果、多步驟互動時，需要：

1. **即時回傳狀態**
2. **非同步回應**
3. **串流輸出**
4. **Server 主動發訊息**

這些 HTTP 很難優雅處理，而 WebSocket 正是為此設計。以下用實際情境說明：

---

#### 1️⃣ 即時回傳狀態（Real-time Status）

**情境：** AI 呼叫工具去爬 1000 個網頁。若沒有即時回報，使用者會以為系統當機。

**MCP Server 回傳：**

```
正在抓取第 1 / 1000 個網站
正在抓取第 2 / 1000 個網站
正在抓取第 3 / 1000 個網站
...
完成
```

**使用者畫面：** `📡 網頁爬蟲執行中... 進度: 37%`

**為什麼 HTTP 不好做：** HTTP 必須等**全部完成才回傳**。

---

#### 2️⃣ 非同步回應（Async Response）

**情境：** AI 呼叫工具去訓練一個 ML 模型，訓練可能需要 10 分鐘。

**MCP 流程：**

```
AI → Server: call_tool("train_model")

Server 立即回傳:
{ job_id: 1234, status: "training" }

（10 分鐘後）

Server → Client:
{ job_id: 1234, status: "completed", accuracy: 0.91 }
```

**重點：** 任務先開始，結果之後再回來。

---

#### 3️⃣ 串流輸出（Streaming Output）

**情境：** AI 呼叫工具讀取大型 PDF。若一次回傳 50000 tokens 會很慢。

**MCP Server 可以：** 一邊讀一邊送

```
chunk 1 → chunk 2 → chunk 3 → chunk 4 → ...
```

**類似 ChatGPT 打字效果：** 文字持續出現，而非等全部完成才顯示。

---

#### 4️⃣ Server 主動發訊息（Server Push）

**情境：** AI 訂閱股票價格或 IoT 感測器。

```
AI: subscribe_stock("TSMC")

Server 主動推送:
TSMC: 620 → 621 → 618 → 623
```

或 IoT：`溫度 27°C → 28°C → 29°C`

**重點：** Server 不必等 Client 請求，可主動推送資料。

---

#### 快速對照表

| 功能 | 實際例子 |
|------|----------|
| 即時回傳狀態 | 顯示爬蟲進度 |
| 非同步回應 | AI 訓練模型，先回 job_id，完成後再通知 |
| 串流輸出 | AI 逐字輸出回答 |
| Server 主動訊息 | 股票報價、IoT 感測資料 |

---

### 教學金句

> **HTTP 是問答式，WebSocket 是對話式。MCP 是讓模型和工具進行「對話」。**

也可以用「點餐」來比喻：

- **HTTP：** 客戶點餐 → 服務生送餐 → 結束
- **WebSocket：** 客戶點餐 → 服務生「料理中」→「再等一下」→「好了」→ 持續互動

---

## FastMCP 在做什麼？

FastMCP 幫你把這件事變得非常簡單。

如果你以前用過：

- **FastAPI**
- 或 **OpenAI Function Calling**

那你會覺得它很像：

> 「專門為 MCP 設計的 FastAPI」

---

## 沒有 FastMCP 會怎樣？

如果不用 FastMCP，你要自己實作所有的底層機制：

### ① WebSocket Server

需自行處理：

- 連線建立
- 訊息格式解析
- 關閉事件
- 錯誤管理

### ② MCP 訊息格式

MCP 訊息不是隨便的 JSON，它有特定格式：

- `initialize`
- `list_tools`
- `call_tool`
- `response id`
- `error` 格式

全部要自己解析與實作。

### ③ 工具註冊系統

需自行維護工具對照表：

```python
tools = {
    "add": add_function,
    "query_db": query_function
}
```

還要將每個工具轉成 JSON Schema 供模型辨識。

---

## FastMCP 幫你做了什麼？

**重點：** 不是因為 FastMCP 才需要 WebSocket，而是 **MCP 協定本身就設計成即時雙向通訊**。FastMCP 只是幫你把這些底層全部包起來。

它幫你：

- 建立 WebSocket Server
- 實作 MCP 協定
- 自動產生 JSON Schema
- 處理 tool 呼叫
- 管理 context

你只要寫：

```python
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b
```

---

## 使用 FastMCP 的好處

1. 自動幫你處理 MCP 協定
2. 只要用 decorator 定義工具
3. 自動轉成 JSON Schema
4. 可以直接被 Open-WebUI 連接
5. 非常適合教學

---

## 範例：最小 FastMCP Server

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """加法工具"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

就這樣。

這個 server 啟動後：

- Open-WebUI
- Claude Desktop
- 任何支援 MCP 的客戶端

都可以呼叫這個 `add()` 工具。

---

## FastMCP 與 Pipeline 的差異

因為你現在在教 MCP 架構，整理成教學對比：

| 比較 | FastMCP | Pipeline Server |
|------|---------|-----------------|
| 標準 | MCP 標準 | OpenAI-compatible |
| 工具決策 | 模型決定要不要呼叫 | 你程式決定流程 |
| 架構類型 | Tool 型 | Flow 型 |
| 適合 | Agent 架構 | 固定流程 |

---

## FastMCP 適合什麼場景？

- 建立工具型 AI Agent
- 教學生理解 Tool Calling
- 整合本地資料庫
- 建立企業內部 AI 工具

---

## 一句話總結

> **FastMCP 是「建立 MCP Tool Server 的 Python 快速框架」。**

---

下一篇：[自訂MCP_01_第一個自訂工具](./自訂MCP_01_第一個自訂工具.md)
