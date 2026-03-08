# 同時安裝多個 MCP Server

## 📋 目錄

- [前言](#前言)
- [一、架構概念](#一架構概念)
- [二、專案結構](#二專案結構)
- [三、config.json](#三configjson)
- [四、Dockerfile](#四dockerfile)
- [五、compose.yaml](#五composeyaml)
- [六、在 Open-WebUI 新增工具](#六在-open-webui-新增工具)
- [七、啟動與驗證](#七啟動與驗證)

---

## 前言

當你需要**多種 MCP 工具**（例如時間查詢 + 天氣查詢）時，可透過 **一個映像、一個容器** 的方式部署。

單一 mcpo 容器透過 `config.json` 配置多個 MCP Server，對應不同的工具端點，由 Open-WebUI 外部工具統一連線。

## 下方是實作範例目錄連結

[實作範例目錄連結](./實作範例/同時安裝多個MCP_Server)

---

## 一、架構概念

```
Open-WebUI
    └── 外部工具 → http://mcpo:8000
                      ├── time   （時間相關）
                      └── weather（天氣相關）
```

**重點：** 一個 mcpo 容器透過 config.json 同時載入多個 MCP Server，對外使用單一埠號 8000。

---

## 二、專案結構

```
同時安裝多個MCP_Server/
├── compose.yaml
├── .env
└── mcpo/
    ├── Dockerfile
    └── config.json
```

---

## 三、config.json

透過 `config.json` 定義多個 MCP Server，每個 server 對應一組 `command` 與 `args`：

```json
{
  "mcpServers": {
    "time": {
      "command": "python",
      "args": ["-m", "mcp_server_time", "--local-timezone=Asia/Taipei"]
    },
    "weather": {
      "command": "python",
      "args": ["-m", "mcp_weather_server"]
    }
  }
}
```

| Server 名稱 | 模組 | 說明 |
|-------------|------|------|
| time | mcp_server_time | 取得目前時間、時間轉換（台北時區） |
| weather | mcp_weather_server | 天氣查詢 |

---

## 四、Dockerfile

在 Dockerfile 中安裝 mcpo 與所需 MCP Server 套件，並複製 config.json：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY config.json /app/config.json

# 安裝 mcpo 與多個 MCP Server
RUN pip install --no-cache-dir mcpo mcp-server-time mcp_weather_server

EXPOSE 8000

CMD ["mcpo", "--port", "8000", "--config", "/app/config.json"]
```

---

## 五、compose.yaml

```yaml
services:
  mcpo:
    build: ./mcpo
    image: mcpo
    container_name: mcpo
    ports:
      - "8000:8000"
    networks:
      - webui-net

  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: always
    networks:
      - webui-net
    ports:
      - "8080:8080" # 宿主機可用 http://localhost:8080 存取
    volumes:
      - open-webui:/app/backend/data
    environment:
      OLLAMA_BASE_URL: http://host.docker.internal:11434
    extra_hosts:
      - "host.docker.internal:host-gateway" # Linux/Raspberry Pi 需要這行才能解析

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

| 服務 | 容器名稱 | 主機埠 | 說明 |
|------|----------|--------|------|
| mcpo | mcpo | 8000 | 單一容器載入多個 MCP Server（time、weather） |
| open-webui | open-webui | 8080 | Open-WebUI 主程式 |
| cloudflared | cloudflared | - | Cloudflare Tunnel 對外連線 |

> 容器之間透過 **服務名稱** 互連，Open-WebUI 使用 `http://mcpo:8000` 即可存取所有 MCP 工具。

---

## 六、在 Open-WebUI 新增工具

**設定位置：** Open-WebUI → 管理員控制台 → 設定 → 外部工具

新增一個工具即可（因多個 MCP Server 都在同一端點）：

| 名稱 | URL | 描述 |
|------|-----|------|
| mcp-tools | `http://mcpo:8000/time` | 時間查詢 |
| mcp-tools | `http://mcpo:8000/weather` | 天氣查詢 |
---

## 七、啟動與驗證

### 啟動服務

```bash
docker compose up -d --build
```

> 若已修改 Dockerfile 或 config.json，加上 `--build` 可強制重新建置映像。

### 驗證

**1. 檢查容器狀態：**

```bash
docker ps
```

確認 `mcpo` 為 `Up`。

**2. 使用瀏覽器驗證：**

- MCP 工具：`http://<樹莓派IP>:8000/docs`

**3. 在 Open-WebUI 中測試：**

於對話中詢問「現在台北時間幾點？」或「台北明天天氣如何？」，模型應能呼叫對應工具並回覆。

---


