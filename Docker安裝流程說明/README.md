# Docker 安裝與基礎入門教學 (for Windows, macOS, and Raspberry Pi)

歡迎來到 Docker 的世界！

這份文件是為初學者設計的，旨在幫助你輕鬆地在你的電腦或 Raspberry Pi 上安裝並開始使用 Docker。別擔心，我們會用最簡單的方式帶你入門！

---

## 1. Docker 是什麼？

![host_image_container關係圖](./images/host_image_container關係圖.png)

想像一下，你正在做一個很酷的專案（例如一個網站），它需要在特定的環境和一堆軟體上才能運行。當你把專案交給同學或老師時，他們可能因為環境不同而無法順利運行。

**Docker 就是來解決這個問題的！**

-   **就像一個「軟體貨櫃」**：Docker 可以將你的應用程式，連同它需要的所有東西（函式庫、設定、環境變數等）全部打包在一起，放進一個標準化的「貨櫃 (Container)」裡。
-   **到處都能跑**：這個貨櫃可以在任何安裝了 Docker 的機器上運行，無論是 Windows、macOS 還是 Linux (像你的 Raspberry Pi)，都能保證環境完全一致。
-   **輕量且快速**：跟傳統的虛擬機比起來，Docker 容器更小、啟動更快，也更節省資源。

簡單來說，Docker 讓軟體開發、分享和部署變得超級簡單又可靠。

---

## 2. Docker 安裝教學

請根據你的作業系統選擇對應的安裝方式。

### 💻 Windows 安裝 (建議 Windows 10/11)

在 Windows 上，我們使用 **Docker Desktop**。它會利用 Windows 內建的 WSL 2 (Windows Subsystem for Linux) 技術來運行 Docker。

1.  **啟用 WSL 2**：如果尚未啟用，請以管理員身分開啟 PowerShell 或命令提示字元，然後執行：
    ```bash
    wsl --install
    ```
    安裝完成後建議重啟電腦。

2.  **下載 Docker Desktop**：前往官方網站下載適用於 Windows 的 Docker Desktop。
    -   [Docker Desktop for Windows 下載頁面](https://docs.docker.com/desktop/install/windows-install/)

3.  **安裝**：雙擊下載的安裝檔，依照畫面提示完成安裝即可。安裝過程它會自動設定好與 WSL 2 的整合。

### 🍎 macOS 安裝

在 macOS 上，我們同樣使用 **Docker Desktop**。

1.  **下載 Docker Desktop**：前往官方網站，根據你的晶片類型（Intel 或 Apple Silicon M1/M2/M3）選擇對應的版本。
    -   [Docker Desktop for Mac 下載頁面](https.docs.docker.com/desktop/install/mac-install/)

2.  **安裝**：打開下載的 `.dmg` 檔案，然後將 Docker 圖示拖曳到「Applications」資料夾中，就這麼簡單！

### 🐧 Raspberry Pi (Linux) 安裝

在 Raspberry Pi 或其他 Linux 系統上，我們通常直接透過指令行來安裝。官方提供了一個方便的腳本，可以自動完成所有事情。

1.  **執行安裝腳本**：打開終端機 (Terminal)，輸入以下指令來下載並執行安裝腳本。
    ```bash
    # 下載腳本
    curl -fsSL https://get.docker.com -o get-docker.sh
    
    # 以管理員權限執行腳本
    sudo sh get-docker.sh
    ```

2.  **將使用者加入 Docker 群組（非常重要！）**：為了避免每次都要輸入 `sudo`，我們需要將目前的使用者加入 `docker` 群組。
    ```bash
    sudo usermod -aG docker $USER
    ```
    **注意**：執行此指令後，你需要**登出再重新登入**（或重啟 Raspberry Pi），設定才會生效。

---

## 3. Docker 基礎指令入門

安裝完成後，讓我們來學習兩個最核心的指令！請打開你的終端機或命令提示字元。

### `docker pull` - 下載映像檔 (Image)

**映像檔 (Image)** 是建立 Docker 容器的「藍圖」或「模板」。它包含了應用程式執行所需的一切。`pull` 指令就是從一個名為 Docker Hub 的公共倉庫中下載這些映像檔。

讓我們來下載一個最簡單的 `hello-world` 映像檔：
```bash
docker pull hello-world
```

### `docker run` - 運行容器 (Container)

**容器 (Container)** 是映像檔的「運行實例」。`run` 指令會根據指定的映像檔建立並啟動一個容器。

現在，讓我們運行剛剛下載的 `hello-world`：
```bash
docker run hello-world
```
如果你看到畫面輸出了 "Hello from Docker!" 的歡迎訊息，恭喜你！這代表你的 Docker 已經安裝成功並正常運作了！

---

## 4. 給 Raspberry Pi 使用者的常用指令

在資源有限的 Raspberry Pi 上，管理好 Docker 容器和映像檔是很重要的。

-   **列出已下載的映像檔**：
    ```bash
    docker images
    ```

-   **列出正在運行的容器**：
    ```bash
    docker ps
    ```

-   **列出所有容器（包含已停止的）**：
    ```bash
    docker ps -a
    ```

-   **移除一個已停止的容器**（需要先從 `docker ps -a` 找到 CONTAINER ID）：
    ```bash
    docker rm <容器的ID或名稱>
    ```

-   **移除一個映像檔**（需要先從 `docker images` 找到 IMAGE ID）：
    ```bash
    docker rmi <映像檔的ID>
    ```

---

## 5. 接下來...

恭喜你完成了 Docker 的第一步！

這只是一個開始。在接下來的進階課程中，我們將會學習更多酷炫的 Docker 技巧，例如：

-   如何自己編寫 **Dockerfile** 來打造專屬的映像檔。
-   使用 **Docker Compose** 一次管理多個容器的複雜應用。
-   Docker 的網路和儲存管理。

準備好迎接更多挑戰了嗎？我們在進階課程見！
