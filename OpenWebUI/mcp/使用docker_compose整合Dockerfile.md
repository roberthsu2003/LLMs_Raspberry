# 使用 Docker Compose 整合 Dockerfile

## 📋 目錄

- [前言](#前言)
- [一、專案結構建議](#一專案結構建議)
- [二、Dockerfile](#二dockerfile)
- [三、docker-compose.yml](#三docker-composeyml)
- [四、啟動方式](#四啟動方式)
- [五、執行流程說明](#五執行流程說明)
- [六、驗證服務](#六驗證服務)

---

## 前言

這一步是把「單一容器」升級成「可管理的服務架構」。

若你已經具備：

- ✅ Dockerfile（mcpo-server）
- ✅ 固定的 network（webui-net）
- ✅ 未來可能還要加入 Open-WebUI

建議改用 `docker-compose.yml` 統一管理。

## 下方是實作範例目錄連結

[實作範例目錄連結](./實作範例/使用docker_compose整合Dockerfile)
---

## 一、專案結構建議

建議的專案目錄結構：

```
mcpo-project/
├── docker-compose.yml
└── mcpo/
    └── Dockerfile
```

---

## 二、Dockerfile

將 Dockerfile 放在 `mcpo/` 目錄內：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir mcpo mcp-server-time

EXPOSE 8000

CMD ["mcpo", "--port", "8000", "--", "mcp-server-time", "--local-timezone=Asia/Taipei"]
```

---

## 三、docker-compose.yml(單獨建立mcpo容器)

在專案根目錄建立 `docker-compose.yml`：

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

networks:
  webui-net:
    name: webui-net
    driver: bridge
```

**說明：**

- `image: mcpo`：只要有build就要指定映像名稱為 `mcpo`,如果沒有寫會產生檔案名稱為目錄名稱的映像
- `build: ./mcpo`：指定 Dockerfile 所在目錄
- `networks: webui-net`：與 Open-WebUI 使用相同網路，方便互通
- `name: webui-net`：網路名稱固定為 `webui-net`，可與既有 Open-WebUI 共用

---

## 三、docker-compose.yml(整合open-webui,mcpo容器,cloudflare tunnel)

[整合open-webui,mcpo容器,cloudflare tunnel](./整合使用open-webui和cloudflare_tunnel.md)


## 四、啟動方式

在專案根目錄執行：

```bash
docker compose up -d
```

> **注意：** 新版 Docker 使用 `docker compose`（無連字號），而非 `docker-compose`。

### 若已修改 Dockerfile，需要重新建置

不需手動刪除映像，執行：

```bash
docker compose up -d --build
```

`--build` 會強制重新建置映像後再啟動。

---

## 五、執行流程說明

當你執行 `docker compose up -d` 時，Docker 會依序進行：

### Step 1：建立或取得 network

若 `webui-net` 不存在，Compose 會自動建立；若已存在（例如由 Open-WebUI 建立），則直接使用。

### Step 2：Build image

等同於：

```bash
docker build -t mcpo-project-mcpo ./mcpo
```

### Step 3：建立並啟動 container

等同於：

```bash
docker run -d --name mcpo --network webui-net -p 8000:8000 mcpo-project-mcpo
```

---

## 六、驗證服務

### 檢查容器狀態

```bash
docker ps
```

確認 `mcpo` 容器狀態為 `Up`。

### 使用瀏覽器驗證 Swagger UI

開啟：`http://<樹莓派IP>:8000/docs`

應能看到 Swagger UI 介面，以及 `/get_current_time`、`/convert_time` 兩個 endpoint。

---
