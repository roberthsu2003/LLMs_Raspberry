# 如何讓 Skill 讀取使用者上傳檔案

在 OpenWebUI 中，當使用者在對話框中上傳檔案（例如 PDF、CSV 或圖片）並呼叫特定功能時，我們有兩種主要方式可以讓系統讀取並處理這些檔案：**基礎的 RAG 手段** 與 **進階的 Python 程式邏輯 (適用於 Tools / Actions)**。

以下為這兩種方式的實作指南。

---

## 🟢 基礎指南：使用預設的 RAG 機制（適合一般 Prompt Skill）

如果您建立的是一個純文字的 **Prompt (提示詞)** 或基礎 **Skill**，最簡單的方法就是讓 OpenWebUI 內建的 RAG（檢索增強生成）引擎來處理檔案。

1. **使用者操作**：點擊對話框旁的 `+` 按鈕（或直接拖曳）上傳檔案。
2. **呼叫 Skill**：在對話中呼叫您的 Skill，例如 `@總結助理 請看這份檔案`。
3. **運作原理**：OpenWebUI 會在背景自動將上傳的文件解析、分塊（Chunking），並寫入預設的向量資料庫中。模型在生成回答時，會自動從資料庫把相關的檔案內容拉進 Context Window（上下文）中供模型參考。

**優點**：不需寫任何程式，支援多種文件格式（PDF, DOCX, TXT）。
**缺點**：如果需要精準的結構化讀取（例如逐行讀取 CSV 或利用特定 Python 套件作圖），RAG 可能會遺漏細節。

---

## 🔴 進階指南：在 Tools / Actions 中使用 `__files__` 參數（需撰寫 Python）

如果您開發的是可以用 Python 驅動的 **Tools (工具)** 或 **Functions (函式)**，您可以使用保留參數 `__files__` 來捕捉會話中夾帶的檔案。

這是最強大、也最能精準控制資料流的方法。

### 步驟與程式碼範例

在您的 Tool Class 中，於工具執行的函式裡加入 `__files__: List[dict] = []` 作為參數。OpenWebUI 在執行該 Tool 時，若系統偵測到使用者對話夾帶檔案，會自動將檔案中介資料（metadata）灌入該列表中。

```python
from typing import List
import os

class Tools:
    def __init__(self):
        pass

    def process_attached_files(self, query: str, __files__: List[dict] = [], __user__: dict = {}) -> str:
        """
        讀取並處理使用者在對話中上傳的檔案。
        
        :param query: 使用者輸入的文字指令
        :param __files__: OpenWebUI 會自動注入此對話附帶的檔案列表
        """
        if not __files__:
            return "❌ 系統沒有偵測到您上傳任何檔案，請先上傳檔案後再試一次。"
            
        results = []
        for file in __files__:
            # 檔案字典 (dict) 通常包含 file_id, filename 等基礎資訊
            # 注意：取決於 OpenWebUI 的版本，有時這只是 metadata，實際內容可能需要另外透過 API 或檔案系統 ID 讀取
            filename = file.get("filename", "未知檔案名稱")
            file_id = file.get("id", "未知 ID")
            
            results.append(f"✅ 成功讀取檔案：{filename} (ID: {file_id})")
            
            # TODO: 您可以在這裡撰寫使用 pandas 讀取檔案、或呼叫特定解析庫的邏輯
            # 例如：
            # file_path = f"/app/backend/data/uploads/{file_id}" # (依據 OpeWebUI 環境架構而定)
            
        return "\n".join(results)
```

### 關鍵開發注意事項：

1. **參數保留字**：請務必確保參數名稱精準拼寫為 `__files__`，這是 OpenWebUI 的環境保留字，系統透過參數名稱來進行資料注入（Dependency Injection）。
2. **Metadata 與實際內容的差異**：`__files__` 列表目前大多攜帶的是**檔案的中介資料 (檔案名稱、ID 等)**。若要在 Python 腳本內剖析檔案「內容」，請留意您的 OpenWebUI docker 對應的實體檔案儲存路徑（通常是藉由解析 `file_id` 找尋實體路徑），或者透過 OpenWebUI 內網 API （/api/v1/files/）來拉取實體檔案。
3. **防呆機制**：務必在腳本開頭撰寫 `if not __files__:` 來處理使用者忘記上傳檔案時的情境，避免腳本因為抓不到資料而報錯崩潰。
4. **Tool 觸發權重**：請在 Tool 函數的 `""" docstring """` 註解中，明確告訴 LLM **「當遇到使用者要求分析檔案時，請呼叫此工具」**，否則 LLM 可能會越過您的 Tool，直接去呼叫內建的 RAG 庫。

---

> 💡 **結語**：一般的問答、摘要情境建議多利用預設的 RAG 機制（寫一個好的 Prompt Skill 即可）；若是需要**統計分析、轉檔、或自動化流程**，再考慮撰寫帶有 `__files__` 參數的 Python Tool。
