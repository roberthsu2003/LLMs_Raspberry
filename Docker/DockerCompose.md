# Docker Compose：輕鬆管理多容器應用程式

在學會使用 Dockerfile 建置單一映像檔後，您很快會發現，一個真實的應用程式通常由多個部分組成，例如一個網站前端、一個後端 API 和一個資料庫。若要手動管理這些容器的啟動順序、網路和資料卷，將會變得非常繁瑣且容易出錯。

**Docker Compose** 就是為了解決這個問題而生的。

---

## 📋 目錄
- [Docker Compose 是什麼？](#docker-compose-是什麼)
- [為什麼我們需要 Docker Compose？](#為什麼我們需要-docker-compose)
- [安裝方式](#安裝方式)
- [Compose 檔案 (`compose.yaml`) 詳解](#compose-檔案-composeyaml-詳解)
- [常用 Docker Compose 指令](#常用-docker-compose-指令)
- [實戰範例：使用 Compose 部署 WordPress 網站](#實戰範例-使用-compose-部署-wordpress-網站)
- [總結](#總結)

---

## 🤔 Docker Compose 是什麼？

Docker Compose 是一個用來**定義和執行多容器 Docker 應用程式**的工具。

您可以透過一個 YAML 檔案 (`compose.yaml`) 來設定應用程式所需的所有**服務 (services)**、**網路 (networks)** 和**資料卷 (volumes)**。然後，只需一個簡單的指令，就能根據您的設定檔，一次啟動或關閉所有相關的容器。

把它想像成一個**交響樂團的指揮**：
-   每個**容器** (Container) 就像一個**樂手**。
-   `docker run` 指令只能一次指揮一位樂手。
-   **Docker Compose** 就像指揮家，拿著**樂譜 (`compose.yaml`)**，只需揮動指揮棒 (`docker compose up`)，就能讓整個樂團（您的應用程式）和諧地演奏起來。

---

## ✨ 為什麼我們需要 Docker Compose？

1.  **簡化多容器管理**
    您不再需要輸入一長串帶有各種參數的 `docker run` 指令。所有設定都集中在一個 YAML 檔案中，清晰明瞭。

2.  **應用程式架構即程式碼 (Architecture as Code)**
    `compose.yaml` 檔案本身就是一份應用程式架構的說明文件，可以與您的專案程式碼一起納入版本控制 (如 Git)，方便團隊協作和追蹤變更。

3.  **環境一致性**
    團隊中的每位成員都可以使用同一個 `compose.yaml` 檔案，一鍵啟動完全相同的開發環境，徹底解決「在我電腦上可以跑」的經典問題。

4.  **內建服務探索 (Service Discovery)**
    Compose 會為您的應用程式建立一個專屬的網路。在該網路中，每個服務都可以直接使用**服務名稱**作為主機名稱 (hostname) 來互相存取。例如，您的 `web` 服務可以直接連接到 `db:5432` 來存取資料庫服務。

---

## 🔧 安裝方式

現代版本的 Docker (無論是 Docker Desktop 或透過官方腳本安裝的 Docker Engine) 都已經**內建了 Docker Compose** 作為一個 CLI 插件。

您可以透過以下指令來驗證是否安裝成功：
```bash
docker compose version
```
如果看到版本號，代表您已經可以開始使用了。

---

## 📄 Compose 檔案 (`compose.yaml`) 詳解

Compose 檔案是一個 YAML 格式的文字檔，預設檔名為 `compose.yaml` 或 `docker-compose.yml`。

一個基本的 `compose.yaml` 結構如下：
```yaml
# 檔案的最頂層，定義了所有服務
services:
  # 服務 A 的定義 (例如：web server)
  web:
    build: .
    ports:
      - "8080:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf

  # 服務 B 的定義 (例如：database)
  db:
    image: postgres:14-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - db-data:/var/lib/postgresql/data

# 統一管理具名資料卷
volumes:
  db-data:

# 統一管理網路
networks:
  default:
    driver: bridge
```

### 核心 `services` 設定詳解

在 `services` 區塊下，您可以定義多個服務，每個服務代表一個容器。以下是一些最常用的設定鍵：

-   `image: <image_name>`：指定要使用的 Docker **映像檔**，例如 `nginx:alpine`。Compose 會先在本地尋找，若找不到則會從 Docker Hub 拉取。
-   `build: <path>`：指定包含 Dockerfile 的**路徑**。Compose 會使用該 Dockerfile 來**建置**一個客製化映像檔。例如 `build: .`。
-   `ports: ["<HOST_PORT>:<CONTAINER_PORT>"]`：將主機的連接埠**映射**到容器的連接埠。
-   `volumes: ["<SOURCE>:<TARGET>"]`：**掛載**資料卷。來源可以是主機的路徑 (`./code:/app`) 或是一個具名資料卷 (`db-data:/var/lib/mysql`)。
-   `environment: ["<KEY>=<VALUE>"]`：設定**環境變數**。
-   `env_file: <file_path>`：從一個檔案讀取環境變數。
-   `depends_on: [<service_name>]`：設定服務間的**依賴關係**，這會影響服務的啟動順序。例如，網站服務應該在資料庫服務啟動後才啟動。
-   `networks: [<network_name>]`：將服務連接到指定的**網路**。
-   `command: <command>`：**覆蓋**映像檔預設的 `CMD` 指令。
-   `restart: <policy>`：設定容器的**重啟策略**，例如 `always` (總是重啟), `on-failure` (失敗時重啟), `unless-stopped` (除非手動停止，否則總是重啟)。

---

## ⌨️ 常用 Docker Compose 指令

所有指令都在包含 `compose.yaml` 檔案的目錄下執行。

-   `docker compose up`
    最常用的指令。它會一次性建置、(重新)建立、啟動並附加到所有服務的容器上。
    -   加上 `-d` (`--detach`) 旗標，可以在**背景執行**。
    -   加上 `--build` 旗標，會在啟動前強制重新建置映像檔。

-   `docker compose down`
    停止並**移除**所有由 `up` 指令建立的容器和網路。
    -   加上 `--volumes` 旗標，會連同具名資料卷一起移除。

-   `docker compose ps`
    列出目前專案中所有容器的狀態。

-   `docker compose logs`
    查看所有服務的日誌輸出。
    -   加上 `-f` (`--follow`) 可以持續追蹤新的日誌。
    -   `docker compose logs <service_name>` 可以只看特定服務的日誌。

-   `docker compose exec <service_name> <command>`
    在一個**正在執行**的服務容器中執行一個指令。
    -   例如：`docker compose exec web bash` 可以在 `web` 服務中開啟一個互動式的 shell。

-   `docker compose build`
    單獨建置或重新建置服務的映像檔。

-   `docker compose pull`
    拉取所有服務所需的最新映像檔。

-   `docker compose stop` / `start` / `restart`
    停止、啟動或重啟專案中的所有服務。

---

## 🚀 實戰範例：使用 Compose 部署 WordPress 網站

WordPress 是一個非常流行的內容管理系統，它需要一個 PHP 執行環境和一個 MySQL 資料庫。這正是 Docker Compose 的完美應用場景。

#### 步驟 1: 建立 `compose.yaml` 檔案
```yaml
services:
  # 資料庫服務
  db:
    image: mysql:8.0
    container_name: wordpress_db
    # 使用具名資料卷來持久化資料庫檔案
    volumes:
      - db_data:/var/lib/mysql
    # 設定資料庫環境變數 (請在生產環境中使用更安全的密碼)
    environment:
      MYSQL_ROOT_PASSWORD: somerootpassword
      MYSQL_DATABASE: wordpress
      MYSQL_USER: wordpress
      MYSQL_PASSWORD: wordpresspassword
    restart: unless-stopped

  # WordPress 服務
  wordpress:
    # 依賴 db 服務，確保 db 先啟動
    depends_on:
      - db
    image: wordpress:latest
    container_name: wordpress_web
    # 將主機的 8080 連接埠映射到容器的 80 連接埠
    ports:
      - "8080:80"
    # 設定 WordPress 連接資料庫所需的環境變數
    # 注意：WORDPRESS_DB_HOST 的值是我們的資料庫服務名稱 "db"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: wordpress
      WORDPRESS_DB_PASSWORD: wordpresspassword
      WORDPRESS_DB_NAME: wordpress
    restart: unless-stopped

# 在檔案最下方定義具名資料卷
volumes:
  db_data:
```

#### 步驟 2: 啟動應用程式
在存放 `compose.yaml` 的目錄中，執行：
```bash
docker compose up -d
```
Compose 會自動：
1.  拉取 `mysql:8.0` 和 `wordpress:latest` 映像檔。
2.  建立一個名為 `db_data` 的具名資料卷。
3.  建立一個專屬的網路，讓 `wordpress` 和 `db` 服務可以互相通訊。
4.  先啟動 `db` 容器，再啟動 `wordpress` 容器。

#### 步驟 3: 設定 WordPress
打開瀏覽器，訪問 `http://localhost:8080`。您會看到 WordPress 的安裝畫面。按照畫面提示完成安裝即可。

您的所有文章、設定都會儲存在 `db` 容器中，而資料庫檔案本身則被安全地存放在 Docker 的 `db_data` 資料卷裡，即使您執行 `docker compose down`，資料也不會遺失。

---

## 📝 總結

Docker Compose 是每一位 Docker 使用者都應該掌握的關鍵工具。它極大地簡化了本地開發和測試環境的設定，讓管理由多個服務組成的複雜應用程式變得輕而易舉。

透過將您的應用程式架構編寫在 `compose.yaml` 檔案中，您不僅提升了開發效率，也為後續的部署和維護打下了堅實的基礎。