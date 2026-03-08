# Pipeline（第 1 章）：第一個 Pipeline

## 📋 目錄

- [範例檔](#範例檔)
- [快速開始：Docker Run](#快速開始docker-run)
- [進階部署：Docker Compose](#進階部署docker-compose)
- [在 Open-WebUI 中連接](#在-open-webui-中連接)
- [管理與啟用 Pipeline](#管理與啟用-pipeline)
- [常見問題](#常見問題)

---

## 範例檔

本教學提供兩種部署方式的範例：

```
Pipeline_01_第一個Pipeline/
├── 範例檔/                      # 選項 1：單獨運行 pipelines
│   ├── docker-compose.yml
│   └── .env
└── 範例檔2_open-webui與pipelines/  # 選項 2：同時啟動 open-webui 和 pipelines
    └── docker-compose.yml
```

| 範例 | 說明 |
|------|------|
| [範例檔](./範例檔/) | 選項 1：單獨運行 Pipeline Server，port 9099 |
| [範例檔2_open-webui與pipelines](./範例檔2_open-webui與pipelines/) | 選項 2：同時啟動 Open-WebUI (8080) 與 Pipeline Server (9099) |

---

## 快速開始(單獨運行pipelines)：Docker Run

### 步驟 1：拉取映像

```bash
docker pull ghcr.io/open-webui/pipelines:main
```

### 步驟 2：啟動容器

```bash
docker run -d -p 9099:9099 \
  --add-host=host.docker.internal:host-gateway \
  -v pipelines:/app/pipelines \
  --name pipelines \
  --restart always \
  ghcr.io/open-webui/pipelines:main
```

### 步驟 3：確認運作

```bash
docker ps
curl http://localhost:9099
curl -H "Authorization: Bearer 0p3n-w3bu!" http://localhost:9099/v1/models
```

| 指令 | 用途 |
|------|------|
| `docker ps` | 確認 `pipelines` 容器是否在運行 |
| `curl http://localhost:9099` | 測試服務是否可連線（可能回傳 404，表示服務有回應） |
| `curl -H "Authorization: Bearer 0p3n-w3bu!" http://localhost:9099/v1/models` | 取得可用模型列表；若回傳 JSON 即表示 Pipeline Server 正常運作 |

**範例回傳：**

```json
{"data":[{"id":"wikipedia_pipeline","name":"Wikipedia Pipeline","object":"model","created":1772963859,"owned_by":"openai","pipeline":{"type":"pipe","valves":true}}],"object":"list","pipelines":true}
```

**回傳內容說明：**

| 欄位 | 說明 |
|------|------|
| `data` | 可用模型／Pipeline 的陣列 |
| `data[].id` | Pipeline 的唯一識別碼（如 `wikipedia_pipeline`） |
| `data[].name` | 顯示名稱（如 `Wikipedia Pipeline`） |
| `data[].object` | 固定為 `"model"`，符合 OpenAI API 規格 |
| `data[].pipeline.type` | Pipeline 類型：`pipe`（管線）或 `filter`（過濾器） |
| `data[].pipeline.valves` | 是否有可調參數（Valves） |
| `pipelines` | `true` 表示此為 Pipeline Server 來源 |

> **注意：** Pipeline Server 沒有 `/health` 端點，請使用 `/v1/models` 搭配 API Key 作為健康檢查。

---

## 進階部署：Docker Compose

### 選項 1：單獨運行 pipelines

```bash
cd 範例檔
docker compose up -d
```

### 選項 2：同時啟動 open-webui 和 pipelines

```bash
cd 範例檔2_open-webui與pipelines
docker compose up -d
```

啟動後：
- **Open-WebUI**：http://localhost:8080
- **Pipeline Server**：http://localhost:9099

**參數說明：**

| 參數 | 說明 |
|------|------|
| `9099:9099` | Pipeline API 埠號 |
| `8080:8080` | Open-WebUI 埠號（選項 2） |
| `-v pipelines:/app/pipelines` | 存放 pipeline 程式碼的 volume |
| `host.docker.internal:host-gateway` | 讓容器可訪問主機（如 Ollama） |

## 在 Open-WebUI 中連接

1. 前往 **Settings → Connections → OpenAI API**
2. 新增連線
3. **API URL：**
   - 都在 Docker：`http://host.docker.internal:9099`
   - 都在本機：`http://localhost:9099`
4. **API key：** `0p3n-w3bu!`（預設）

---

## 管理與啟用 Pipeline

連線設定完成後，可在 Open WebUI 介面中管理 Pipeline。

### 進入 Pipelines 管理頁面

路徑：**管理員控制台 → 設定 → Pipelines 分頁**

在此頁面可：
- 查看已安裝的 Pipeline 列表
- 啟用／停用個別 Pipeline
- 調整 Valves（可調參數，如速率限制、字數上限等）
- 安裝新的 Pipeline

### 安裝 Pipeline 的兩種方式

| 方式 | 適用情境 | 操作說明 |
|------|----------|----------|
| **從 GitHub URL 安裝** | 無額外依賴的範例 | 點選「從 GitHub URL 安裝」，貼上 `.py` 檔的 raw URL，例如：<br>`https://raw.githubusercontent.com/open-webui/pipelines/main/examples/pipelines/integrations/wikipedia_pipeline.py` |
| **上傳 Python 檔案** | 自訂或本機開發的 Pipeline | 點選上傳，選擇本機的 `.py` 檔案，檔案會傳送至 Pipeline Server 的 `/app/pipelines` 目錄 |

> **注意：** 從 URL 安裝僅適用於**無額外 Python 套件依賴**的 Pipeline。若 Pipeline 需要 `wikipedia`、`requests` 等套件，需自訂 Dockerfile 並重建映像。

### Pipeline 程式碼存放位置

Pipeline 程式碼實際存放在 **Pipeline Server 容器**內的 `/app/pipelines` 目錄：

| Volume 類型 | 修改方式 |
|-------------|----------|
| **Named Volume**（`-v pipelines:/app/pipelines`） | 需透過 Open WebUI 上傳，或進入容器修改：`docker exec -it pipelines sh` |
| **Bind Mount**（`-v ./pipelines:/app/pipelines`） | 直接在主機編輯 `./pipelines/` 下的 `.py` 檔，容器會自動重新載入 |

```
Open WebUI (網頁)  ──管理介面──►  Pipeline Server (容器)
                                      │
                                      ▼
                               /app/pipelines/
                               ├── wikipedia_pipeline.py
                               └── my_custom_pipeline.py
```

---

## 常見問題

### Python 檔改了要不要 rebuild？

- **只改 `pipelines/` 下的 .py 檔：** 不需要，會自動重新載入
- **改 requirements.txt 或 Dockerfile：** 需要 `docker compose up -d --build`

### 如何確認 Pipeline 正常運作？

```bash
curl -H "Authorization: Bearer 0p3n-w3bu!" http://localhost:9099/v1/models
docker logs pipelines
```

---

上一篇：[Pipeline_00_認識Pipeline](../Pipeline_00_認識Pipeline/README.md)  
下一篇：[Pipeline_02_整合Cloudflare](../Pipeline_02_整合Cloudflare/README.md)
