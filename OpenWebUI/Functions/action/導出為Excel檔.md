# Action 進階教學 2：導出為 Excel 檔案 (資料整理)

此方案將把整段對話的所有訊息歷程（User 與 AI）結構化，結合 Pandas 轉換表格，並透過 Base64 Data URI 技巧匯出成 Excel 檔案 (`.xlsx`)。

> 若需了解 Base64 Data URI 下載的核心概念與機制，建議先參考：[進階 Action 教學 1：導出為 Word 檔](./導出為Word檔.md)。

---

## 📊 完整程式碼

```python
"""
title: 導出為 Excel
author: 您的姓名
version: 1.0
description: 將完整聊天對話記錄導出為 Excel 試算表。
requirements: pandas, openpyxl
"""

import base64
from io import BytesIO
from typing import Optional
from datetime import datetime

import pandas as pd
from fastapi import Request

class Action:
    def __init__(self):
        self.type = "action"
        self.id = "export_to_excel"
        self.name = "📊 導出為 Excel"

    async def action(
        self, body: dict, __user__: Optional[dict] = None, __event_emitter__=None
    ) -> Optional[dict]:
        
        messages = body.get("messages", [])
        if not messages:
            return body
        
        data = []
        for msg in messages:
            data.append({
                "發言角色": "使用者" if msg.get("role") == "user" else "AI 助手",
                "對話內容": msg.get("content", ""),
                "導出時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        
        # [步驟 2] 利用 Pandas 產生 DataFrame
        df = pd.DataFrame(data)
        
        # [步驟 3] 將 DataFrame 轉換為 Excel 二進制緩衝
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='歷史聊天記錄', index=False)
        buffer.seek(0)
        
        # [步驟 4] 編碼為 Base64
        file_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        # [步驟 5] 組合 Data URI 並附加至最後一則對話
        data_uri = f"data:{mime_type};base64,{file_base64}"
        
        messages[-1]["content"] += f"\n\n---\n✅ **Excel 檔案已生成** (共 {len(data)} 條)：\n\n[📥 點擊下載 (.xlsx)]({data_uri})"
        
        return body
```

---

## 💡 開發解析

1. 本範例運用了 `pandas` 強大的資料結構 `DataFrame` 收集所有歷史訊息。包含發言角色、內容與時間等。
2. 因為在 Open WebUI Functions 中我們並沒有實際的主機檔案寫入權限 (或不建議寫入)，我們將 `pd.ExcelWriter` 指向一個虛擬記憶體區塊 `BytesIO`。
3. 把此二進位緩衝區的數據進一步用 Base64 編碼，最後以 HTML 連結形式塞入對話底部，然後回傳 `body`。這可避免使用 `__event_emitter__` 時觸發前端串流解析錯誤 (`Unexpected token d in JSON`)。
