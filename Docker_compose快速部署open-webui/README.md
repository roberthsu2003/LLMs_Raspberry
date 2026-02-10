# 使用Docker compose,快速部署open-webui相關容器

## 以下docker是安裝在Raspberry Pi本機上

> ollama是安裝在raspberry pi本機上

主要是以network bridge模式部署,可以快速部署open-webui,cloudflare tunnel,pipeline server,MCPO server等相關容器

- **1.open-webui和 cloudflare tunnel 部署**
- **2.open-webui,cloudflare tunnel 和 MCPO 部署**
- **3.open-webui, cloudflare tunnel 和 pipeline 部署**
- **4.open-webui, cloudflare tunnel 和 pipeline 和 MCPO 部署**

## 1.open-webui和 cloudflare tunnel 部署

### 使用 Docker Compose - host network模式

![host network模式](./images/pic1.png)

如果您希望使用 Docker Compose 來管理多個容器，可以使用以下方式統一部署 Open WebUI 和 Cloudflare Tunnel。

#### 為什麼要使用 network_mode: host？


**只要三者需要共用 `127.0.0.1`，使用 `network_mode: host`**


**架構關係圖：**

```
[ Internet ]
     │
     ▼
Cloudflare Tunnel
     │  (cloudflared container)
     ▼
Raspberry Pi localhost
     │
     ├── Open WebUI : http://127.0.0.1:3000
     └── Ollama     : http://127.0.0.1:11434
```

👉 **重要觀念：**

* Tunnel **不是連 Docker 容器**
* Tunnel **是連 Pi 本機服務**

#### 建立 docker-compose.yml

請在任意資料夾建立一個檔案 `docker-compose.yml`，內容如下：

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
    command: tunnel run --token <TOKEN>

volumes:
  open-webui:
    external: true
```

📌 **這個 compose 檔案的功能，與您原本的兩個 `docker run` 指令完全等價**

#### 啟動與管理方式

**啟動服務：**

```bash
docker compose up -d
```

**檢查容器狀態：**

```bash
docker compose ps
```

**查看日誌（非常重要，用於排查問題）：**

```bash
docker compose logs -f cloudflared
```

#### 進階優化建議（選用）

等您熟悉基本操作後，可以考慮以下優化：

**1. 使用環境變數檔案（.env）管理 Token**

建立 `.env` 檔案：

```
CLOUDFLARE_TOKEN=xxxxx
```

在 `docker-compose.yml` 中使用：

```yaml
command: tunnel run --token ${CLOUDFLARE_TOKEN}
```

**2. 固定服務端口**

如果未來不使用 host network，可以為 open-webui 固定端口。

**3. 添加依賴關係**

雖然 host network 模式下不強制，但可以加上 `depends_on` 來確保啟動順序。

---

```yaml
docker compose up -d
```

### 使用 Docker Compose（推薦）- bridge network模式

如果您希望使用 Docker Compose 來管理多個容器，可以使用以下方式統一部署 Open WebUI 和 Cloudflare Tunnel。

#### 為什麼要使用 bridge network模式？

**在 Raspberry Pi 上的網路架構：**

| 容器 | 呼叫host主機 |
|------|-------------------|
| open-webui | http://host.docker.internal |
| cloudflared | http://host.docker.internal |
| ollama | ollama |

**只要三者需要共用 `127.0.0.1`，使用 `network_mode: host`**

❌ **如果改成 bridge network：**

* `127.0.0.1` 會變成「容器自己」
* cloudflared 會找不到 open-webui
* open-webui 會找不到 ollama

**架構關係圖：**

```
[ Internet ]
     │
     ▼
Cloudflare Tunnel
     │  (cloudflared container)
     ▼
Raspberry Pi localhost
     │
     ├── Open WebUI : http://127.0.0.1:3000
     └── Ollama     : http://127.0.0.1:11434
```

👉 **重要觀念：**

* Tunnel **不是連 Docker 容器**
* Tunnel **是連 Pi 本機服務**

#### 建立 docker-compose.yml

請在任意資料夾建立一個檔案 `docker-compose.yml`，內容如下：

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
    command: tunnel run --token <TOKEN>

volumes:
  open-webui:
    external: true
```

📌 **這個 compose 檔案的功能，與您原本的兩個 `docker run` 指令完全等價**

#### 啟動與管理方式

**啟動服務：**

```bash
docker compose up -d
```

**檢查容器狀態：**

```bash
docker compose ps
```

**查看日誌（非常重要，用於排查問題）：**

```bash
docker compose logs -f cloudflared
```

#### 進階優化建議（選用）

等您熟悉基本操作後，可以考慮以下優化：

**1. 使用環境變數檔案（.env）管理 Token**

建立 `.env` 檔案：

```
CLOUDFLARE_TOKEN=xxxxx
```

在 `docker-compose.yml` 中使用：

```yaml
command: tunnel run --token ${CLOUDFLARE_TOKEN}
```

**2. 固定服務端口**

如果未來不使用 host network，可以為 open-webui 固定端口。

**3. 添加依賴關係**

雖然 host network 模式下不強制，但可以加上 `depends_on` 來確保啟動順序。

---

```yaml
docker compose up -d
```



## 2.open-webui,cloudflare tunnel 和 MCPO 部署
```bash
docker compose up -d
```

## 3.open-webui, cloudflare tunnel 和 pipeline 部署
```bash
docker compose up -d
```

## 4.open-webui, cloudflare tunnel 和 pipeline 和 MCPO 部署
```bash
docker compose up -d
```
