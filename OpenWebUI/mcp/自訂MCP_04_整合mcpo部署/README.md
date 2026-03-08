# 自訂 MCP Server（四）：整合 mcpo 部署

## 📋 目錄

- [範例檔](#範例檔)
- [前言](#前言)
- [一、專案結構](#一專案結構)
- [二、mcpo Dockerfile](#二mcpo-dockerfile)
- [三、docker-compose 設定](#三docker-compose-設定)
- [uv 開發環境](#uv-開發環境)
- [四、啟動與驗證](#四啟動與驗證)
- [五、Open-WebUI 連線設定](#五open-webui-連線設定)
- [Debug 與測試](#debug-與測試)
- [六、常見問題](#六常見問題)

---

## 範例檔

本範例完整檔案位於 [範例檔](./範例檔/) 資料夾，**架構與主專案一致**：

```
範例檔/
├── docker-compose.yml
├── .env
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

本階段目標：將自訂的 `server.py` 透過 **mcpo** 整合到 Docker 環境，並在 Open-WebUI 中啟用。

關鍵指令：

```
mcpo --port 8000 -- python server.py
```

mcpo 會以 stdio 模式啟動你的 MCP Server，並將其轉成 HTTP 服務。

---

## 一、專案結構

```
範例檔/
├── docker-compose.yml
├── .env
└── mcpo-custom/
    ├── Dockerfile
    ├── requirements.txt
    ├── server.py
    └── test_tools.py
```

---

## 二、mcpo Dockerfile

`mcpo-custom/Dockerfile` 套件從 `requirements.txt` 安裝，映像內不含啟動指令（由 docker-compose 的 `command` 覆寫）：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 8000
```

### 進階：若完成階段二、三，需額外套件

若 `server.py` 有使用 `requests`、`psycopg2-binary` 等，請在 `requirements.txt` 加入對應套件：

```
mcp
mcpo
requests
psycopg2-binary
```

---

## 三、docker-compose 設定

在 `docker-compose.yml` 中新增 `mcpo-custom` service：

```yaml
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
```

### 說明

| 項目 | 說明 |
|------|------|
| `build: ./mcpo-custom` | 以 mcpo-custom 目錄建置映像 |
| `ports: 8003:8000` | 主機 8003 對應容器 8000 |
| `command` | mcpo 以 stdio 模式執行 `python server.py` |

> **進階：** 若希望修改程式後重啟即可生效（無需重建映像），可加入 volume 掛載：`volumes: - ./mcpo-custom:/app`

---

## uv 開發環境

若使用 **uv** 建立虛擬環境進行本機開發，可參考：[uv 開發環境](./uv開發環境.md)

該文件包含：uv 安裝、建立 `.venv`、安裝依賴、啟動與驗證等完整步驟。

---

## 四、啟動與驗證

### 4.1 啟動服務

```bash
cd 範例檔
docker compose up -d --build
```

### 4.2 檢查容器

```bash
docker ps
```

確認 `mcpo-custom` 狀態為 `Up`。

### 4.3 Swagger UI 測試

開啟：`http://localhost:8003/docs`

應能看到工具列表（如 `hello`、`add` 等）及對應的 API 端點。

---

## 五、Open-WebUI 連線設定

### 5.1 新增 MCP Provider

路徑：**管理員控制台 → 設定 → 外部工具**

新增工具：

| 名稱 | URL |
|------|-----|
| mcp-custom | `http://mcpo-custom:8000` |

> 使用**容器名稱** `mcpo-custom`，同一 Docker 網路內可互相解析。

### 5.2 測試

在對話中輸入：

> 請幫我用工具加總 3 + 5

模型應會呼叫 `add` 工具並回傳結果。

---

## 六、常見問題

### 工具未被呼叫

- 確認 Open-WebUI 外部工具 URL 為 `http://mcpo-custom:8000`
- 確認 `mcpo-custom` 與 `open-webui` 在同一網路 `webui-net`

### 容器無法啟動

```bash
docker compose logs mcpo-custom
```

檢查是否為 Python 語法錯誤或缺少套件。

### 修改 server.py 後無效

若無 volume 掛載，需重建映像：

```bash
docker compose up -d --build
```

若有 volume 掛載，重啟容器即可：

```bash
docker compose restart mcpo-custom
```

### 埠號衝突

若 8003 已被佔用，可改成 `8004:8000` 等，並在 Open-WebUI 中仍使用 `http://mcpo-custom:8000`（容器內部埠不需變）。

---

## Debug 與測試

四種除錯與測試方式（直接呼叫工具、mcpo + Swagger UI、logging、MCP Client）請參考：[Debug 與測試](./Debug與測試.md)

---

## 快速檢查清單

- [ ] `mcpo-custom/server.py` 含 `@mcp.tool()` 與 `mcp.run()`
- [ ] `mcpo-custom/requirements.txt` 至少包含 `mcp`、`mcpo`
- [ ] `mcpo-custom/Dockerfile` 已安裝依賴
- [ ] docker-compose 中 `command` 為 `mcpo --port 8000 -- python server.py`
- [ ] `mcpo-custom` 加入 `webui-net`
- [ ] Open-WebUI 新增外部工具 `http://mcpo-custom:8000`

---

上一篇：[自訂MCP_03_整合資料庫](../自訂MCP_03_整合資料庫/README.md)  
回目錄：[MCP README](../README.md)
