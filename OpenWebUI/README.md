# Open-WebUI 
## **🔎 一、Open WebUI 是什麼？**

**Open WebUI** 是一個開源、自架的 AI 介面平台，可以在本地或私有環境運行大型語言模型（LLM），用戶透過瀏覽器 GUI 操作模型並執行對話、生成、資料整合等任務。它強調 **易用性、可擴充性與離線運作能力**，支援各種 LLM 運行器（如 Ollama、自訂 OpenAI API 等），並具備豐富的功能插件與工作流整合支援。



### **📌 1. 互動式聊天與模型操作**

學生可透過視覺化界面直接與語言模型對話、設定參數、選擇不同模型。

**實作**
- 使用 Ollama 運行模型
- 使用 Open Router 運行模型
- 使用大模型API（如 GPT-4)

### **📌 2. 檢索增強生成（RAG）**

可將教學文件、知識庫導入，讓模型回答時結合本地文件知識。

### **📌 3. 自訂工作流與管線（Pipelines）**

Open WebUI 提供管線機制，可用 Python 擴充流程，例如：

- 自動翻譯
- 函數呼叫整理
- 事件監控或資料預處理
- 讓 AI 對話和外部邏輯整合。

### **📌 4. 外部工具與網頁內容整合**

可在對話中串接網站內容、Web API、甚至建立 OpenAPI 伺服器來擴充工作流程。

## **⚙️ 如何把 Open WebUI 導入工作流程**


### **📍案例 1：樹莓派 + Open WebUI 做知識查詢教學**

1. 在樹莓派上安裝 Open WebUI
2. 將教學文件（如 PDF、文本）加入 RAG 索引
3. 讓學生用 WebUI 問答自動整理文件重點

這讓學生體驗「模型不只聊天，還能結合知識庫回答問題」。

---

### **📍案例 2：建立自動化流程（Pipelines）**

1. 安裝 Pipelines framework
2. 寫一個簡單 Python 管線，例如：

```other
def translate_pipeline(input_text):
    # 用翻譯 API 對輸入文本翻譯
    return translated_text
```

1. 在 Open WebUI 設定對應流程
2. 學生測試：輸入英文 -> 自動翻譯成中文

這是將 AI 工作流整合到實際應用的好例子。

---

### **📍案例 3：串接外部 Web API**

透過 OpenAPI 工具伺服器：

1. 建立一個可回傳時間/天氣資料的 API 伺服器
2. 在 Open WebUI 設定 External Tool
3. 用 LLM 與工具互動

這種練習可以讓學生理解「AI + API 整合」的實際價值。

## **🧪 五、課堂練習建議**

| **練習主題**       | **目標**        |
| -------------- | ------------- |
| 安裝 Open WebUI  | 學生理解基本架構與運行方式 |
| RAG 文件查詢       | 將教材知識變成可查詢知識庫 |
| Pipelines 自訂流程 | 學生寫簡易 AI 工作流  |
| API 整合         | 了解如何擴充 AI 服務  |

---
## **🔗 怎麼串接 Open WebUI 與 n8n**

### **📌 1. 使用「n8n Pipe Function」**

社群有專門為 Open WebUI 寫的 **n8n pipe function（或稱 n8n integration）**，這是一段可以放在 Open WebUI 裡的程式碼，用來：

- 把對話的文字送到 n8n workflow（通常透過 webhook）
- 等 n8n workflow 處理完再把回應送回 Open WebUI

    這樣 Open WebUI 裡的對話就能呼叫你在 n8n 設計的流程與邏輯。

這種方式是目前比較直接的整合方式，概念是「Open WebUI 作為介面，n8n 負責處理流程與邏輯」。

---

### **📌 2. 用 Webhook 與 HTTP Request**

最簡單的串接方式是：

1. 在 n8n 裡建立一個 **Webhook Trigger 節點**
2. Open WebUI 呼叫這個 webhook（透過 HTTP 請求）
3. n8n workflow 處理後，再把結果回傳

這樣基本上就可以讓 Open WebUI 與 n8n 溝通。

---

### **📌 3. 用「OpenAI-Compatible Bridge」**

社群也有人寫出 **OpenAI 兼容的中介橋接器**（bridge），讓 n8n workflow 看起來像一個 OpenAI 模型：

- 把 n8n workflow 包裝成 OpenAI API 格式
- 然後 Open WebUI 用原生的 OpenAI API node 直接呼叫它

這樣可以省去一些客製化的流程。

---

## **🧪 教學重點 & 實作建議**

### **📍 使用情境示例**

| **情境**                                  | **做法**              |
| --------------------------------------- | ------------------- |
| 想從 Open WebUI 呼叫 n8n 來處理資料、查 DB 或外部 API | 用 webhook + HTTP 請求 |
| 想讓對話上下文能夠帶入 n8n 的自動化流程邏輯                | 用 n8n pipe function |
| 想把 n8n workflow 當成「LLM 模型」去呼叫           | 用 OpenAI Bridge 模式  |

---

## **📌 注意事項**

❗ **n8n 的 OpenAI node 可能不完全兼容 Open WebUI**

有些使用者回報 OpenAI node 設定可能會失敗，需要改用 HTTP Request 或調整參數。

❗ **串接可能需要處理格式與身份驗證**

例如使用 bearer token 或 webhook 安全設定等。

---

### **🧠 簡單結論**

✅ 是可以串接

🔧 需要用 webhook / pipe function 或 bridge

🛠️ 不是單純按一個按鈕就完成，但社群已經有不少實作例子可以參考

---

如果你需要，我也可以整理成 **樹莓派上實作的步驟（含 webhook 設定、n8n 範例工作流程、Open WebUI pipe function 示範程式碼）**。需要嗎？
