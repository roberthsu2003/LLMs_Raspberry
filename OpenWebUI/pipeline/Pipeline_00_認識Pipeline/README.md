# Pipeline（第 0 章）：認識 Pipeline

## 📋 目錄

- [什麼是 Pipeline？](#什麼是-pipeline)
- [OpenAI 規格](#openai-規格)
- [為什麼需要 Pipeline Server？](#為什麼需要-pipeline-server)
- [Pipeline 與 Filter / Tools 的差異](#pipeline-與-filter--tools-的差異)
- [Pipeline 與 MCP 的差異](#pipeline-與-mcp-的差異)

---

## 什麼是 Pipeline？

**Pipeline** 是一個**模組化、可自訂的工作流程框架**，讓你可以：

- ✅ 把複雜流程拆成多個步驟
- ✅ 自訂函數、呼叫外部 API
- ✅ 實作訊息過濾器（例如內容過濾）
- ✅ 整合 RAG、Langfuse、搜尋工具等
- ✅ 利用 Python 庫做更複雜的處理

**最重要的特性：**  
Pipeline 會提供一個 **OpenAI 相容的 API server**，所以 Open-WebUI 可以將它當成一個 API 來源來使用。

---

## OpenAI 規格

### 什麼是「符合 OpenAI 規格（OpenAI-compatible）」？

**不是**指一定要使用 OpenAI 的模型，而是指 **API 的設計方式**遵循 OpenAI API 的介面規格。

**三個必要條件：**

| 條件 | 說明 |
|------|------|
| **Endpoint 一樣** | `POST /v1/chat/completions`、`GET /v1/models` |
| **Request 結構** | 有 `model`、`messages`（含 `role`、`content`） |
| **Response 結構** | `choices[0].message.content` |

**常見誤解澄清：**

- ❌ 一定要使用 OpenAI 雲端模型、付費、有 API Key
- ✅ 只要 API「外觀」符合即可，背後可以是本地模型、私有模型、自架 API

**生活化比喻：** Open-WebUI 只插「USB-C」，只要你的服務也做成 USB-C，就能用。

---

## 為什麼需要 Pipeline Server？

**什麼時候 Filter / Tools 不夠用？**

| 情境 | 建議 |
|------|------|
| 流程不只一個步驟 | Pipeline |
| 需要和 Open-WebUI 以外系統共用 | Pipeline |
| 模型前後都要做處理 | Pipeline |
| 想把 AI 行為做成「一個服務」 | Pipeline |
| 單一請求的簡單調整 | Filter / Tools |

**一句話：**  
> Pipeline Server = 把「和模型互動的整個流程」獨立成一個 API 服務

---

## Pipeline 與 Filter / Tools 的差異

| 比較 | Filter | Tools | Pipeline |
|------|--------|-------|----------|
| **定位** | 即時加工 | 單次能力擴充 | 流程設計 |
| **適合** | 修改 prompt、加系統訊息 | 查資料、呼叫 API | 多步驟、可重組流程 |
| **限制** | 順序固定、難模組化 | 工具間難串接 | 需獨立部署 |

**簡單判斷：**  
Filter / Tools 解決「會不會做」，Pipeline 解決「怎麼串」。

---

## Pipeline 與 MCP 的差異

| 比較 | Pipeline | MCP |
|------|-----------|-----|
| **標準** | OpenAI-compatible | MCP 協定 |
| **流程決策** | 程式決定流程 | 模型決定是否呼叫工具 |
| **架構類型** | Flow 型（固定流程） | Tool 型（Agent 架構） |

---

上一篇：—  
下一篇：[Pipeline_01_第一個Pipeline](../Pipeline_01_第一個Pipeline/README.md)
