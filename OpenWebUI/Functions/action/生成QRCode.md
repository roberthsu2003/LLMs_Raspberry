# 生成 QR Code

> 🔲 視覺化很震撼

```python
"""
title: Generate QR Code
author: Your Name
version: 0.1.0
"""

from pydantic import BaseModel
import qrcode
import base64
from io import BytesIO

class Action:
    class Valves(BaseModel):
        size: int = 10

    def __init__(self):
        self.valves = self.Valves()

    async def action(
        self,
        body: dict,
        __user__=None,
        __event_emitter__=None,
        __event_call__=None,
    ) -> Optional[dict]:
        """將訊息轉成 QR Code"""
        
        message_content = body.get("message", "")[:500]  # QR 有大小限制
        
        if not message_content:
            return {"status": "empty"}
        
        try:
            # 生成 QR Code
            qr = qrcode.QRCode(box_size=self.valves.size)
            qr.add_data(message_content)
            qr.make()
            
            img = qr.make_image()
            
            # 轉成 Base64
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            if __event_emitter__:
                await __event_emitter__({
                    "type": "message",
                    "data": {
                        "content": f"✅ QR Code 已生成！\n![QR Code](data:image/png;base64,{img_base64})"
                    }
                })
        
        except Exception as e:
            if __event_emitter__:
                await __event_emitter__({
                    "type": "message",
                    "data": {
                        "content": f"❌ 生成失敗: {str(e)}"
                    }
                })
        
        return {"status": "completed"}
```
