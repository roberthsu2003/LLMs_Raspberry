# 使用 Docker Compose 快速部署 Open-WebUI 相關容器

## 📋 目錄

- [前言](#前言)
- [部署選項一覽](#部署選項一覽)
- [選項 1：Open-WebUI + Cloudflare Tunnel](#選項-1open-webui--cloudflare-tunnel)
- [選項 2：Open-WebUI + Cloudflare Tunnel + MCPO](#選項-2open-webui--cloudflare-tunnel--mcpo)
- [選項 3：Open-WebUI + Cloudflare Tunnel + Pipeline](#選項-3open-webui--cloudflare-tunnel--pipeline)
- [選項 4：Open-WebUI + Cloudflare Tunnel + Pipeline + MCPO](#選項-4open-webui--cloudflare-tunnel--pipeline--mcpo)

---

## 前言

本教學假設 **Docker 與 Ollama 已安裝在 Raspberry Pi 本機**。

採用 **bridge network** 模式為主，可快速部署以下組合：

- Open-WebUI
- Cloudflare Tunnel（對外曝光服務）
- Pipeline Server
- MCPO Server

---

## 部署選項一覽

| 選項 | 包含服務 | 適用情境 |
|------|----------|----------|
| **1** | Open-WebUI + Cloudflare Tunnel | 基本部署，對外連線 |
| **2** | Open-WebUI + Cloudflare Tunnel + MCPO | 需要 MCP 工具（如時間查詢） |
| **3** | Open-WebUI + Cloudflare Tunnel + Pipeline | 需要自訂 Pipeline 流程 |
| **4** | Open-WebUI + Cloudflare Tunnel + Pipeline + MCPO | 完整功能一次部署 |

---

## 選項 1：Open-WebUI + Cloudflare Tunnel

### 方法 A：Host Network 模式

![host network 模式](./images/pic1.png)

適合需要 **Open-WebUI、Cloudflare Tunnel、Ollama 共用 `127.0.0.1`** 的情境。

**架構關係圖：**

```
[ Internet ]
     │
     ▼
Cloudflare Tunnel (cloudflared)
     │
     ▼
host 主機
     ├── Open-WebUI : http://127.0.0.1:8080
     └── Ollama     : http://127.0.0.1:11434
```

> **重要觀念：** Tunnel 連線目標是 **host 主機上的服務**，不是 cloudflared 容器本身。

#### 建立 docker-compose.yml

```yaml
version: "3.9"

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: always
    network_mode: host
    volumes:
      - open-webui:/app/backend/data
    environment:
      OLLAMA_BASE_URL: http://127.0.0.1:11434

  cloudflared:
    image: cloudflare/cloudflared:latest
    container_name: cloudflared
    restart: unless-stopped
    network_mode: host
    command: tunnel run --token <YOUR_CLOUDFLARE_TOKEN>

volumes:
  open-webui:
    external: true
```

#### 啟動與管理

```bash
# 啟動
docker compose up -d

# 檢查狀態
docker compose ps

# 查看 cloudflared 日誌（排錯用）
docker compose logs -f cloudflared
```

#### 進階建議（選用）

**1. 使用 .env 管理 Token**

建立 `.env`：

```
CLOUDFLARE_TOKEN=your_token_here
```

在 docker-compose.yml 中改為：

```yaml
command: tunnel run --token ${CLOUDFLARE_TOKEN}
```

**2. 添加依賴關係**

可加上 `depends_on` 確保啟動順序（host 模式下非必要）。

---

### 方法 B：Bridge Network 模式（推薦）

![bridge network 模式](./images/pic2.png)

容器各自有獨立網路命名空間，透過 Docker 網路互通。較易與其他服務（MCPO、Pipeline）整合。

#### 建立 docker-compose.yml

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
    extra_hosts:
      - "host.docker.internal:host-gateway"

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

#### Cloudflare Tunnel 設定

在 Cloudflare Dashboard 的 Tunnel 設定中，將 Public Hostname 指向：

```
http://open-webui:8080
```

#### 啟動與管理

```bash
docker compose up -d
docker compose ps
docker compose logs -f cloudflared
```

---

## 選項 2：Open-WebUI + Cloudflare Tunnel + MCPO

### 專案結構

```
mcpo-project/
├── docker-compose.yml
├── .env
└── mcpo/
    └── Dockerfile
```

### Dockerfile（mcpo/Dockerfile）

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir mcpo mcp-server-time

EXPOSE 8000

CMD ["mcpo", "--port", "8000", "--", "mcp-server-time", "--local-timezone=Asia/Taipei"]
```

### docker-compose.yml

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

  mcpo:
    build: ./mcpo
    container_name: mcpo
    restart: always
    networks:
      - webui-net
    ports:
      - "8000:8000"

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

### Cloudflare Tunnel 設定

Public Hostname 指向：`http://open-webui:8080`

### 啟動方式

```bash
docker compose up -d --build
```

---

## 選項 3：Open-WebUI + Cloudflare Tunnel + Pipeline

> **注意：** 此設定**不**對外暴露 Pipeline 的 9099 埠，僅能透過 Docker 內部網路存取。
> Open-WebUI 連接 Pipeline 時，請使用：`http://pipelines:9099`

> **注意：** Pipeline 的 `extra_hosts` 不可移除，否則無法解析 `host.docker.internal`，也就無法連線到 Raspberry Pi 上的 Ollama。

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
    extra_hosts:
      - "host.docker.internal:host-gateway"

  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    container_name: pipelines
    restart: always
    networks:
      - webui-net
    volumes:
      - pipelines:/app/pipelines
    extra_hosts:
      - "host.docker.internal:host-gateway"

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
  pipelines:
    external: true

networks:
  webui-net:
    name: webui-net
    driver: bridge
```

### Open-WebUI Pipeline 設定

在 Open-WebUI 管理員控制台 → Pipelines 中，將 Pipeline 的 URL 設為：

```
http://pipelines:9099
```

---

## 選項 4：Open-WebUI + Cloudflare Tunnel + Pipeline + MCPO

完整部署所有服務。

### 專案結構

```
full-project/
├── docker-compose.yml
├── .env
└── mcpo/
    └── Dockerfile
```

### docker-compose.yml

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

  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    container_name: pipelines
    restart: always
    networks:
      - webui-net
    volumes:
      - pipelines:/app/pipelines
    extra_hosts:
      - "host.docker.internal:host-gateway"

  mcpo:
    build: ./mcpo
    container_name: mcpo
    restart: always
    networks:
      - webui-net
    ports:
      - "8000:8000"

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
  pipelines:
    external: true

networks:
  webui-net:
    name: webui-net
    driver: bridge
```

### 設定重點

| 項目 | 設定值 |
|------|--------|
| **Pipeline URL**（Open-WebUI 內） | `http://pipelines:9099` |
| **MCP 工具 URL**（Open-WebUI 內） | `http://mcpo:8000` |
| **Cloudflare Tunnel** | 指向 `http://open-webui:8080` |

### 啟動方式

```bash
docker compose up -d --build
```

---
