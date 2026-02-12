# 自訂 MCP Server（四）：整合 mcpo 部署

## 📋 目錄

- [前言](#前言)
- [一、專案結構](#一專案結構)
- [二、mcpo Dockerfile](#二mcpo-dockerfile)
- [三、docker-compose 設定](#三docker-compose-設定)
- [四、啟動與驗證](#四啟動與驗證)
- [五、Open-WebUI 連線設定](#五open-webui-連線設定)
- [六、常見問題](#六常見問題)

---

## 前言

本階段目標：將自訂的 `server.py` 透過 **mcpo** 整合到 Docker 環境，並在 Open-WebUI 中啟用。

關鍵指令：

```
mcpo --port 8000 -- python /custom/server.py
```

mcpo 會以 stdio 模式啟動你的 MCP Server，並將其轉成 HTTP 服務。

---

## 一、專案結構

```
Docker_compose快速部署open-webui/
├── docker-compose.yml
├── .env
├── mcpo/
│   └── Dockerfile
└── mcp-custom/
    ├── requirements.txt
    └── server.py
```

---

## 二、mcpo Dockerfile

`mcpo/Dockerfile` 需安裝 `mcpo` 與 Python 環境，自訂程式透過 volume 掛載：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir mcpo mcp

EXPOSE 8000
```

### 進階：若完成階段二、三，需額外套件

若 `server.py` 有使用 `requests`、`chromadb` 等，可擴充 Dockerfile：

```dockerfile
RUN pip install --no-cache-dir mcpo mcp requests chromadb
```

或改為在啟動時安裝 `mcp-custom` 的依賴（需調整 `command` 或使用 entrypoint 腳本）。

---

## 三、docker-compose 設定

在 `docker-compose.yml` 中新增 `mcpo-custom` service：

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

### 說明

| 項目 | 說明 |
|------|------|
| `build: ./mcpo` | 使用 mcpo 的 Dockerfile |
| `ports: 8003:8000` | 主機 8003 對應容器 8000 |
| `command` | mcpo 以 stdio 模式執行 `python /custom/server.py` |
| `volumes` | 將 `mcp-custom` 掛載到 `/custom`，修改程式後重啟即可生效 |

---

## 四、啟動與驗證

### 4.1 啟動服務

```bash
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

若有 volume 掛載，重啟容器即可：

```bash
docker compose restart mcpo-custom
```

### 埠號衝突

若 8003 已被佔用，可改成 `8004:8000` 等，並在 Open-WebUI 中仍使用 `http://mcpo-custom:8000`（容器內部埠不需變）。

---

## 快速檢查清單

- [ ] `mcp-custom/server.py` 含 `@mcp.tool()` 與 `mcp.run()`
- [ ] `mcp-custom/requirements.txt` 至少包含 `mcp`
- [ ] `mcpo/Dockerfile` 已安裝 `mcpo`
- [ ] docker-compose 中 `command` 為 `mcpo --port 8000 -- python /custom/server.py`
- [ ] `mcpo-custom` 加入 `webui-net`
- [ ] Open-WebUI 新增外部工具 `http://mcpo-custom:8000`

---

上一篇：[自訂MCP_03_整合資料庫](./自訂MCP_03_整合資料庫.md)  
回目錄：[MCP README](./README.md)
