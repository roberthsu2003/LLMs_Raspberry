# 最簡單的Filter範例

**目標**：讓所有 AI 回答的結尾都自動加上一句固定文字。

## class Filter 是固定名稱（不能改）

這是 **Open WebUI 的規定**，不是 Python 的語法規則。  
類別名稱必須是 `Filter`，Open WebUI 才會辨識。


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

