## 串接本機 Ollama 模型 (API Proxy Pipe)

在實際應用中，我們可以用 Pipe 把 Open WebUI 的對話**轉發**到同一台機器（或區網內）執行的 **Ollama**。Ollama 提供與 **OpenAI Chat Completions 相容**的 HTTP API（`/v1/chat/completions`），因此不必像 Gemini 那樣改成另一套 SDK 物件；只要把 `body["messages"]` 組進 JSON 再 `POST` 即可。寫法可對照 [`resume_assistant_ollama_pipe.py`](./docx檔含佔位符_template/resume_assistant_ollama_pipe.py) 中的 `requests.post`、`payload` 與回應解析。

**為什麼轉發時多半可以直接用 `messages`？** Open WebUI 傳入的每一則訊息通常是 `{"role": "...", "content": "..."}`，與 Ollama 這條相容 API 所期待的欄位一致（例如 `user`、`assistant`、`system`）。與 **Gemini** 那類必須轉成 `Content`／`Part` 的 API 不同，這裡**兩邊的操作介面相近**，Pipe 裡主要是**指定模型名稱、端點 URL、溫度**等參數，再把回應裡的 `choices[0].message.content` 回傳給畫面。

> **Container 須知**：若 Open WebUI 跑在 **Docker 容器**內，而 Ollama 裝在**宿主機**上，容器裡的 `http://127.0.0.1:11434` 指向的是**容器自己**，通常**連不到**宿主機的 Ollama。請把 Valves 的 `OLLAMA_API_URL` 改成可從容器連到宿主機的位址（例如 Linux 上常用宿主機在橋接網段的 IP，或 Docker Desktop 的 `http://host.docker.internal:11434/v1/chat/completions`，實際依你的環境為準），並確認 Ollama 有監聽對應介面（例如設定 `OLLAMA_HOST=0.0.0.0` 以利區網／容器存取）。

**前置需求**：

- Function 的 **`requirements`**：`requests, pydantic`（Open WebUI 可能已內建其一，仍建議寫明）。
- 本機已安裝並啟動 Ollama，且已 `ollama pull` 目標模型。
- 在 Pipe 的 **Valves** 設定 `OLLAMA_API_URL`、`OLLAMA_MODEL`，必要時搭配環境變數 `OLLAMA_API_URL`／`OLLAMA_MODEL`。

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
            default="llama3.2",
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

        # 與 resume_assistant_ollama_pipe 相同：OpenAI 相容 JSON，stream 關閉方便一次取完整回覆
        payload = {
            "model": self._model_name(),
            "messages": messages,
            "stream": False,
            "temperature": 0.7,
        }
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                api_url, json=payload, headers=headers, timeout=300
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]

        except requests.exceptions.ConnectionError:
            return (
                f"❌ 無法連線至 Ollama：{api_url}。"
                "請確認 Ollama 正在執行；若在 Docker 內連宿主機，請勿使用 127.0.0.1，並確認 OLLAMA_HOST。"
            )
        except Exception as e:
            return f"❌ Ollama 呼叫失敗: {str(e)}"
```

**說明摘要**（與 `resume_assistant_ollama_pipe.py` 對照）：

- **`OLLAMA_API_URL`**：完整路徑需含 **`/v1/chat/completions`**（與參考檔預設相同）。
- **`payload`**：`messages` 直接沿用 Open WebUI，必要時你也可像履歷 Pipe 一樣在串列**開頭**插入一則 `system` 訊息做行為約束。
- **`timeout=300`**：大模型在地端推論可能很慢，與參考檔一致拉長逾時；可依硬體調整。
- **回應**：由 `result["choices"][0]["message"]["content"]` 取出文字（OpenAI 相容格式）。

若你需要**狀態列提示**（「正在呼叫 Ollama…」），可將 `pipe` 改為 `async def pipe(self, body, __user__=None, __event_emitter__=None)`，並仿照 `resume_assistant_ollama_pipe.py` 在 `requests.post` 前後呼叫 `__event_emitter__`；單純轉發時維持同步 `def pipe` 即可。
