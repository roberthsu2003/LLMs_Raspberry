# OpenWebUI 如何安裝與使用 MCP 工具

## 📋 目錄

- [測試現在的模型（未啟用 MCP）](#測試現在的模型未啟用-mcp)
- [透過 MCP 取得現在的時間](#透過-mcp-取得現在的時間)
  - [整體架構原理](#整體架構原理從上到下)
  - [為什麼要 MCP_ENABLE=true？](#為什麼要-mcp_enabletrue)
  - [為什麼要 mcpo？](#為什麼要-mcpo)
  - [建立 mcpo 工具伺服器](#建立-mcpo-工具伺服器)
  - [測試 mcpo 是否正常運行](#測試-mcpo-工具伺服器是否正常運行)
  - [在 OpenWebUI 新增工具伺服器](#新增工具伺服器的-url)
  - [使用模型測試](#使用模型測試工具伺服器)
  - [核心概念總結](#-真正的核心概念)

---

## 測試現在的模型（未啟用 MCP）

在**未啟用 MCP 工具**的情況下，詢問模型：

```
現在台北時間幾點？
```

模型可能會回覆類似以下內容（無法取得即時時間）：

```
抱歉，作為一個語言模型，我沒有實時的時鐘資訊，無法直接告訴你「現在」台北的精確時間...
```

**這正是我們要透過 MCP 解決的問題。**

---

## 透過 MCP 取得現在的時間

以下步驟說明如何設定 MCP，讓模型能呼叫外部工具取得即時時間。

---

### 🧠 整體架構原理（從上到下）

實際的資料流架構是：

```
瀏覽器
   ↓
Open-WebUI (LLM UI)
   ↓
MCP Client (內建於 WebUI)
   ↓
mcpo (MCP → OpenAPI 轉換器)
   ↓
mcp-server-time
```

接下來我們一層一層說明。

---

### 為什麼要 MCP_ENABLE=true？

`MCP_ENABLE=true` 的作用是：

> 啟用 Open-WebUI 內建的 MCP Client 模組

若未設定此環境變數：

- UI 不會出現「外部工具」選項
- WebUI 無法呼叫 MCP 工具

**設定方式：**  
在 Docker Compose 的環境變數中新增 `MCP_ENABLE=true`。

---

### 為什麼要 mcpo？

MCP 是一種協定（Model Context Protocol），  
但 Open-WebUI 的工具系統是**基於 OpenAPI**，兩者格式不同。

因此需要一個「翻譯器」：

```
MCP 協定
   ↓
mcpo 轉成 OpenAPI HTTP server
   ↓
Open-WebUI 可辨識並呼叫
```

WebUI 其實不知道 MCP 的存在，它只知道：**這是一個 OpenAPI 工具伺服器**。

**設定位置：** OpenWebUI → 管理員控制台 → 設定 → 外部工具

---

### 建立 mcpo 工具伺服器

#### 方式一：使用 docker run 建立

```bash
docker run -d \
  --name mcpo \
  --network webui-net \
  -p 8000:8000 \
  python:3.11 \
  sh -c "pip install --no-cache-dir mcpo mcp-server-time && \
         mcpo --port 8000 -- mcp-server-time --local-timezone=Asia/Taipei"
```

**參數說明：**

| 參數 | 說明 |
|------|------|
| `-d` | 背景執行（detached mode），容器啟動後在背景運行 |
| `--name mcpo` | 將容器命名為 `mcpo`，Open-WebUI 透過此名稱在 webui-net 網路內解析 |
| `--network webui-net` | 加入 webui-net 網路，與 Open-WebUI 同網段才能互通 |
| `-p 8000:8000` | 將容器內的 8000 埠對應到主機的 8000 埠 |
| `python:3.11` | 使用官方 Python 3.11 映像作為基礎 |
| `sh -c "..."` | 在容器啟動時執行指令：先安裝 mcpo 與 mcp-server-time，再啟動服務 |
| `mcpo --port 8000 -- mcp-server-time` | mcpo 在 8000 埠監聽，並將請求轉發給 mcp-server-time |
| `--local-timezone=Asia/Taipei` | 設定 mcp-server-time 的時區為台北時間 |

#### 方式二：使用 Dockerfile 建立

> 建議先完成方式一，確認 mcpo 可正常運作後，再參考此進階方式。

詳見：[使用 Dockerfile 建立 MCPO 工具伺服器](./使用Dockerfile建立MCPO.md)

---

### 測試 mcpo 工具伺服器是否正常運行

#### 步驟 1：檢查容器狀態

```bash
docker ps
```

確認 `mcpo` 容器已啟動且狀態為 `Up`。

#### 步驟 2：使用瀏覽器驗證

在電腦瀏覽器開啟：`http://<樹莓派IP>:8000/docs`

必須看到 Swagger UI 介面，並確認以下內容表示 mcpo 運作正常：

| 區塊 | 說明 |
|------|------|
| **標題與版本** | 顯示 `mcp-time`、版本號（如 1.26.0）、`OAS 3.1`（符合 OpenAPI 規格） |
| **Endpoints（default）** | 兩個工具 API：`POST /get_current_time`、`POST /convert_time` |
| **Schemas** | 定義各 API 的請求／回應結構 |
| **/openapi.json** | 完整 OpenAPI 規格檔，Open-WebUI 會使用此規格認識可呼叫的工具 |

**為什麼要看這個畫面？**

mcpo 會把 MCP 的 `mcp-server-time` 轉成 OpenAPI 格式；Swagger UI 是這份 OpenAPI 的可視化介面。若能看到上述 endpoint，代表 mcpo 已正確啟動，Open-WebUI 即可透過這些 API 呼叫時間工具。

---

### 新增工具伺服器的 URL

**設定位置：** OpenWebUI → 管理員控制台 → 設定 → 外部工具

| 欄位 | 建議值 |
|------|--------|
| **URL** | `http://mcpo:8000` |
| **驗證** | 無 |
| **名稱** | 自訂（例如：mcp-time） |
| **描述** | 自訂（例如：取得目前時間與時間轉換） |

> **注意：** 使用 `http://mcpo:8000` 而非 `http://localhost:8000`，因為 Open-WebUI 與 mcpo 同屬 Docker 網路，需透過容器名稱 `mcpo` 互相解析。

---

### 使用模型測試工具伺服器

設定完成後，當模型支援 function calling 時，流程如下：

1. **WebUI** 把 OpenAPI schema 傳給模型
2. **模型** 辨識到可用工具：`get_current_time`、`convert_time`
3. 當你問：「現在台北時間幾點？」
4. **模型** 判斷需呼叫工具 → 輸出 tool call
5. **WebUI** 呼叫 mcpo → mcpo 轉發給 mcp-server-time
6. **回傳結果** → 模型生成自然語言回答

---

### 🔥 真正的核心概念

你現在完成的不只是「接 API」。

你完成的是：

> **讓模型具備「外部能力」**

這就是 Agent 的基礎。

---
