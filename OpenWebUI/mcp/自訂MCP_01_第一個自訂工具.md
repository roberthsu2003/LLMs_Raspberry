# 自訂 MCP Server（一）：撰寫第一個自訂工具

## 📋 目錄

- [前言](#前言)
- [一、環境準備](#一環境準備)
- [二、建立專案結構](#二建立專案結構)
- [三、撰寫 server.py](#三撰寫-serverpy)
- [四、本機測試](#四本機測試)
- [五、驗證與練習](#五驗證與練習)

---

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

程式會以 stdio 模式運行，等待輸入。若要完整測試，需搭配 mcpo 或後續章節的部署方式。

---

## 五、驗證與練習

完成本階段後，在 Open-WebUI 中測試（需先完成 [自訂MCP_04_整合mcpo部署](./自訂MCP_04_整合mcpo部署.md)）：

- 「請幫我用工具加總 3 + 5」
- 「用 hello 工具跟小明打招呼」

### 練習題

1. 新增 `multiply(a: int, b: int)` 工具，回傳兩數相乘結果。
2. 新增 `greet(name: str, language: str)` 工具，依 `language` 參數回傳不同語言的問候語。

---

下一章：[自訂MCP_02_呼叫外部API](./自訂MCP_02_呼叫外部API.md)
