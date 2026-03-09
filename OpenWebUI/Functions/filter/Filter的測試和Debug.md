# Filter 的測試與 Debug 指南

本文件說明如何使用 **uv 虛擬環境** 進行 Filter 的本地開發、除錯與測試，以及如何安裝額外的 Python 套件。

---

## 📋 目錄

- [為什麼要用虛擬環境開發？](#為什麼要用虛擬環境開發)
- [使用 uv 建立開發環境](#使用-uv-建立開發環境)
- [安裝額外套件](#安裝額外套件)
- [Debug 方式](#debug-方式)
- [測試方式](#測試方式)
- [常見問題](#常見問題)

---

## 為什麼要用虛擬環境開發？

| 項目 | 虛擬環境（本地） | 透過 Open WebUI 介面 |
|------|------------------|----------------------|
| **Debug** | 可用 `pdb`、`breakpoint()`、IDE 中斷點 | 僅能看 log |
| **修改程式** | 改完直接重跑 | 需重新匯入或重啟服務 |
| **安裝依賴** | `uv pip install` 即可 | 依賴 `requirements` 或手動安裝 |
| **迭代速度** | 快 | 較慢 |

**建議流程：** 先用 uv 虛擬環境開發、debug、單元測試，確認沒問題後再匯入至 Open WebUI 或部署。

---

## 使用 uv 建立開發環境

### 前置需求

- **Python 3.11**（Open WebUI 官方支援版本）
- `uv` 套件管理工具

### 步驟 1：安裝 uv

**macOS / Linux：**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)：**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

驗證安裝：

```bash
uv --version
```

### 步驟 2：建立專案目錄與虛擬環境

```bash
# 進入你的 Filter 開發目錄
cd OpenWebUI/Functions/filter

# 使用 uv 建立虛擬環境（會產生 .venv/）
uv venv

# 啟動虛擬環境
source .venv/bin/activate   # macOS / Linux
# 或 .venv\Scripts\activate  # Windows
```

### 步驟 3：安裝基礎依賴

Filter 通常會用到 `pydantic`（Valves 設定），若你的 Filter 有呼叫外部 API 則需要 `requests`：

```bash
# 安裝常用套件
uv pip install pydantic requests
```

---

## 安裝額外套件

### 方式一：在 uv 虛擬環境中安裝（開發時推薦）

使用 uv 時，用 `uv pip install` 安裝額外套件：

```bash
# 啟動虛擬環境後
source .venv/bin/activate

# 安裝單一套件
uv pip install requests
uv pip install langdetect
uv pip install spacy

# 若有多個套件，可建立 requirements.txt 後一次安裝
echo "requests>=2.28.0" >> requirements.txt
echo "pydantic>=2.0" >> requirements.txt
uv pip install -r requirements.txt
```

**常用 uv 指令：**

| 指令 | 說明 |
|------|------|
| `uv pip install <套件>` | 安裝單一套件 |
| `uv pip install -r requirements.txt` | 依 requirements.txt 安裝 |
| `uv pip list` | 列出已安裝套件 |
| `uv pip freeze > requirements.txt` | 匯出目前環境的套件清單 |

### 方式二：在 Filter 程式碼中宣告 requirements（Open WebUI 介面匯入時）

當你透過 Open WebUI 的**管理員 → 函式**匯入 Filter 時，可在程式碼開頭的 docstring 中宣告 `requirements`：

```python
"""
title: 繁中轉換為英文
author: 教學用
version: 1.0
description: 將使用者輸入的中文轉換為英文，並在輸出加上公司資訊
requirements: requests, pydantic
"""

from typing import Optional
import requests
from pydantic import BaseModel, Field

class Filter:
    # ...
```

**格式說明：**

- `requirements:` 後面用**逗號分隔**套件名稱
- 範例：`requirements: requests, pydantic, langdetect`
- Open WebUI 在**首次載入**該 Filter 時會嘗試安裝這些套件

**注意事項：**

1. **Docker 部署**：若 Open WebUI 跑在 Docker 內，套件會安裝到**容器內**，重啟容器後需重新安裝（除非有 volume 或自訂 Dockerfile 預裝）
2. **多實例部署**：若使用 Kubernetes 等多實例，套件只會安裝在「新增 Filter 時」處理請求的那個實例，其他實例可能沒有該套件，需在映像或啟動腳本中預先安裝

### 方式三：自訂 Dockerfile 預裝（正式部署推薦）

若 Filter 需要 `requests`、`langdetect` 等套件，且使用 Docker 部署 Open WebUI，建議在自訂 Dockerfile 中預裝：

```dockerfile
FROM ghcr.io/open-webui/open-webui:main

# 預裝 Filter 所需的額外套件
RUN pip install --no-cache-dir requests pydantic langdetect
```

---

## Debug 方式

### 方式 1：使用 `print()` 快速輸出

最簡單的方式，在 `inlet` 或 `outlet` 內加入 `print()`：

```python
def inlet(self, body: dict, __user__: dict | None = None) -> dict:
    user_message = body["messages"][-1]["content"]
    print(f"[Filter Debug] 使用者輸入: {user_message}")  # 會出現在 Open WebUI 的 log
    # ...
    return body
```

**查看 log：**

- **Docker**：`docker logs -f <open-webui-container-id>`
- **本機執行**：終端機直接顯示

### 方式 2：使用 `breakpoint()` 或 `pdb`

在 Filter 的 `inlet` 或 `outlet` 內加入：

```python
def inlet(self, body: dict, __user__: dict | None = None) -> dict:
    breakpoint()  # Python 3.7+ 內建，會暫停並進入互動式 debugger
    # 或
    import pdb; pdb.set_trace()

    user_message = body["messages"][-1]["content"]
    # ...
    return body
```

當請求觸發到該行時會暫停，可輸入：

- `n`：下一行
- `s`：進入函數
- `c`：繼續執行
- `p 變數名`：印出變數值
- `q`：離開

> ⚠️ **注意**：`breakpoint()` 需在**本機執行** Open WebUI 時才有用。若跑在 Docker 內，需進入容器或使用遠端除錯。

### 方式 3：VS Code / Cursor 除錯

若你從原始碼執行 Open WebUI（非 Docker），可在專案根目錄建立 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Open WebUI",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["open_webui.main:app", "--host", "0.0.0.0", "--port", "8080"],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

需先安裝 `debugpy`：`uv pip install debugpy`

在 Filter 程式碼中設中斷點，按 **F5** 啟動除錯。

### 方式 4：使用 `logging` 模組

適合正式環境，可控制 log 等級：

```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def inlet(self, body: dict, __user__: dict | None = None) -> dict:
    user_message = body["messages"][-1]["content"]
    logger.info(f"[Filter] 使用者輸入: {user_message}")
    logger.debug(f"[Filter] body keys: {body.keys()}")
    # ...
    return body
```

---

## 測試方式

### 方式 1：直接測試 Filter 邏輯（不需啟動 Open WebUI）

建立 `test_filter.py`，模擬 `inlet` / `outlet` 的輸入：

```python
"""
直接測試 Filter 邏輯，不需啟動 Open WebUI
"""
import sys
sys.path.insert(0, ".")  # 或你的 Filter 所在目錄

# 假設 Filter 寫在 my_filter.py 中
from my_filter import Filter

# 建立 Filter 實例
f = Filter()

# 模擬 inlet 的 body
body_inlet = {
    "messages": [
        {"role": "user", "content": "你好，請介紹台灣"}
    ],
    "model": "llama3.1"
}

# 測試 inlet
result = f.inlet(body_inlet, None)
print("inlet 輸出:", result["messages"][-1]["content"])

# 模擬 outlet 的 body（含 AI 回答）
body_outlet = {
    "messages": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！有什麼可以幫你的？"}
    ]
}

# 測試 outlet
result = f.outlet(body_outlet, None)
print("outlet 輸出:", result["messages"][-1]["content"])
```

執行：

```bash
source .venv/bin/activate
uv pip install pydantic requests  # 依你的 Filter 需求
python test_filter.py
```

### 方式 2：使用 pytest 單元測試

```bash
uv pip install pytest
```

建立 `tests/test_my_filter.py`：

```python
import pytest
import sys
sys.path.insert(0, "..")
from my_filter import Filter

def test_inlet_preserves_messages():
    f = Filter()
    body = {"messages": [{"role": "user", "content": "test"}]}
    result = f.inlet(body, None)
    assert "messages" in result
    assert len(result["messages"]) >= 1

def test_outlet_appends_content():
    f = Filter()
    body = {
        "messages": [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "Hello!"}
        ]
    }
    result = f.outlet(body, None)
    assert result["messages"][-1]["role"] == "assistant"
```

執行：

```bash
pytest tests/ -v
```

### 方式 3：透過 Open WebUI 整合測試

1. 將 Filter 程式碼匯入 Open WebUI：**管理員 → 函式 → 建立新函式**
2. 啟用 Filter 並指派給測試用的模型
3. 在聊天介面發送訊息，觀察 Filter 是否正確修改輸入/輸出
4. 查看 Docker 或終端機的 log 確認 `print` / `logger` 輸出

---

## 常見問題

### Q: Filter 需要 `requests`，但匯入後出現 `ModuleNotFoundError`？

**解法：**

1. 在 Filter 的 docstring 加上 `requirements: requests`
2. 或手動在 Open WebUI 的執行環境中安裝：若用 Docker，進入容器執行 `pip install requests`
3. 或自訂 Dockerfile 預裝 `requests` 後重建映像

### Q: 使用 uv 開發時，如何確保與 Open WebUI 的 Python 版本一致？

Open WebUI 使用 Python 3.11，建立虛擬環境時可指定：

```bash
uv venv --python 3.11
```

### Q: `outlet` 沒有被呼叫？

`outlet` 僅在 **Web UI 聊天**完成時觸發，**直接呼叫 `/api/chat/completions` 的 API** 不會觸發。若需 outlet 處理 API 請求，客戶端需在收到完整回應後再呼叫 `/api/chat/completed`。

### Q: 如何驗證 Filter 的 Valves 是否生效？

在 `inlet` 或 `outlet` 內加入：

```python
print(f"[Filter] Valves: {self.valves.model_dump()}")
```

在管理介面調整 Valves 後，重新發送訊息，檢查 log 中的輸出是否改變。

---

## 參考資源

- [Open WebUI Filter Function 官方文件](https://docs.openwebui.com/features/extensibility/plugin/functions/filter/)
- [最簡單 Filter 結構](./最簡單Filter結構.md)
- [在 AI 回答結尾自動加文字](./在AI回答結尾自動加文字.md)
- [繁中轉換為英文](./繁中轉換為英文.md)
- [Pipeline 測試與 Debug](../../pipeline/Pipeline_測試與Debug.md)（可參考虛擬環境與 Debug 流程）
