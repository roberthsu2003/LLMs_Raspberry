# 自訂 MCP Server（二）：呼叫外部 API

## 📋 目錄

- [範例檔](#範例檔)
- [前言](#前言)
- [一、核心概念](#一核心概念)
- [二、實作範例：天氣查詢](#二實作範例天氣查詢)
- [三、錯誤處理](#三錯誤處理)
- [四、API Key 管理（選用）](#四api-key-管理選用)
- [uv 開發環境](#uv-開發環境)
- [五、驗證與測試](#五驗證與測試)
- [Debug 與測試](#debug-與測試)
- [六、整合 mcpo 部署](#六整合-mcpo-部署)
- [七、延伸練習](#七延伸練習)

---

## 範例檔

本範例完整檔案位於 [範例檔](./範例檔/) 資料夾，**架構與主專案一致**：

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
| [docker-compose.yml](./範例檔/docker-compose.yml) | 整合 open-webui、mcpo-weather、cloudflared |
| [mcpo-custom/requirements.txt](./範例檔/mcpo-custom/requirements.txt) | Python 依賴（mcp、mcpo、requests） |
| [mcpo-custom/server.py](./範例檔/mcpo-custom/server.py) | MCP Server 主程式（get_weather 天氣查詢工具） |
| [mcpo-custom/Dockerfile](./範例檔/mcpo-custom/Dockerfile) | mcpo 部署用映像 |
| [mcpo-custom/test_tools.py](./範例檔/mcpo-custom/test_tools.py) | 本機測試腳本 |

> 可直接複製 `範例檔/` 至你的 `Docker_compose快速部署open-webui/` 專案，或將 `mcpo-custom/` 與 `docker-compose.yml` 合併至既有專案。

---

## 前言

本階段目標：讓 MCP 工具呼叫**外部 API**，取得即時資料。

學習重點：

- 使用 `requests` 呼叫 HTTP API
- 錯誤處理與逾時設定
- API Key 的環境變數管理（選用）

---

## 一、核心概念

```
使用者：「台北現在天氣如何？」
    │
    ▼
Open-WebUI + LLM 判斷需呼叫 MCP 工具
    │
    ▼
MCP Tool：get_weather("台北")
    │
    ▼
requests.get() → Open-Meteo API
    │
    ▼
回傳結果給 LLM → 整理後回覆使用者
```

---

## 二、實作範例：天氣查詢

### 2.1 專案結構

```
範例檔/
├── docker-compose.yml   # 整合 open-webui、mcpo-weather、cloudflared
└── mcpo-custom/
    ├── Dockerfile       # 建置 MCPO + 自訂 tools
    ├── server.py       # MCP 工具（天氣查詢）
    └── test_tools.py   # 測試腳本
```

### 2.2 使用 Open-Meteo API（免 API Key）

本範例使用 [Open-Meteo](https://open-meteo.com/) 免費天氣 API，無需註冊或 API Key。

### 2.3 完整程式碼（server.py）

```python
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Custom Tools")

# 台灣城市經緯度對照
CITY_MAP = {
    "台北": (25.0330, 121.5654),
    "新北": (25.1124, 121.6062),
    "桃園": (24.9700, 121.5350),
    "台中": (24.1477, 120.6736),
    "台南": (22.9964, 120.2271),
    "高雄": (22.6272, 120.3014),
    "基隆": (25.1141, 121.7181),
    "新竹": (24.8165, 120.9636),
    "嘉義": (23.4789, 120.4605),
    "宜蘭": (24.7019, 121.7817),
    "苗栗": (24.7200, 120.5836),
    "南投": (24.1648, 120.5921),
    "彰化": (24.0401, 120.6423),
    "雲林": (23.5401, 120.5049),
    "嘉義縣": (23.4701, 120.5005),
    "屏東": (22.7931, 120.6511),
    "花蓮": (23.9605, 121.5906),
    "台東": (22.9975, 121.5594),
    "澎湖": (23.3576, 120.4531),
    "金門": (24.4399, 118.5882),
    "連江": (22.7723, 118.2144),
}

CITY_NAMES = tuple(CITY_MAP.keys())


@mcp.tool()
def get_weather(city: str) -> str:
    """
    查詢指定城市的天氣概況。
    參數 city: 要查詢的城市名稱，應為台灣內部城市之一。
    支援城市: 台北, 新北, 桃園, 台中, 台南, 高雄, 基隆, 新竹, 嘉義, 宜蘭, 苗栗, 南投, 彰化, 雲林, 嘉義縣, 屏東, 花蓮, 台東, 澎湖, 金門, 連江
    """
    if city not in CITY_MAP:
        return f"不支援的城市:{city},只支援台灣的城市"

    lat, lon = CITY_MAP[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        weather = data.get("current_weather", {})
        temperature = weather.get("temperature", "N/A")
        desc = weather.get("weathercode", 0)
        return f"{city}目前氣溫約{temperature}°C,天氣代碼{desc}"
    except Exception as e:
        return f"查詢失敗:{e}"


if __name__ == "__main__":
    mcp.run()
```

### 2.4 重點說明

| 項目 | 說明 |
|------|------|
| `timeout=10` | 避免長時間等待，逾時則拋出 `requests.Timeout` |
| `response.raise_for_status()` | HTTP 4xx/5xx 時拋出 `requests.HTTPError` |
| `except Exception` | 將例外轉成字串回傳，避免 MCP 呼叫失敗 |
| `CITY_MAP` | 城市經緯度對照，Open-Meteo 需經緯度查詢 |

> **天氣代碼**：Open-Meteo 的 `weathercode` 對應 WMO 標準（0=晴、1–3=多雲、45/48=霧、51–67=雨等），可依需求擴充為中文描述。

---

## 三、錯誤處理

建議模式：Tool 盡量回傳有意義的字串，而非拋出例外，讓 LLM 能向使用者說明狀況。

```python
try:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # 處理資料...
    return result
except requests.Timeout:
    return "查詢逾時，請稍後再試"
except requests.RequestException as e:
    return f"網路錯誤：{str(e)}"
except (KeyError, ValueError) as e:
    return f"資料解析失敗：{str(e)}"
```

---

## 四、API Key 管理（選用）

若使用需 API Key 的服務（如 weatherapi.com、Twelve Data）：

### 4.1 使用環境變數

```python
import os

API_KEY = os.environ.get("WEATHER_API_KEY", "")

@mcp.tool()
def get_weather_pro(city: str) -> str:
    if not API_KEY:
        return "請設定 WEATHER_API_KEY 環境變數"
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
    # ...
```

### 4.2 Docker 環境

在 docker-compose 中傳入：

```yaml
mcpo-weather:
  environment:
    - WEATHER_API_KEY=${WEATHER_API_KEY}
```

---

## uv 開發環境

若使用 **uv** 建立虛擬環境進行本機開發，可參考：[uv 開發環境](./uv開發環境.md)

該文件包含：uv 安裝、建立 `.venv`、安裝依賴、啟動與驗證等完整步驟。

---

## 五、驗證與測試

四種除錯與測試方式（直接呼叫工具、mcpo + Swagger UI、logging、MCP Client）請參考：[Debug 與測試](./Debug與測試.md)

### 5.1 本機測試

```bash
cd 範例檔/mcpo-custom
pip install -r requirements.txt
python test_tools.py
```

`test_tools.py` 會呼叫 `get_weather(city="台北")` 並印出結果。

### 5.2 在 Open-WebUI 測試

部署完成後，可輸入：

- 「台北現在天氣如何？」
- 「查詢高雄的氣溫」

---

## 六、整合 mcpo 部署

將自訂 MCP Server 整合至 Docker 環境，讓 Open-WebUI 能呼叫。專案結構請參考上方 [範例檔](#範例檔)。

### 6.1 mcpo-custom/Dockerfile

套件從 `requirements.txt` 安裝，映像內不含啟動指令（由 docker-compose 的 `command` 覆寫）：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 8000
```

> **說明：** `requirements.txt` 含 `mcp`（FastMCP）、`mcpo`（HTTP 橋接）與 `requests`（呼叫外部 API），所有依賴統一管理。啟動指令放在 docker-compose 的 `command`，方便之後覆寫或切換不同腳本，無需重建映像。

### 6.2 docker-compose.yml 服務設定

```yaml
mcpo-weather:
  build: ./mcpo-custom
  container_name: mcpo-weather
  restart: always
  networks:
    - webui-net
  ports:
    - "8001:8000"
  command: >
    mcpo --port 8000 --
    python server.py
```

| 項目 | 說明 |
|------|------|
| `build: ./mcpo-custom` | 以 mcpo-custom 目錄建置映像 |
| `8001:8000` | 主機 8001 對應容器 8000 |
| `mcpo --port 8000 -- python server.py` | 啟動 MCPO，並執行自訂 tools |

### 6.3 完整架構（docker-compose.yml）

完整設定請參考 [範例檔/docker-compose.yml](./範例檔/docker-compose.yml)，包含 open-webui、mcpo-weather、cloudflared 服務。

### 6.4 啟動與連線

```bash
cd 範例檔
docker compose up -d --build
```

**Open-WebUI 設定**：管理員控制台 → 設定 → 外部工具 → 新增 `http://mcpo-weather:8000`

> 完整說明與常見問題請參考 [自訂MCP_04_整合mcpo部署](../自訂MCP_04_整合mcpo部署/README.md)。

---

## 七、延伸練習

1. **串接其他天氣 API**：如 weatherapi.com（需 API Key）。
2. **擴充天氣描述**：將 `weathercode` 轉成中文（晴、多雲、雨等）。
3. **新增股票查詢**：使用 `yfinance` 查詢即時股價。
4. **新增匯率查詢**：`get_exchange_rate(from_curr: str, to_curr: str)`。

---

上一篇：[自訂MCP_01_第一個自訂工具](../自訂MCP_01_第一個自訂工具/README.md)  
下一篇：[自訂MCP_03_整合資料庫](../自訂MCP_03_整合資料庫/README.md)
