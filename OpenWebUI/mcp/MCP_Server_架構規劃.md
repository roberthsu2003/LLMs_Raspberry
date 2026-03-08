# Open-WebUI 自訂 MCP Server 架構規劃

> 本文檔整合「建立自訂的MCP_Server.md」內容，並依據現有專案結構規劃完整架構。

---

## 📋 目錄

- [一、整體架構概覽](#一整體架構概覽)
- [二、專案目錄結構](#二專案目錄結構)
- [三、技術架構層級](#三技術架構層級)
- [四、元件職責說明](#四元件職責說明)
- [五、部署模式比較](#五部署模式比較)
- [六、教學階段規劃](#六教學階段規劃)
- [七、擴充與維運](#七擴充與維運)

---

## 一、整體架構概覽

### 1.1 系統關係圖

```
                    ┌─────────────────────────────────────────────────┐
                    │                   Open-WebUI                      │
                    │  (管理員控制台 → 設定 → 外部工具 → 新增 MCP)      │
                    └────────────────────────┬──────────────────────────┘
                                             │
                    ┌────────────────────────┼──────────────────────────┐
                    │                        │                          │
                    ▼                        ▼                          ▼
            ┌───────────────┐        ┌───────────────┐        ┌───────────────┐
            │   mcpo-time    │        │ mcpo-weather  │        │  mcpo-custom  │
            │  (port 8001)   │        │  (port 8002)  │        │  (port 8003)  │
            │               │        │               │        │               │
            │ mcp-server-   │        │ mcp_weather_  │        │ server.py     │
            │ time          │        │ server        │        │ (自訂工具)     │
            └───────────────┘        └───────────────┘        └───────────────┘
                    │                        │                          │
                    └────────────────────────┴──────────────────────────┘
                                             │
                                    webui-net (bridge network)
```

### 1.2 核心概念

| 概念 | 說明 |
|------|------|
| **mcpo** | MCP-over-HTTP 的橋接器，將 stdio 模式的 MCP Server 轉成 HTTP 服務 |
| **mcp-custom** | 自訂 MCP Server，用 Python + FastMCP 撰寫，可擴充任意工具 |
| **stdio 模式** | MCP Server 透過標準輸入/輸出溝通，需 mcpo 轉成 HTTP |
| **HTTP 模式** | MCP Server 直接提供 HTTP，不需 mcpo（適合正式部署） |

---

## 二、專案目錄結構

### 2.1 建議的完整結構

```
LLMs_Raspberry/
│
├── Docker_compose快速部署open-webui/
│   ├── docker-compose.yml          # 主 compose 檔（整合所有服務）
│   ├── .env                        # 環境變數（CLOUDFLARE_TOKEN 等）
│   │
│   ├── mcpo/                       # 共用 mcpo 映像（預裝套件）
│   │   └── Dockerfile
│   │
│   └── mcp-custom/                 # 自訂 MCP Server 專案
│       ├── Dockerfile
│       ├── requirements.txt
│       ├── server.py
│       └── tools/                  # 選用：進階時可拆分工具模組
│           ├── __init__.py
│           └── weather.py
│
└── OpenWebUI/
    └── mcp/
        ├── 建立自訂的MCP_Server.md
        ├── MCP_Server_架構規劃.md   # 本文件
        └── ...
```

### 2.2 與現有專案的整合方式

若你已有 `Docker_compose快速部署open-webui` 專案，有兩種整合策略：

| 策略 | 說明 | 適用情境 |
|------|------|----------|
| **策略 A：單一 docker-compose** | 在既有 docker-compose.yml 中新增 `mcpo-custom` service | 所有服務一起管理 |
| **策略 B：獨立 mcp-custom 專案** | 建立獨立 `mcp-custom/` 目錄，透過 volumes 掛載到共用 mcpo 映像 | 專案分離、開發時熱 reload |

> 教學建議：**策略 A** 較簡單，適合初學者；**策略 B** 適合多人協作或需要頻繁修改 server.py。

---

## 三、技術架構層級

### 3.1 三層架構

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 1: 前端 / 使用者介面                                       │
│  Open-WebUI 聊天介面、管理員控制台                                 │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 2: MCP 橋接層                                              │
│  mcpo (stdio → HTTP) 或 直接 HTTP transport                       │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│  Layer 3: 工具實作層                                              │
│  mcp-server-time / mcp_weather_server / server.py (自訂)          │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 資料流

```
使用者輸入：「台北現在幾點？」
    │
    ▼
Open-WebUI + LLM 判斷需呼叫 get_current_time
    │
    ▼
HTTP POST → http://mcpo-time:8000/tools/call
    │
    ▼
mcpo 轉成 stdio → mcp-server-time
    │
    ▼
mcp-server-time 執行 → 回傳 "台北時間 14:30"
    │
    ▼
mcpo 轉成 HTTP 回應 → Open-WebUI → 顯示給使用者
```

---

## 四、元件職責說明

### 4.1 mcpo 映像（共用基礎）

| 項目 | 內容 |
|------|------|
| **位置** | `mcpo/Dockerfile` |
| **角色** | 預裝 `mcpo`、`mcp-server-time`、`mcp_weather_server` 等套件 |
| **自訂服務** | 透過 `command` 覆寫，執行 `python /custom/server.py` |

### 4.2 mcp-custom 專案

| 檔案 | 職責 |
|------|------|
| **server.py** | FastMCP 定義、工具註冊、入口點 |
| **requirements.txt** | `mcp`（必需）、`requests`（若需呼叫 API） |
| **Dockerfile** | 獨立建置時使用；或透過 volume 掛載到 mcpo 容器 |

### 4.3 docker-compose 整合

```yaml
mcpo-custom:
  build: ./mcpo
  container_name: mcpo-custom
  restart: always
  networks:
    - webui-net
  ports:
    - "8003:8000"
  command: >
    mcpo --port 8000 --
    python /custom/server.py
  volumes:
    - ./mcp-custom:/custom
```

> **關鍵**：`mcpo --port 8000 -- python /custom/server.py` 表示 mcpo 以 stdio 模式啟動自訂 MCP Server。

---

## 五、部署模式比較

### 5.1 教學模式（stdio + mcpo）

| 優點 | 說明 |
|------|------|
| ✅ 理解層次清楚 | 學生可分辨「MCP 協議」與「HTTP 轉換」兩件事 |
| ✅ 與現有 MCP 生態一致 | 多數 MCP Server 預設 stdio |
| ✅ 易除錯 | 可單獨執行 `python server.py` 測試 |

**適用**：初學、教學、開發階段。

### 5.2 正式部署模式（HTTP transport）

| 優點 | 說明 |
|------|------|
| ✅ 少一層 mcpo | 自訂 Server 直接開 HTTP，架構簡化 |
| ✅ 延遲較低 | 少了 stdio 轉換 |
| ✅ 易水平擴展 | 可直接掛 Load Balancer |

**程式碼調整**：

```python
# server.py
mcp.run(transport="http")
```

**注意**：需在 Dockerfile 中 expose 對應 port，並修改 docker-compose 的 `command`，不再使用 mcpo。

---

## 六、教學階段規劃

### 階段一：靜態工具（約 1–2 小時）

| 目標 | 內容 |
|------|------|
| **工具** | `hello(name)`、`add(a, b)` |
| **學習重點** | FastMCP 基本用法、`@mcp.tool()` 裝飾器、參數型別 |
| **驗證** | 「請幫我用工具加總 3 + 5」 |

### 階段二：外部 API 工具（約 2–3 小時）

| 目標 | 內容 |
|------|------|
| **工具** | `get_weather(city)`、`get_stock(symbol)` |
| **學習重點** | `requests` 呼叫外部 API、錯誤處理、API Key 管理 |
| **驗證** | 「台北明天天氣如何？」、「查詢台積電股價」 |

### 階段三：資料庫工具（約 2–3 小時）

| 目標 | 內容 |
|------|------|
| **工具** | ChromaDB 查詢、SQLite 查詢 |
| **學習重點** | MCP = LLM 與外部世界的橋樑、RAG 整合概念 |
| **驗證** | 「從知識庫找關於信用卡的資訊」 |

---

## 七、擴充與維運

### 7.1 新增自訂工具流程

1. 在 `server.py` 中新增 `@mcp.tool()` 函式
2. 若需新套件，更新 `requirements.txt`
3. 若有 volume 掛載：直接重啟容器即可
4. 若無 volume：`docker compose up -d --build`

### 7.2 除錯建議

| 情境 | 方法 |
|------|------|
| 工具未被呼叫 | 檢查 Open-WebUI 外部工具 URL 是否為 `http://mcpo-custom:8000` |
| 容器無法啟動 | `docker compose logs mcpo-custom` 檢查錯誤 |
| 本機測試 | `cd mcp-custom && python server.py`（需手動用 stdio 測試，或先改成 HTTP 模式） |

### 7.3 埠號分配表

| 服務 | 主機埠 | 容器埠 | Open-WebUI 設定 URL |
|------|--------|--------|---------------------|
| mcpo-time | 8001 | 8000 | `http://mcpo-time:8000` |
| mcpo-weather | 8002 | 8000 | `http://mcpo-weather:8000` |
| mcpo-custom | 8003 | 8000 | `http://mcpo-custom:8000` |

---

## 附錄：快速檢查清單

建立自訂 MCP Server 時，確認以下項目：

- [ ] 撰寫 `server.py`（FastMCP + `@mcp.tool()`）
- [ ] 建立 `requirements.txt`（至少包含 `mcp`）
- [ ] mcpo 的 Dockerfile 已安裝 `mcpo`，或透過 volume 掛載自訂程式
- [ ] docker-compose 中 `command` 正確：`mcpo --port 8000 -- python /custom/server.py`
- [ ] 與 Open-WebUI 共用 `webui-net`
- [ ] Open-WebUI 管理員控制台 → 外部工具 → 新增 `http://mcpo-custom:8000`

---

