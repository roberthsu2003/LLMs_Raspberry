# 自訂 MCP Server（三）：整合資料庫

## 📋 目錄

- [範例檔](#範例檔)
- [前言](#前言)
- [一、核心概念](#一核心概念)
- [二、實作範例：COVID-19 資料查詢](#二實作範例covid-19-資料查詢)
- [三、整合 PostgreSQL](#三整合-postgresql)
- [uv 開發環境](#uv-開發環境)
- [四、驗證與測試](#四驗證與測試)
- [Debug 與測試](#debug-與測試)
- [五、整合 mcpo 部署](#五整合-mcpo-部署)
- [六、延伸閱讀](#六延伸閱讀)

---

## 範例檔

本範例完整檔案位於 [範例檔](./範例檔/) 資料夾，**架構與主專案一致**。此範例整合自 [7.mcpo-sql](../7.mcpo-sql/) 的內容，並統一為與 MCP_01、MCP_02 相同的目錄結構。

```
範例檔/
├── docker-compose.yml
├── .env
└── mcpo-custom/
    ├── Dockerfile
    ├── requirements.txt
    ├── server.py
    └── test_tools.py
```

| 檔案 | 說明 |
|------|------|
| [docker-compose.yml](./範例檔/docker-compose.yml) | 整合 open-webui、postgres、postgres-mcp、cloudflared |
| [mcpo-custom/requirements.txt](./範例檔/mcpo-custom/requirements.txt) | Python 依賴（mcp、mcpo、psycopg2-binary） |
| [mcpo-custom/server.py](./範例檔/mcpo-custom/server.py) | MCP Server 主程式（COVID-19 查詢工具） |
| [mcpo-custom/Dockerfile](./範例檔/mcpo-custom/Dockerfile) | mcpo 部署用映像 |
| [mcpo-custom/test_tools.py](./範例檔/mcpo-custom/test_tools.py) | 本機測試腳本 |

> 可直接複製 `範例檔/` 至你的 `Docker_compose快速部署open-webui/` 專案，或將 `mcpo-custom/` 與 `docker-compose.yml` 合併至既有專案。**注意：** 需先建立 `world` 資料表並匯入 COVID-19 資料。

---

## 前言

本階段目標：讓 MCP 工具存取**資料庫**，實現 LLM 與既有資料的橋接。

學習重點：

- MCP = LLM 與外部世界的橋樑
- PostgreSQL 查詢工具實作
- FastMCP + MCPO 整合部署

---

## 一、核心概念

```
使用者：「查詢台灣的 COVID-19 疫情數據」
    │
    ▼
Open-WebUI + LLM 判斷需呼叫 MCP 工具
    │
    ▼
MCP Tool：get_covid_by_country("台灣")
    │
    ▼
PostgreSQL 查詢 world 資料表
    │
    ▼
回傳結果給 LLM → 整理後回覆使用者
```

---

## 二、實作範例：COVID-19 資料查詢

### 2.1 專案結構

```
範例檔/
├── docker-compose.yml    # 整合 open-webui、postgres、postgres-mcp、cloudflared
└── mcpo-custom/
    ├── Dockerfile        # 建置 MCPO + 自訂 tools
    ├── requirements.txt  # mcp, mcpo, psycopg2-binary
    ├── server.py        # MCP 工具（查詢 COVID-19 資料）
    └── test_tools.py    # 測試腳本
```

### 2.2 資料表結構（world）

| 欄位名稱 | 說明 |
|---------|------|
| 國家 | 國家/地區名稱 |
| 日期 | 資料日期 |
| 總確診數 | 累計確診人數 |
| 總死亡數 | 累計死亡人數 |
| 解除隔離數 | 康復人數 |

> 若你的資料表欄位不同，可執行 `python test_tools.py --schema-only` 取得實際欄位清單，並更新 `server.py` 的 `SCHEMA` 設定。

### 2.3 MCP 工具一覽

| 工具名稱 | 功能 |
|---------|------|
| `get_covid_by_country` | 查詢指定國家的疫情數據（依日期由新到舊） |
| `get_covid_by_date` | 查詢指定日期的全球疫情摘要（前 20 國） |
| `get_top_countries` | 查詢確診或死亡數最高的國家 |
| `get_covid_summary` | 取得資料庫整體摘要 |
| `list_table_columns` | 列出資料表欄位（除錯用） |

### 2.4 關鍵程式碼說明

**連線設定**（使用環境變數 `DATABASE_URI`）：

```python
def get_connection():
    uri = os.environ.get(
        "DATABASE_URI",
        "postgresql://pi:raspberry@10.170.1.218:5432/mydb",
    )
    return psycopg2.connect(uri)
```

**繁體中文欄位**：PostgreSQL 識別符需加雙引號：

```python
def _q(name: str) -> str:
    """PostgreSQL 識別符加雙引號（繁體中文欄位必須）"""
    return f'"{name}"'
```

**工具註冊**：使用 `@mcp.tool()` 裝飾器：

```python
@mcp.tool()
def get_covid_by_country(country_name: str, limit: int = 10) -> str:
    """
    查詢指定國家或地區的 COVID-19 疫情數據，依日期由新到舊排序。
    參數 country_name: 國家/地區名稱（如 台灣、美國、日本）
    參數 limit: 回傳筆數，預設 10
    """
    # ... 查詢邏輯
```

---

## 三、整合 PostgreSQL

### 3.1 為何需要 Volume？

若只建立 container 而**沒有掛載 volume**，資料會存在 container 裡，刪除 container 後資料會遺失。

若希望：

- container 刪掉後資料還在
- 清楚管理資料目錄

就需要加上 `-v` 參數掛載 volume。

---

### 3.2 方法一：使用「命名 Volume」（建議）

```bash
docker run \
  --name my-postgres \
  -e POSTGRES_USER=pi \
  -e POSTGRES_PASSWORD=raspberry \
  -e POSTGRES_DB=mydb \
  -p 5432:5432 \
  -v my-postgres-data:/var/lib/postgresql/data \
  -d postgres
```

| 參數 | 說明 |
|------|------|
| `-v my-postgres-data:/var/lib/postgresql/data` | 建立命名 volume，對應 PostgreSQL 官方 image 的資料目錄 |
| `/var/lib/postgresql/data` | PostgreSQL 官方 image 的預設資料目錄 |

Docker 會自動建立 `my-postgres-data` 這個 volume。

---

### 3.3 方法二：綁定本機資料夾（Bind Mount）

若資料直接存在本機資料夾：

```bash
docker run \
  --name my-postgres \
  -e POSTGRES_PASSWORD=raspberry \
  -p 5432:5432 \
  -v $(pwd)/pgdata:/var/lib/postgresql/data \
  -d postgres
```

或指定絕對路徑：

```bash
-v /Users/yourname/pgdata:/var/lib/postgresql/data
```

---

### 3.4 教學角度補充

| 類型 | 優點 | 適合情境 |
|------|------|----------|
| Named Volume | Docker 管理、易備份 | 正式環境 |
| Bind Mount | 可直接看到檔案 | 教學 / Debug |

---

### 3.5 使用 docker-compose（範例）

```yaml
services:
  postgres:
    image: postgres
    container_name: postgres
    environment:
      POSTGRES_USER: pi
      POSTGRES_PASSWORD: raspberry
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - my-postgres-data:/var/lib/postgresql/data
    networks:
      - webui-net

volumes:
  my-postgres-data:
```

---

### 3.6 查看 Volume

```bash
docker volume ls
docker volume inspect my-postgres-data
```

---

## uv 開發環境

若使用 **uv** 建立虛擬環境進行本機開發，可參考：[uv 開發環境](./uv開發環境.md)

該文件包含：uv 安裝、建立 `.venv`、安裝依賴、PostgreSQL 連線設定等完整步驟。

---

## 四、驗證與測試

除錯與測試方式（Docker 內測試、本機測試、mcpo + Swagger UI）請參考：[Debug 與測試](./Debug與測試.md)

### 4.1 在 Docker 內測試（推薦）

```bash
cd 範例檔
docker compose up -d postgres
docker compose run --rm postgres-mcp python test_tools.py
```

### 4.2 僅檢查資料表欄位

若需確認 `world` 資料表實際欄位，以更新 `SCHEMA`：

```bash
docker compose run --rm postgres-mcp python test_tools.py --schema-only
```

### 4.3 本機測試（PostgreSQL 在遠端）

若 PostgreSQL 在樹莓派或其他主機：

```bash
DATABASE_URI=postgresql://pi:raspberry@<樹莓派IP>:5432/mydb python 範例檔/mcpo-custom/test_tools.py
```

---

## 五、整合 mcpo 部署

將自訂 MCP Server 整合至 Docker 環境，專案結構請參考上方 [範例檔](#範例檔)。`docker-compose.yml` 包含：

| 服務 | 說明 |
|------|------|
| open-webui | Open WebUI 介面 |
| postgres | PostgreSQL 資料庫 |
| postgres-mcp | MCP Server（COVID-19 查詢工具） |
| cloudflared | Cloudflare Tunnel（可選） |

MCP Server 透過 `DATABASE_URI` 連線至同一網路內的 `postgres` 服務。

**啟動與連線：**

```bash
cd 範例檔
docker compose up -d --build
```

**Open-WebUI 設定**：管理員控制台 → 設定 → 外部工具 → 新增 `http://postgres-mcp:8000`

詳細 MCPO 設定與 Open WebUI 連線方式，請參考 [自訂MCP_04_整合mcpo部署](../自訂MCP_04_整合mcpo部署/README.md)。

---

## 從 7.mcpo-sql 遷移

若你先前使用 [7.mcpo-sql](../7.mcpo-sql/) 的結構，可依下表對應遷移：

| 7.mcpo-sql | 自訂MCP_03 範例檔 |
|------------|-------------------|
| `mcpo/tools.py` | `mcpo-custom/server.py` |
| `mcpo/tools_test.py` | `mcpo-custom/test_tools.py` |
| `mcpo/` 目錄 | `mcpo-custom/` 目錄 |
| `build: ./mcpo` | `build: ./mcpo-custom` |
| port 8001 | port 8002（避免與 MCP_02 衝突） |

**PostgreSQL volume 路徑**：7.mcpo-sql 若使用 `/var/lib/postgresql`，請改為 `/var/lib/postgresql/data`（PostgreSQL 官方 image 的正確資料目錄）。

---

## 六、延伸閱讀

- [PostgreSQL 官方文件](https://www.postgresql.org/docs/)
- [FastMCP 文件](https://github.com/jlowin/fastmcp)
- [MCPO 部署說明](../自訂MCP_04_整合mcpo部署/README.md)

---

上一篇：[自訂MCP_02_呼叫外部API](../自訂MCP_02_呼叫外部API/README.md)  
下一篇：[自訂MCP_04_整合mcpo部署](../自訂MCP_04_整合mcpo部署/README.md)
