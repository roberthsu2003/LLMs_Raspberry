# OpenWebUI 安裝教學

## 1. 簡介

[OpenWebUI](https://github.com/open-webui/open-webui) 是一個功能豐富、對使用者友善的自架設 AI Web 介面。它設計為可完全離線運行，並支援多種大型語言模型 (LLM) 執行器，例如 **Ollama** 和與 OpenAI 相容的 API。

簡單來說，它可以讓你透過一個漂亮的網頁來與安裝在本地（例如你的 Raspberry Pi 或電腦）的 Ollama 模型進行互動，就像是擁有一個私人的 ChatGPT 介面一樣。

---

## 2. 安裝方式 (Docker - 強力推薦)

官方最推薦、也是最簡單的安裝方式是使用 Docker。它可以確保所有環境都已設定妥當，一鍵啟動。

**安裝前提**：你的系統上需要先安裝好 Docker。如果你還沒安裝，請參考：
-   [**Docker 安裝與基礎入門教學**](../Docker安裝流程說明/README.md)

請根據您的情況選擇一種安裝方式：

---

### 情況 A：主機已安裝 Ollama (適用於您的情況)

如果您的電腦或 Raspberry Pi 上已經手動安裝了 Ollama，請使用此方法。它會只啟動 OpenWebUI 容器，並設定它去連接您主機上正在運行的 Ollama 服務。

**第 1 步：確保 Ollama 服務可被網路訪問**

**（這一步對 Raspberry Pi / Linux 使用者至關重要！）**

預設情況下，您主機上的 Ollama 服務可能只會監聽 `127.0.0.1` (本機)，這會導致 Docker 容器內部無法訪問它。您需要設定 Ollama 監聽所有網路介面 (`0.0.0.0`)。

請在啟動 Ollama 服務**之前**，先在終端機設定環境變數：
```bash
export OLLAMA_HOST=0.0.0.0
```
然後再啟動 Ollama 服務 (`ollama serve`)。這樣設定後，容器才能透過主機的 IP 位址找到 Ollama。

**第 2 步：執行 OpenWebUI 容器**

打開終端機，執行以下指令：

```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

**第 3 步：連接到 Ollama**

啟動後，進入 OpenWebUI 介面 (`http://localhost:3000`)，在設定中，將 Ollama API 的位址從預設的 `http://localhost:11434` 修改為 `http://host.docker.internal:11434`。這樣 UI 就能正確連接到主機的 Ollama 了。

---

### 情況 B：想使用整合包一鍵安裝 (適合全新環境)

如果您不想在主機上手動安裝 Ollama，可以使用這個整合了 Ollama 的映像檔。一個指令就能搞定所有事。

#### 🐧 CPU 版本 (適用於 Raspberry Pi 和大部分沒有 NVIDIA 顯示卡的電腦)

```bash
docker run -d -p 3000:8080 -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama
```

#### 🎮 GPU 版本 (適用於有 NVIDIA 顯示卡的電腦)

```bash
docker run -d -p 3000:8080 --gpus=all -v ollama:/root/.ollama -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:ollama
```

---

### 指令參數說明

-   `-d`：讓容器在背景運行。
-   `-p 3000:8080`：將你機器的 `3000` 連接埠映射到容器的 `8080` 連接埠。
-   `--add-host=host.docker.internal:host-gateway`：（僅情況A）在容器內新增一個域名 `host.docker.internal` 並指向主機，讓容器可以訪問主機的服務。
-   `-v open-webui:/app/backend/data`：建立一個資料卷 (volume) 來存放 OpenWebUI 的設定，防止容器刪除後資料遺失。
-   `-v ollama:/root/.ollama`：（僅情況B）建立一個資料卷來存放 Ollama 的模型。
-   `--name open-ui`：為容器取個名字。
-   `--restart always`：讓 Docker 總是在啟動時自動重啟這個容器。

---

## 3. 安裝後步驟

安裝指令執行完畢後，等待幾分鐘讓服務啟動。

1.  **訪問 WebUI**：打開你的網頁瀏覽器，輸入 `http://localhost:3000` (如果你是在 Raspberry Pi 上安裝，可以在同一網路下的另一台電腦輸入 `http://<你的RaspberryPi的IP位址>:3000`)。

2.  **註冊管理員帳號**：第一次進入時，系統會引導你註冊第一個使用者帳號，這個帳號將會是管理員。

完成後，你就可以開始使用了！你可以在設定中，從 Ollama 拉取 (pull) 你想要使用的模型，然後開始對話。

---

## 4. 如何更新 OpenWebUI

官方推薦使用 `Watchtower` 這個工具來幫助你更新 Docker 容器。

你可以執行以下指令來手動觸發一次更新：

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock nickfedor/watchtower --run-once open-webui
```

它會自動拉取最新的 `ghcr.io/open-webui/open-webui:ollama` 映像檔，並用新的映像檔重啟你的容器。

---

## 5. 其他安裝方式 (進階)

除了 Docker，官方也提供了使用 Python `pip` 的手動安裝方式，適合不想使用 Docker 的進階使用者。

```bash
# 1. 安裝 OpenWebUI 套件
pip install open-webui

# 2. 啟動服務
open-webui serve
```
使用這種方式，預設的訪問網址會是 `http://localhost:8080`。

**注意**：手動安裝需要自行處理 Python 環境、依賴套件和資料庫設定，相對複雜，因此對於初學者，強烈建議使用 Docker 方式。
