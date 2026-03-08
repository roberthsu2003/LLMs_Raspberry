# Debug 與測試

本文件說明自訂 MCP Server（COVID-19 資料庫查詢）的除錯與測試方式。

---

## 建立 Python 的虛擬環境

進行本機測試前，建議先建立虛擬環境以隔離依賴。

### 使用 uv（推薦）

```bash
cd 範例檔/mcpo-custom
uv venv
uv pip install -r requirements.txt
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

> 詳細步驟請參考 [uv 開發環境](./uv開發環境.md)

### 使用 venv + pip

```bash
cd 範例檔/mcpo-custom
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 方法一：在 Docker 內測試（推薦）

PostgreSQL 與 MCP Server 在同一 Docker 網路，連線最簡單：

```bash
cd 範例檔
docker compose up -d postgres
docker compose run --rm postgres-mcp python test_tools.py
```

### 僅檢查資料表欄位

若需確認 `world` 資料表實際欄位，以更新 `SCHEMA`：

```bash
docker compose run --rm postgres-mcp python test_tools.py --schema-only
```

---

## 方法二：本機測試（PostgreSQL 在遠端）

若 PostgreSQL 在樹莓派或其他主機，需設定 `DATABASE_URI`：

```bash
cd 範例檔/mcpo-custom
DATABASE_URI=postgresql://pi:raspberry@<樹莓派IP>:5432/mydb python test_tools.py
```

---

## 方法三：透過 mcpo + Swagger UI

在虛擬環境內使用 mcpo 啟動 MCP Server，透過 Swagger 介面測試：

```bash
cd 範例檔/mcpo-custom
source .venv/bin/activate
DATABASE_URI=postgresql://pi:raspberry@localhost:5432/mydb mcpo --port 8000 -- python server.py
```

用瀏覽器開啟：`http://localhost:8000/docs`，可看到所有 COVID-19 查詢工具並直接呼叫測試。

---

## 常見問題

### 查詢失敗：連線被拒絕

- 確認 PostgreSQL 已啟動（`docker compose up -d postgres` 或本機 postgres 服務）
- 確認 `DATABASE_URI` 的 IP、port、帳密正確

### 查詢失敗：relation "world" does not exist

- 需先建立 `world` 資料表並匯入 COVID-19 資料
- 可執行 `python test_tools.py --schema-only` 檢查現有資料表欄位

### 欄位不符

若 `world` 資料表欄位與 `SCHEMA` 不同，請依 `list_table_columns` 的輸出更新 `server.py` 的 `SCHEMA` 設定。

---

[← 回 README](./README.md)
