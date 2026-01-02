# Docker Volume：讓您的容器資料不再消失

Docker 容器天生就是**短暫的 (ephemeral)**。當一個容器被停止並移除後，它在執行期間寫入其內部檔案系統的所有資料都會跟著消失。對於需要保存狀態的應用程式（例如資料庫、使用者上傳的檔案、日誌等）來說，這是一個致命的問題。

**Docker Volume (資料卷)** 就是為了解決這個問題而生的核心機制，它讓資料的生命週期可以獨立於容器之外，實現資料的持久化。

---

## 📋 目錄
- [問題：容器的無狀態性](#問題-容器的無狀態性)
- [解決方案：Docker 的三種掛載模式](#解決方案-docker-的三種掛載模式)
  - [1. Volumes (資料卷) - 官方推薦](#1-volumes-資料卷---官方推薦)
  - [2. Bind Mounts (綁定掛載)](#2-bind-mounts-綁定掛載)
  - [3. tmpfs Mounts (記憶體掛載)](#3-tmpfs-mounts-記憶體掛載)
- [如何在 Docker Compose 中使用](#如何在-docker-compose-中使用)
- [使用 Docker CLI 管理 Volumes](#使用-docker-cli-管理-volumes)
- [實戰範例：為資料庫實現資料持久化](#實戰-範例-為資料庫實現資料持久化)
- [備份、還原與遷移資料](#備份-還原與遷移資料)
- [總結：如何選擇？](#總結-如何選擇)

---

## 🤔 問題：容器的無狀態性

想像一下，您啟動了一個 PostgreSQL 資料庫容器，並在裡面儲存了重要的使用者資料。
```bash
docker run -d --name my-db postgres
```
某天，您因為需要升級版本或其他原因，移除了這個容器：
```bash
docker stop my-db
docker rm my-db
```
糟糕！您儲存的所有使用者資料都隨著容器的移除而**永久消失**了。這是因為資料是寫在容器的可寫層中，它的生命週期與容器綁定。

---

## ✨ 解決方案：Docker 的三種掛載模式

為了解決這個問題，Docker 允許我們將一塊儲存空間「掛載」到容器內部。這塊儲存空間位於主機上，獨立於容器存在，因此即使容器被刪除，資料依然安全。Docker 提供了三種掛載模式：

### 1. Volumes (資料卷) - 官方推薦

**這是 Docker 持久化資料的首選方式。**

-   **是什麼**：Volume 是由 **Docker 管理**的、儲存在主機檔案系統上的一個目錄（在 Linux 上通常是 `/var/lib/docker/volumes/`）。當您建立一個 Volume 時，您只需給它一個名字，Docker 會處理其在主機上的具體儲存位置。
-   **優點**：
    -   **易於管理**：可以透過 Docker CLI 指令 (`docker volume create`, `ls`, `rm`) 進行管理。
    -   **更安全**：Volume 與主機的核心檔案系統隔離，非 Docker 程序不會輕易修改到它。
    -   **跨平台相容**：在 Linux 和 Windows 容器上都能良好運作。
    -   **易於備份與遷移**：管理和遷移 Volume 比管理主機上散落各處的目錄更簡單。
    -   **效能更佳**：在某些平台上，Volume 的 I/O 效能優於 Bind Mount。
    -   可以由多個容器**共享**。

-   **如何使用**：
    -   **具名資料卷 (Named Volume)** - **推薦**
        ```bash
        # 1. 建立一個 Volume
        docker volume create my-data

        # 2. 執行容器時掛載它
        docker run -d --name my-container -v my-data:/app/data nginx
        ```
    -   **匿名資料卷 (Anonymous Volume)** - Docker 會自動生成一個隨機名稱，不易管理，不推薦。
        ```bash
        # -v 後面只提供容器內路徑，Docker 會自動建立一個匿名 Volume
        docker run -d --name another-container -v /app/data nginx
        ```

### 2. Bind Mounts (綁定掛載)

-   **是什麼**：將主機上的一個**指定路徑**（檔案或目錄）直接映射到容器內部的一個路徑。
-   **優點**：
    -   **開發方便**：非常適合在開發環境中使用。您可以將專案的原始碼目錄掛載到容器中，在主機上修改程式碼後，容器內能**立即看到變更**，實現熱重載 (Hot Reloading)。
    -   **共享設定檔**：可以方便地將主機上的設定檔共享給容器使用。

-   **如何使用**：
    ```bash
    # 將主機當前目錄下的 `src` 子目錄掛載到容器的 `/app` 目錄
    docker run -d -v $(pwd)/src:/app my-node-app
    ```

-   **缺點**：
    -   **可移植性差**：它依賴於主機上固定的目錄結構，在不同環境中可能需要修改路徑。
    -   **權限問題**：容易出現主機和容器間的檔案權限衝突 (UID/GID 不匹配)。
    -   **安全風險**：容器可以修改主機的檔案系統，包括系統重要檔案，帶來安全隱患。

### 3. tmpfs Mounts (記憶體掛載)

-   **是什麼**：將資料直接儲存在主機的**記憶體**中，完全不會寫入硬碟。
-   **優點**：
    -   **速度極快**：因為是記憶體 I/O，讀寫速度非常快。
    -   **安全性**：當容器停止時，記憶體中的資料會立刻消失，適合存放無需持久化的敏感性資料。

-   **如何使用**：
    ```bash
    # 在容器的 /app/cache 目錄下建立一個 tmpfs 掛載
    docker run -d --name my-tmpfs-container --tmpfs /app/cache nginx
    ```
-   **適用場景**：不常用，僅適用於特定場景，如臨時快取、密鑰等。

---

## 📄 如何在 Docker Compose 中使用

在 `compose.yaml` 中使用資料持久化非常直觀。

```yaml
services:
  # 使用 Bind Mount 進行開發
  web:
    build: .
    volumes:
      # 將當前目錄掛載到容器的 /app
      # 實現程式碼熱重載
      - .:/app

  # 使用 Volume 持久化資料
  db:
    image: postgres:14
    volumes:
      # 掛載名為 "db-data" 的具名資料卷
      - db-data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=mysecretpassword

# 在檔案最下方聲明頂層的 Volume
# 這樣 Docker Compose 會為我們管理這個 Volume
volumes:
  db-data:
```

---

## ⌨️ 使用 Docker CLI 管理 Volumes

-   **建立 Volume**
    `docker volume create <volume_name>`

-   **列出所有 Volume**
    `docker volume ls`

-   **查看 Volume 詳細資訊**（包含在主機上的實際路徑）
    `docker volume inspect <volume_name>`

-   **移除 Volume**（必須先停止並移除所有使用該 Volume 的容器）
    `docker volume rm <volume_name>`

-   **清理無用的 Volume**（移除所有未被任何容器使用的 Volume）
    `docker volume prune`

---

## 🚀 實戰範例：為資料庫實現資料持久化

讓我們實際操作一次，感受 Volume 的威力。

1.  **建立一個具名 Volume**
    ```bash
    docker volume create postgres-db-data
    ```

2.  **啟動 PostgreSQL 容器並掛載 Volume**
    ```bash
    docker run --name my-postgres -d \
      -e POSTGRES_PASSWORD=mysecretpassword \
      -v postgres-db-data:/var/lib/postgresql/data \
      postgres:14
    ```
    現在，所有資料庫檔案都會被寫入 `postgres-db-data` 這個 Volume 中。

3.  **模擬資料操作** (此步驟可選，用於驗證)
    您可以連入資料庫，建立一個測試資料表。

4.  **移除容器**
    ```bash
    docker stop my-postgres
    docker rm my-postgres
    ```
    此時，雖然容器被移除了，但 `postgres-db-data` 這個 Volume 及其中的資料仍然存在。

5.  **重新啟動一個新容器，並掛載同一個 Volume**
    ```bash
    docker run --name new-postgres -d \
      -e POSTGRES_PASSWORD=mysecretpassword \
      -v postgres-db-data:/var/lib/postgresql/data \
      postgres:14
    ```

6.  **驗證資料**
    當您連入這個 `new-postgres` 容器時，您會驚喜地發現，之前建立的測試資料表**依然存在**！資料持久化成功。

---

## 🔄 備份、還原與遷移資料

Volume 的一大好處是易於備份。基本思路是啟動一個新容器，同時掛載您想備份的 Volume 和一個用於存放備份檔的本地目錄，然後在容器中執行壓縮指令。

**備份 `my-data` Volume 到目前目錄的 `backup.tar`：**
```bash
docker run --rm -v my-data:/data -v $(pwd):/backup ubuntu tar cvf /backup/backup.tar /data
```

**還原備份到一個新的 Volume `restored-data`：**
```bash
# 1. 建立新 Volume
docker volume create restored-data

# 2. 執行還原容器
docker run --rm -v restored-data:/data -v $(pwd):/backup ubuntu bash -c "cd /data && tar xvf /backup/backup.tar --strip 1"
```

---

## ✅ 總結：如何選擇？

-   **Volumes (資料卷)**：
    -   **適用場景**：**生產環境**、需要持久化儲存的任何資料 (資料庫檔案、使用者上傳內容、應用程式狀態)。這是**最佳實踐**。
-   **Bind Mounts (綁定掛載)**：
    -   **適用場景**：**開發環境**、需要將主機程式碼或設定檔同步到容器中。
-   **tmpfs Mounts (記憶體掛載)**：
    -   **適用場景**：**特殊用途**、無需持久化且對效能極度敏感的臨時資料。

掌握 Docker Volume 是執行**有狀態 (stateful)** 應用程式的基礎，也是從「玩 Docker」到「用 Docker 於生產」的關鍵一步。