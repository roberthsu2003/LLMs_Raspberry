# 範例三：高階 Python 腳本（檔案讀取與 UI 狀態回報）

在這個最高階的範例中，我們會結合兩個 OpenWebUI 非常專屬且強大（但文件較少提及）的保留功能：
1. `__files__`：自動抓取使用者上傳的檔案陣列。
2. `__event_emitter__`：主動將後台的進度動畫（如 ⏳ 讀取中...）推送到前端畫面上。

如果您的應用情境需要花較長的時間（例如讀取一張極大的 CSV、呼叫極慢的外部 API），使用 `__event_emitter__` 能大幅提升使用者體驗 (UX)，讓使用者不會以為系統當機了。

---

## 🛠️ 實作步驟

1. 在 OpenWebUI 介面，進入 **Workspace (工作區) → Tools (工具)** 點擊新增。
2. 名稱定義為 `FileAnalyzerTool`。
3. 將以下完整結構的 Python 程式碼貼上：

### 🐍 Python 程式碼範例

```python
from typing import Callable, Awaitable, Any, List
import asyncio

class Tools:
    def __init__(self):
        pass

    async def analyze_uploaded_document(
        self,
        query: str,
        __files__: List[dict] = [],
        __event_emitter__: Callable[[dict], Awaitable[None]] = None
    ) -> str:
        """
        當使用者要求檢查或解析上傳的檔案時，使用這個工具。
        此工具會讀取檔案 Metadata 並發送即時進度狀態給前端畫面。
        
        :param query: 使用者原本提出的任何要求。
        :param __files__: (勿填) 系統自動注入的使用者上傳檔案列表。
        :param __event_emitter__: (勿填) 系統自動注入的狀態回報發射器。
        """

        # 1. 檢查是否有收到檔案
        if not __files__:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "❌ 警告：沒有偵測到上傳檔案", "done": True}
                })
            return "系統未偵測到您的檔案，請確認是否上傳成功。"

        try:
            # 2. 通知前端開始工作 (顯示 Loading 圖示)
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "⏳ 正在讀取並解析您上傳的檔案...", "done": False}
                })

            # 3. 模擬一個需要耗時運算的情境 (例如：呼叫外部伺服器或做大量矩陣運算)
            await asyncio.sleep(3) 

            # 4. 讀取並整理檔案資訊
            files_info = []
            for f in __files__:
                filename = f.get('filename', 'Unknown')
                file_id = f.get('id', 'N/A')
                # 這裡僅取得檔名與 ID，實戰中您可能需要利用 file_id 去伺服器路徑下讀取實體檔案內容
                files_info.append(f"檔名: {filename} (ID: {file_id})")

            final_report = "\n".join(files_info)

            # 5. 回報工作完成
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "✅ 檔案解析完成！", "done": True}
                })

            # 將結果傳回給 LLM 進行最後語意整理
            return f"以下是您上傳的檔案清單分析結果：\n{final_report}\n\n指令(請直接告訴使用者)：我已幫您檢查完畢了。"

        except Exception as e:
            # 發生失敗時的除錯處理
            if __event_emitter__:
                await __event_emitter__({
                    "type": "status",
                    "data": {"description": "❌ 解析失敗，發生錯誤！", "done": True}
                })
            return f"分析工具發生嚴重錯誤：{str(e)}"
```

---

## 🚀 測試與運作原理

1. 儲存工具並確認掛載後，請開啟對話視窗。
2. 點擊對話視窗的 `+` 上傳一份隨意的測試檔案（例如隨便一張圖片或 Markdown 檔）。
3. 接著輸入：「`請幫我執行檔案的詳細檢查。`」
4. **觀察畫面變化：**
   * 您會立刻在畫面上看到一個轉圈動畫寫著 **「⏳ 正在讀取並解析您上傳的檔案...」**
   * 三秒鐘後，這段字會變成綠色打勾字樣 **「✅ 檔案解析完成！」**
   * 隨後 AI 會結合工具算出的結果，回報您上傳的檔名與內部 ID！

---

> 💡 **結語**：
> 這個範例極其重要，因為在串接企業內部資料庫或是處理大型 Excel 時，往往需要數秒鐘甚至數十秒鐘的運算。
> 若沒有 `__event_emitter__`，使用者會看著畫面發呆以為樹莓派當機了。加上這個狀態推播，就能創造出專業且流暢的 AI 使用者體驗 (UX)！
