# 自訂 MCP Server（第 0 章）：認識 FastMCP

## 📋 目錄

- [FastMCP 是什麼？](#fastmcp-是什麼)
- [先理解：什麼是 MCP？](#先理解什麼是-mcp)
- [FastMCP 在做什麼？](#fastmcp-在做什麼)
- [沒有 FastMCP 會怎樣？](#沒有-fastmcp-會怎樣)
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

## FastMCP 在做什麼？

FastMCP 幫你把這件事變得非常簡單。

如果你以前用過：

- **FastAPI**
- 或 **OpenAI Function Calling**

那你會覺得它很像：

> 「專門為 MCP 設計的 FastAPI」

---

## 沒有 FastMCP 會怎樣？

如果不用 FastMCP，你要自己處理：

- WebSocket / HTTP Server
- MCP 協定格式
- JSON schema
- Tool 註冊機制
- Context 管理

會非常麻煩。

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
