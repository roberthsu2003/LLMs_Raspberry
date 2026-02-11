# 同時安裝多個 MCP Server

## 📋 目錄

- [前言](#前言)
- [一、架構概念](#一架構概念)
- [二、專案結構](#二專案結構)
- [三、Dockerfile](#三dockerfile)
- [四、docker-compose.yml](#四docker-composeyml)
- [五、在 Open-WebUI 新增多個工具](#五在-open-webui-新增多個工具)
- [六、啟動與驗證](#六啟動與驗證)

---

## 前言

當你需要**多種 MCP 工具**（例如時間查詢 + 天氣查詢）時，可透過 **一個映像、多個容器** 的方式部署。

每個 MCP Server 由獨立的 mcpo 容器負責，對應不同的埠號與 Open-WebUI 外部工具設定。

---

## 一、架構概念

```
Open-WebUI
    ├── 外部工具 1 → http://mcpo-time:8000    （時間相關）
    └── 外部工具 2 → http://mcpo-weather:8000 （天氣相關）
```

**重點：** 一個 mcpo 容器對應一個 MCP Server，各自使用不同埠號對外映射。

---

## 二、專案結構

```
mcpo-project/
├── docker-compose.yml
├── .env
└── mcpo/
    └── Dockerfile
```

---

## 三、Dockerfile

在同一個 Dockerfile 中安裝多個 MCP Server 套件，之後在 docker-compose 中用 `command` 指定要啟動哪一個：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
  mcpo \
  mcp-server-time \
  mcp_weather_server

EXPOSE 8000
```

> 每個服務的實際啟動指令由 docker-compose.yml 的 `command` 覆寫。

---

## 四、docker-compose.yml

```yaml
version: "3.9"

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

  mcpo-time:
    build: ./mcpo
    container_name: mcpo-time
    restart: always
    networks:
      - webui-net
    ports:
      - "8001:8000"
    command: >
      mcpo --port 8000 --
      mcp-server-time --local-timezone=Asia/Taipei

  mcpo-weather:
    build: ./mcpo
    container_name: mcpo-weather
    restart: always
    networks:
      - webui-net
    ports:
      - "8002:8000"
    command: >
      mcpo --port 8000 --
      mcp_weather_server

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

**說明：**

| 服務 | 容器名稱 | 主機埠 | 內部埠 | MCP Server |
|------|----------|--------|--------|------------|
| mcpo-time | mcpo-time | 8001 | 8000 | mcp-server-time |
| mcpo-weather | mcpo-weather | 8002 | 8000 | mcp_weather_server |

> 容器之間透過 **服務名稱** 互連，Open-WebUI 使用 `http://mcpo-time:8000`、`http://mcpo-weather:8000`，無需使用主機埠。

---

## 五、在 Open-WebUI 新增多個工具

**設定位置：** Open-WebUI → 管理員控制台 → 設定 → 外部工具

需**分別新增**兩個工具：

| 名稱 | URL | 描述 |
|------|-----|------|
| mcp-time | `http://mcpo-time:8000` | 取得目前時間、時間轉換 |
| mcp-weather | `http://mcpo-weather:8000` | 天氣查詢 |

---

## 六、啟動與驗證

### 啟動服務

```bash
docker compose up -d --build
```

> 若已修改 Dockerfile，加上 `--build` 可強制重新建置映像，無需手動刪除舊映像。

### 驗證

**1. 檢查容器狀態：**

```bash
docker ps
```

確認 `mcpo-time`、`mcpo-weather` 皆為 `Up`。

**2. 使用瀏覽器驗證：**

- 時間工具：`http://<樹莓派IP>:8001/docs`
- 天氣工具：`http://<樹莓派IP>:8002/docs`

**3. 在 Open-WebUI 中測試：**

於對話中詢問「現在台北時間幾點？」或「台北明天天氣如何？」，模型應能呼叫對應工具並回覆。

---
