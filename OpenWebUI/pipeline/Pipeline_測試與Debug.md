# Pipeline 測試與 Debug 指南

本文件說明如何使用 **Python 虛擬環境** 進行 Pipeline 的本地開發、除錯與測試，無需每次都透過 Docker 重建映像。

---

## 📋 目錄

- [為什麼要用虛擬環境開發？](#為什麼要用虛擬環境開發)
- [本地開發環境設定](#本地開發環境設定)
- [Debug 方式](#debug-方式)
- [測試方式](#測試方式)
- [與 Docker 的差異](#與-docker-的差異)

---

## 為什麼要用虛擬環境開發？

| 項目 | 虛擬環境（本地） | Docker |
|------|------------------|--------|
| **Debug** | 可用 `pdb`、`breakpoint()`、IDE 中斷點 | 需進入容器或遠端除錯 |
| **修改程式** | 改完直接重跑或 `--reload` | 需重啟容器 |
| **安裝依賴** | `pip install` 即可 | 需改 Dockerfile 並 rebuild |
| **迭代速度** | 快 | 較慢 |

**建議流程：** 先用虛擬環境開發、debug、單元測試，確認沒問題後再打包成 Docker 或上傳至 Open WebUI。

---

## 本地開發環境設定

### 前置需求

- **Python 3.11**（官方唯一支援版本）
- `git`

### 步驟 1：克隆 Pipelines 專案

```bash
git clone https://github.com/open-webui/pipelines.git
cd pipelines
```

### 步驟 2：建立虛擬環境

**方式 A：使用 venv**

```bash
python3.11 -m venv venv
source venv/bin/activate   # macOS / Linux
# 或
# venv\Scripts\activate    # Windows
```

**方式 B：使用 uv（較快）**

```bash
# 安裝 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 建立虛擬環境
uv venv
source .venv/bin/activate  # macOS / Linux
```

### 步驟 3：安裝依賴

```bash
pip install -r requirements.txt

# 若你的 Pipeline 需要額外套件（如 Wikipedia Pipeline）
pip install wikipedia
```

### 步驟 4：放置你的 Pipeline 程式碼

將你的 `.py` 檔放到 `pipelines/` 目錄（或自訂目錄）：

```bash
mkdir -p pipelines
cp /path/to/your_pipeline.py pipelines/
```

### 步驟 5：啟動 Pipeline Server

```bash
# 使用預設 pipelines 目錄
sh ./start.sh

# 或指定自訂目錄
export PIPELINES_DIR=./my_pipelines
sh ./start.sh
```

Server 會在 `http://localhost:9099` 啟動。

### 步驟 6：熱重載（開發時推薦）

專案內有 `dev.sh`，會啟用 `--reload`，修改 `.py` 後會自動重載：

```bash
sh ./dev.sh
```

---

## Debug 方式

### 方式 1：使用 `breakpoint()` 或 `pdb`

在 Pipeline 的 `pipe()` 方法內加入：

```python
def pipe(self, user_message, model_id, messages, body):
    breakpoint()  # Python 3.7+ 內建，會暫停並進入互動式 debugger
    # 或
    import pdb; pdb.set_trace()

    # ... 你的邏輯
```

執行 `sh ./start.sh` 或 `sh ./dev.sh` 後，當請求觸發到該行時會暫停，可輸入：

- `n`：下一行
- `s`：進入函數
- `c`：繼續執行
- `p 變數名`：印出變數值
- `q`：離開

### 方式 2：VS Code / Cursor 除錯

在 pipelines 專案根目錄建立 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Pipeline Server",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["main:app", "--host", "0.0.0.0", "--port", "9099"],
      "cwd": "${workspaceFolder}",
      "env": {
        "PIPELINES_DIR": "./pipelines"
      }
    }
  ]
}
```

需先安裝 `debugpy`：`pip install debugpy`

在程式碼中設中斷點，按 **F5** 啟動除錯。

### 方式 3：加入 Log 輸出

```python
from logging import getLogger
logger = getLogger(__name__)
logger.setLevel("DEBUG")

def pipe(self, user_message, model_id, messages, body):
    logger.info(f"user_message: {user_message}")
    logger.debug(f"body: {body}")
    # ...
```

---

## 測試方式

### 方式 1：直接測試 `pipe()` 邏輯（不需啟動 Server）

建立 `test_my_pipeline.py`：

```python
import sys
sys.path.insert(0, "./pipelines")

# 依你的 Pipeline 檔名調整
from wikipedia_pipeline_zh import Pipeline

p = Pipeline()
for chunk in p.pipe("Taiwan", "wikipedia_pipeline", [], {"stream": True}):
    print(chunk, end="")
```

執行：

```bash
python test_my_pipeline.py
```

可快速驗證 `pipe()` 的輸入輸出，無需啟動完整 API。

### 方式 2：使用 pytest 單元測試

```bash
pip install pytest
```

建立 `tests/test_wikipedia_pipeline.py`：

```python
import pytest
import sys
sys.path.insert(0, "../pipelines")
from wikipedia_pipeline_zh import Pipeline

def test_pipe_returns_content():
    p = Pipeline()
    result = list(p.pipe("Python", "wikipedia_pipeline", [], {"stream": True}))
    assert len(result) > 0

def test_pipe_handles_empty():
    p = Pipeline()
    result = list(p.pipe("", "wikipedia_pipeline", [], {"stream": True}))
    assert len(result) >= 0
```

執行：

```bash
pytest tests/ -v
```

### 方式 3：透過 API 測試（需先啟動 Server）

```bash
# 測試 /v1/models
curl -H "Authorization: Bearer 0p3n-w3bu!" http://localhost:9099/v1/models

# 測試 chat completion
curl -X POST http://localhost:9099/v1/chat/completions \
  -H "Authorization: Bearer 0p3n-w3bu!" \
  -H "Content-Type: application/json" \
  -d '{"model": "wikipedia_pipeline", "messages": [{"role": "user", "content": "Taiwan"}]}'
```

### 方式 4：透過 Open WebUI 整合測試

1. 啟動本地 Pipeline Server：`sh ./start.sh`
2. 在 Open WebUI 的 **Settings → Connections → OpenAI API** 新增連線
3. API URL：`http://localhost:9099`（若 Open WebUI 在 Docker 內則用 `http://host.docker.internal:9099`）
4. API key：`0p3n-w3bu!`
5. 在聊天介面選擇 Wikipedia Pipeline 進行實際對話測試

---

## 與 Docker 的差異

| 情境 | 虛擬環境 | Docker |
|------|----------|--------|
| **開發、Debug、單元測試** | ✅ 推薦 | ❌ 較不便 |
| **正式部署** | 需自行管理環境 | ✅ 推薦 |
| **與 Open WebUI 整合** | 兩者都支援 | 兩者都支援 |

---

## 常見問題

### Q: 虛擬環境開發完後，如何部署到 Docker？

將 Pipeline 的 `.py` 檔放到 volume 或 bind mount 的目錄，或透過 Open WebUI 的 **Settings → Pipelines** 上傳。若需額外套件，自訂 Dockerfile 加入 `RUN pip install wikipedia` 等指令後重建映像。

### Q: `PIPELINES_DIR` 預設是什麼？

預設為 `./pipelines`。可透過環境變數覆寫：`export PIPELINES_DIR=/path/to/your/pipelines`

### Q: 如何測試需要 Ollama 的 Pipeline？

確保 Ollama 在本機運行（`http://127.0.0.1:11434`），Pipeline 程式內使用 `http://127.0.0.1:11434` 或 `http://localhost:11434` 連線即可。

---

## 參考資源

- [Open-WebUI Pipelines GitHub](https://github.com/open-webui/pipelines)
- [Pipeline 完整教學指南](./Pipeline_完整教學指南.md)
- [Pipeline_03 程式碼實作](./Pipeline_03_程式碼實作/README.md)
