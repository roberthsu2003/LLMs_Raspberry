# Pipeline（第 3 章）：程式碼實作

## 📋 目錄

- [範例檔](#範例檔)
- [下載官方範例](#下載官方範例)
- [Pipeline 類別結構](#pipeline-類別結構)
- [Valves 設定](#valves-設定)
- [安裝與使用](#安裝與使用)
- [測試與 Debug](#測試與-debug)

---

## 範例檔

本範例完整檔案位於 [範例檔](./範例檔/) 資料夾：

```
範例檔/
└── wikipedia_pipeline_zh.py   # 中文維基百科 Pipeline
```

| 檔案 | 說明 |
|------|------|
| [wikipedia_pipeline_zh.py](./範例檔/wikipedia_pipeline_zh.py) | 中文維基百科查詢 Pipeline，使用 `wikipedia` 套件 |

---

## 下載官方範例

```bash
wget https://raw.githubusercontent.com/open-webui/pipelines/main/examples/pipelines/integrations/wikipedia_pipeline.py
```

[官方範例目錄](https://github.com/open-webui/pipelines/tree/main/examples)

---

## Pipeline 類別結構

```python
class Pipeline:
    class Valves(BaseModel):
        # 可調參數
        RATE_LIMIT: int = Field(default=5, description="...")
        WORD_LIMIT: int = Field(default=300, description="...")

    def __init__(self):
        self.name = "Pipeline 名稱"
        self.valves = self.Valves(...)

    async def on_startup(self):
        # 伺服器啟動時呼叫
        pass

    async def on_shutdown(self):
        # 伺服器關閉時呼叫
        pass

    def pipe(self, user_message, model_id, messages, body):
        # 主要處理邏輯，可 yield 串流或 return 完整結果
        yield "chunk1"
        yield "chunk2"
```

---

## Valves 設定

Valves 是 Pipeline 的可調參數，會在 Open-WebUI 的 Pipeline 設定頁面顯示：

| 參數 | 說明 |
|------|------|
| `RATE_LIMIT` | 每秒請求限制 |
| `WORD_LIMIT` | 摘要字數上限 |
| `WIKIPEDIA_ROOT` | 維基百科根網址（中文版：zh.wikipedia.org） |

---

## 安裝與使用

### 1. 複製 Pipeline 到 volume

若使用 bind mount：

```bash
cp 範例檔/wikipedia_pipeline_zh.py /path/to/pipelines/
```

若使用 named volume，可透過 Open-WebUI 的 **Settings → Pipelines** 上傳。

### 2. 安裝依賴

Wikipedia Pipeline 需要 `wikipedia` 套件。若使用官方映像，需自訂 Dockerfile：

```dockerfile
FROM ghcr.io/open-webui/pipelines:main
RUN pip install --no-cache-dir wikipedia
```

### 3. 在 Open-WebUI 中啟用

Settings → Pipelines → 選擇「中文維基百科 Pipeline」→ 啟用

---

## 測試與 Debug

使用 Python 虛擬環境進行本地開發、除錯與測試，可加快迭代速度。詳細說明請參考：

> [Pipeline 測試與 Debug](../Pipeline_測試與Debug.md)

---

上一篇：[Pipeline_02_整合Cloudflare](../Pipeline_02_整合Cloudflare/README.md)  
下一篇：—
