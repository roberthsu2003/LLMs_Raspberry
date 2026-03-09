# 最簡單的Filter範例

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