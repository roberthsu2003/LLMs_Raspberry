# OpenWebUI 過濾器範例：

## 中文轉英文翻譯工具

## 功能概述

建立一個 OpenWebUI Filter 擴充程式，自動將使用者輸入的中文內容翻譯成英文，提升與 AI 模型的互動品質。

### 核心功能
- **函式名稱**: 繁中轉換為英文
- **函式描述**: 將輸入的中文 prompt 自動轉換為英文

---

## 實作要求

### 1. 基本設定
- 建立 `Filter` 類別
- 在 `Valves` 中設定 `enable_translation` 開關（預設值：True）

### 2. 核心邏輯 (inlet 函式)
- 讀取使用者輸入的最後一句話
- 當開關啟用時，呼叫翻譯函式將中文翻譯成英文
- 取代原始內容

### 3. 翻譯函式 (_translate_to_english)
- 使用 `requests` 套件呼叫本地 Ollama API
- **API 端點**: `http://127.0.0.1:11434/api/generate`（Host 網路模式）
- **模型指定**: 強制使用 `"gpt-oss:20b-cloud"` 模型
- **翻譯指令**: 純翻譯結果，不包含任何解釋

---

## 程式碼規範

### Python 語法要求
- 使用 Python 3.10+ 新語法
- 型別檢查採用 `str | None` 或 `dict | None` 格式
- 避免使用 `Optional` 語法

### 程式碼結構
- 結構簡潔明瞭（角色 + 任務 + 條件）
- 加上詳細中文註解
- 遵循 OpenWebUI Filter 標準架構

---

## Prompt 範本（給 AI 使用）

```markdown
# 角色
你是一位 Python 程式設計教學專家，專精於 OpenWebUI 擴充程式開發。

# 任務
請建立一個 OpenWebUI Filter 擴充程式，實現中文到英文的自動翻譯功能。

# 技術規格
1. **基本架構**：
   - 建立 Filter 類別與 Valves 設定
   - enable_translation 開關（預設 True）

2. **核心功能**：
   - inlet 函式處理使用者輸入
   - 自動偵測中文並翻譯為英文
   - 取代原始訊息內容

3. **翻譯服務**：
   - 連接本地 Ollama API (127.0.0.1:11434)
   - 強制使用 gpt-oss:20b-cloud 模型
   - 純翻譯輸出，無額外解釋

4. **程式碼品質**：
   - Python 3.10+ 語法（str | None 型別）
   - 完整中文註解
   - 例外處理機制
```

---

## 設計重點

### 簡化複雜度
- **移除技術雜訊**: 不要求 pydantic 欄位定義或詳細 function 簽章
- **口語化指令**: 使用更自然的語言描述
- **保留關鍵限制**: 維持重要技術要求

### 關鍵技術限制
- **模型固定**: 必須使用 `"gpt-oss:20b-cloud"`，不可使用動態 model_id
- **新語法支援**: 採用 Python 3.10+ 的聯合型別語法
- **網路設定**: 確保連接到正確的本地 API 端點

---

## 預期程式碼結構

```python
import requests
import json
from pydantic import BaseModel, Field
from typing import Optional

class Filter:
    class Valves(BaseModel):
        enable_translation: bool = Field(
            default=True, 
            description="是否啟用自動翻譯為英文"
        )

    def __init__(self):
        self.valves = self.Valves()

    def inlet(self, body: dict, __user__: dict | None = None) -> dict:
        # 實作核心邏輯
        pass

    def _translate_to_english(self, text: str, model_id: str | None):
        # 實作翻譯功能
        pass

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
```

---

### 【個資守門員】(Privacy Guard)

* **情境 (Pain Point)**：
學生在使用 AI 時，常會不小心把電話、身分證或 API Key 貼進去。
* **功能描述 (Inlet 處理)**：
* 在訊息傳給 LLM **之前**，自動偵測手機號碼或是 Email。
* 將其替換成 `[已隱藏個資]`。


* **程式邏輯**：
* 使用簡單的 Regular Expression (正規表達式) 掃描文字。
* Python 的 `re.sub()` 功能。


* **學生會有感覺的點**：
* 輸入：「我的電話是 0912-345-678」，結果 AI 回答：「我看到了，您的電話是 [已隱藏個資]」。
* **亮點**：體會到 Filter 是如何保護安全的。


---

### 【AI 時空旅人】(Time Injector)

* **情境 (Pain Point)**：
學生問 AI：「今天是星期幾？」或「現在幾點？」，AI 通常會亂回答（因為它訓練時不知道當下時間）。
* **功能描述 (Inlet 處理)**：
* 在訊息傳給 LLM **之前**，偷偷在最後面補上一句系統提示：`"（系統資訊：現在時間是 2025-01-14 星期三 14:30）"`。


* **程式邏輯**：
* 使用 Python 的 `datetime` 套件取得系統時間。
* 字串串接。


* **學生會有感覺的點**：
* 原本問 AI 時間，它說「我只是一個模型...」；加了 Filter 後，它精準回答「現在是下午兩點半！」。
* **亮點**：讓 AI 瞬間擁有「時間觀念」。


---

### 【懶人重點摘要師】(TL;DR Generator)

* **情境 (Pain Point)**：
AI 有時候廢話太多，學生只想看結論。
* **功能描述 (Outlet 處理)**：
* 在 AI 回答完 **之後**，Filter 抓取那個回答。
* 偷偷再呼叫一次小模型 (如 Gemma:2b)，要求：「用 3 個 bullet points 總結上面這段話」。
* 把總結附加在原本回答的最後面。


* **程式邏輯**：
* 類似我們剛做的翻譯功能，只是這次是在 `outlet` 做。
* 使用 `Valves` 做一個開關，想看摘要時才開。


* **學生會有感覺的點**：
* AI 寫了一篇長作文，但最後面自動多出一個「📌 **重點整理**」區塊。
* **亮點**：大幅提升閱讀效率，覺得 Filter 很貼心。


---

### 【心情調色盤】(Emoji Enhancer)

* **情境 (Pain Point)**：
AI 的回答有時候冷冰冰的，全是文字，閱讀起來很無聊。
* **功能描述 (Outlet 處理)**：
* 不改變 AI 的文字內容，但要求 AI 分析這段話的情緒。
* 在每一段落的結尾，自動加上適合的 Emoji (😀, 🚀, 💡)。


* **程式邏輯**：
* 修改 System Prompt 或是透過 Outlet 二次處理。
* 這可以練習 Prompt Engineering 的技巧。


* **學生會有感覺的點**：
* 原本嚴肅的程式教學，瞬間變得很活潑。
* **亮點**：視覺上的直接回饋，很有趣。
