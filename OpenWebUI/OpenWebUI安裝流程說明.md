# OpenWebUI 安裝教學 (重構版)

這份文件旨在提供一份清晰、易於遵循的 OpenWebUI 安裝指南，特別為初學者優化了學習路徑。

## 1. 這是什麼？

[OpenWebUI](https://github.com/open-webui/open-webui) 是一個功能強大、介面友善的網頁UI，可以讓你與在本機（例如你的電腦或 Raspberry Pi）上運行的 Ollama 大型語言模型進行互動。

你可以把它想像成一個完全由你掌控的、私人的 ChatGPT。

---


---

## 2. 安裝(適合windows和mac)：連接到現有的 Ollama -> bridge

> **注意**：此路徑適合已在我windows或mac主機上手動安裝並運行 Ollama 的使用者。  
> network:bridge -> 適合windows和mac,一般windows和mac不需要設定,預設就有了



### 第2-1步：啟動 OpenWebUI 容器-

- **重要:此指令只會啟動 OpenWebUI，而不會啟動 Ollama。**
- 
- 可以移除--restart always

> 使用--add-host=host.docker.internal:host-gateway -> 會失敗(適合windows和mac,一般windows和mac不需要設定,預設就有了)

```bash
docker run -d \
-p 3000:8080 \
-v open-webui:/app/backend/data \
-e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
--name open-webui \
--restart always \
ghcr.io/open-webui/open-webui:main
```

### 第2-2步:連接到 Ollama

1.  **訪問 WebUI**：打開瀏覽器，輸入 `http://localhost:3000` 並註冊管理員帳號。
2.  **修改 API 位址**：進入「設定」 -> 「連線」，將 Ollama API 的位址修改為(預設已經是host.docker.internal:11434)：
    ```
    http://host.docker.internal:11434
    ```
3.  **儲存設定**，系統應能成功連接到你主機上的 Ollama。

---

## 3. 安裝(適合raspberry)：連接到現有的 Ollama -> network:host

> **注意**：此路徑適合已在 Raspberry Pi 上手動安裝並運行 Ollama 的使用者。   
> network:host 


### 第3-1步：啟動 OpenWebUI 容器-適合raspberry

- 可以移除--restart always

```bash
docker run -d \
--network=host \
-v open-webui:/app/backend/data \
-e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
--name open-webui \
--restart always \
ghcr.io/open-webui/open-webui:main
```


### 第3-2步：連接到 Ollama

1.  **訪問 WebUI**：打開瀏覽器，輸入 `http://localhost:8080` 並註冊管理員帳號。
2.  **修改 API 位址**：進入「設定」 -> 「連線」，將 Ollama API 的位址修改為(預設已經是127.0.0.1:11434)：

    ```
    http://127.0.0.1:11434
    ```

3.  **儲存設定**，系統應能成功連接到你主機上的 Ollama。

---

## 4. 安裝(適合raspberry)：連接到現有的 Ollama -> network:bridge
> **注意**：此路徑適合已在 Raspberry Pi 上手動安裝並運行 Ollama 的使用者。   
> network:bridge 


### 第4-1步：啟動 OpenWebUI 容器-適合raspberry

- 可以移除--restart always

```bash
docker run -d \
-p 3000:8080 \
-v open-webui:/app/backend/data \
-e OLLAMA_BASE_URL=http://pi4Robert0301:11434 \
--name open-webui \
--restart always \
ghcr.io/open-webui/open-webui:main
```


### 第4-2步：連接到 Ollama

1.  **訪問 WebUI**：打開瀏覽器，輸入 `http://localhost:3000` 並註冊管理員帳號。
2.  **修改 API 位址**：進入「設定」 -> 「連線」，將 Ollama API 的位址修改為(預設已經是http://pi4Robert0301:11434)：

    ```
    http://pi4Robert0301:11434
    ```

3.  **儲存設定**，系統應能成功連接到你主機上的 Ollama。

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


