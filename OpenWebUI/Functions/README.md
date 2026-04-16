# Open WebUI Functions 講義

> **官方參考**：[Open WebUI Functions 文件](https://docs.openwebui.com/features/extensibility/plugin/functions/)  
> **說明**：本文件以「課堂講義」形式撰寫，建議搭配實機操作 Open WebUI 一併練習。

---

## 課前導讀

### 如何使用本講義
| 項目 | 說明 |
|------|------|
| **建議順序** | 依首章至終章循序閱讀；各類型 Function 可搭配「安裝與啟用」章節邊做邊學。 |
| **先備知識** | 具備基本瀏覽器操作與文字編輯能力；若具備 Python 基礎知識（如：變數、函式、`class`）將有助於理解程式碼範例。 |
| **實作環境** | 須有可登入的 Open WebUI（本機或課堂伺服器），並具備**管理員 / 函式管理**權限。 |

### 學習目標
完成本講義與實作練習後，您應能夠：
1. **區辨** Functions 與 Tools（工具）的差異，並說明 Pipe、Filter、Action 三種類型的應用場景。  
2. **操作** 介面完成 Function 的安裝與啟用，並正確指派 Filter、Action 或選用 Pipe 等自訂模型。  
3. **理解** 基礎範例程式碼，辨識 `inlet`、`outlet`、`pipe` 與 Valves（參數閥門）的功能。  
4. **落實** 安全實務規範，確保不在正式環境隨意安裝來源不明之程式碼。

---

## 目錄

1. [第一章：認識 Functions](#第一章認識-functions)
2. [第二章：Filter Function (過濾器)](#第二章filter-function-過濾器)
3. [第三章：Action Function (動作按鈕)](#第三章action-function-動作按鈕)
4. [第四章：Pipe Function (管道與自訂模型)](#第四章pipe-function-管道與自訂模型)
5. [第五章：Valves (參數閥門)](#第五章valves-參數閥門)
6. [第六章：安裝、啟用與指派](#第六章安裝啟用與指派)

*（於編輯器或 GitHub 平台中，可利用「大綱 / Outline」功能快速導覽各節）*

---

## 第一章：認識 Functions

### 1.1 什麼是 Functions？
- **定義**：Functions 為 Open WebUI 內建的「插件」機制，用以**擴充**系統介面與行為邏輯。  
- **特點**：
  - 高度整合於 Open WebUI，無須複雜的外部設定。  
  - 具備模組化特性與優異的執行效能。  
  - 統一使用 **Python** 語言撰寫，提供極大的客製化彈性。

### 1.2 Functions 與 Tools (工具) 的差異
初學者常混淆 Functions 與 Tools，請參考下表進行區分：

| 比較項目 | **Tools (工具)** | **Functions (本講義主題)** |
|----------|-------------------|-----------------------------|
| **決策者** | 由 **AI 模型**根據對話上下文「自主決定」是否呼叫 | 由 **系統層**依類型在固定流程中強制執行 |
| **常見範例** | 查詢天氣、網頁搜尋、數學計算 | Pipe、Filter、Action 三大類型 |

> **重點提醒**：**Tool 並不屬於 Functions** 範疇，兩者為各自獨立的擴充機制。本講義專注探討 Functions。

### 1.3 三種 Functions 類型總覽
| 類型 | 功能說明 | 介面呈現方式 |
|------|--------------|----------------|
| **Filter** | 在傳送至模型**前**或模型輸出**後**對文字內容進行加工 | 對指定模型或全域生效，一般使用者「無感」 |
| **Action** | 於對話訊息旁新增特定操作**按鈕** | 顯示於每則對話（使用者/AI）下方，點擊後觸發 |
| **Pipe** | 註冊成為一個**自訂模型**供使用者選擇 | 直接出現於首頁的**模型選擇下拉清單**中 |

### 1.4 管理介面路徑
如需管理 Functions，請前往：**點擊使用者大頭貼 → 管理員控制台 (Admin Panel) → 函式 (Functions)**。

---

## 第二章：Filter Function (過濾器)

> **官方說明**：[Filter Function](https://docs.openwebui.com/features/extensibility/plugin/functions/filter)

### 2.1 核心概念
Filter 扮演「資料攔截器」的角色，可在 AI 模型接收與回覆的過程中對內容進行後加工。
- **Inlet (入口)**：於送進模型**之前**處理（如：修改使用者輸入、附加系統提示、驗證請求）。  
- **Outlet (出口)**：於模型回答**之後**處理（如：過濾敏感字詞、修改最終顯示文字）。

### 2.2 運作流程圖
```text
使用者輸入 → [Filter: Inlet] → LLM AI 模型 → [Filter: Outlet] → 顯示最終結果給使用者
```

### 2.3 Filter 與 Tool 的比較
| 比較項目 | Tool (工具) | Filter (過濾器) |
|----------|--------------|------------------|
| **執行時機** | AI 認為有需要時才隨機呼叫 | **每則對話都會強制經過** (依指派設定) |
| **概念比喻** | 賦予 AI 「特殊技能」 | 設定對話流的「安檢門」 |
| **實際作用** | 獲取外部資訊 (如查資料) | 分析或修改訊息本體內容 |

### 2.4 最小可用架構
- 類別名稱必須嚴格為 `Filter` (系統規範，**不可更改**)。  
- 需實作 `inlet()` 或 `outlet()` 方法 (依需求擇一，或兩者皆寫)。  
- 常用參數為 `body: dict`，內含 `messages` 陣列等重要欄位。

### 2.5 實作範例參考
> **開發與除錯指南**：[Filter 的測試和 Debug](./filter/Filter的測試和Debug.md)

建議依難度循序閱讀以下範例：
1. **基礎骨架**：[最簡單 Filter 結構](./filter/最簡單Filter結構.md)  
2. **加工範例**：[在 AI 回答結尾自動加文字](./filter/在AI回答結尾自動加文字.md)  
3. **現行 `body` 簽名**：[在回答結尾加天天開心](./filter/在回答結尾加天天開心.md)  
4. **進階應用**：[繁中轉換為英文](./filter/繁中轉換為英文.md) (搭配公司資訊輸出)

---

## 第三章：Action Function (動作按鈕)

### 3.1 核心概念
Action 可於**每則對話訊息下方**建立**自訂互動按鈕**，當使用者**點選**該按鈕時，才會觸發您所撰寫的系統邏輯。

### 3.2 常見使用情境
- 執行長文摘要、重點翻譯。
- 提供一鍵複製、匯出至特定系統之功能。
- 打造客製化工作流程與快捷鍵。

### 3.3 基本架構
- 類別名稱必須嚴格命名為 `Action`。  
- 核心方法為：`async def action(self, body, __user__, __event_emitter__)`。  
- 可利用 `__event_emitter__` 參數，即時向前端介面發送推播狀態或通知訊息。

### 3.4 基礎範例：訊息字數統計
此範例將於訊息下方產生按鈕，點擊後會計算該則訊息字數，並將統計結果附加於訊息結尾。

```python
"""
title: 基礎 Action 範例
author: YourName
version: 1.0
"""
from typing import Optional, Callable, Any

class Action:
    def __init__(self):
        pass

    async def action(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__: Optional[Callable[..., Any]] = None,
    ) -> Optional[dict]:
        
        # 取得所有對話
        messages = body.get("messages", [])
        if not messages:
            return body

        # 取得最後點擊欲處理的那則訊息
        last_message = messages[-1]
        message_content = last_message.get("content", "")
        message_len = len(message_content)

        # ⚠️ 由於目前前端接收 Action 的 SSE 串流時易發生 JSON 解析錯誤
        # 最穩定相容的做法是直接將結果附加在對話內容中並回傳 body
        last_message["content"] += f"\n\n*(系統分析：這則訊息的長度是 {message_len} 個字)*"

        # 回傳變更後的 body 讓前端更新畫面
        return body
```
<details>
<summary>💡 點此查看程式的工作流程(workflow)</summary>

這是一個**最小可運作的 Action 範例**，核心目的為：在使用者點擊 Action 時，讀取最後一則訊息並附加分析結果，再回傳更新後的對話。

**整體執行流程**：
1. **使用者觸發 Action**：前端將整段對話內容 (`messages`) 傳送給後端。
2. **呼叫 `action()` 方法**：Open WebUI 自動載入 Action 類別並非同步執行此函式。
3. **安全取得對話資料**：從 `body` 取出 `messages` 並防呆，若無對話則不執行邏輯。
4. **提取最後一則訊息**：透過 `messages[-1]` 取得使用者觸發 Action 當下的該則訊息。
5. **進行資料分析**：取得訊息文字 (`content`) 並計算字數。
6. **附加結果並回傳**：將分析結果接續在原對話內容的結尾處，並回傳更新後的 `body` 讓 UI 畫面更新。
  > **重要觀念**：因為前端接收 Action 串流時易有 JSON 解析錯誤，因此最穩定的做法是**直接修改原始 body，而不是嘗試推送新訊息**。

</details>

> 注意:當滑鼠移到Action按鈕時，顯示的名稱並非由程式碼決定，而是由建立Action時所填寫的名稱決定。

### 3.5 測試 Action 功能
1. 前往**聊天頁面**，發送任意文字訊息。  
2. 於**該則訊息下方**工具列 (按讚、複製等圖示旁) 尋找新增的 Action 按鈕。  
3. **點擊按鈕**，觀察該則訊息的最下方是否多出了一段關於「字數統計」的附註。

> **除錯提示**：若找不到按鈕，請確認該 Action 已於系統後台啟用，並已指派給當前對話使用的自訂模型。

### 3.6 進階實作案例 (檔案下載實務)

如果您已經熟悉基礎 Action 的掛載與操作邏輯，可以嘗試挑戰更進階實用的技巧：**如何在不污染系統碟的情況下，讓使用者一鍵下載對話記錄 (Word/Excel)**。利用修改訊息內容配合純文字的 Markdown 連結技巧，可以實現順暢的檔案導出。

1. [👉 進階教學 1：複製到剪貼簿](./action/複製到剪貼簿.md)
2. [👉 進階教學 2：生成 QR Code](./action/生成QRCode.md)
3. [👉 進階教學 3：保存會話到檔案](./action/保存會話到檔案.md)
4. [👉 進階教學 4：送出 Slack 通知](./action/送出Slack通知.md)
5. [👉 進階教學 5：中英翻譯小助手](./action/中英翻譯小助手.md)
6. [👉 進階教學 6：導出為 Word 檔案](./action/導出為Word檔.md)
7. [👉 進階教學 7：導出為 Excel 檔案](./action/導出為Excel檔.md)
8. [👉 進階教學 8：多重格式導出選擇器](./action/多重格式導出.md)

---

## 第四章：Pipe Function (管道與自訂模型)

### 4.1 核心概念
Pipe 允許我們創造出**全新自訂模型**，使其與一般大語言模型並列於介面上的**模型選擇清單**中，但實際上它的底層處理流程可以被任意定義與抽換。

### 4.2 常見使用情境
- 串接非預設支援的外部 API。
- 整合多個模型實現複雜的提詞鏈 (Prompt Chain)。
- 介接公司內部搜尋引擎或其他非 AI 功能 (如：天氣服務、IoT 裝置)。

### 4.3 基本架構
- 類別名稱必須命名為：`Pipe`
- 核心方法為：`pipe(self, body: dict) -> Union[str, Generator, Iterator]`
- 在 `__init__` 中設定 `self.id` (系統識別碼) 與 `self.name` (前端顯示名稱)。

> **重要觀念**：啟動 Pipe 後，系統清單會**自動**出現對應選項，無需另外於模型管理頁面手動建立實體模型。

### 4.4 基礎範例：鸚鵡回聲 Pipe
這是一個最小可運行的 Pipe 範例：它會攔截使用者最後一句話，不呼叫任何 AI 模型，直接回傳固定格式的字串對話。

```python
"""
title: 基礎 Pipe 範例
author: YourName
version: 1.0
"""
from typing import Union, Generator, Iterator

class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "test_pipe"
        self.name = "測試用鸚鵡模型"

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        # 提取使用者最後發送的訊息
        user_message = body["messages"][-1]["content"]
        
        # 組合並回傳結果
        response = f"[系統測試]：我收到了您的訊息，內容為「{user_message}」"
        return response
```
**測試方法**：部署後，於對話視窗左上角的**模型下拉清單**中選擇「測試用鸚鵡模型」，發送文字即可看見回覆。
<details>
<summary>💡 點此查看程式碼詳細解說</summary>

- **基本設定 (`__init__`)**：
  - `self.type = "pipe"`：宣告這是一個 Pipe 類型的 Function。
  - `self.id` 與 `self.name`：定義系統內部的唯一識別碼與前端顯示的模型名稱。啟動此 Pipe 後，聊天介面的模型清單就會出現對應的選項。
- **處理邏輯 (`pipe` 方法)**：
  - 此方法會接收前端傳來的 `body` 字典參數。最重要的資訊都放在 `body["messages"]` 這個對話歷史陣列中。
  - `body["messages"][-1]["content"]`：透過 `[-1]` 取出陣列的最後一筆元素，藉此獲得使用者最新傳送的文字內容。
  - 因為這是一個最簡單的回聲範例，所以完全沒有呼叫外部 API 或 LLM。我們只是單純將取出的訊息內容包裝進新字串中並直接 `return`，系統便會將這個字串作為生成結果顯示給使用者看。
</details>

### 4.5 進階技巧：自訂跟進問題 (Follow-up Suggestions)

#### 為什麼會出現 `Question 1?`
如果您啟用了 Open WebUI 的「聊天建議 (Chat Suggestions)」功能，每次您送出對話後，前端都會**自動發起第二次隱藏對話**，並在最後一句安插類似 `suggest 3 follow-up questions...` 的系統提示語，要求模型給出三個建議選項（預期回傳 JSON 陣列 `["選項A", "選項B"]`）。
由於**基礎鸚鵡 Pipe 只會硬生生地把文字當成一般對話彈回去**，導致前端收到錯亂的非 JSON 格式字串並解析失敗崩潰，最終就會預設使用 `Question 1?`, `Question 2?`, `Question 3?` 這些**錯誤回退 (Fallback)** 墊檔文字。

#### 實作「攔截器」來動態提供我們自己的選項
我們可以修改原先的 `pipe` 方法，去判斷如果對方的最後一句話是在詢問 `follow-up` 等關鍵字，我們就不把它當作普通對話，而是直接「攔截」下來，並丟還一個標準的 **JSON 陣列字串**。

```python
import json
from typing import Union, Generator, Iterator

class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "test_pipe"
        self.name = "測試用鸚鵡模型"

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        messages = body.get("messages", [])
        if not messages:
            return ""
            
        last_message = messages[-1].get("content", "")
        
        # [關鍵攔截]：如果發現系統是在詢問跟進問題 (通常帶有 follow-up 或 suggest 關鍵字)
        if "follow-up" in last_message.lower() or "suggest" in last_message.lower():
            # 必須回傳一個標準的 JSON 陣列字串！
            custom_questions = [
                "鸚鵡平常都吃什麼呀？", 
                "鸚鵡的心情好嗎？", 
                "再示範一次系統測試"
            ]
            return json.dumps(custom_questions, ensure_ascii=False)
        
        # 如果是一般正常對話，就正常回覆
        response = f"[系統測試]：我收到了您的訊息，內容為「{last_message}」"
        return response
```
<details>
<summary>💡 點此查看程式碼詳細解說</summary>

- **關鍵攔截 (`if "follow-up" in ...`)**：這是本段程式碼的核心。當前端介面在每次對話結束後自動發起「建議跟進問題」的請求時，提示詞通常會包含 `follow-up` 或 `suggest`，透過判斷這些字眼，我們可以區分這是一般對話還是系統的隱藏請求。
- **回傳 JSON 陣列 (`json.dumps(...)`)**：前端在處理「跟進問題」時，預期收到的是一個 JSON 格式的字串陣列。因此我們使用 `json.dumps()` 將 Python 的串列轉換為 JSON 字串，並設定 `ensure_ascii=False` 以確保繁體中文字元能正確顯示。
- **防止錯誤回退 (Fallback)**：如果不實作這個攔截邏輯，基礎版 Pipe 就會把系統發出的 `suggest 3 follow-up questions...` 當成一般對話語句並原樣彈回。這會導致前端由於接收不到預期的 JSON 而崩潰，最終只能顯示預設的錯誤回退文字 `Question 1?`。

> 當系統運行這段進階的 Pipe 時，您的對話框下方就會漂亮地長出您專屬的繁體中文客製按鈕了！如果您不需要這個功能，也可以直接前往 Open WebUI 【設定 ➔ 介面】將「生成跟進問題」關閉。

</details>

### 進階實作案列
1. [👉 串接本機 Ollama](./Pipe/串接本機ollama_api.md)

2. [👉 串接外部 Gemini API key (API Proxy Pipe)](./Pipe/串接外部api_proxy_pipe.md)

3. [👉 docx檔含佔位符_template/README.md](./Pipe/docx檔含佔位符_template/README.md)
---

## 第五章：Valves (參數閥門)

在 Open WebUI 系統中，**Valves** 提供了一種極佳的設計模式，負責將程式碼內的「變數」轉換成 UI 介面上的**輸入框、開關、數字欄位**，讓終端使用者能在**不動任何 `.py` 檔案**的情況下自訂參數 (如：API 金鑰、調整提示詞)。

> **注意**：**Pipe**、**Filter**、**Action** 三種 Function 皆支援 Valves 架構。

### 5.1 核心優勢
- **資訊安全**：避免將敏感資訊 (Tokens, API Keys) 寫死 (Hardcoded) 於程式碼內。
- **動態調整**：使用者於介面存檔後，下次對話即可自動套用新配置，即時生效。
- **型態映射**：利用 `Pydantic` 實作自動綁定變數型別與對應的前端 UI 元件。

| 設定之變數型別 | UI 元件呈現樣貌 |
|---------|-------------|
| `str` | 文字輸入框 |
| `bool` | 開關 (Toggle Switch) |
| `int` / `float` | 數字輸入框 |

### 5.2 實作範例 (以 Filter 為例)
```python
from pydantic import BaseModel, Field

class Filter:
    class Valves(BaseModel):
        # UI 開關設定
        is_active: bool = Field(
            default=True,
            description="是否啟用此附加文字功能",
        )
        # UI 文字輸入設定
        prefix: str = Field(
            default="[System Alarm]",
            description="要在訊息之前加入的標記文字",
        )

    def __init__(self):
        self.valves = self.Valves()

    async def inlet(self, body: dict, user: dict) -> dict:
        # 動態讀取 Valves 設定
        if not self.valves.is_active:
            return body

        messages = body.get("messages", [])
        if messages:
             # 加工加入 prefix 字串
             messages[-1]["content"] = f"{self.valves.prefix} {messages[-1]['content']}"
            
        return body
```

### 5.3 介面設定路徑
1. 開啟 **Functions (函式)** 清單頁面。
2. 點擊該 Function 右側的 **⚙️ 齒輪 (Settings)** 圖示。
3. 切換至 **Valves** 分頁區塊，在此改變的值將實質覆寫程式碼內的 `default` 值。

---

## 第六章：安裝、啟用與指派

開發或取得 Function 後，必須經由正確流程配置才能生效，請遵循以下步驟：

### 6.1 安裝 Functions
- **方式一**：於管理介面中，直接從 [Open WebUI Community 庫](https://openwebui.com/search) 尋找並一鍵匯入。
- **方式二**：點擊系統中的「+ 新增函式 (Add Function)」按鈕，手動貼上 Python 程式碼或上傳 `.py` 檔案。

### 6.2 啟用 Functions
匯入後預設皆為關閉狀態，請務必點擊清單項目右側的**啟用開關 (Toggle)** 啟用該功能模組。

### 6.3 依據類型進行指派
| 類型 | 取用方式 | 指派設定路徑說明 |
|------|-----------|--------------|
| **Pipe** | 獨立模型 | 啟用後自動出現於聊天介面的**模型選擇清單**中，無須額外指派。 |
| **Filter** | 增強套件 | **必須透過指派才能生效**。請至 **工作區 (Workspace) → 模型 (Models)**，編輯或新建自訂模型，於設定頁面將該 Filter 加入使用白名單；亦可於 Function 清單中設定為 **Global (全域生效)**。 |
| **Action** | 擴增按鈕 | 與 Filter 類似，需至自訂模型管理頁的 **行動 (Actions)** 區塊勾選，或設定為全球 (Global) 作用。 |

---
