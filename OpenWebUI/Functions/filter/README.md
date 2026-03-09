# Open WebUI 過濾器（Filter）教學講義

**設定位置**：Open WebUI → 管理員控制台 → 函式 → 新增函式

在 Open WebUI 裡，**管理員控制台 → 函式 → class Filter** 實際在做什麼?

---

## 重要觀念

**過濾器（Filter）不是工具（Tool），而是「在 AI 回答前或後，先對內容加工一次」的機制。**

- 它**不負責**查資料或計算  
- 它**只負責**修改對話內容本身

---

## 一、Filter 在 Open WebUI 裡扮演的角色

可以用下面這個流程圖幫學生建立概念：

```
使用者輸入
    ↓
（Filter：前處理）
    ↓
LLM（模型回答）
    ↓
（Filter：後處理）
    ↓
顯示給使用者
```

> 👉 Filter 就像「攔截器」  
> 👉 不是由 AI 主動呼叫，而是**每一則對話都會經過這裡**

---

## 二、掌握的 3 個重點

### ✅ 1. Filter ≠ 工具（Tool）

| 比較 | 工具（Tool） | 過濾器（Filter） |
|------|--------------|------------------|
| 由誰決定？ | AI 決定要不要用 | **一定會執行** |
| 比喻 | 像「技能」 | 像「安檢門」 |
| 作用範圍 | 有參數、可選擇 | 對所有訊息生效 |

---

### ✅ 2. Filter 只做一件事：改訊息

說明：

> **Filter 不適合做太複雜的事。**  
> 它的工作就是：**拿到文字 → 改一改 → 再傳回去**。

---

### ✅ 3. class Filter 是固定名稱（不能改）

這是 **Open WebUI 的規定**，不是 Python 的語法規則。  
類別名稱必須是 `Filter`，Open WebUI 才會辨識。

---

## 三、最小可用 Filter 架構

⭐ **最簡單的Filter範例**

```python
"""
title: 最簡單的 Filter 範例
author: 教學用
version: 1.0
description: 示範 Filter 的基本結構
"""

from typing import List, Dict, Any

class Filter:

    def inlet(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        在送進模型「之前」處理訊息
        """
        return messages

    def outlet(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        在模型回答「之後」處理訊息
        """
        return messages
```

> 👉 這份程式碼雖然「什麼都沒做」  
> 👉 但它是 **正確、可執行的標準骨架**

---

## 四、逐行說明

### 1️⃣ 為什麼類別一定要叫 Filter？

Open WebUI 在啟動時，**只會尋找名為 `Filter` 的類別**。  
若找不到，就視為這個函式不存在，因此類別名稱不能更改。

---

### 2️⃣ messages 是什麼？

```python
messages: List[Dict[str, Any]]
```

**白話**：`messages` 就是「**整段對話紀錄**」。

實際結構類似下面這樣：

```python
[
  {"role": "user", "content": "你好"},
  {"role": "assistant", "content": "你好，有什麼我可以幫你？"}
]
```

---

### 3️⃣ inlet()：送進模型之前

- **inlet** = 入口  
- 在 AI 開始思考**之前**，可以先檢視或修改使用者輸入的內容。

---

### 4️⃣ outlet()：離開模型之後

- **outlet** = 出口  
- AI 已經回答完畢，但我們可以**再修改一次**，再顯示給使用者。

---

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

