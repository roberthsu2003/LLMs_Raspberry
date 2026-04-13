# Open WebUI Pipe Functions 講義

## 什麼是 Pipe？

**Pipe** 是 Open WebUI 中最強大的擴充功能之一。如果說 Filter 是「中間人（攔截訊息）」，那麼 Pipe 就是「後端供應商（提供模型）」。

當你在聊天選單中選擇一個 Pipe 時，Open WebUI 會將使用者的對話傳送給該 Pipe 實作的 `pipe()` 方法。你可以透過 Pipe 來：
1. **串接外部 API**（例如 Anthropic, Google Gemini, 或自建的推理伺服器）。
2. **建立自訂 Agent**（例如一個專門處理數學運算的 Agent）。
3. **多模型管理 (Manifold)**：讓一個 Pipe 同時提供多個模型選項。

---

## 範例一：入門級 —— 簡單的文字回傳 (Echo Pipe)

這個範例展示了 Pipe 最基本的結構。它不呼叫任何 AI，只是單純地將使用者的訊息回傳，並加上一段前綴。這對於理解資料流（Data Flow）非常有幫助。

**核心概念**：了解 `pipe()` 方法如何接收 `body` 並回傳字串。

```python
from typing import Union, Generator, Iterator

class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "echo_pipe"
        self.name = "回聲模型 (Echo Pipe)"

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        # 從 body 中取得最後一則使用者訊息
        user_message = body["messages"][-1]["content"]
        
        # 直接回傳加工後的文字
        return f"【回聲回應】：{user_message}"
```

---

## 範例二：進階級 —— 串接外部 API (API Proxy Pipe)

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

---

## 範例三：專家級 —— 多模型管理 (Manifold Pipe)

這是最進階的用法。透過實作 `pipes()` 方法，你可以讓一個 Pipe 函數變身為一個「模型包」，在選單中出現多個不同的模型選項。

**核心概念**：利用 `pipes()` 方法定義模型清單，實現一個 Pipe 管理多個後端。

```python
from typing import Union, Generator, Iterator

class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "manifold_pipe"
        self.name = "多模型組合包 (Manifold)"

    def pipes(self) -> list[dict]:
        """
        這是在 Manifold 模式下最重要的部分。
        回傳一個清單，包含你想在選單中顯示的模型 ID 與名稱。
        """
        return [
            {"id": "math_agent", "name": "數學專家 Agent"},
            {"id": "translator_agent", "name": "翻譯專家 Agent"},
        ]

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        # 判斷使用者目前選的是哪一個模型 ID
        model_id = body.get("model", "")
        user_message = body["messages"][-1]["content"]

        if model_id == "math_agent":
            return f"[數學模式] 正在計算：{user_message} ... 結果為 42"
        
        elif model_id == "translator_agent":
            return f"[翻譯模式] 翻譯結果：{user_message} (English version)"
        
        else:
            return "未知的模型 ID"
```
