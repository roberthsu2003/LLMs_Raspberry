# 範例二：基礎 Python 工具（讓 AI 調用外部功能）

當單純的 Prompt 已經無法滿足需求時（例如：計算精準的數學數字、取得當下的真實時間、聯網爬蟲），我們就需要開發帶有 Python 程式碼的 **Tool (工具)**。

大語言模型 (LLM) 在面對複雜數學計算時很容易「產生幻覺」給出錯的答案。這個中階範例將教您如何寫一個 **「精準計算機」** 工具，讓 AI 遇到算數問題時，會自動切換為呼叫這個 Python 工具來得出 100% 正確的結果。

---

## 🛠️ 實作步驟

1. 在 OpenWebUI 介面，進入 **Workspace (工作區) → Tools (工具)**。
2. 點擊 **+ New Tool (新增工具)** 或 **+ 功能**。
3. 為它命名，例如 `CalculatorTool`，接著將下方的 Python 程式碼完整貼上。

### 🐍 Python 程式碼範例

```python
import operator

class Tools:
    def __init__(self):
        # 這裡可以放置需要初始化的變數
        pass

    def calculate(self, number1: float, number2: float, operation: str) -> str:
        """
        當使用者詢問任何數學計算問題時，請務必呼叫這個工具來取得精準的解答。
        
        :param number1: 第一個數字 (float)
        :param number2: 第二個數字 (float)
        :param operation: 要執行的算術運算，僅限於 "add" (加), "subtract" (減), "multiply" (乘), "divide" (除)
        """
        operations = {
            "add": operator.add,
            "subtract": operator.sub,
            "multiply": operator.mul,
            "divide": operator.truediv
        }

        if operation not in operations:
            return "錯誤：不支援該運算符號，請使用 add, subtract, multiply 或 divide。"

        try:
            # 讓 Python 來執行真實的計算
            result = operations[operation](number1, number2)
            return f"計算結果：{number1} 與 {number2} 進行 {operation} 運算，答為 {result}"
        except ZeroDivisionError:
            return "計算錯誤：除數不能為零！"
        except Exception as e:
            return f"發生未知的系統錯誤：{e}"
```

---

## 🚀 測試與運作原理

1. 儲存工具後，請確認您的帳號對此工具有「啟用」權限。
2. 回到首頁建立一個新的對話視窗。
3. 在輸入框下方點擊 `+`（或相應的工具面板），將剛才建立的 **CalculatorTool** 掛載到當次對話中。
4. 試著問 AI：「`請幫我計算 2345.67 乘以 9876.54 是多少？`」
5. **觀察結果**：您會發現對話中會彈出一個小視窗顯示 **"Tool Call: calculate"**，這代表 AI 自己意識到它正在面對數學問題，並且聰明地把 `2345.67` 跟 `9876.54` 以及 `multiply` 傳給了您寫的 Python 程式。
6. 最後輸出的答案將完全精準，因為它是 Python 算出來，而不是 AI 用猜的。

---

> 💡 **小結**：
> 在這個範例中，最核心的技巧在於 `""" 這段註解 (Docstring) """`。LLM 本身上並不包含 Python，它能在看懂這段註解後，將對話拆解成 `number1`、`number2` 參數並餵給您的 Python 腳本。
> 在下一篇最高階範例中，我們將教您如何讀取「檔案」並在畫面上動態顯示「讀取中」的動畫！
