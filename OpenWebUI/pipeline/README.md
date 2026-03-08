# Pipeline

## 名詞解釋：什麼是「Pipeline」？

**Pipeline** 是一個**模組化、可自訂的工作流程框架**，讓你可以：

- ✅ 把複雜流程拆成多個步驟
- ✅ 自訂函數、呼叫外部 API
- ✅ 實作訊息過濾器（例如內容過濾）
- ✅ 整合 RAG、Langfuse、搜尋工具等
- ✅ 利用 Python 庫做更複雜的處理

**最重要的特性：**  
Pipeline 會提供一個 **OpenAI 相容的 API server**，所以 Open-WebUI 可以將它當成一個 API 來源來使用。

---

## 📋 目錄

### 第一篇：認識 Pipeline

| 順序 | 主題 | 說明 |
|------|------|------|
| 0 | [認識 Pipeline](./Pipeline_00_認識Pipeline/README.md) | OpenAI 規格、Pipeline 與 Filter/Tools 的差異、為何需要 Pipeline Server |

### 第二篇：實作 Pipeline

| 階段 | 主題 | 說明 |
|------|------|------|
| 1 | [第一個 Pipeline](./Pipeline_01_第一個Pipeline/README.md) | Docker Run、Docker Compose、在 Open-WebUI 中連接 |
| 2 | [整合 Cloudflare](./Pipeline_02_整合Cloudflare/README.md) | 整合 open-webui、pipelines、cloudflared 完整部署 |
| 3 | [程式碼實作](./Pipeline_03_程式碼實作/README.md) | Wikipedia Pipeline 範例、Pipeline 類別結構、Valves 設定 |

---

### 實作範例

| 範例 | 說明 |
|------|------|
| [整合 Cloudflare Pipeline](./實作範例/整合CloudflarePipeline/) | open-webui + pipelines + cloudflared 完整 compose |

---

### 參考文件

| 文件 | 說明 |
|------|------|
| [Pipeline 完整教學指南](./Pipeline_完整教學指南.md) | 完整版教學內容（含常見問題、觀念釐清、教學比喻） |
| [Pipeline 測試與 Debug](./Pipeline_測試與Debug.md) | 虛擬環境開發、除錯與測試指南 |

---

### 參考資源

- [Open-WebUI Pipelines GitHub](https://github.com/open-webui/pipelines)
- [Open-WebUI 官方文件](https://docs.openwebui.com/)
