# 從零開始：在 Raspberry Pi 上打造您的本地端 LLM 應用

**一份涵蓋從硬體選購、Linux 基礎到 AI 模型部署的完整實戰指南**
---

## 🎯 專案目標
本專案旨在提供一份從無到有的完整教學，引導開發者與技術愛好者，如何在資源有限的 Raspberry Pi 平台上，成功部署並運行自己的大型語言模型（LLM），並透過網頁介面（OpenWebUI）進行互動。

## ✨ 核心功能
- **🧠 本地端 LLM**：在您的 Raspberry Pi 上運行 Ollama，支援多種開源模型。
- **🌐 網頁使用者介面**：透過 Docker 部署 OpenWebUI，提供直觀的聊天與管理介面。
- **☁️ 遠端安全存取**：整合 SSH、Cloudflare Tunnel 等多種方案，讓您隨時隨地連線操作。
- **🔧 高度客製化**：提供前端開發、檔案伺服器等進階應用的配置指南。

---

## 🚀 安裝與部署路徑
請依照以下步驟循序漸進，打造您的專屬 AI 助理。

### 零、前置準備：硬體與系統需求
在開始之前，請確保您已具備推薦的硬體與作業系統。

| 項目 | 推薦規格 |
|------|----------|
| 主板 | **Raspberry Pi 5** |
| 記憶體 | 8 GB / 16 GB <br>※ **8 GB** 為日常開發的平衡選擇 <br>※ **16 GB** 建議用於大型 LLM 生成式應用 |
| 作業系統 | **PiOS (64-bit)** |

> 建議使用最新的 64 位元映像檔，以確保對大容量記憶體的完整支援。

### 基礎設定：安裝 Raspberry Pi
首先，完成 Raspberry Pi 的初始安裝與基礎設定。
> 📚 **詳細指南**：[Raspberry Pi 安裝流程說明](./pi安裝流程說明/README.md)

- **透過 SSH 連線時，中文輸入變亂碼？**
  > 參考解決方案：[透過 SSH 連線，輸入中文會有亂碼的解決方法](./透過ssh連線-輸入中文會有亂碼的解決方法.md)


---

### 基礎操作：熟悉 Linux 指令
掌握 Linux 的基本操作是管理伺服器的必備技能。本章節將帶您熟悉常用指令。
> Warp:AI終端機  
> 📚 **詳細指南**：[Linux 指令操作說明](./Linux指令操作說明)

---

### 核心服務：部署 LLM 模型與 WebUI
這是整個專案的核心。我們將安裝 Ollama 來運行語言模型，並透過 Docker 部署 OpenWebUI 作為操作介面。

1.  **安裝 Docker**：OpenWebUI 推薦使用 Docker 部署。

    > 📚 **詳細指南**：[Docker 安裝流程說明](./Docker/raspberry安裝docker.md)

2.  **安裝 Ollama**：作為本地端 LLM 的運行框架。

    > 📚 **詳細指南**：[Ollama 安裝流程說明](./ollama安裝流程說明/README.md)

3.  **部署 OpenWebUI**：安裝並設定網頁使用者介面。

    > 📚 **詳細指南**：[OpenWebUI](./OpenWebUI)

---


### 遠端連線：隨時隨地存取您的 Pi
Tunnel的主要用途是建立加密通道，保護資料傳輸並突破防火牆限制，讓無法直接存取的服務變得可達。
| 連線方案 | 使用場景 | 特點 |
| :--- | :--- | :--- |
| **SSH Tunnel** | 安全的本機端口轉發 | 加密、穩定，適合開發與管理 |
| **Ngrok** | 臨時外部網路測試 | 快速產生公開網址，適合臨時分享與測試 |
| **Tailscale** | 虛擬區域網路 | 簡易組建跨裝置的私人網路，適合多裝置協作 |
| **Cloudflare Tunnel**| 正式上線的遠端連線 | 提供 DDoS 防護、自訂域名與高穩定性 |

> 📚 **SSH Tunnel**：[SSH Tunnel](./tunnel/ssh_tunnel.md)  
> 📚 **Ngrok Tunnel**：[Ngrok Tunnel](./tunnel/ngrok_tunnel.md)   
> ---
> 📚GoDaddy 域名 + Cloudflare DNS 應用流程說明  
> 📚 **cloudflare Tunnel**：[cloudflare Tunnel](./tunnel/cloudflare_tunnel.md)  

---

### 雲端 AI 編輯器與開發工具

-   **[Lovable](https://lovable.dev/)**：一個 AI 前端工程師，能學習您現有的 UI 組件庫，並自動為您建構新的頁面與功能。(可以透過github下載,點數機制,每日增加點數,邀請可增加點數)
-   **[Bolt](https://www.bolt.dev/)**：一個 AI 原生的開發工作環境，旨在透過深度整合的 AI 功能，讓開發者能以思維的速度進行編碼與建構。(可以透過github下載,訂閱機制,邀請可增加token,每月有1M_token)
-   **[Replit](https://replit.com/)**：一個功能強大的線上 IDE，其 AI 輔助編碼功能 (Ghostwriter) 能幫助使用者在瀏覽器中快速編寫、測試、部署及協作專案。(可以直接下載,每日有免費次數,無邀請點數)
-   **[Manus](https://manus.co/)**：專注於將設計轉為程式碼的 AI 開發者，能讀取您的 Figma 設計稿，並自動生成高品質的前端程式碼。(訂閱制,每日進入可以增加點數,邀請可增加點數,可直接下載)
-   **[v0.dev](https://v0.dev/)**：由 Vercel 團隊打造的生成式 UI 工具，可以根據您的文字描述，快速產生基於 React、Shadcn UI 和 Tailwind CSS 的使用者介面。(訂閱制,有邀請點數,每日有免費次數,有樣版可以直接使用,可以直接下載)


### 掌握 Docker

-   [**樹莓派安裝 Docker**](./Docker/raspberry安裝docker.md) - 一份在 Raspberry Pi 上安裝與設定 Docker 的完整指南，包含前置準備、安裝步驟與驗證。
-   [**Docker容器化基礎與n8n部署準備**](./Docker/Docker容器化基礎與n8n部署準備.md) - 一窺Docker容器的全貌
-   [**Docker 常用指令**](./Docker/Docker常用的指令.md) - 一份 Docker 常用指令的速查表，分類整理了容器、映像檔、系統管理等常用操作。
-   [**Docker Run 指令詳解**](./Docker/Docker_Run.md) - 深入解析 `docker run` 的用法與常用參數，掌握啟動容器的各種技巧。
-   [**撰寫 Dockerfile**](./Docker/DockerFile.md) - 學習如何撰寫 Dockerfile，將應用程式打包成標準化、可重現的 Docker 映像檔。
-   [**Docker Compose 入門**](./Docker/DockerCompose.md) - 介紹如何使用 Docker Compose 來定義和管理多容器應用程式，簡化開發與部署流程。
-   [**Docker Volume 管理**](./Docker/DockerVolume.md) - 探討 Docker 的資料持久化機制，學習如何使用 Volume 來安全地保存容器資料。

### n8n
- [**n8n講義**](https://github.com/roberthsu2003/n8n)

### 進階應用 
完成核心部署後，您可以依照需求擴充更多功能。

- **File Server 檔案伺服器**
  > 將您的 Raspberry Pi 變成一台檔案伺服器，支援 SFTP、WebDAV 等多種協定。
  > 📚 **詳細指南**：[File Server 安裝流程說明](./file_server安裝流程說明/README.md)

- **前端開發環境配置nginx伺服器**
  > 說明如何配置一個現代化的前端開發環境（Vite + React + TypeScript），以便未來打造客製化介面。
  > 📚 **詳細指南**：[前端開發環境配置](./前端開發環境配置/README.md)

- **後端應用程式wsgi伺服器**

	> 實作LineBot(message API)整合LLM大模型


---

> 若您在過程中發現任何錯誤或有改進建議，歡迎提交 Issue 或 Pull Request。祝您開發順利！🚀
