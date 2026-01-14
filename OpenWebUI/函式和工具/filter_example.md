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

## 部署注意事項

### Raspberry Pi 環境
- 確保網路連線穩定
- 設定適當的 timeout 值（建議 20 秒）
- 監控系統資源使用狀況

### 錯誤處理
- API 連線失敗時的回退機制
- 翻譯服務不可用時的原始內容保留
- 詳細的錯誤日誌記錄

---

## 效能最佳化建議

1. **快取機制**: 對於重複內容可考慮加入快取
2. **批次處理**: 多句話同時翻譯可提升效率
3. **資源監控**: 定期檢查記憶體與 CPU 使用率
4. **網路最佳化**: 調整 timeout 與重試參數

這個工具能顯著改善中文使用者在 OpenWebUI 環境中的體驗，確保與 AI 模型的溝通更加順暢。
