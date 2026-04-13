!## Open WebUI Functions 講義

> **官方參考**：[Open WebUI Functions 文件](https://docs.openwebui.com/features/extensibility/plugin/functions/)  
> **說明**：本文件以「課堂講義」撰寫，建議搭配實機操作 Open WebUI 一併練習。

---

## 如何使用本講義

| 項目 | 說明 |
|------|------|
| **建議順序** | 依第一章 → 第六章閱讀；Filter／Pipe 可搭配第五章「安裝與啟用」邊做邊學。 |
| **先備知識** | 會開啟瀏覽器、會簡單編輯文字；若已學過 Python 基礎（變數、函式、`class`）會更輕鬆。 |
| **實作環境** | 須有可登入的 Open WebUI（本機或課堂伺服器），並具備**管理員／函式管理**權限者佳。 |

---

## 學習目標

讀完並完成練習後，你應能夠：

1. **說出** Functions 與 **Tools** 的差異，以及 Pipe、Filter、Action 三種類型各解決什麼問題。  
2. **在介面上** 安裝、啟用 Function，並正確指派 Filter／Action 或選用 Pipe 模型。  
3. **閱讀** 範例程式碼時，辨識 `inlet`／`outlet`／`pipe` 與 Valves 的用途。  
4. **遵守** 安全與實務建議（不隨意安裝來源不明的 Function）。

---

## 目錄

1. 第一章：認識 Functions  
2. 第二章：Filter（過濾器）  
3. 第三章：Action（動作按鈕）  
4. 第四章：Pipe（自訂模型）  
5. 第五章：安裝、啟用與指派  
6. 第六章：依賴套件管理 (Requirements)
7. 第七章：安全與實務  
8. 第八章：課後練習建議  
9. 第九章：附錄  

（在編輯器或 GitHub 中可用「大綱／Outline」快速跳轉各節標題。）

---

## 第一章：認識 Functions

### 1.1 什麼是 Functions？

- **定義**：Functions 是 Open WebUI 的「插件」，用來**擴充**介面與行為。  
- **特點**：
  - 內建於 Open WebUI，不需額外複雜整合  
  - 執行速度快、模組化  
  - 以 **Python** 撰寫，可自由客製  

### 1.2 Functions 與 Tools（工具）的差異

| 項目 | **Tools（工具）** | **Functions（本講義主題）** |
|------|-------------------|-----------------------------|
| 誰決定要不要用？ | **模型**可依對話內容「選擇呼叫」 | 依類型在**系統層**固定流程中執行（見下表） |
| 常見例子 | 查天氣、搜尋、計算 | Pipe、Filter、Action 三種 |

**請記住**：**Tool 不屬於 Functions**，而是另一種擴充機制；本講義專注於 **Pipe、Filter、Action**。

### 1.3 三種 Functions 類型總覽

| 類型 | 用途（白話） | 在介面上像什麼 |
|------|--------------|----------------|
| **Filter** | 在送進模型**前**或**後**修改內容 | 對指定模型或全域生效，使用者通常「無感」 |
| **Action** | 在訊息旁加**按鈕**，點了才執行 | 每則訊息下方出現可點擊按鈕 |
| **Pipe** | 假裝成一個**自訂模型** | 出現在**模型選擇清單**裡 |

### 1.4 到哪裡管理 Function？

- 路徑：**管理員控制台** → **函式**（Functions）

**本章重點**：Functions 是 Python 插件；與 Tools 不同；三種類型要分得清。

---

## 第二章：Filter Function（過濾器）

> 官方說明：[Filter Function](https://docs.openwebui.com/features/extensibility/plugin/functions/filter)

### 2.1 核心概念

- Filter 是「攔截器」，在 AI 回答**前**或**後**對內容加工。  
- **Inlet**：送進模型**之前**處理（使用者輸入／請求 body）。  
- **Outlet**：模型回答**之後**處理（可改最後顯示給使用者的文字）。

### 2.2 流程圖

```
使用者輸入 → [Filter: inlet] → LLM 模型 → [Filter: outlet] → 顯示給使用者
```

### 2.3 Filter 與 Tool 比較

| 比較項目 | Tool（工具） | Filter（過濾器） |
|----------|--------------|------------------|
| 由誰決定執行？ | AI 決定要不要用 | **每一則對話都會經過**（依指派） |
| 比喻 | 像「技能」 | 像「安檢門」 |
| 作用 | 查資料、計算等 | 修改訊息內容 |

### 2.4 最小可用 Filter 架構

- 類別名稱必須為 `Filter`（Open WebUI 規定，**不可改名**）。  
- 實作 `inlet()`、`outlet()`（依需求擇一或兩者都寫）。  
- 現行介面常使用 **`body: dict`**，內含 `messages` 等欄位（請以官方／範例為準）。

### 2.5 實作範例（依難度閱讀）

> **開發、測試與除錯**：[Filter 的測試和 Debug](./filter/Filter的測試和Debug.md)

1. **骨架**：[最簡單 Filter 結構](./filter/最簡單Filter結構.md)  
2. **有感範例**：[在 AI 回答結尾自動加文字](./filter/在AI回答結尾自動加文字.md)  
3. **現行 `body` 簽名**：在結尾加「天天開心」→ [在回答結尾加天天開心](./filter/在回答結尾加天天開心.md)  
4. **進階**：[語言過濾器程式碼](./filter/繁中轉換為英文.md) + 輸出加公司資訊  

### 2.6 Valves（閥門／可調參數）

> **適用範圍**：**Pipe**、**Filter**、**Action** 皆可使用 Valves。本節放在第二章是因為常與 Filter 一併實作，請勿誤會「只有 Filter 才有 Valves」。

在 Open WebUI 裡，**Valves** 負責把「可調參數」變成網頁上的**輸入框、開關、數字欄位**等。你在程式裡用 **Pydantic** 宣告欄位，使用者不必改 `.py` 就能調整 API 金鑰、網址、語言等。

#### 2.6.1 核心作用

程式碼中定義的欄位會對應到管理介面；執行時通常透過 **`self.valves`** 讀取（部分版本另有 **User Valves**，依官方文件為準）。

#### 2.6.2 程式碼範例（Pipe + Valves：前綴與大寫）

```python
from pydantic import BaseModel, Field
from typing import Union, Generator, Iterator

class Filter:
    class Valves(BaseModel):
        # 1. 布林值 (bool) -> UI 會呈現為「開關 (Toggle Switch)」
        is_active: bool = Field(
            default=True,
            description="是否啟用此過濾功能",
        )
        # 2. 整數 (int) -> UI 會呈現為「數字輸入框 (Number Input)」
        max_length: int = Field(
            default=50,
            description="限制使用者訊息的最大長度",
        )
        # 3. 浮點數 (float) -> UI 會呈現為「可輸入小數的數字框」
        intensity: float = Field(
            default=0.5,
            description="過濾強度 (0.0 到 1.0)",
        )
        # 4. 字串 (str) -> UI 會呈現為「文字輸入框 (Text Input)」
        prefix: str = Field(
            default="[System]",
            description="要在訊息前加入的標記",
        )

    def __init__(self):
        self.type = "filter"
        self.id = "multi_type_valves_filter"
        self.name = "全型態設定教學過濾器"
        self.valves = self.Valves()

    async def inlet(self, body: dict, user: dict) -> dict:
        # 如果開關關閉，直接回傳原始內容
        if not self.valves.is_active:
            return body

        messages = body["messages"]
        if messages:
            content = messages[-1]["content"]
            
            # 應用整數限制：如果太長就截斷
            if len(content) > self.valves.max_length:
                content = content[:self.valves.max_length]
            
            # 應用字串標記
            content = f"{self.valves.prefix} {content}"
            
            # 模擬 float 強度的邏輯：如果強度很高，將文字轉為大寫
            if self.valves.intensity > 0.8:
                content = content.upper()

            messages[-1]["content"] = content
            
        return body
```

#### 2.6.3 優點

- **安全性**：敏感資訊可放在 Valves，由使用者在**自己環境**填寫，不寫死在程式裡。  
- **動態調整**：在介面修改並儲存後，後續執行會讀到新設定（實際行為依版本而定）。  
- **介面對應**（常見，依版本可能略有差異）：  
  - `str`：文字  
  - `bool`：開關  
  - `int`／`float`：數字  
  - `Enum`、`Literal` 等：下拉或固定選項  

#### 2.6.4 在介面哪裡設定？

1. 在 Function 列表中，點該項目旁的 **齒輪（Settings）**。  
2. 找到 **Valves** 區塊。  
3. 在此輸入的值會在執行時由 `self.valves` 讀取。

**比喻**：**Pipe** 像輸送資料的管路；**Valves** 像管路上的開關與調節閥，在執行時調整行為而不必改程式本體。

### 2.7 Filter 的指派位置（重要）

- 建立並啟用 Filter 後，通常還要在**模型／工作區**裡**指派**，才會套用到對話。  
- **工作區（Workspace）** → **新增模型**／**建立模型**（或編輯自訂模型）：在該頁可**選取** **Filter**（過濾器），以及 **行動：**／**Actions** 中的 **Action**（與第三章、第五章對照）。  
- 亦可 **Workspace → Models** 選擇既有自訂模型後，在同畫面調整 Filter／行動。

**本章重點**：Filter 有 inlet／outlet；類別名必須叫 `Filter`；Valves 三種 Function 都能用；指派後才會在對話中生效。

---

## 第三章：Action Function（動作按鈕）

### 3.1 核心概念

- 在**每則訊息下方**新增**自訂按鈕**。  
- 使用者**點擊**後才執行你寫的邏輯（摘要、翻譯、匯出等）。

### 3.2 使用情境

- 摘要長訊息、翻譯、一鍵複製或匯出  
- 自訂工作流程快捷鍵  

### 3.3 基本架構

- 類別名稱必須為 `Action`（依 Open WebUI 規定）。  
- 主要方法為 **`async def action(self, body, __user__, __event_emitter__)`**（參數名稱與是否可選依版本／官方文件為準）。  
- 可透過 **`__event_emitter__`** 對介面發送狀態或通知（例如本範例的「訊息長度」提示）。

### 3.4 實作範例

#### 基礎範例：顯示目前訊息字數

點擊按鈕後，用 **status** 通知顯示該則訊息長度。完整說明與程式碼見：[基礎 Action 範例](./action/基礎Action範例.md)。

```python
"""
title: 基礎 Action 範例
author: Gemini
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
        message_content = body.get("message", {}).get("content", "")
        message_len = len(message_content)

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"這則訊息的長度是：{message_len} 個字",
                        "done": True,
                    },
                }
            )

        return None
```

- 延伸：摘要按鈕、翻譯按鈕等可在此骨架上改寫 `action()` 內邏輯，或參考社群範例。  

### 3.5 指派方式（與 Filter 相同：工作區 → 新增／建立模型）

Action 的啟用方式與 **Filter** 一樣：在**工作區（Workspace）**裡透過**自訂模型**來掛載，而不是只在「函式」頁面啟用就自動出現在聊天室。

1. 進入 **工作區** → **新增模型**（介面也可能顯示為 **建立模型**，依版本而異）。  
2. 在建立或編輯自訂模型的畫面中，除了可選 **Filter（過濾器）** 外，通常還會看到 **行動：**（或 **Actions**）區塊。  
3. **行動：** 後方會**列出目前已啟用的所有 Action**，勾選或選取你要套用到這個自訂模型上的項目。  
4. 儲存後，使用**這個自訂模型**開啟對話時，訊息旁才會出現對應按鈕。

**補充**：亦可透過 **Workspace → Models** 編輯既有自訂模型，在同樣的 Filter／行動區塊調整指派；**全域**啟用方式見第五章。

### 3.6 測試步驟（基礎範例：訊息字數通知）

**測試按鈕是否生效：**

1. 到**聊天頁面**，隨便輸入一段話（例如：「你好，這是一次測試」）。  
2. 在**這則訊息下方**（通常在按讚、複製等按鈕旁邊），會多出一個**新的按鈕圖示**（預設可能是小圓點、閃電符號等，依 Open WebUI 版本而定）。  
3. **點擊該按鈕**，畫面上方應會彈出**狀態通知**，內容為這則訊息的字數（與範例程式中的 `description` 一致）。

若看不到按鈕：請確認此 Action 已啟用、已指派給你正在使用的**自訂模型**，且目前對話確實使用該模型。

**本章重點**：Action 是「按了才做」的按鈕；指派路徑與 Filter 相同（工作區 → 新增／建立模型 → **行動：** 選取）；最簡骨架為 `async def action` + 可選的 `__event_emitter__` 通知介面。

---

## 第四章：Pipe Function（管道／自訂模型）

### 4.1 核心概念

- Pipe 會在**模型選擇清單**裡多出一個**自訂條目**，像一個新「模型」。  
- 不一定需要呼叫 LLM，可串接搜尋 API、天氣、Home Assistant 等。

### 4.2 使用情境

- 串接外部 API、多模型串接、整合非 AI 服務  

### 4.3 基本架構

- 類別名稱：`Pipe`
- 主要方法：`pipe(self, body: dict)` → 回傳字串或串流等（依官方簽名）

**Open WebUI 與「自訂模型」的對應：**

- 啟用 Pipe 後，清單會多出對應條目，**不必**另外在後台手動建立「模型」實體。  
- **`self.id`**：在清單中辨識此 Pipe 的 **id**（例如 `test_pipe`）。  
- **`self.name`**：使用者較容易看到的**顯示名稱**。  
- 修改 `self.id` 時，清單中的識別也會跟著變。

### 4.4 實作範例

#### 基礎範例：回顯使用者訊息（最簡 Pipe）

以下為最小可運行範例：在模型清單中選此 Pipe 後，會把使用者**最後一句話**包在固定格式回覆中（可再改為呼叫 OpenAI、Claude 等）。

```python
"""
title: 基礎 Pipe 範例
author: Gemini
version: 1.0
"""

from typing import Union, Generator, Iterator


class Pipe:
    def __init__(self):
        self.type = "pipe"
        self.id = "test_pipe"
        self.name = "我的測試模型"

    def pipe(self, body: dict) -> Union[str, Generator, Iterator]:
        user_message = body["messages"][-1]["content"]
        response = f"[測試回覆]：我收到了你的訊息，內容是「{user_message}」"
        return response
```

**操作提示**：儲存並啟用後，在對話視窗的**模型選擇器**中選擇 **id 為 `test_pipe`** 的項目（與 `self.id` 一致），即可走上述 `pipe()` 邏輯。

- 進階範例一：簡單的搜尋 Pipe  
- 進階範例二：多模型串接 Pipe  

**本章重點**：Pipe 出現在模型清單；`id` 與 `name` 要分清楚；`body["messages"]` 含對話內容。

---

## 第五章：安裝、啟用與指派

### 5.1 安裝 Functions

- **方式一**：透過 Open WebUI 介面從**社群函式庫**安裝  
- **方式二**：手動匯入（貼上程式碼或上傳檔案）  
- 社群來源：[Open WebUI Community](https://openwebui.com/search)

### 5.2 啟用 Functions

- 安裝後通常需**手動啟用**  
- **Pipe**：啟用後通常即出現在**模型清單**  
- **Filter／Action**：啟用後還需**指派**（見下節）

### 5.3 指派 Filter 或 Action

- **建立／編輯自訂模型**：**工作區** → **新增模型**／**建立模型** → 在該頁掛載 **Filter（過濾器）**，並在 **行動：**（**Actions**）區塊選取要啟用的 **Action**（與第三章、第二章路徑相同）。  
- **既有模型**：**Workspace** → **Models** → 選擇自訂模型 → 在同畫面調整 Filter／行動。  
- **全域**：**Workspace** → **Functions** → 該 Function 的「…」→ **Global**（依版本而定）

### 5.4 快速對照表

| 類型 | 啟用後 | 額外步驟 |
|------|--------|----------|
| Pipe | 出現在模型清單 | 通常不需指派 |
| Filter | 已啟用 | 需指派給模型或設為全域 |
| Action | 已啟用 | 需指派給模型或設為全域 |

**本章重點**：先安裝、再啟用；Filter／Action 多半還要指派才會作用。

---

## 第六章：安全注意事項與實務建議

### 6.1 安全警告

- Functions 在伺服器上執行**任意 Python 程式碼**。  
- 只從**可信來源**安裝；匯入前**閱讀原始碼**。  
- 惡意 Function 可能：存取檔案、竊取資料、破壞系統。

### 6.2 實務建議

1. 先在**測試環境**驗證  
2. 用 **Valves** 放可調參數，避免寫死金鑰  
3. 適當的錯誤處理與紀錄（log）  
4. **Filter** 每則訊息可能都會執行，避免過重計算  

### 6.3 為什麼要學 Functions？

- **擴充**：新模型、API、資料庫、智慧裝置  
- **優化**：輸入／輸出符合教學或組織需求  
- **簡化**：按鈕與捷徑提升操作效率  

**本章重點**：安全優先；先讀程式再安裝；注意效能與權限。

---

## 課後練習建議

1. 在測試環境安裝一個**官方或社群 Filter**，並完成指派，觀察對話前後變化。  
2. 匯入並啟用**基礎 Pipe**範例，在模型清單找到 `test_pipe`，送出一則訊息並截圖或記錄結果。  
3. 開啟某 Function 的 **Valves**（若範例有提供），修改一個參數後再測一次，比較差異。  
4. 以條列寫出：**Tools** 與 **Functions** 各一個你熟悉的例子。

---

## 附錄

### A. 本倉庫與延伸閱讀

| 檔案／資料夾 | 說明 |
|--------------|------|
| `README.md`（本文件） | 講義總覽 |
| [`filter/`](./filter/) | Filter 範例與除錯說明 |
| [`action/`](./action/) | Action 範例（基礎按鈕與通知） |

### B. 教學／維護者參考：建議檔案結構（選讀）

```
OpenWebUI/Functions/
├── README.md          # 本講義
├── filter/            # Filter 範例與除錯
├── action/            # Action 範例
└── （可依課程再拆 01_認識 Functions.md …） 
```

---

## 版本與用語

- Open WebUI 介面可能隨版本更新；路徑名稱（例如 **Workspace**、**Functions**）以你實機為準。  
- 英文術語（如 Inlet、Outlet、Valves）本講義保留原文，方便對照官方文件。
