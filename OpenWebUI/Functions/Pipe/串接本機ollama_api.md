# 串接本機 Ollama 模型 (API Proxy Pipe)

在實際應用中，我們可以用 Pipe 把 Open WebUI 的對話**轉發**到同一台機器（或區網內）執行的 **Ollama**。Ollama 提供與 **OpenAI Chat Completions 相容**的 HTTP API（`/v1/chat/completions`），只要把 `body["messages"]` 組進 JSON 再 `POST` 即可。

---

### 💡 為什麼轉發時多半可以直接用 `messages`？
Open WebUI 傳入的每一則訊息通常是 `{"role": "...", "content": "..."}`，與 Ollama 這條相容 API 所期待的欄位一致（例如 `user`、`assistant`、`system`）。與 **Gemini** 那類必須轉成 `Content`／`Part` 的 API 不同，這裡**兩邊的操作介面相近**，Pipe 裡主要是**指定模型名稱、端點 URL、溫度**等參數，再把回應裡的 `choices[0].message.content` 回傳給畫面。

> [!IMPORTANT]
> **Container 部署須知**：
> 若 Open WebUI 跑在 **Docker 容器**內，而 Ollama 裝在**宿主機**上，容器裡的 `http://127.0.0.1:11434` 指向的是**容器自己**，主要建置容器時使用 `--network=host`
> - **Linux/Windows/Mac**: 建議使用 `http://127.0.0.1:11434/v1/chat/completions`。
> - **Ollama 設定**: 務必確認 Ollama 有監聽對應介面（例如設定環境變數 `OLLAMA_HOST=0.0.0.0`）。

---

### 🛠️ 前置需求

- **Function `requirements`**: `requests`, `pydantic`（建議明確列出）。
- **Ollama 運行狀態**: 確保本機已安裝並啟動 Ollama。
- **Valves 設定**: 在 Pipe 設定畫面的 Valves 填入 `OLLAMA_API_URL` 與 `OLLAMA_MODEL`。

> [!WARNING]
> **務必先在本機下載（取得）模型**
> Pipe 裡填的 `OLLAMA_MODEL` 必須是 **Ollama 已經下載好** 的模型名稱（與 `ollama list` 顯示的一致）。若尚未下載就呼叫 API，會回傳錯誤或找不到模型。
> - **建議方式**：在終端機執行 `ollama pull <模型名>`（例如：`ollama pull gemma2:2b`）。

---

### 📄 程式碼實作

```python
"""
title: 本機 Ollama 代理 Pipe
author: YourName
version: 1.0
requirements: requests, pydantic
"""

import os
from typing import Union, Generator, Iterator

import requests
from pydantic import BaseModel, Field


class Pipe:
    class Valves(BaseModel):
        OLLAMA_API_URL: str = Field(
            default="http://127.0.0.1:11434/v1/chat/completions",
            description="Ollama OpenAI 相容 API（chat completions）",
        )
        OLLAMA_MODEL: str = Field(
            default="gemma4:31b-cloud",
            description="本機 ollama 已下載的模型名稱（與 ollama list 一致）",
        )

    def __init__(self):
        self.type = "pipe"
        self.id = "ollama_proxy_pipe"
        self.name = "本機 Ollama 代理模型"
        self.valves = self.Valves()

    def _api_url(self):
        return self.valves.OLLAMA_API_URL or os.environ.get(
            "OLLAMA_API_URL", "http://127.0.0.1:11434/v1/chat/completions"
        )

    def _model_name(self):
        return self.valves.OLLAMA_MODEL or os.environ.get("OLLAMA_MODEL", "llama3.2")

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        api_url = self._api_url()
        if not api_url:
            return "❌ 請設定 OLLAMA_API_URL"

        messages = body.get("messages", [])
        if not messages:
            return ""

        # 與 OpenAI 相容的 JSON 格式
        payload = {
            "model": self._model_name(),
            "messages": messages,
            "stream": False,
            "temperature": 0.7,
        }
        headers = {"Content-Type": "application/json"}

        try:
            # 呼叫本機 API，設定較長的 timeout 以應對地端推論延遲
            response = requests.post(
                api_url, json=payload, headers=headers, timeout=300
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

        except requests.exceptions.ConnectionError:
            return (
                f"❌ 無法連線至 Ollama：{api_url}。"
                "請確認 Ollama 正在執行；若在 Docker 內連宿主機，請勿使用 127.0.0.1。"
            )
        except Exception as e:
            return f"❌ Ollama 呼叫失敗: {str(e)}"
```

---

### 🔍 參數說明

| 欄位名 | 說明 | 預設值 |
| :--- | :--- | :--- |
| **OLLAMA_API_URL** | 完整路徑需含 `/v1/chat/completions` | `http://127.0.0.1:11434/v1/chat/completions` |
| **OLLAMA_MODEL** | 必須與 `ollama list` 顯示的標籤完全一致 | `gemma4:31b-cloud` |
| **timeout** | 因地端模型推論較慢，預設設為 300 秒 | `300` |

---

<details>
<summary>💡 程式碼詳細說明（給 Python 初學者）</summary>

### 1. 為什麼要用 `requests`？
`requests` 是 Python 最受歡迎的 HTTP 函式庫。因為我們是要「呼叫別人的 API（Ollama）」，本質上就是發出一個網路請求。
- **`requests.post`**：發送資料（payload）給伺服器。
- **`response.json()`**：把伺服器回傳的 JSON 格式純文字轉成 Python 字典，方便我們取出對話內容。

### 2. `Valves` 與 `os.environ` 的優先順序
在 `_api_url()` 函式中，我們寫了 `self.valves.OLLAMA_API_URL or os.environ.get(...)`。
這代表程式會**優先使用**你在 Open WebUI 網頁介面上填寫的數值；如果你沒填，它才會去嘗試讀取系統的環境變數。這能提供最大的彈性。

### 3. Payload 結構
Ollama 的 `/v1` 相容 API 格式與 OpenAI 完全一致：
- **`model`**：指定要用哪一個模型。
- **`messages`**：包含整段對話歷程的清單。
- **`stream: False`**：在這個簡單範例中，我們選擇等模型全部講完再一次回傳，這樣程式碼最精簡。

### 4. 錯誤處理 (Try/Except)
網路連線很容易出問題（例如忘記開 Ollama）。使用 `try...except` 區塊可以攔截這些錯誤，並把「人看得懂」的錯誤訊息（例如 ❌ 無法連線）回傳到對話視窗，而不是讓整個 Pipe 直接崩潰消失。

</details>

---

> [!TIP]
> **延伸進階**：
> 若你需要**狀態列提示**（顯示「正在呼叫 Ollama…」），可以直接複製以下完整程式碼。此版本將 `pipe` 改為了 `async def pipe`，並在 `requests.post` 前後呼叫 `__event_emitter__` 來發送狀態事件。
>
> ```python
> """
> title: 本機 Ollama 代理 Pipe (含狀態提示版)
> author: YourName
> version: 1.0
> requirements: requests, pydantic
> """
> 
> import os
> from typing import Union, Generator, Iterator
> 
> import requests
> from pydantic import BaseModel, Field
> 
> 
> class Pipe:
>     class Valves(BaseModel):
>         OLLAMA_API_URL: str = Field(
>             default="http://127.0.0.1:11434/v1/chat/completions",
>             description="Ollama OpenAI 相容 API（chat completions）",
>         )
>         OLLAMA_MODEL: str = Field(
>             default="gemma4:31b-cloud",
>             description="本機 ollama 已下載的模型名稱（與 ollama list 一致）",
>         )
> 
>     def __init__(self):
>         self.type = "pipe"
>         self.id = "ollama_proxy_pipe_async"
>         self.name = "本機 Ollama 代理模型"
>         self.valves = self.Valves()
> 
>     def _api_url(self):
>         return self.valves.OLLAMA_API_URL or os.environ.get(
>             "OLLAMA_API_URL", "http://127.0.0.1:11434/v1/chat/completions"
>         )
> 
>     def _model_name(self):
>         return self.valves.OLLAMA_MODEL or os.environ.get("OLLAMA_MODEL", "llama3.2")
> 
>     async def pipe(self, body: dict, __user__: dict = None, __event_emitter__=None) -> Union[str, Generator, Iterator]:
>         # 1. 透過 __event_emitter__ 發送正在呼叫的狀態
>         if __event_emitter__:
>             await __event_emitter__({
>                 "type": "status",
>                 "data": {"description": "正在呼叫本機 Ollama 推論中...", "done": False}
>             })
> 
>         api_url = self._api_url()
>         if not api_url:
>             if __event_emitter__:
>                 await __event_emitter__({"type": "status", "data": {"description": "❌ 缺少 API URL", "done": True}})
>             return "❌ 請設定 OLLAMA_API_URL"
> 
>         messages = body.get("messages", [])
>         if not messages:
>             if __event_emitter__:
>                 await __event_emitter__({"type": "status", "data": {"description": "✅ 完成", "done": True}})
>             return ""
> 
>         # 與 OpenAI 相容的 JSON 格式
>         payload = {
>             "model": self._model_name(),
>             "messages": messages,
>             "stream": False,
>             "temperature": 0.7,
>         }
>         headers = {"Content-Type": "application/json"}
> 
>         try:
>             # 呼叫本機 API，設定較長的 timeout 以應對地端推論延遲
>             response = requests.post(
>                 api_url, json=payload, headers=headers, timeout=300
>             )
>             response.raise_for_status()
>             result = response.json()
> 
>             # 2. 結束前發送完成狀態（done: True）
>             if __event_emitter__:
>                 await __event_emitter__({
>                     "type": "status",
>                     "data": {"description": "Ollama 處理完成", "done": True}
>                 })
> 
>             return result["choices"][0]["message"]["content"]
> 
>         except requests.exceptions.ConnectionError:
>             error_msg = (
>                 f"❌ 無法連線至 Ollama：{api_url}。"
>                 "請確認 Ollama 正在執行；若在 Docker 內連宿主機，請勿使用 127.0.0.1。"
>             )
>             if __event_emitter__:
>                 await __event_emitter__({
>                     "type": "status",
>                     "data": {"description": "連線失敗", "done": True}
>                 })
>             return error_msg
>         except Exception as e:
>             # 發生錯誤也記得把狀態關閉
>             if __event_emitter__:
>                 await __event_emitter__({
>                     "type": "status",
>                     "data": {"description": f"發生錯誤: {e}", "done": True}
>                 })
>             return f"❌ 呼叫失敗: {e}"
> ```


