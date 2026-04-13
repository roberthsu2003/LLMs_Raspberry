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
