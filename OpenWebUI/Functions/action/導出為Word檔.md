# Action 進階教學 1：實作 Base64 檔案導出 (以 Word 為例)

> **適用情境**：將大語言模型（如 Gemma4 等）分析或生成的結果，一鍵導出為 Word 格式檔案並觸發下載。  
> **核心技術**：Base64 檔案編碼、Data URI 協定、修改訊息本文回傳下載連結。

---

## 🎯 學習目標

本教學旨在引導您於 Open WebUI 的 Action Function 中，利用 **Base64 Data URI** 技巧實作純前端的檔案下載功能，無須仰賴伺服器存取外部檔案系統。

**常見應用場景**：
- 快速將單次且冗長的聊天紀錄或對話保存為 Word 文檔 (`.docx`)。

---

## 💡 核心原理與機制

### 1. 運作流程
```text
[1] 使用者點擊對話下方的 Action 按鈕
 └→ [2] 觸發後端 Action Function 執行 Python 邏輯
     └→ [3] 將目標內容寫入記憶體緩衝區 (BytesIO) 並轉換為檔案格式
         └→ [4] 將二進制檔案 (bytes) 編碼為 Base64 字串
             └→ [5] 組合 Data URI 並附加至最後一則對話的底端
                 └→ [6] 使用者點選對話下方的連結即可觸發下載
```

### 2. Base64 Data URI 語法結構
透過標準 HTML 支援的 Data URI，我們可以把整個檔案內容塞進網址列中：
```html
<a href="data:[MIME_TYPE];base64,[BASE64_STRING]" download="[FILENAME]">
    點此下載檔案
</a>
```

**常見的 MIME 類型對照表**：

| 檔案格式 | MIME 類型 (MIME Type) |
|---------|---------|
| **Word** (`.docx`) | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| **Excel** (`.xlsx`) | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| **PDF** (`.pdf`) | `application/pdf` |
| **JSON** (`.json`) | `application/json` |
| **純文字** (`.txt`) | `text/plain` |

---

## 📝 導出為 Word 檔案 (基礎實作)

此方案擷取對話中的最後一次 Assistant (AI) 回應，將其包裝為 `.docx` 格式後提供下載。

### 完整程式碼

```python
"""
title: 導出為 Word
author: 您的姓名
version: 1.0
description: 將聊天內容導出為 Word 檔案，支援一鍵下載。
requirements: python-docx
"""

import base64
from io import BytesIO
from typing import Optional
from datetime import datetime

from docx import Document

class Action:
    def __init__(self):
        self.type = "action"
        self.id = "export_to_word"
        self.name = "📝 導出為 Word"

    async def action(
        self, body: dict, __user__: Optional[dict] = None, __event_emitter__=None
    ) -> Optional[dict]:
        """
        將最後的聊天回應導出為 Word 檔案。
        """
        
        messages = body.get("messages", [])
        last_response_idx = -1
        
        for i, msg in enumerate(reversed(messages)):
            if msg.get("role") == "assistant":
                last_response_idx = len(messages) - 1 - i
                break
        
        if last_response_idx == -1:
            return body
            
        last_response = messages[last_response_idx].get("content", "")
        
        # [步驟 2] 建立 Word 文件與排版
        doc = Document()
        doc.add_heading("AI 助手回應記錄", level=1)
        
        user_name = __user__.get('name', 'Anonymous') if __user__ else 'Anonymous'
        doc.add_paragraph(f"使用者: {user_name}")
        doc.add_paragraph(f"導出時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.add_paragraph("─" * 50)
        
        doc.add_heading("AI 回應內容", level=2)
        doc.add_paragraph(last_response)
        
        # [步驟 3] 輸出至記憶體緩衝區
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        # [步驟 4] 編碼為 Base64
        file_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        # [步驟 5] 組合 Data URI 並附加至訊息末端
        mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        data_uri = f"data:{mime_type};base64,{file_base64}"
        
        # 將連結以 Markdown 格式塞入目前的對話紀錄中，OpenWebUI 會自動將 Markdown 連結加上 target="_blank" 以在新分頁開啟/下載
        messages[last_response_idx]["content"] += f"\n\n---\n✅ **Word 檔案已生成**：\n\n[📥 點擊此處立即下載 (.docx)]({data_uri})"
        
        # 回傳變更後的 body 讓前端更新畫面
        return body
```

---

## 🔧 技術細節與常見問題

### 1. 為什麼直接加進 `content` 中？
因為目前 Open WebUI 的 Action 按鈕在架構上預設只接收純 JSON 回傳，並不完全支援 SSE 串流 (也就是 `__event_emitter__`) 或網頁物件 (`HTMLResponse`)，如果強行使用，會導致前端拋出 JSON 解析錯誤 (`not valid JSON`)。因此將超連結附加在對話內容中並回傳 `body` 是最穩定相容的做法。但請注意：這會使得 Base64 成為對話紀錄的一部份，可能導致對話的上下文 (Context Window) 長度增加。

### 2. Base64 機制的優勢與限制
- **優勢**：安全且優雅。檔案在記憶體中生成後直達瀏覽器，**不留痕跡於伺服器硬碟**，避免硬碟佔用與權限存取風險。
- **限制**：檔案體積。Base64 編碼會導致傳輸體積暴增約 **33%**，且瀏覽器位址列處理 Data URI 約有 100MB 上下的硬性上限。故僅適合用於文書處理或中小型數據傳輸。

### 3. 常見錯誤排除
- **按鈕為何沒有出現？**
  請確認此 Action 已於管理後台啟用，並已指派至當前的工作區自訂模型（Workspace → Models → Actions）。
- **下載的檔案打不開 / 提示毀損？**
  請檢查 `buffer.seek(0)` 是否有在編碼前正確執行；並且確認 MIME Type 與副檔名是否確實對齊。
- **為何少了套件錯誤 (ModuleNotFoundError)？**
  請確保標頭區塊宣告了 `requirements: python-docx` 等依賴套件，使系統能在啟動此 Function 時自動呼叫 pip 裝填環境。

---
 
**🎓 最終建議**：您可以搭配使用 `__event_emitter__` 實現載入動畫（請參見【[基礎 Action 範例](./基礎Action範例.md)】），提升檔案建立過程中的互動體驗。
