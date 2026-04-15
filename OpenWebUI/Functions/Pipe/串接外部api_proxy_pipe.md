# 串接外部 Gemini API (API Proxy Pipe)

在實際應用中，我們通常會用 Pipe 來串接**自己的**模型或雲端 API。本範例改為使用 **Google Gemini API**（以 **Valves** 填寫 API Key，並將整段對話歷程轉成 Gemini 的 `Content` 後呼叫 `generate_content`）。

---

### 💡 為什麼要把 `body["messages"]` 轉成 `history`？
Open WebUI 傳進 Pipe 的 `messages`，格式是「介面與內部對話流程」約定好的**純資料**：常見為一連串字典，例如 `role` 可能是 `user`、`assistant`、`system` 等。與 Open WebUI 相對地，**Google Gemini 的 Python SDK** 要求你送出的內容是另一套型別與結構（例如 `types.Content`、`types.Part`），且對話角色在 Gemini 端主要區分為 **`user`** 與 **`model`**。
因此必須在 Pipe 裡做一次**轉換**：把「前端／Open WebUI 的訊息陣列」對應成「Gemini API 看得懂的物件序列」。

> [!IMPORTANT]
> **Container 部署須知**：
> Open WebUI 常以 **Docker／Docker Compose** 跑在容器裡。若你打算用 **環境變數** 提供金鑰：
> - 請在**建立或更新容器**時一併設定（如 `docker-compose.yml` 中加入 `GEMINI_API_KEY: <你的金鑰>`）。
> - 僅在主機的 shell 匯出變數，**不會**自動進到容器內；若未傳入，程式在容器裡會讀不到該變數。

---

### 🛠️ 前置需求

- **Function `requirements`**: `google-genai>=1.0.0`, `pydantic`（若使用 Valves）。
- **Valves 設定**: 於 Pipe 的 Valves 填入 `GEMINI_API_KEY` 與 `GEMINI_MODEL`，或設定環境變數 `GEMINI_API_KEY`。

> [!WARNING]
> **金鑰安全保護**
> 建議優先使用 Valves 或其他的秘密管理機制來填寫 API Key，以避免將金鑰直接寫死在程式碼中造成外洩風險。

---

### 📄 程式碼實作

```python
"""
title: Gemini API 代理 Pipe
author: YourName
version: 1.0
requirements: google-genai>=1.0.0, pydantic
"""

import os
from typing import Union, Generator, Iterator

from google import genai
from google.genai import types
from pydantic import BaseModel, Field


class Pipe:
    class Valves(BaseModel):
        GEMINI_API_KEY: str = Field(default="", description="Gemini API Key")
        GEMINI_MODEL: str = Field(default="gemini-2.5-flash", description="Gemini 模型名稱")

    def __init__(self):
        self.type = "pipe"
        self.id = "api_proxy_pipe"
        self.name = "Gemini API 代理模型"
        self.valves = self.Valves()

    def _api_key(self):
        return self.valves.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")

    def _model_name(self):
        return self.valves.GEMINI_MODEL or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        api_key = self._api_key()
        if not api_key:
            return "❌ 請在 Pipe 的 Valves 填寫 GEMINI_API_KEY，或設定環境變數 GEMINI_API_KEY"

        messages = body.get("messages", [])
        if not messages:
            return ""

        try:
            client = genai.Client(api_key=api_key)

            # 將 Open WebUI 訊息轉成 Gemini 的 Content 串
            history = []
            for msg in messages[:-1]:
                role = "user" if msg.get("role") == "user" else "model"
                history.append(
                    types.Content(role=role, parts=[types.Part(text=msg.get("content", ""))])
                )
            history.append(
                types.Content(
                    role="user",
                    parts=[types.Part(text=messages[-1].get("content", ""))],
                )
            )

            response = client.models.generate_content(
                model=self._model_name(),
                contents=history,
                config=types.GenerateContentConfig(
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    ),
                ),
            )

            return response.text or ""

        except Exception as e:
            return f"Gemini API 呼叫失敗: {str(e)}"
```

---

### 🔍 參數說明

| 欄位名 | 說明 | 預設值 |
| :--- | :--- | :--- |
| **GEMINI_API_KEY** | 你的 Gemini API 金鑰 | *(空字串)* |
| **GEMINI_MODEL** | 欲使用的 Gemini 模型名稱 | `gemini-2.5-flash` |

---

<details>
<summary>💡 程式碼詳細說明（給 Python 初學者）</summary>

### 1. 檔案開頭在做什麼？
- **三引號 `"""..."""`**：這是 Python 的「多行字串」，當作 docstring。Open WebUI 會讀取其中的 `title`、`requirements` 等欄位，決定顯示名稱及依賴套件。
- **`import`/`from ... import ...`**：引入第三方套件與標準備模組，例如 `genai.Client`。

### 2. `Valves` 的用途
- **`class Valves(BaseModel)`**：Pydantic 的寫法。這裡定義的變數（如 `GEMINI_API_KEY`）會自動變成 Open WebUI 前端的輸入框，讓使用者不需改 Code 就可以調整設定。

### 3. API Key 與環境變數層級
在 `_api_key()` 中使用 `self.valves.GEMINI_API_KEY or os.environ.get(...)`：
會先讀取 Valves 的設定，如果沒填才採用系統變數，提供最大的部署彈性。

### 4. `genai.Client` 與對話歷程轉換
- 我們將 `messages` 中所有的歷史訊息進行迭代。
- 若角色為 `user`，在 Gemini 的 `types.Content` 就設為 `user`，否則皆當作 **`model`** 角色。
- 最後使用 `generate_content` 生成回覆，並將 `response.text` 傳出。

</details>

---

> [!TIP]
> **延伸進階：非同步與狀態列提示版**
> 若你需要**狀態列提示**（顯示「正在呼叫 Gemini…」），可以使用包含 non-blocking 的 async 版本。以下為完整範例：
>
> ```python
> """
> title: Gemini API 代理 Pipe (含狀態提示版)
> author: YourName
> version: 1.0
> requirements: google-genai>=1.0.0, pydantic
> """
>
> import os
> from typing import Union, Generator, Iterator
>
> from google import genai
> from google.genai import types
> from pydantic import BaseModel, Field
>
> class Pipe:
>     class Valves(BaseModel):
>         GEMINI_API_KEY: str = Field(default="", description="Gemini API Key")
>         GEMINI_MODEL: str = Field(default="gemini-2.5-flash", description="Gemini 模型名稱")
>
>     def __init__(self):
>         self.type = "pipe"
>         self.id = "api_proxy_pipe_async"
>         self.name = "Gemini API 代理模型"
>         self.valves = self.Valves()
>
>     def _api_key(self):
>         return self.valves.GEMINI_API_KEY or os.environ.get("GEMINI_API_KEY", "")
>
>     def _model_name(self):
>         return self.valves.GEMINI_MODEL or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
>
>     async def pipe(self, body: dict, __user__: dict = None, __event_emitter__=None) -> Union[str, Generator, Iterator]:
>         # 1. 透過 __event_emitter__ 發送正在呼叫的狀態
>         if __event_emitter__:
>             await __event_emitter__({
>                 "type": "status",
>                 "data": {"description": "正在呼叫 Gemini 推論中...", "done": False}
>             })
>
>         api_key = self._api_key()
>         if not api_key:
>             if __event_emitter__:
>                 await __event_emitter__({"type": "status", "data": {"description": "❌ 缺少 API Key", "done": True}})
>             return "❌ 請在 Pipe 的 Valves 填寫 GEMINI_API_KEY，或設定環境變數 GEMINI_API_KEY"
>
>         messages = body.get("messages", [])
>         if not messages:
>             if __event_emitter__:
>                 await __event_emitter__({"type": "status", "data": {"description": "✅ 完成", "done": True}})
>             return ""
>
>         try:
>             client = genai.Client(api_key=api_key)
>             history = []
>             for msg in messages[:-1]:
>                 role = "user" if msg.get("role") == "user" else "model"
>                 history.append(types.Content(role=role, parts=[types.Part(text=msg.get("content", ""))]))
>             history.append(types.Content(role="user", parts=[types.Part(text=messages[-1].get("content", ""))]))
>
>             # 使用 async 對應方法，或在一般套件上可替換為 client.aio.models.generate_content(...) 等非同步 API
>             response = client.models.generate_content(
>                 model=self._model_name(),
>                 contents=history,
>                 config=types.GenerateContentConfig(
>                     automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
>                 ),
>             )
>
>             if __event_emitter__:
>                 await __event_emitter__({
>                     "type": "status",
>                     "data": {"description": "Gemini 處理完成", "done": True}
>                 })
>
>             return response.text or ""
>
>         except Exception as e:
>             if __event_emitter__:
>                 await __event_emitter__({
>                     "type": "status",
>                     "data": {"description": f"發生錯誤: {str(e)}", "done": True}
>                 })
>             return f"❌ Gemini API 呼叫失敗: {str(e)}"
> ```
