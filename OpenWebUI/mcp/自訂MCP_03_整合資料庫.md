# 自訂 MCP Server（三）：整合資料庫

## 📋 目錄

- [前言](#前言)
- [一、核心概念](#一核心概念)
- [二、整合 SQLite](#二整合-sqlite)
- [三、整合 ChromaDB](#三整合-chromadb)
- [四、RAG 整合概念](#四rag-整合概念)
- [五、驗證與練習](#五驗證與練習)
- [六、整合 mcpo 部署](#六整合-mcpo-部署)

---

## 前言

本階段目標：讓 MCP 工具存取**資料庫**，實現 LLM 與既有資料的橋接。

學習重點：

- MCP = LLM 與外部世界的橋樑
- SQLite 查詢工具
- ChromaDB 向量搜尋與 RAG 概念

---

## 一、核心概念

```
使用者：「從知識庫找關於信用卡的資訊」
    │
    ▼
Open-WebUI + LLM 判斷需呼叫 MCP 工具
    │
    ▼
MCP Tool：query_knowledge_base("信用卡")
    │
    ▼
ChromaDB / SQLite 查詢
    │
    ▼
回傳結果給 LLM → 整理後回覆使用者
```

---

## 二、整合 SQLite

### 2.1 新增依賴

```
mcp
requests
```

（SQLite 為 Python 內建，無需額外安裝）

### 2.2 範例：查詢 SQLite

```python
import sqlite3

@mcp.tool()
def query_sqlite(query: str, db_path: str = "/data/sample.db") -> str:
    """對 SQLite 資料庫執行查詢（僅支援 SELECT）。"""
    if ";" in query and "SELECT" not in query.upper():
        return "僅支援 SELECT 查詢"
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        
        if not rows:
            return "查詢結果為空"
        # 轉成可讀格式
        result = [dict(row) for row in rows]
        return str(result[:10])  # 限制筆數
    except sqlite3.Error as e:
        return f"資料庫錯誤：{str(e)}"
```

### 2.3 注意事項

-  production 環境應限制可執行的 SQL 類型，避免寫入或危險指令
- 透過 volume 掛載資料庫檔案路徑

---

## 三、整合 ChromaDB

### 3.1 新增依賴

```
mcp
requests
chromadb
```

### 3.2 範例：向量搜尋

```python
import chromadb

@mcp.tool()
def query_chromadb(query: str, collection_name: str = "knowledge") -> str:
    """在 ChromaDB 知識庫中搜尋與查詢最相關的內容。"""
    try:
        client = chromadb.PersistentClient(path="/data/chroma")
        collection = client.get_or_create_collection(collection_name)
        results = collection.query(
            query_texts=[query],
            n_results=5
        )
        if not results or not results["documents"]:
            return "未找到相關內容"
        docs = results["documents"][0]
        return "\n---\n".join(docs)
    except Exception as e:
        return f"查詢失敗：{str(e)}"
```

### 3.3 說明

- ChromaDB 使用向量相似度搜尋，適合 semantic search
- 需事先建立 collection 並插入 embedding 後的文件

---

## 四、RAG 整合概念

| 步驟 | 說明 |
|------|------|
| 1. 建立知識庫 | 將文件 chunk、embedding 後存入 ChromaDB |
| 2. MCP 工具 | 提供 `query_knowledge_base(keyword)` 給 LLM 呼叫 |
| 3. LLM 整合 | 使用者提問 → LLM 決定呼叫工具 → 取得檢索結果 → 生成回答 |

MCP 在此扮演「讓 LLM 能存取外部資料」的橋樑。

---

## 五、驗證與練習

完成後在 Open-WebUI 測試：

- 「從知識庫找關於信用卡的資訊」
- 「查詢資料庫中有哪些產品」

### 練習題

1. 使用 Open-WebUI 的 RAG 檔案上傳功能，建立知識庫，再透過 MCP 查詢。
2. 設計 `search_products(keyword: str)` 工具，查詢 SQLite 產品表。
3. 結合 ChromaDB 與 LLM，實作「先檢索、再生成」的 RAG 流程。

---

## 六、整合 mcpo 部署

本階段使用 `chromadb`，mcpo 映像需額外安裝，並掛載資料目錄。

### 6.1 mcpo/Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir mcpo mcp requests chromadb
EXPOSE 8000
```

### 6.2 docker-compose.yml 新增服務

```yaml
mcpo-custom:
  build: ./mcpo
  container_name: mcpo-custom
  restart: always
  networks:
    - webui-net
  ports:
    - "8003:8000"
  command: >
    mcpo --port 8000 --
    python /custom/server.py
  volumes:
    - ./mcp-custom:/custom
    - ./mcp-custom/data:/data
```

- `./mcp-custom:/custom`：掛載程式碼
- `./mcp-custom/data:/data`：掛載 SQLite／ChromaDB 資料，`server.py` 中的 `db_path`、`chromadb path` 需對應 `/data`

### 6.3 啟動與連線

```bash
docker compose up -d --build
```

**Open-WebUI 設定**：管理員控制台 → 設定 → 外部工具 → 新增 `http://mcpo-custom:8000`

> 完整說明與常見問題請參考 [自訂MCP_04_整合mcpo部署](./自訂MCP_04_整合mcpo部署.md)。

---

上一篇：[自訂MCP_02_呼叫外部API](./自訂MCP_02_呼叫外部API.md)  
下一篇：[自訂MCP_04_整合mcpo部署](./自訂MCP_04_整合mcpo部署.md)
