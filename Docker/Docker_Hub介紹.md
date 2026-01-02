# Docker Hub 介紹：您的 Docker 映像檔註冊中心

在上一份文件中，我們學會了如何在 Raspberry Pi 上安裝 Docker。現在，我們來認識一下 Docker 生態系統中一個至關重要的部分：**Docker Hub**。

---

## 1. Docker Hub 是什麼？

![Docker Logo](https://www.docker.com/wp-content/uploads/2022/03/Moby-logo.png)

簡單來說，**Docker Hub 就像是 Docker 映像檔的 GitHub**。

-   **是一個雲端服務**：它是一個由 Docker 公司維護的雲端儲存庫 (Registry)，專門用來儲存、分享和管理 Docker 映像檔。
-   **預設的映像檔來源**：當您執行 `docker pull` 或 `docker run` 一個本地不存在的映像檔時，Docker 預設會從 Docker Hub 上尋找並下載。
-   **社群與官方的集散地**：它不僅是個人開發者分享作品的地方，也是各大軟體公司發布官方版本的平台。

把 Docker Hub 想像成一個巨大的線上圖書館，裡面收藏了數百萬個預先做好的「軟體安裝包」（也就是 Docker 映像檔），您可以隨時取用。

---

## 📋 目錄
- [為什麼我們需要 Docker Hub？](#為什麼我們需要-docker-hub)
- [核心概念](#核心概念)
- [常用 Docker Hub 指令](#常用-docker-hub-指令)
- [實戰 1：搜尋並執行官方映像檔](#實戰-1-搜尋並執行官方映像檔)
- [實戰 2：建立並推送您自己的映像檔](#實戰-2-建立並推送您自己的映像檔)
- [總結](#總結)

---

## 🤔 為什麼我們需要 Docker Hub？

1.  **快速取得官方軟體**
    您不再需要從頭手動安裝和設定複雜的軟體（例如資料庫、Web 伺服器）。可以直接從 Docker Hub 下載由官方維護、安全可靠的映像檔。例如：`python`, `node`, `mysql`, `nginx`, `ubuntu` 等。

2.  **版本控制與重現性**
    Docker Hub 上的映像檔可以透過 **標籤 (Tag)** 來管理不同版本。這確保您和您的團隊成員使用的都是完全相同的軟體環境，避免了「在我電腦上可以跑」的窘境。

3.  **分享您的應用程式**
    您可以將自己開發的應用程式打包成一個映像檔，推送到 Docker Hub，這樣任何地方的任何人都可以輕鬆地一鍵下載並執行您的應用程式。

4.  **私有儲存庫 (Private Repositories)**
    除了公開分享，Docker Hub 也允許您建立私有儲存庫，用來存放公司內部或個人的敏感專案，只有授權的成員才能存取。

5.  **自動化建置 (Automated Builds)**
    Docker Hub可以與您的 GitHub 或 Bitbucket 帳號連結。當您更新原始碼時，Docker Hub可以自動抓取最新的程式碼，並建置成新的 Docker 映像檔。

---

## 🧩 核心概念

-   **Repository (倉庫)**：一個倉庫包含了一個特定應用程式的所有映像檔版本。例如，`nginx` 是一個倉庫，裡面存放了各種版本的 Nginx 映像檔。倉庫名稱的格式通常是 `<username>/<repository_name>`（社群映像檔）或 `nginx`（官方映像檔）。

-   **Image (映像檔)**：唯讀的範本，包含了執行應用程式所需的程式碼、函式庫、環境變數和設定檔。

-   **Tag (標籤)**：用來識別倉庫中不同的映像檔版本。例如，在 `python` 倉庫中，`3.9-slim`、`3.10`、`latest` 都是標籤。
    > **⚠️ 注意**：`latest` 標籤雖然方便，但在生產環境中建議使用更明確的版本標籤 (如 `python:3.9.12`)，以確保環境的穩定與可預測性。

-   **Official Images (官方映像檔)**：由 Docker 官方團隊審核和維護的映像檔，代表了該軟體的最佳實踐，安全且穩定。在 Docker Hub 上會有「Official Image」的標記。

-   **Verified Publisher Images (認證發行者映像檔)**：由軟體供應商直接提供和驗證的映像檔，例如 `microsoft/dotnet` 或 `oracle/database`。

---

## ⌨️ 常用 Docker Hub 指令

### 1. 登入 Docker Hub
在使用 `push` 或存取私有倉庫前，您需要先登入。
```bash
# 系統會提示您輸入 Docker Hub 的使用者名稱和密碼
docker login
```

### 2. 搜尋映像檔
```bash
# 在 Docker Hub 上搜尋關鍵字，例如 "redis"
# --filter is-official=true 可以只顯示官方映像檔
docker search --filter is-official=true redis
```

### 3. 拉取 (下載) 映像檔
```bash
# 從 Docker Hub 下載最新版的 Nginx (Alpine Linux 版本)
docker pull nginx:alpine

# 如果不指定標籤，預設會使用 "latest"
docker pull nginx
```

### 4. 推送 (上傳) 映像檔
在推送之前，您的映像檔名稱必須符合格式：`<Your-DockerID>/<image-name>:<tag>`。
```bash
# 假設您已經建置了一個名為 my-app:1.0 的映像檔
# 1. 重新標記映像檔以符合推送格式
docker tag my-app:1.0 your-dockerid/my-app:1.0

# 2. 推送映像檔到您的 Docker Hub 倉庫
docker push your-dockerid/my-app:1.0
```
*請將 `your-dockerid` 替換為您自己的 Docker Hub 使用者名稱。*

### 5. 登出 Docker Hub
```bash
docker logout
```

---

## 🚀 實戰 1：搜尋並執行官方映像檔

讓我們來執行一個 **httpd** (Apache HTTP Server) 官方映像檔，這是一個非常流行的 Web 伺服器。

#### 步驟 1: 搜尋映像檔
```bash
docker search httpd
```
您會看到一個名為 `httpd` 的官方映像檔。

#### 步驟 2: 拉取並執行映像檔
我們不需要手動 `pull`，`docker run` 會自動完成。我們選擇 `alpine` 版本，因為它非常輕量。
```bash
# -d: 在背景執行容器
# -p 8080:80: 將主機的 8080 連接埠轉發到容器的 80 連接埠
# --name my-web-server: 為容器命名
docker run -d -p 8080:80 --name my-web-server httpd:alpine
```
當您執行此指令時，Docker 會：
1.  檢查本地是否有 `httpd:alpine` 映像檔。
2.  如果沒有，就從 Docker Hub 下載它。
3.  根據該映像檔建立並啟動一個新的容器。

#### 步驟 3: 驗證
在您的瀏覽器中開啟 `http://localhost:8080` 或 `http://<您的樹莓派IP>:8080`，您應該會看到 "It works!" 的頁面。

---

## 🚀 實戰 2：建立並推送您自己的映像檔

現在，讓我們將上一份指南中的 Python Flask 應用程式打包並推送到 Docker Hub。

#### 步驟 1: 準備應用程式
確保您有 `app.py`, `requirements.txt` 和 `Dockerfile` 這三個檔案。
-   **app.py**:
    ```python
    from flask import Flask
    app = Flask(__name__)
    @app.route('/')
    def hello():
        return 'Hello from my custom Docker image!'
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000)
    ```
-   **requirements.txt**:
    ```
    Flask>=3.0.0
    ```
-   **Dockerfile**:
    ```dockerfile
    FROM python:3.9-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    EXPOSE 5000
    CMD ["python", "app.py"]
    ```

#### 步驟 2: 建置映像檔
使用您的 Docker ID 為映像檔命名。
```bash
# 將 "your-dockerid" 替換成您的 Docker Hub 使用者名稱
docker build -t your-dockerid/my-flask-app:1.0 .
```

#### 步驟 3: 本地測試
```bash
docker run -d -p 5001:5000 --name my-test-app your-dockerid/my-flask-app:1.0
```
開啟 `http://localhost:5001`，確認您能看到訊息。

#### 步驟 4: 登入並推送
```bash
# 登入 Docker Hub
docker login

# 推送您的映像檔
docker push your-dockerid/my-flask-app:1.0
```

完成！現在您可以登入 Docker Hub 網站，在您的個人頁面上就會看到剛剛推送的 `my-flask-app` 倉庫。您可以在任何安裝了 Docker 的電腦上，用 `docker run your-dockerid/my-flask-app:1.0` 來執行它。

---

## 📝 總結

Docker Hub 是 Docker 工作流程的核心。它讓開發者能夠輕鬆地：
-   存取數以萬計的現成軟體。
-   確保開發、測試和生產環境的一致性。
-   與全世界分享自己的應用程式。

熟悉如何使用 Docker Hub，是掌握 Docker 的關鍵一步。現在就去探索一下，看看您能找到哪些有趣的映像檔吧！