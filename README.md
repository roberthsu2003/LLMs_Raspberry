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

---

### 基礎操作：熟悉 Linux 指令
掌握 Linux 的基本操作是管理伺服器的必備技能。本章節將帶您熟悉常用指令。
> Warp:AI終端機  
> 📚 **詳細指南**：[Linux 指令操作說明](./Linux指令操作說明)

---

### 核心服務：部署 LLM 模型與 WebUI
這是整個專案的核心。我們將安裝 Ollama 來運行語言模型，並透過 Docker 部署 OpenWebUI 作為操作介面。

1.  **安裝 Docker**：OpenWebUI 推薦使用 Docker 部署。
    > 📚 **詳細指南**：[Docker 安裝流程說明](./Docker/Docker安裝流程說明.md)

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

> 📚 **詳細指南與比較**：[Tunnel 連線待整理資料](./tunnel連線待整理資料.md)  
> 📚 **SSH Tunnel**：[SSH Tunnel](./tunnel/ssh_tunnel.md)  
> 📚 **Ngrok Tunnel**：[Ngrok Tunnel](./tunnel/ngrok_tunnel.md)  
> 📚 **cloudflare Tunnel**：[cloudflare Tunnel](./tunnel/cloudflare_tunnel.md)  

---

### 雲端AI編輯器應用

- lovable
- bolt
- replit
- manus
- v0


### 掌握Docker

- [**掌握Docker**](./Docker/掌握Docker.md)
- [**Docker Hub**](./Docker/直接使用Docker_Hub.md)
- [**Docker Image**](./Docker/DockerFile.md)
- [**Docker Run**](./Docker/DockerRun.md)
- [**Docker Compose**](./Docker/DockerRun.md)

### N8N
- [**N8N是什麼?**](./n8n/n8n是什麼.md)
- [**N8N伺服器架設-Docker**](./n8n/使用Docker架設n8n.md)

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

- **N8N基礎操作**

---

## ⚠️ 常見問題與除錯
- **透過 SSH 連線時，中文輸入變亂碼？**
  > 參考解決方案：[透過 SSH 連線，輸入中文會有亂碼的解決方法](./透過ssh連線-輸入中文會有亂碼的解決方法.md)

---

> 若您在過程中發現任何錯誤或有改進建議，歡迎提交 Issue 或 Pull Request。祝您開發順利！🚀
