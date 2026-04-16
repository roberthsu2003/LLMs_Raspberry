# 送出 Telegram 通知

> 🔔 展示外部 API 整合 (Webhook / Bot 串接)
> 相比 Slack，Telegram Bot 申請極為簡單，非常適合個人推播使用！

## Telegram 申請與設定

比起申請 Slack Webhook，Telegram 的這項功能「**完全免費**、**申請極速**、**而且永遠不會過期**」，所以非常推薦做為串接教學的第一站！

### 🤖 申請與設定三步圖解：
1. **取得 Token**：在 Telegram 搜尋框尋找 `@BotFather` (官方爸爸)，點擊 Start 後輸入 `/newbot` 建立機器人。依照指示取個好名字後，系統就會噴給您長長一串的 `HTTP API Token`。
2. **取得 Chat ID**：接著在 Telegram 搜尋 `@userinfobot` 或 `@getmyid_bot`，一樣點擊 Start，它馬上會吐出您個人專屬的數字 ID（例如：`123456789`）。
3. **填入設定 (Valves)**：回到 Open WebUI，將這兩個數值貼到這個 Action 的 Valves (管理介面的設定齒輪) 欄位中，立刻就可以一鍵把重要的總結傳進自己的手機裡！

```python
"""
title: Send to Telegram
author: Your Name
version: 0.1.0
requirements: requests, pydantic
"""

from pydantic import BaseModel, Field
from typing import Optional
import requests

class Action:
    class Valves(BaseModel):
        bot_token: str = Field(
            default="",
            description="Telegram Bot Token (從 @BotFather 取得)"
        )
        chat_id: str = Field(
            default="",
            description="你的 Telegram Chat ID (可向 @userinfobot 查詢)"
        )

    def __init__(self):
        self.valves = self.Valves()

    async def action(
        self,
        body: dict,
        __user__=None,
        __event_emitter__=None,
        __event_call__=None,
    ) -> Optional[dict]:
        """將訊息發送到 Telegram"""
        
        # 安全取得最後一句對話
        messages = body.get("messages", [])
        if not messages:
            return {"status": "empty"}
            
        last_message = messages[-1]
        message_content = last_message.get("content", "")
        
        if not self.valves.bot_token or not self.valves.chat_id:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "message",
                    "data": {
                        "content": "❌ 未設定 Telegram 機器人 Token 或 Chat ID"
                    }
                })
            return {"status": "failed"}
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "description": "正在發送到 Telegram...",
                    "done": False
                }
            })
        
        try:
            # Telegram Bot API URL
            api_url = f"https://api.telegram.org/bot{self.valves.bot_token}/sendMessage"
            
            # 加入發送者名稱提示
            sender = __user__.get("name", "一般使用者") if __user__ else "使用者"
            formatted_msg = f"🔔 **來自 {sender} 的備忘錄**:\n\n{message_content}"
            
            payload = {
                "chat_id": self.valves.chat_id,
                "text": formatted_msg,
                "parse_mode": "Markdown" # 讓 Telegram 支援字體加粗等排版
            }
            
            response = requests.post(api_url, json=payload, timeout=10)
            result = response.json()
            
            if __event_emitter__:
                if response.status_code == 200 and result.get("ok"):
                    await __event_emitter__({
                        "type": "message",
                        "data": {
                            "content": "✅ 訊息已經用小飛機 ✈️ 發送到 Telegram 囉！"
                        }
                    })
                else:
                    await __event_emitter__({
                        "type": "message",
                        "data": {
                            "content": f"❌ Telegram 發送失敗: {result.get('description', '未知錯誤')}"
                        }
                    })
        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "message",
                    "data": {
                        "content": f"❌ 系統發生錯誤: {str(e)}"
                    }
                })
        
        return {"status": "completed"}
```

