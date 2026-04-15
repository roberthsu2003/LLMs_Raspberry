# 送出 Slack 通知

> 🔔 展示外部 API 整合

```python
"""
title: Send to Slack
author: Your Name
version: 0.1.0
"""

from pydantic import BaseModel, Field
import requests

class Action:
    class Valves(BaseModel):
        webhook_url: str = Field(
            default="",
            description="Slack Webhook URL"
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
        """將訊息發送到 Slack 頻道"""
        
        message_content = body.get("message", "")
        
        if not self.valves.webhook_url:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "message",
                    "data": {
                        "content": "❌ 未設定 Slack Webhook URL"
                    }
                })
            return {"status": "failed"}
        
        if __event_emitter__:
            await __event_emitter__({
                "type": "status",
                "data": {
                    "description": "正在發送到 Slack...",
                    "done": False
                }
            })
        
        try:
            payload = {
                "text": message_content,
                "username": __user__.get("name", "Open WebUI Bot") if __user__ else "Bot"
            }
            
            response = requests.post(self.valves.webhook_url, json=payload)
            
            if __event_emitter__:
                if response.status_code == 200:
                    await __event_emitter__({
                        "type": "message",
                        "data": {
                            "content": "✅ 訊息已發送到 Slack！"
                        }
                    })
                else:
                    await __event_emitter__({
                        "type": "message",
                        "data": {
                            "content": f"❌ 發送失敗: {response.status_code}"
                        }
                    })
        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "message",
                    "data": {
                        "content": f"❌ 錯誤: {str(e)}"
                    }
                })
        
        return {"status": "completed"}
```
