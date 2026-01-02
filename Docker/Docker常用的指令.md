# Docker 常用指令大全 (Cheat Sheet)

這是一份 Docker 常用指令的速查表，旨在幫助您快速找到日常開發和維護中需要用到的指令。文件將指令分為映像檔、容器、Compose、網路與資料卷、系統管理等類別。

---

## 💻 容器管理 (Container Management)

管理容器的生命週期，從建立、執行到停止和移除。

| 指令 | 說明 |
| :--- | :--- |
| `docker run [OPTIONS] IMAGE [COMMAND]` | 根據指定的映像檔建立並啟動一個新容器。 |
| `docker ps` | 列出目前**正在執行**的容器。 |
| `docker start [CONTAINER]` | 啟動一個或多個已經停止的容器。 |
| `docker stop [CONTAINER]` | 停止一個或多個正在執行的容器。 |
| `docker restart [CONTAINER]` | 重啟一個或多個容器。 |
| `docker rm [CONTAINER]` | 移除一個或多個已經停止的容器。 |
| `docker logs [CONTAINER]` | 獲取容器的日誌。 |
| `docker exec [OPTIONS] [CONTAINER] [COMMAND]` | 在一個正在執行的容器內部執行指令。 |
| `docker inspect [CONTAINER]` | 顯示一個或多個容器的詳細資訊。 |

#### `docker run` 常用選項

-   `-d`：在背景 (detached mode) 執行容器。
-   `-p <HOST_PORT>:<CONTAINER_PORT>`：將主機的連接埠映射到容器的連接埠。
-   `-it`：以互動模式 (`-i`) 和 TTY (`-t`) 執行容器，通常用於進入容器的 shell。
-   `--name <CONTAINER_NAME>`：為容器指定一個名稱。
-   `--rm`：當容器停止時自動將其移除。
-   `-v <SOURCE>:<TARGET>`：掛載一個資料卷或綁定一個主機目錄。
-   `-e <KEY>=<VALUE>`：設定環境變數。

**範例：**
```bash
# 啟動一個名為 my-nginx 的 Nginx 容器，並將主機的 8080 連接埠映射到容器的 80 連接埠
docker run -d -p 8080:80 --name my-nginx nginx

# 進入一個 Ubuntu 容器的 bash shell
docker run -it --rm ubuntu bash
```

#### `docker ps` 常用選項

-   `-a` 或 `--all`：列出所有容器，包括已經停止的。
-   `-q` 或 `--quiet`：只顯示容器的 ID。

#### `docker rm` 常用選項

-   `-f` 或 `--force`：強制移除一個正在執行的容器。

#### `docker logs` 常用選項

-   `-f` 或 `--follow`：持續追蹤日誌輸出。
-   `--tail <NUMBER>`：只顯示最後 N 行的日誌。

**範例：**
```bash
# 持續追蹤 my-nginx 容器的日誌
docker logs -f my-nginx

# 移除所有已停止的容器
docker rm $(docker ps -aqf "status=exited")
```

---

## 🖼️ 映像檔管理 (Image Management)

管理 Docker 映像檔，包括建置、拉取、推送和移除。

| 指令 | 說明 |
| :--- | :--- |
| `docker build [OPTIONS] PATH` | 根據指定路徑下的 Dockerfile 建置一個映像檔。 |
| `docker pull [IMAGE]` | 從倉庫 (Registry，預設為 Docker Hub) 拉取一個映像檔。 |
| `docker images` 或 `docker image ls` | 列出本地儲存的所有映像檔。 |
| `docker rmi [IMAGE]` 或 `docker image rm [IMAGE]` | 移除一個或多個映像檔。 |
| `docker tag [SOURCE_IMAGE] [TARGET_IMAGE]` | 為映像檔建立一個新的標籤 (tag)。 |
| `docker push [IMAGE]` | 將一個映像檔推送到遠端倉庫。 |
| `docker history [IMAGE]` | 顯示一個映像檔的建置歷史。 |
| `docker inspect [IMAGE]` | 顯示一個映像檔的詳細資訊。 |

#### `docker build` 常用選項

-   `-t <NAME>:<TAG>` 或 `--tag <NAME>:<TAG>`：為建置的映像檔指定名稱和標籤。
-   `--no-cache`：建置時不使用任何快取。

**範例：**
```bash
# 使用當前目錄的 Dockerfile 建置一個名為 my-app:1.0 的映像檔
docker build -t my-app:1.0 .

# 移除所有懸空 (dangling) 的映像檔
docker rmi $(docker images -qf "dangling=true")
```

---

## 🚀 Docker Compose (多容器管理)

使用 `compose.yaml` 檔案來管理多容器應用程式。

| 指令 | 說明 |
| :--- | :--- |
| `docker compose up` | 根據 `compose.yaml` 建立並啟動所有服務。 |
| `docker compose down` | 停止並移除所有服務的容器、網路。 |
| `docker compose ps` | 列出 Compose 專案中的所有容器。 |
| `docker compose logs` | 查看所有服務的日誌。 |
| `docker compose exec [SERVICE] [COMMAND]` | 在指定的服務容器中執行指令。 |
| `docker compose build` | 建置或重新建置所有服務的映像檔。 |
| `docker compose pull` | 拉取所有服務所需的映像檔。 |
| `docker compose stop` / `start` / `restart` | 停止 / 啟動 / 重啟所有服務。 |

**範例：**
```bash
# 在背景啟動所有服務
docker compose up -d

# 停止並移除所有資源，包含資料卷
docker compose down --volumes

# 進入 `web` 服務的 shell
docker compose exec web sh
```

---

## 🔗 網路與資料卷 (Network & Volume Management)

管理 Docker 的網路和資料卷，實現容器間通訊和資料持久化。

| 類別 | 指令 | 說明 |
|:--- |:---|:---|
| **網路** | `docker network ls` | 列出所有網路。 |
| | `docker network create [NETWORK]` | 建立一個新的網路。 |
| | `docker network inspect [NETWORK]` | 查看網路的詳細資訊。 |
| | `docker network rm [NETWORK]` | 移除一個或多個網路。 |
| | `docker network prune` | 移除所有未被使用的網路。 |
| **資料卷** | `docker volume ls` | 列出所有資料卷。 |
| | `docker volume create [VOLUME]` | 建立一個新的資料卷。 |
| | `docker volume inspect [VOLUME]` | 查看資料卷的詳細資訊。 |
| | `docker volume rm [VOLUME]` | 移除一個或多個資料卷。 |
| | `docker volume prune` | 移除所有未被使用的資料卷。 |

---

## ⚙️ 系統管理 (System Management)

查看 Docker 系統資訊和清理佔用的資源。

| 指令 | 說明 |
| :--- | :--- |
| `docker info` | 顯示 Docker 系統的全域資訊。 |
| `docker version` | 顯示 Docker 的版本資訊。 |
| `docker system df` | 顯示 Docker 佔用的磁碟空間。 |
| `docker system prune` | 清理系統中所有未使用的資源。 |

#### `docker system prune`
這是一個強大但需要謹慎使用的指令。

-   `docker system prune`：
    -   移除所有已停止的容器。
    -   移除所有未被任何容器使用的網路。
    -   移除所有懸空 (dangling) 的映像檔。
    -   移除所有懸空的建置快取。

-   `docker system prune -a` 或 `--all`：
    -   在上述基礎上，額外移除**所有未被任何容器使用**的映像檔。

-   `docker system prune --volumes`：
    -   在 `prune` 的基礎上，額外移除所有未被任何容器使用的**資料卷**。

> **⚠️ 警告**：`docker system prune -a --volumes` 是清理磁碟空間的終極手段，它會刪除大量未使用的資源。在執行前，請務必確認沒有您想保留但暫時未使用的映像檔或資料卷。
