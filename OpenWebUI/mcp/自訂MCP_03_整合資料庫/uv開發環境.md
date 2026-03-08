# uv 開發環境

本文件說明如何使用 **uv** 為本範例建立獨立的 Python 虛擬環境，進行本機開發與測試。

---

## 什麼是 uv？

**uv** 是由 Astral 開發的快速 Python 套件管理工具（以 Rust 撰寫），可取代 pip 與 venv，安裝與建立環境速度顯著較快。

---

## 安裝 uv

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 驗證安裝

```bash
uv --version
```

---

## 建立開發環境

### 1. 進入範例目錄

```bash
cd 自訂MCP_03_整合資料庫/範例檔/mcpo-custom
```

### 2. 建立虛擬環境

```bash
uv venv
```

會在當前目錄建立 `.venv/` 資料夾。

### 3. 安裝依賴

```bash
uv pip install -r requirements.txt
```

### 4. 啟動虛擬環境

**macOS / Linux：**

```bash
source .venv/bin/activate
```

**Windows (PowerShell)：**

```powershell
.venv\Scripts\activate
```

### 5. 驗證

本範例需連接 PostgreSQL。若 PostgreSQL 在遠端（如樹莓派），請先設定 `DATABASE_URI`：

```bash
export DATABASE_URI="postgresql://pi:raspberry@<樹莓派IP>:5432/mydb"
python test_tools.py
```

或使用 Docker 啟動 postgres 後，在容器內測試：

```bash
cd 範例檔
docker compose up -d postgres
docker compose run --rm postgres-mcp python test_tools.py
```

---

## 目錄結構（含 .venv）

```
mcpo-custom/
├── .venv/           # uv 建立的虛擬環境（建議加入 .gitignore）
├── Dockerfile
├── requirements.txt
├── server.py
└── test_tools.py
```

> **建議：** 將 `.venv/` 加入 `.gitignore`，避免將虛擬環境提交至版控。

---

## 與 Docker 的關係

- **uv 虛擬環境**：用於**本機開發**，需能連線至 PostgreSQL
- **Docker**：用於**部署與整合**，postgres-mcp 與 postgres 在同一網路，透過 `DATABASE_URI` 連線

兩者互不衝突，可依需求選擇本機開發或 Docker 部署。
