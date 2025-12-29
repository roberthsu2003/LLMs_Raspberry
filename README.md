# 從 Linux 作業系統到人工智慧生成式模型的實作開發
**本地端 LLM（Large Language Model）在 Raspberry Pi 上的完整應用指南**

---

## 📑 目錄
1. [硬體需求](#硬體需求)  
2. [作業系統需求](#作業系統需求)  
3. [待完成事項 (Roadmap)](#待完成事項-roadmap)  
4. [安裝與設定說明](#安裝與設定說明)  
   - [Raspberry Pi 安裝流程](#raspberry-pi-安裝流程說明)  
   - [Linux 常用指令教學](#linux-指令操作說明)  
   - [Ollama 安裝流程](#ollama-安裝流程說明)  
   - [OpenWebUI 安裝與 API 使用](#openwebui-安裝流程說明)  
   - [Tunnel 連線方式比較](#tunnel-連線說明)  
   - [File Server 部署說明](#file_server-安裝流程說明)  
   - [前端開發環境配置](#前端開發環境配置)  
5. [常見問題與除錯](#常見問題與除錯)  

---

## 🛠 硬體需求
| 項目 | 推薦規格 |
|------|----------|
| 主板 | **Raspberry Pi 5** |
| 記憶體 | 4 GB / 8 GB / 16 GB <br>※ **8 GB** 為日常開發的平衡選擇，<br>※ **16 GB** 建議用於大型 LLM 生成式應用 |

## 📦 作業系統需求
- **PiOS**（官方 Raspberry Pi 作業系統）<br>建議使用最新的 64 位元映像檔，以確保對大容量記憶體的完整支援。

---

## 🚀 待完成事項 (Roadmap)
- **遠端連線**
  - SSH 連線設定與圖形化工具（FileZilla / SFTP）使用
- **Linux 基礎操作**
  - 常用指令快速上手
  - 使用者、群組與檔案/目錄權限（rwx）管理
- **Tunnel 方案整理**（[待整理資料](./tunnel連線待整理資料.md)）
  - SSH Tunnel
  - Ngrok（開發階段臨時通道）
  - Tailscale（虛擬區域網路）
  - Cloudflare Tunnel（正式上線遠端連線）
- **本機套件安裝**
  - Node.js（npm）  
  - Python（pip）  
  - uv（Rust‑based Python 包管理器）  
  - Miniconda（多環境管理）
- **LLM 應用整合**
  - Ollama + OpenWebUI 基本部署
  - OpenWebUI API 呼叫範例
  - 自訂模型推理流程

---

## 📚 安裝與設定說明

### Raspberry Pi 安裝流程說明
> 詳細步驟請參考 [Raspberry Pi 安裝流程說明](./pi安裝流程說明/README.md)

---

### Linux 指令操作說明
> 目錄：`./Linux指令操作說明`  
> 包含檔案、權限、網路、系統監控等核心指令教學。

---

### Ollama 安裝流程說明
> 目錄：`./ollama安裝流程說明`  
> 包括二進位下載、服務管理與 GPU 加速設定。

---

### OpenWebUI 安裝流程說明
> 目錄：`./openwebui安裝流程說明`  
> 步驟涵蓋 Docker 部署、環境變數設定與常見錯誤排除。

---

### Tunnel 連線說明
- **SSH Tunnel**：安全加密的本機端口轉發。  
- **Ngrok**：快速建立外部可訪問的隧道，適合測試階段。  
- **Tailscale**：以 WireGuard 為底的虛擬私人網路，簡易共享內部資源。  
- **Cloudflare Tunnel**：適合正式上線，提供 DDoS 防護與自訂子域名。

> 詳細教學請參考相應的專案文件或官方文件。

---

### File Server 安裝流程說明
> 目錄：`./file_server安裝流程說明/README.md`  
> 支援 SFTP、WebDAV、以及簡易的 HTTP 靜態檔案服務。

---

### 前端開發環境配置
> 目錄：`./前端開發環境配置/README.md`  
> 包含 Vite、React、TypeScript 與 Hot Reload 設定說明。

---

## ⚠ 常見問題與除錯
> **中文輸入亂碼**（透過 SSH 連線時）  
> 參考: [透過 SSH 連線，輸入中文會有亂碼的解決方法](./透過ssh連線-輸入中文會有亂碼的解決方法.md)

---  

> 本 README 仍在持續更新中，若有任何建議或發現錯誤，歡迎提交 Issue 或 Pull Request。祝開發順利 🚀