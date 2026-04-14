# OpenWebUI 技能 (Skills)

**Skills（技能）是 OpenWebUI 賦予大型語言模型（LLM）「執行任務」的核心擴充機制**。透過 Skills，AI 不再只是單純回答文字，而是具備了呼叫外部工具、執行自動化流程與處理複雜文件的能力。

本文件整理了 Skills 的用途、使用方法、實際情境，幫助您快速掌握這項強大功能。

---

## 🎯 為什麼需要 Skills？

根據官方文件定義，**Skills 提供了一段可被模型載入的指令與能力描述，模型會根據對話情境自動決定何時使用該能力**。
簡而言之，它就像是給 AI 的「專業能力說明書」。

### 1️⃣ 擴充 AI 的基礎功能
OpenWebUI 本身這套平台支援多種擴展機制，透過 Skills 可以輕易賦予 AI 額外能力：
*   **查詢外部資料**：如查詢公司內部資料庫（RAG）、股價、天氣、匯率 API。
*   **檔案處理與分析**：解析 PDF 文件、讀取 CSV 進行數據分析。
*   **執行程式碼**：自動執行 Python 腳本或 Shell 指令。

### 2️⃣ 建立專屬 AI 助手 (Agent)
將特定 Skill 綁定到模型，就能建立各種專業助手。例如：
*   **程式碼助教**：套用 Code Review Skill。
*   **企業助理**：套用 CRM 查詢 Skill。
*   **研究助理**：套用學術論文檢索 Skill。

### 3️⃣ 自動化工作流程 (Agent Workflow)
多個 Skill 也能組合串接成完整的工作流。
*   *範例情境（重點摘要流程）*：`PDF 解析 Skill` ➡️ `重點摘要 Skill` ➡️ `多國語言翻譯 Skill`。

---

## 🛠️ 如何建立與使用 Skills？

OpenWebUI 提供了多種管理 Skills 的方式，可依個人開發習慣選擇。

### 方法 1：透過網頁介面建立 (推薦新手)
1. 進入 **Workspace (工作區) → Skills (技能)**。
2. 點擊 **+ New Skill**（新增技能）。
3. 填寫以下核心欄位：
   *   **Name (名稱)**：定義此 Skill 的顯示名稱。
   *   **Skill ID**：作為系統中的唯一識別碼。
   *   **Description (描述)**：清楚描述該技能的作用，**模型將依賴此欄位判斷是否觸發**。
   *   **Content (內容)**：此處可使用 Markdown 撰寫給模型的 System Prompt 或操作指令。

> **🌟 最小 Skill 範例（中翻英小幫手）：**
> ```yaml
> Name: translate-en
> Description: translate Traditional Chinese to English
> Content:
> When user writes Chinese, translate it to English natively.
> ```

### 方法 2：透過資料夾架構管理 (進階開發)
OpenWebUI 伺服器會自動監聽並載入 `skills/` 目錄下的設定。每個子資料夾代表一個獨立的 Skill。
```text
skills/
 └── pdf-summary/
      ├── SKILL.md      # 用於描述此 skill 的能力與使用時機
      └── script.py     # 實際執行該任務的 Python 腳本或後端邏輯
```

### 方法 3：在對話中呼叫
當 Skill 建立完成後：
*   **手動觸發**：在聊天室輸入對話時，打出以 `#` 或 `$` 開頭的快速指令，強制呼叫特定功能。
*   **自動觸發**：當您的問題符合該 Skill 的 Description 時，模型會自動決定並調用。

---

## 💡 常見實際使用情境

| 情境 | 代表 Skill 名稱 | 實際用途 |
| :--- | :--- | :--- |
| **RAG 知識庫查詢** | `search_docs` | 連接外掛的向量資料庫（Vector DB），讓 AI 查詢企業內部請假規範或專案文件後進行回答。 |
| **外部 API 整合** | `weather_api` | 讓 AI 能即時抓取並回報當地的天氣、最新匯率或股票資料。 |
| **本地多模型協同** | `translate_by_llama` | 在同一個流程內，讓強大的主模型調用輕量化本地模型（如 Llama3、Gemma）執行翻譯或摘要等輕型任務。 |

---

## 🔍 Skills 與 Tools 的關係

在 OpenWebUI 的擴充生態系中，有幾個容易與 Skills 混淆的概念：

*   **Skills (技能)**：側重於賦予模型額外的行為指令或能力，可視為封裝好的任務提示包或程式擴展。
*   **Tools (工具)**：提供給 LLM 呼叫的外部函式與腳本（像是聯網搜尋、API 呼叫）。
*   **Pipelines (管線)**：自訂整個資料流入與模型輸出的客製化工作流程機制。
*   **MCP (外部工具協定)**：一個標準化的工具通訊協定，用來讓 AI 安全地存取本機的特定資源（如檔案系統、資料庫）。

---

## 📚 延伸學習資源

如果您想深入實作，以下為您整理了相關的進階教學資源，請參考各篇獨立文件：

- [1️⃣ Skill vs Function vs Filter 差異](./1-Skill_vs_Function_vs_Filter差異.md)
- [2️⃣ open-webui skill 範例（完整程式）](./2-open-webui_skill範例.md)
- [3️⃣ 如何讓 skill 讀取使用者上傳檔案](./3-如何讓skill讀取使用者上傳檔案.md)
- [4️⃣ 最常用 skill 清單（教學版）](./4-最常用skill清單.md)