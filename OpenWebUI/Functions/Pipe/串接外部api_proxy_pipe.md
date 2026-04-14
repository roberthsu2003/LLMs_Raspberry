##  串接外部 API (API Proxy Pipe)

在實際應用中，我們通常會用 Pipe 來串接尚未被 Open WebUI 原生支援的 API。這個範例展示如何使用 `requests` 套件來呼叫一個外部的 HTTP API。

**核心概念**：如何在 Pipe 中進行網路請求，並將 API 的回傳結果轉化為 Open WebUI 的回應。

```python
import requests
from typing import Union, Generator, Iterator

class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "api_proxy_pipe"
        self.name = "外部 API 代理模型"

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        user_message = body["messages"][-1]["content"]
        
        # 模擬呼叫外部 API (例如某個翻譯或摘要服務)
        api_url = "https://api.example.com/v1/chat"
        payload = {
            "prompt": user_message,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(api_url, json=payload, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["text"]
        except Exception as e:
            return f"API 呼叫失敗: {str(e)}"
```