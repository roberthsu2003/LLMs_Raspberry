# 自訂 MCP Server（一）：撰寫第一個自訂工具

## 📋 目錄

- [範例檔](#範例檔)
- [前言](#前言)
- [一、環境準備](#一環境準備)
- [uv 開發環境](#uv-開發環境)
- [二、建立專案結構](#二建立專案結構)
- [三、撰寫 server.py](#三撰寫-serverpy)
- [四、本機測試](#四本機測試)
- [五、Debug 與測試](#五debug-與測試)
- [六、驗證與練習](#六驗證與練習)
- [七、整合 mcpo 部署](#七整合-mcpo-部署)

---

## 範例檔

本範例完整檔案位於 [範例檔](./範例檔/) 資料夾，**架構與主專案一致**：

```
範例檔/
├── docker-compose.yml
└── mcpo-custom/
    ├── Dockerfile
    ├── requirements.txt
    ├── server.py
    └── test_tools.py
```

| 檔案 | 說明 |
|------|------|
| [docker-compose.yml](./範例檔/docker-compose.yml) | 整合 open-webui、mcpo-custom、cloudflared |
| [mcpo-custom/requirements.txt](./範例檔/mcpo-custom/requirements.txt) | Python 依賴（mcp、mcpo） |
| [mcpo-custom/server.py](./範例檔/mcpo-custom/server.py) | MCP Server 主程式（hello、add 工具） |
| [mcpo-custom/Dockerfile](./範例檔/mcpo-custom/Dockerfile) | mcpo 部署用映像 |
| [mcpo-custom/test_tools.py](./範例檔/mcpo-custom/test_tools.py) | 本機測試腳本 |

> 可直接複製 `範例檔/` 至你的 `Docker_compose快速部署open-webui/` 專案，或將 `mcpo-custom/` 與 `docker-compose.yml` 合併至既有專案。

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

## uv 開發環境

若使用 **uv** 建立虛擬環境進行本機開發，可參考：[uv 開發環境](./uv開發環境.md)

該文件包含：uv 安裝、建立 `.venv`、安裝依賴、啟動與驗證等完整步驟。

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

程式會以 stdio 模式運行，等待輸入。若要完整測試，需搭配 mcpo 或 [Debug 與測試](./Debug與測試.md) 的方式。

---

## 五、Debug 與測試

四種除錯與測試方式（直接呼叫工具、mcpo + Swagger UI、logging、MCP Client）請參考：[Debug 與測試](./Debug與測試.md)

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
├── .env
├── mcpo-custom/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── server.py
└── ...
```

### 7.2 mcpo-custom/Dockerfile

套件從 `requirements.txt` 安裝，映像內不含啟動指令（由 docker-compose 的 `command` 覆寫）：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 8000
```

> **說明：** `requirements.txt` 含 `mcp`（FastMCP）與 `mcpo`（HTTP 橋接），所有依賴統一管理。啟動指令放在 docker-compose 的 `command`，方便之後覆寫或切換不同腳本，無需重建映像。

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

  mcpo-custom:
    build: ./mcpo-custom
    image: mcpo-custom
    container_name: mcpo-custom
    restart: always
    networks:
      - webui-net
    ports:
      - "8003:8000"
    command: >
      mcpo --port 8000 --
      python server.py

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

| 項目 | 說明 |
|------|------|
| `command` 在 yaml | 啟動指令放 compose，修改後重啟即可，無需 `docker build` |
| `mcpo-custom` | 與第一章「自訂工具」對應，與第二章 `mcpo-weather` 區分 |

#### `command: >` 是什麼？

`command: >` 是 **YAML 的折疊區塊（folded block）** 語法：

| 符號 | 名稱 | 作用 |
|------|------|------|
| `>` | Folded block | 多行會合併成一行，換行變成空格 |

範例：

```yaml
command: >
  mcpo --port 8000 --
  python server.py
```

等同於 `command: "mcpo --port 8000 -- python server.py"`，多行會合併成一個字串，中間以空格連接。這樣寫可讓較長的指令更易閱讀。

#### 為什麼啟動指令放在 docker-compose 比較好？

| 比較 | 放在 Dockerfile CMD | 放在 docker-compose `command` |
|------|---------------------|------------------------------|
| **修改指令** | 需執行 `docker build` 重建映像 | 改 yaml 後 `docker compose restart` 即可 |
| **開發迭代** | 每次改指令都要重建，較慢 | 快速調整，適合學習與除錯 |
| **同一映像多用途** | 一個映像只能跑一種指令 | 同一映像可跑不同腳本（如 `server.py`、`tools.py`） |
| **埠號或參數調整** | 需重建 | 直接改 yaml 即可 |

**建議：** 開發與教學階段將 `command` 放在 docker-compose；若部署到正式環境且指令已固定，可改回 Dockerfile 的 `CMD`，讓映像更自包含。

### 7.4 啟動與連線

```bash
docker compose up -d --build
```

**Open-WebUI 設定**：管理員控制台 → 設定 → 外部工具 → 新增 `http://mcpo-custom:8000`

> 完整說明與常見問題請參考 [自訂MCP_04_整合mcpo部署](../自訂MCP_04_整合mcpo部署/README.md)。

---

上一篇：[自訂MCP_00_認識FastMCP](../自訂MCP_00_認識FastMCP.md)  
下一篇：[自訂MCP_02_呼叫外部API](../自訂MCP_02_呼叫外部API/README.md)
