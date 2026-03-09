# 輸入時-將中文轉變為英文

### ✅ 3. class Filter 是固定名稱（不能改）

這是 **Open WebUI 的規定**，不是 Python 的語法規則。  
類別名稱必須是 `Filter`，Open WebUI 才會辨識。

---

## 三、最小可用 Filter 架構

⭐ **最簡單的Filter範例**



## 五、第一個「有感」的 Filter 範例

**目標**：讓所有 AI 回答的結尾都自動加上一句固定文字。

```python
class Filter:

    def outlet(self, messages):
        if messages and messages[-1]["role"] == "assistant":
            messages[-1]["content"] += "\n\n（以上回答由 AI 產生）"
        return messages
```

### 重點

- ❗ **AI 不會知道**這句話是 Filter 加上的  
- ❗ 模型會「以為」自己本來就是這樣回答  
- ❗ 這是**系統層級的控制**，不是透過 prompt 告訴 AI 的  

---

## 六、心智模型（比喻）

| 名詞 | 比喻 |
|------|------|
| **Prompt** | 跟 AI 說話 |
| **工具（Tool）** | 給 AI 新技能 |
| **Filter** | 在旁邊**偷偷改對話** |

---


## 語言過濾器程式碼（實例）

- **函式名稱**：繁中轉換為英文

### 目標

1. 將使用者輸入（prompt）的中文轉換為英文  
2. 在模型輸出的內容後面加上公司資料  

### 程式碼

```python
from typing import Optional

import requests
from pydantic import BaseModel, Field


class Filter:
    class Valves(BaseModel):
        enable_translation: bool = Field(
            default=True, description="是否啟用自動翻譯為英文"
        )
        pass

    def __init__(self):
        self.valves = self.Valves()

    def inlet(self, body: dict, __user__: dict | None = None) -> dict:
        user_message = body["messages"][-1]["content"]

        if self.valves.enable_translation and user_message:
            try:
                model_id = body.get("model")
                translated_text = self._translate_to_english(user_message, model_id)

                print(f"[Company A] 原始內容: {user_message}")
                print(f"[Company A] 翻譯後內容: {translated_text}")

                body["messages"][-1]["content"] = translated_text

            except Exception as e:
                print(f"翻譯出錯: {e}")

        return body

    def _translate_to_english(self, text: str, model_id: str | None):
        host_ip = "127.0.0.1"
        url = f"http://{host_ip}:11434/api/generate"

        prompt = f"Translate the following Chinese text to English. Output ONLY the English translation, no explanation.\nText: {text}\nEnglish:"

        payload = {
            "model": "gpt-oss:20b-cloud",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.0},
        }

        try:
            response = requests.post(url, json=payload, timeout=20)

            if response.status_code == 404:
                print("錯誤：找不到 API 路徑，請檢查 Ollama 版本")
                return text

            response.raise_for_status()
            result = response.json()
            translated = result.get("response", "").strip()

            return translated.replace('"', "") if translated else text

        except Exception as e:
            print(f"翻譯請求失敗: {e}")
            return text

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if body.get("messages"):
            last_msg = body["messages"][-1]
            if last_msg.get("role") == "assistant":
                text = last_msg.get("content", "")
                last_msg["content"] = (
                    text
                    + """\n
                    公司:飛肯股份有限公司
                    地址:台北市信義區信義路五段1號
                    電話:02-2345-6789
                    網址:https://www.flyken.com
                    """
                )
        return body
```

