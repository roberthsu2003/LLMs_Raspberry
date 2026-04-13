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
7. [第七章：安全注意事項與實務建議](#第七章安全注意事項與實務建議)
8. [第八章：課後練習建議](#第八章課後練習建議)
9. [第九章：附錄與用語說明](#第九章附錄與用語說明)

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

### 3.5 測試 Action 功能
1. 前往**聊天頁面**，發送任意文字訊息。  
2. 於**該則訊息下方**工具列 (按讚、複製等圖示旁) 尋找新增的 Action 按鈕。  
3. **點擊按鈕**，觀察該則訊息的最下方是否多出了一段關於「字數統計」的附註。

> **除錯提示**：若找不到按鈕，請確認該 Action 已於系統後台啟用，並已指派給當前對話使用的自訂模型。

### 3.6 進階實作案例 (檔案下載實務)

如果您已經熟悉基礎 Action 的掛載與操作邏輯，可以嘗試挑戰更進階實用的技巧：**如何在不污染系統碟的情況下，讓使用者一鍵下載對話記錄 (Word/Excel)**。利用修改訊息內容配合純文字的 Markdown 連結技巧，可以實現順暢的檔案導出。

1. [👉 進階教學 1：導出為 Word 檔案](./action/導出為Word檔.md)
2. [👉 進階教學 2：導出為 Excel 檔案](./action/導出為Excel檔.md)
3. [👉 進階教學 3：多重格式導出選擇器](./action/多重格式導出.md)

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
當系統運行這段進階的 Pipe 時，您的對話框下方就會漂亮地長出您專屬的繁體中文客製按鈕了！如果您不需要這個功能，也可以直接前往 Open WebUI 【設定 ➔ 介面】將「生成跟進問題」關閉。

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

## 第七章：安全注意事項與實務建議

強大的擴充機制伴隨著較高的潛在風險。由於 Functions 允許系統伺服器執行**任意 Python 代碼**，請嚴格遵守以下準則：

### 7.1 安全警告
1. **拒絕不明信任來源**：請勿安裝社群上未經審查或功能過於特異之 Function。
2. **親自審查程式碼**：因具備 Server 端檔案讀寫及外網存取權限，惡意程式可能導致資料外洩，匯入前強烈建議親手檢閱原始碼。

### 7.2 開發與維運建議
1. **建立測試環境先驗**：所有的自訂 Function 都應優先於測試區間段進行行為驗證，確認穩定後再佈署給一般使用者。
2. **全面落實 Valves**：機敏資訊 (API Keys, Token等) **嚴禁**明文寫死在系統庫中，請統一採用 Valves 模式來提取介面參數。
3. **留意 Filter 效能開銷**：Filter 為攔截器，它將涉足使用者的每一次對話。若在此執行過於龐大或耗時的處理作業及網路請求，將直接拖慢對話反應速度，甚至引發伺服器 Timeout。

---

## 第八章：課後練習建議

為驗證您的學習成效，請於實機上盡量完成下列操作任務：
1. **搜尋與安裝**：至社群資源區尋找並安裝一款熱門的 Filter 功能，透過系統指派機制體驗實際效果。
2. **開發與佈署**：將本講義提供的「測試用鸚鵡模型 (Pipe)」複製匯入系統，開啟新對話並成功觸發回話。
3. **體驗 Valves 操作**：修改現有的 Function 範例代碼，添增一個名為 `System Prompt Prefix` 的 Valve，並透過介面動態變更參數後觀察覆寫結果。
4. **觀念重塑**：請嘗試用精煉的話語，向身邊的人具體總結 **Tools (工具)** 與 **Functions (函式)** 操作上的本質差別。

---

## 第九章：附錄與用語說明

### A. 本地教材參考結構
| 檔案/資料夾路徑 | 標的說明 |
|--------------|------|
| `README.md` (本文件) | 總覽與教材知識本體 |
| [`filter/`](./filter/) | Filter 進階開發範例與除錯技巧說明 |
| [`action/`](./action/) | Action 互動按鈕各類範例集合 |

*（註：如欲深入各章節實作，請參照本源碼庫對應資料夾內之延伸文件）*

### B. 常見用語辭典
- **Workspace (工作區)**：供管理員建立並自定義模型 (Models)、知識庫 (Knowledge)、系統提示與函式的基地。
- **Inlet / Outlet**：資料傳輸的流口，對應文字進出 LLM 模型前的前處理與後處理階段。
- **Valves**：參數控制閥門，一套無縫橋接「後端變數」與「前端 UI 設定表單」之機制。

