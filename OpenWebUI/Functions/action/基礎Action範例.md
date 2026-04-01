# Action 範例：顯示目前訊息字數（最簡）

**行為**：使用者點擊訊息下方的 Action 按鈕後，在介面上顯示一則**狀態通知**，內容為該則訊息的字元長度。

**重點**：

- 類別名稱必須為 **`Action`**。
- 主要邏輯寫在 **`async def action(...)`**。
- **`body["message"]["content"]`**：目前這則訊息的文字（依 Open WebUI 版本，結構請以實機為準）。
- **`__event_emitter__`**：可選，用來對前端發送通知（例如 `type: "status"`）。

```python
"""
title: 基礎 Action 範例
author: Gemini
version: 1.0
"""

from typing import Optional, Callable, Any


class Action:
    def __init__(self):
        pass

    async def action(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[..., Any]] = None,
    ) -> Optional[dict]:
        message_content = body.get("message", {}).get("content", "")
        message_len = len(message_content)

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"這則訊息的長度是：{message_len} 個字",
                        "done": True,
                    },
                }
            )

        return None
```

## 說明

- 多數 Action 在完成後可 **`return None`**（不需把結果再餵回模型時）。  
- 若需 Valves（可調參數），可仿照講義第二章 Valves 小節，在 `Action` 內加上內部類別 `Valves` 與 `self.valves`。

## 指派方式（與 Filter 相同）

使用方式與 **Filter** 一樣：到 **工作區** → **新增模型**（或 **建立模型**，依版本而異），在建立／編輯自訂模型的畫面中：

- 可選 **過濾器（Filter）** 與 **行動：**（或 **Actions**）。  
- **行動：** 後方會列出目前可用的 Action，**勾選**本範例後儲存。  
- 聊天時請選用**這個自訂模型**，訊息旁才會出現按鈕。

詳見講義第三章 §3.5、第五章 §5.3。

## 測試步驟

1. 到**聊天頁面**，隨便輸入一段話（例如：「你好，這是一次測試」）。  
2. 在**這則訊息下方**（通常在按讚、複製等按鈕旁邊），會多出一個**新的按鈕圖示**（預設可能是小圓點、閃電符號等，依版本而定）。  
3. **點擊該按鈕**，畫面上方應會彈出**通知**，顯示這則訊息的字數。
