# 撰寫 Dockerfile：打造您專屬的 Docker 映像檔

`Dockerfile` 是 Docker 自動化建置映像檔的核心。它就像一份食譜，詳細記載了從無到有建立一個 Docker 映像檔所需的所有步驟和指令。透過撰寫 Dockerfile，您可以確保建置過程的透明、可重現和自動化。

這份文件將帶您深入了解 Dockerfile 的世界。

---

## 📋 目錄
- [Dockerfile 是什麼？](#dockerfile-是什麼)
- [基本結構與語法](#基本結構與語法)
- [核心指令詳解](#核心指令詳解)
- [實戰範例：打包一個 Node.js 應用程式](#實戰-範例-打包一個-nodejs-應用程式)
- [撰寫 Dockerfile 的最佳實踐](#撰寫-dockerfile-的最佳實踐)
- [進階主題：多階段建置 (Multi-stage Builds)](#進階主題-多階段建置-multi-stage-builds)
- [總結](#總結)

---

## 🤔 Dockerfile 是什麼？

Dockerfile 是一個純文字檔案，裡面包含了一系列用來建置 Docker 映像檔的指令。當您執行 `docker build` 指令時，Docker 會讀取 Dockerfile 的內容，並依序執行其中的指令，最終生成一個新的 Docker 映像檔。

**建置流程：**
`Dockerfile` (文字腳本) -> `docker build` (執行建置) -> `Docker Image` (唯讀的映像檔範本)

**主要優點：**
- **自動化**：將手動、繁瑣的環境設定步驟程式碼化。
- **可重現性**：無論在何時何地，只要有相同的 Dockerfile，就能建置出完全一樣的環境。
- **透明化**：任何人都能透過閱讀 Dockerfile 了解該映像檔的組成與建置過程。

---

## 🏗️ 基本結構與語法

- Dockerfile 中的指令不區分大小寫，但按照慣例，**指令本身會使用大寫**，以和參數區分。
- 檔案中的第一行必須是 `FROM` 指令。
- 使用 `#` 來加入註解。
- 每條指令都會在現有的映像檔上建立一個新的**層 (Layer)**。

```dockerfile
# 這是一行註解
FROM ubuntu:22.04
LABEL maintainer="your-name@example.com"
RUN apt-get update && apt-get install -y nginx
CMD ["echo", "Image created"]
```

---

## ⚙️ 核心指令詳解

### `FROM`
指定此映像檔的**基礎映像檔 (Base Image)**。所有後續的指令都會基於這個映像檔來建置。
```dockerfile
# 使用官方的 Ubuntu 22.04 作為基礎
FROM ubuntu:22.04

# 使用輕量的 Alpine Linux 版本的 Python 3.9
FROM python:3.9-alpine

# 從零開始建置，不依賴任何基礎映像檔 (進階用法)
FROM scratch
```

### `WORKDIR`
設定後續指令 (如 `RUN`, `COPY`, `CMD`) 的**工作目錄**。如果目錄不存在，`WORKDIR` 會自動建立它。
```dockerfile
# 設定工作目錄為 /app
WORKDIR /app

# 現在執行 ls 指令時，等同於在容器內的 /app 目錄下執行
RUN ls -la
```
> **最佳實踐**：使用 `WORKDIR` 來切換目錄，而不是 `RUN cd /some/dir`。`WORKDIR` 能確保後續所有指令都在正確的目錄下執行。

### `COPY`
將檔案或目錄從**主機 (建置上下文)** 複製到映像檔的檔案系統中。
```dockerfile
# 將主機當前目錄下的 package.json 檔案複製到映像檔的 /app 目錄下
COPY package.json /app/

# 將主機當前目錄下的所有檔案複製到映像檔的當前工作目錄
COPY . .
```

### `RUN`
在映像檔中執行指定的命令。常用於安裝套件、建立目錄、編譯程式碼等。每執行一次 `RUN` 都會建立一個新的映像檔層。
```dockerfile
# 更新套件列表並安裝 curl
RUN apt-get update && apt-get install -y curl

# 執行一個 shell 命令
RUN echo "Hello from build process" > /tmp/hello.txt
```
> **最佳實踐**：盡量將多個相關的 `RUN` 命令用 `&&` 串連起來，以減少映像檔的層數。

### `CMD`
提供容器啟動時**預設執行的指令**。一個 Dockerfile 中只能有最後一個 `CMD` 指令會生效。
```dockerfile
# 格式一：Exec form (推薦)
CMD ["python", "app.py"]

# 格式二：Shell form
CMD python app.py
```
如果在 `docker run` 時指定了其他指令，`CMD` 的內容將會被覆蓋。

### `ENTRYPOINT`
與 `CMD` 類似，都是設定容器啟動時執行的指令。但 `ENTRYPOINT` **不容易被覆蓋**。`docker run` 後面附加的參數會被當作 `ENTRYPOINT` 的參數傳入。
```dockerfile
# 容器啟動時會執行 `ping localhost`
ENTRYPOINT ["ping", "localhost"]

# 如果搭配 CMD
ENTRYPOINT ["ping"]
CMD ["localhost"]
# 執行 `docker run <image>` 會得到 `ping localhost`
# 執行 `docker run <image> google.com` 會得到 `ping google.com`
```

### `EXPOSE`
聲明容器在執行時會監聽的網路**連接埠**。這是一個文件性質的指令，**不會**實際將連接埠發布到主機。
```dockerfile
# 聲明容器會監聽 80 連接埠
EXPOSE 80
```
實際的連接埠映射仍需在 `docker run` 時使用 `-p` 或 `-P` 旗標來完成。

### `ENV`
設定**環境變數**。這些環境變數在映像檔的建置過程和容器的執行期間都有效。
```dockerfile
# 設定一個環境變數
ENV APP_VERSION=1.0.0

# 後續指令可以引用這個變數
RUN echo "Building version $APP_VERSION"
```

---

## 🚀 實戰範例：打包一個 Node.js 應用程式

讓我們來為一個簡單的 Express 網站撰寫 Dockerfile。

#### 步驟 1: 準備檔案
1.  **`server.js`**:
    ```javascript
    const express = require('express');
    const app = express();
    const PORT = 3000;

    app.get('/', (req, res) => {
      res.send('Hello from Dockerized Node.js app!');
    });

    app.listen(PORT, () => {
      console.log(`Server is running on http://localhost:${PORT}`);
    });
    ```

2.  **`package.json`**:
    ```json
    {
      "name": "my-node-app",
      "version": "1.0.0",
      "description": "",
      "main": "server.js",
      "scripts": {
        "start": "node server.js"
      },
      "dependencies": {
        "express": "^4.17.1"
      }
    }
    ```

3.  **`.dockerignore`** (非常重要！):
    ```
    node_modules
    npm-debug.log
    Dockerfile
    .git
    ```
    這個檔案告訴 Docker 在建置時忽略哪些檔案，避免將不必要的檔案複製進映像檔，同時可以防止快取失效。

#### 步驟 2: 撰寫 `Dockerfile`
```dockerfile
# 階段 1: 使用官方 Node.js 18 的 alpine 輕量版本作為基礎映像檔
FROM node:18-alpine

# 階段 2: 設定工作目錄
WORKDIR /usr/src/app

# 階段 3: 複製 package.json 和 package-lock.json
# 這樣做可以利用 Docker 的快取機制。只有當這兩個檔案變更時，才會重新執行 npm install
COPY package*.json ./

# 階段 4: 安裝應用程式依賴
RUN npm install

# 階段 5: 複製應用程式的原始碼
COPY . .

# 階段 6: 聲明容器監聽的連接埠
EXPOSE 3000

# 階段 7: 設定容器啟動時執行的指令
CMD [ "node", "server.js" ]
```

#### 步驟 3: 建置與執行
```bash
# 在包含 Dockerfile 的目錄下執行建置指令
docker build -t my-node-app .

# 執行建置好的映像檔
docker run -d -p 3000:3000 --name my-app-instance my-node-app
```
現在，打開瀏覽器訪問 `http://localhost:3000`，您就能看到網站的訊息了。

---

## ✨ 撰寫 Dockerfile 的最佳實踐

1.  **使用 `.dockerignore` 檔案**：保持建置上下文乾淨，加速建置過程，減小映像檔體積。
2.  **使用輕量的基礎映像檔**：例如 `alpine`, `slim` 版本，可以大幅縮小最終映像檔的體積。
3.  **善用建置快取 (Build Cache)**：將變動頻率低的指令放在前面 (如安裝依賴)，變動頻率高的指令放在後面 (如複製原始碼)。
4.  **合併 `RUN` 指令**：使用 `&&` 將多個 `RUN` 指令串連成一個，以減少映像檔層數。
5.  **以非 root 使用者執行**：為了安全，建立一個專用使用者和群組，並在最後切換成該使用者來執行應用程式。
6.  **使用多階段建置**：對於需要編譯的語言 (如 Go, Java, C++ 或前端框架)，使用多階段建置可以讓最終的正式映像檔極度輕量。

---

## 🌟 進階主題：多階段建置 (Multi-stage Builds)

多階段建置允許您在一個 Dockerfile 中定義多個建置階段。您可以利用一個包含完整編譯工具的「建置階段」來編譯程式碼，然後只將最終的產出物複製到一個乾淨、輕量的「正式階段」映像檔中。

**範例：打包一個 React 前端應用**

```dockerfile
# --- 建置階段 (Build Stage) ---
# 使用 Node.js 作為建置環境
FROM node:18-alpine AS build

WORKDIR /app

# 複製 package.json 並安裝依賴
COPY package*.json ./
RUN npm install

# 複製所有原始碼
COPY . .

# 執行建置指令，產生靜態檔案
RUN npm run build

# --- 正式階段 (Production Stage) ---
# 使用 Nginx 作為 Web 伺服器來託管靜態檔案
FROM nginx:1.23-alpine

# 從 "build" 階段複製建置好的靜態檔案到 Nginx 的網站根目錄
COPY --from=build /app/build /usr/share/nginx/html

# 聲明監聽的連接埠
EXPOSE 80

# Nginx 映像檔預設的 CMD 會啟動 Nginx 服務
```
**優點**：最終的映像檔只包含了 Nginx 和打包好的靜態檔案，完全不包含 Node.js、npm 和原始碼，體積非常小。

---

## 📝 總結

Dockerfile 是實現「基礎設施即程式碼」的關鍵工具。掌握它，您就能夠建立出標準化、可移植且易於維護的應用程式環境。希望這份文件能幫助您踏出成功的第一步！