# OpenWebUI 安裝教學 (重構版)

這份文件旨在提供一份清晰、易於遵循的 OpenWebUI 安裝指南，特別為初學者優化了學習路徑。

## 1. 這是什麼？

[OpenWebUI](https://github.com/open-webui/open-webui) 是一個功能強大、介面友善的網頁UI，可以讓你與在本機（例如你的電腦或 Raspberry Pi）上運行的 Ollama 大型語言模型進行互動。

你可以把它想像成一個完全由你掌控的、私人的 ChatGPT。

---

## 2. 選擇你的安裝路徑

請根據你的情況，選擇一條路徑：

*   **路径 A：我想快速體驗 (推薦)**
    *   如果你的電腦是乾淨的，或你不確定該怎麼選，請走這條路。
    *   我們會用一個指令幫你裝好所有東西。
    *   **[前往 👉 3. 快速體驗：整合安裝](#3-快速體驗整合安裝-推薦)**

*   **路径 B：我已經有 Ollama 了**
    *   如果你的電腦**已經安裝並正在運行 Ollama**，而且你清楚如何操作它，請選這條路。
    *   **[前往 👉 4. 進階安裝：連接到現有的 Ollama](#4-進階安裝連接到現有的-ollama)**

---

## 3. 快速體驗：整合安裝 (推薦)

這是最簡單、最無痛的方式，推薦所有初學者使用。它會使用一個同時包含 OpenWebUI 和 Ollama 的 Docker 映像檔。

**前提**：你的系統需已安裝 Docker。若未安裝，請參考 [**Docker 安裝教學**](../Docker安裝流程說明/README.md)。

### 安裝指令

打開終端機，執行以下指令。它會下載映像檔並在背景啟動服務。

```bash
docker run -d -p 3000:8080 -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama
```
> **註**：如果你有 NVIDIA 顯示卡並想使用 GPU 加速，可將上述指令中的 `ghcr.io/open-webui/open-webui:ollama` 替換為 `ghcr.io/open-webui/open-webui:ollama-cuda`。

### 訪問與使用

安裝指令執行完畢後，等待約一分鐘讓服務啟動。
1.  **訪問 WebUI**：打開瀏覽器，輸入 `http://localhost:3000`。
2.  **註冊帳號**：第一次進入時，系統會引導你註冊第一個使用者帳號，此帳號即為管理員。

**恭喜！** 你現在已經可以開始使用了。在設定頁面中，你可以從 Ollama 拉取 (pull) 你想用的模型，然後開始對話。

---

## 4. 進階安裝：連接到現有的 Ollama

此路徑適合已在主機上手動安裝並運行 Ollama 的使用者。

### 第 1 步：啟動 OpenWebUI 容器

- **重要:此指令只會啟動 OpenWebUI，而不會啟動 Ollama。**
- 可以移除--restart always

> 使用--add-host=host.docker.internal:host-gateway -> 會失敗(適合windows和mac,一般windows和mac不需要設定,預設就有了)

```bash
docker run -d \
-p 3000:8080 \
--add-host=host.docker.internal:host-gateway \
-v open-webui:/app/backend/data \
--name open-webui \
--restart always \
ghcr.io/open-webui/open-webui:main
```

---

**使用官方備分做法才可以成功**

- 可以移除--restart always



```bash
docker run -d \
--network=host \
-p 3000:8080 \
-v open-webui:/app/backend/data \
-e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
--name open-webui \
--restart always \
ghcr.io/open-webui/open-webui:main
```

> 1. 使用`--network=host`官方備分作法,才可以連線上ollama  
> 2. 連線進入open-webui必需使用port:8080--> `http://你的網址:8080`  
> 3. 連線成功,設定ollama的連線要設成`http://127.0.0.1:11434`

### 第 2 步：連接到 Ollama

1.  **訪問 WebUI**：打開瀏覽器，輸入 `http://localhost:3000` 並註冊管理員帳號。
2.  **修改 API 位址**：進入「設定」 -> 「連線」，將 Ollama API 的位址修改為：
    ```
    http://host.docker.internal:11434
    ```
3.  **儲存設定**，系統應能成功連接到你主機上的 Ollama。

### 第 3 步：疑難排解與觀念解析 (選讀)

如果你在第 2 步遇到連線失敗的問題，或者想深入理解其背後原理，請展開以下說明。

<details>
<summary><strong>🤔 為什麼容器連不到我主機上的 Ollama？(點此展開)</strong></summary>

這個問題其實**問得非常好，而且很關鍵**。

#### 一句話結論
👉 **環境變數不是給 OpenWebUI 用的，而是用來改變「Ollama 這個服務本身的監聽行為」。**

#### 三個角色
1.  **Ollama**：一個在「主機（host）」上執行的 **伺服器 (Server)**。
2.  **OpenWebUI**：一個在「Docker容器」中運行的 **客戶端 (Client)**。
3.  **Docker 容器**：一個擁有獨立網路環境的沙盒。**容器內的 `localhost` ≠ 主機的 `localhost`**。

#### 問題核心
預設情況下，Ollama 服務只監聽 `127.0.0.1` (本機)，意思是**只接受來自「主機自己」的連線**。由於 Docker 容器不等於「主機自己」，因此它的請求會被拒絕。

#### 解決方案
我們需要在啟動 Ollama 服務**之前**，先告訴它「請監聽所有網卡的連線」。方法就是設定環境變數：
```bash
export OLLAMA_HOST=0.0.0.0
ollama serve
```
這樣設定後，Ollama 就會監聽 `0.0.0.0:11434`，允許來自 Docker 容器的連線。

</details>

<details>
<summary><strong>🤔 如何讓 OLLAMA_HOST 設定永久生效？(點此展開)</strong></summary>

這個問題**已經進入「Linux 啟動流程等級」的理解了**。

#### 核心觀念
在 Linux 中，我們需要區分「給**服務**用的環境變數」和「給**使用者**用的環境變數」。
*   **Ollama 服務**是由 `systemd` 管理的，它不讀取你個人的設定檔 (`.bashrc`)。
*   `~/.bashrc` 是給**使用者**在打開終端機時使用的。

#### 最完整的解法
我們需要「分層設定」，一勞永逸地解決問題。

**1. 給「服務」用：修改 systemd 設定 (最關鍵)**
這一步確保電腦重開機後，Ollama 服務本身就是以正確的方式啟動。
```bash
# 編輯 ollama 的 systemd 設定
sudo systemctl edit ollama
```
在打開的編輯器中加入：
```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
```
存檔後，重載設定並重啟 Ollama 服務：
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```
✅ 這一步就徹底解決了服務層級的連線問題。

**2. 給「人」用：修改 `.bashrc` 設定 (方便測試)**
這一步讓你在終端機裡手動測試時，也擁有相同的環境。
```bash
# 編輯你個人家目錄下的 .bashrc 檔案
nano ~/.bashrc
```
在檔案的**最下面**加入 `export OLLAMA_HOST=0.0.0.0`，存檔後執行 `source ~/.bashrc` 即可。

</details>

---

## 5. 管理與維護

### 更新 OpenWebUI

官方推薦使用 `Watchtower` 來更新你的 Docker 容器。它會自動拉取最新的映像檔，並用新映像檔重啟容器。

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nickfedor/watchtower --run-once open-webui
```
> **註**：`open-webui` 是你當初用 `--name` 參數設定的容器名稱。此指令對上述兩種安裝方式都適用。

### 其他常用指令

```bash
# 停止 OpenWebUI 容器
docker stop open-webui

# 重新啟動 OpenWebUI 容器
docker start open-webui

# 查看 OpenWebUI 容器的日誌
docker logs open-webui

# 移除 OpenWebUI 容器 (需先停止)
docker rm open-webui
```

---

## 6. 其他安裝方式 (專家級)

對於不想使用 Docker 的專家，官方也提供了使用 Python `pip` 的手動安裝方式。
```bash
# 1. 安裝 OpenWebUI 套件
pip install open-webui

# 2. 啟動服務
open-webui serve
```
**注意**：此方法需要自行處理 Python 環境、依賴套件與資料庫設定，極不推薦初學者使用。
