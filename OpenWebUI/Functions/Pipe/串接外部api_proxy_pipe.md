## 串接外部 Gemini API (API Proxy Pipe) 

在實際應用中，我們通常會用 Pipe 來串接**自己的**模型或雲端 API。本範例改為使用 **Google Gemini API**（以 **Valves** 填寫 API Key，並將整段對話歷程轉成 Gemini 的 `Content` 後呼叫 `generate_content`）。

**為什麼要把 `body["messages"]` 轉成 `history`？** Open WebUI 傳進 Pipe 的 `messages`，格式是「介面與內部對話流程」約定好的**純資料**：常見為一連串字典，例如 `role` 可能是 `user`、`assistant`、`system` 等，欄位名與語意都依 Open WebUI／OpenAI 相容慣例而定。相對地，**Google Gemini 的 Python SDK** 要求你送出的內容是另一套型別與結構（例如 `types.Content`、`types.Part`），且對話角色在 Gemini 端主要區分為 **`user`** 與 **`model`**，呼叫方式也是 `client.models.generate_content(...)` 這條路徑，**並不能**直接把 Open WebUI 的 `messages` 原封不動丟給 Gemini。因此必須在 Pipe 裡做一次**轉換**（範例裡用 `history` 這個串列承接轉好的內容）：把「前端／Open WebUI 的訊息陣列」對應成「Gemini API 看得懂的物件序列」。兩邊是**不同的 API／不同的操作介面**，資料形狀與角色命名都不相同，這正是要手動轉換的主要原因。

**核心概念**：在 Pipe 內建立 `genai.Client(api_key=...)`，將 `body["messages"]` **映射並組裝**成 Gemini 所需的 `history`（`user`／`model` 與 `Content`／`Part`），再回傳 `response.text` 作為 Open WebUI 畫面上的模型回覆。

> **Container 部署須知**：Open WebUI 常以 **Docker／Docker Compose** 跑在容器裡。若你打算用 **環境變數** 提供金鑰（讓 Pipe 裡的 `os.environ.get("GEMINI_API_KEY", "")` 讀得到），請在**建立或更新容器**時就一併設定，例如在 `docker-compose.yml` 的 `environment:` 區塊加入 `GEMINI_API_KEY: <你的金鑰>`，或使用 `docker run ... -e GEMINI_API_KEY=<你的金鑰> ...`。僅在主機的 shell 匯出變數，**不會**自動進到容器內；若未傳入，程式在容器裡會讀不到該變數。若改為只在 Open WebUI 介面的 Pipe **Valves** 填寫 API Key，則可不必依賴容器環境變數（仍建議以 Valves 或秘密管理機制擇一，避免金鑰外洩）。

**前置需求**：

- 在 Function 編輯器為此 Pipe 加上 **`requirements`**：`google-genai>=1.0.0`（若使用 Valves 亦需 `pydantic`，Open WebUI 多已內建）。
- 於 Pipe 的 **Valves** 填入 `GEMINI_API_KEY`，或於**容器／執行 Open WebUI 的環境**設定環境變數 `GEMINI_API_KEY`（見上方 Container 說明）。

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

**說明摘要**：

- **`genai.Client(api_key=...)`**：與履歷 Pipe 相同，金鑰來自 Valves 或 `GEMINI_API_KEY` 環境變數。
- **`types.Content` / `types.Part`**：使用者訊息用 `role="user"`，其餘（含 assistant）對 Gemini 一律用 `model`，與參考檔一致。
- **`GenerateContentConfig` + 關閉 automatic function calling**：避免非預期的工具呼叫；若你確定要讓 Gemini 使用工具，可再自行調整。

若需 **非同步** `async def pipe`（與部分 Open WebUI 版本一致），可將 `generate_content` 改為 SDK 提供的 async 對應方法（請依你安裝的 `google-genai` 版本文件為準），邏輯與上方相同。

<details>
<summary>程式碼詳細說明（給 Python 初學者）</summary>

### 檔案開頭在做什麼？

- **三引號 `"""..."""`**：這是 Python 的「多行字串」，放在檔案最上面時，常用來當作說明整支程式的註解（docstring）。Open WebUI 會讀取其中的 `title`、`version`、`requirements` 等欄位，決定在介面上顯示的名稱，以及要自動安裝哪些套件。
- **`import`**：告訴 Python「我要使用別人寫好的工具」。例如 `import os` 之後，才能用 `os.environ` 讀取環境變數。
- **`from ... import ...`**：只從某個模組裡「挑出」需要的名稱，例如 `from google import genai`，之後就可以寫 `genai.Client(...)`。

### `class Pipe` 與巢狀的 `Valves`

- **`class`**：用來定義一種「自訂的型別」，把資料與函式包在一起。這裡的 `Pipe` 就是 Open WebUI 規定要實作的一個類別名稱。
- **內層的 `class Valves(BaseModel)`**：這是 **Pydantic** 的寫法。`Valves` 裡的每一個欄位（例如 `GEMINI_API_KEY`）會變成 Open WebUI 介面上的輸入框或說明文字，讓使用者**不用改程式碼**就能填入 API Key 與模型名稱。
- **`Field(default="", description="...")`**：`default=""` 表示預設是空字串；`description` 會顯示在設定畫面上，提醒這個欄位要做什麼。

### `__init__`：建立 Pipe 時會跑一次

- **`def __init__(self):`**：當系統載入這個 Pipe 時，會先執行這個方法。
- **`self.type`、`self.id`、`self.name`**：告訴 Open WebUI 這是一支 **pipe**，以及在清單裡要顯示什麼名稱。
- **`self.valves = self.Valves()`**：建立一組預設的 Valves 設定物件，之後 `_api_key()` 會從 `self.valves` 讀使用者填的值。

### `_api_key` 與 `_model_name`：前面加底線的函式

- **底線 `_`**：在 Python 慣例裡，表示「主要在這個類別內部使用」，給人讀程式時的提示，不是給 Open WebUI 的特殊語法。
- **`return A or B`**：若 `A` 是空字串，就會改用 `B`。這裡的意思是：**優先使用 Valves 裡填的 Key**；若沒填，再試試環境變數 `GEMINI_API_KEY`。

### `pipe(self, body)`：每一則對話請求都會呼叫它

- **`body` 是什麼？** Open WebUI 傳進來的一個 **字典（dict）**，裡面至少會有 `messages`（對話列表）。
- **`body.get("messages", [])`**：安全地取出 `messages`；若沒有這個鍵，就用空列表 `[]`，避免程式直接報錯。
- **提早 `return`**：若沒有 API Key、或沒有任何訊息，就**立刻結束**並回傳字串。這樣後面就不會對空的資料去呼叫 API。

### `try` / `except`：處理「可能失敗」的步驟

- 網路請求、API 金鑰錯誤、回應格式不符等，都可能拋出例外。**`try`** 裡放主要邏輯；若發生錯誤，會跳到 **`except`**，這裡我們把錯誤訊息包成字串回傳，讓使用者在聊天視窗裡看得到發生什麼事，而不是整支程式無聲崩潰。

### `genai.Client` 與對話歷程 `history`

- **`client = genai.Client(api_key=api_key)`**：建立一個「已登入」的 Gemini 用戶端，後面的 `generate_content` 都透過它送出。
- **`messages[:-1]`**：Python 的切片語法，代表「除了最後一則以外的所有訊息」。我們先把較早的訊息逐則加入 `history`，最後再**單獨**把最後一則也加進去（這樣寫與參考的履歷 Pipe 相同，結構清楚）。
- **`role == "user"` 與否**：Open WebUI 裡除了使用者，還可能有助手、系統等角色。Gemini 這邊主要分 **`user`** 與 **`model`**（模型），所以不是 `user` 的就當成 **`model`**。
- **`types.Content` 與 `types.Part`**：這是 Google SDK 要求的「訊息格式」：一則內容（Content）裡可以有多個片段（Part），這裡我們只有一段純文字，所以用 `types.Part(text=...)`。

### `generate_content` 與 `response.text`

- **`model=self._model_name()`**：要呼叫哪一個 Gemini 模型（例如 `gemini-2.5-flash`），名稱可從 Valves 改。
- **`contents=history`**：把剛才組好的整段對話丟給模型。
- **`GenerateContentConfig`**：額外設定；這裡關閉 **automatic function calling**，避免模型在未預期的情況下去呼叫「工具」，對初學者範例較單純。
- **`return response.text or ""`**：模型回覆的文字在 `response.text`；若偶爾為空，就回傳空字串，減少前端顯示錯誤。

</details>
