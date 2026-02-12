# 自訂 MCP Server（二）：呼叫外部 API

## 📋 目錄

- [前言](#前言)
- [一、新增依賴](#一新增依賴)
- [二、天氣查詢工具](#二天氣查詢工具)
- [三、股票查詢工具](#三股票查詢工具)
- [四、錯誤處理](#四錯誤處理)
- [五、API Key 管理](#五api-key-管理)
- [六、驗證與練習](#六驗證與練習)

---

## 前言

本階段目標：讓 MCP 工具呼叫**外部 API**，取得即時資料。

學習重點：

- 使用 `requests` 呼叫 HTTP API
- 錯誤處理與逾時設定
- API Key 的環境變數管理

---

## 一、新增依賴

更新 `requirements.txt`：

```
mcp
requests
```

---

## 二、天氣查詢工具

### 2.1 範例：Open-Meteo API（免 API Key）

```python
import requests

@mcp.tool()
def get_weather(city: str) -> str:
    """查詢指定城市的天氣概況。"""
    # Open-Meteo 免費 API，台北座標
    coords = {
        "台北": (25.0330, 121.5654),
        "高雄": (22.6273, 120.3014),
        "台中": (24.1477, 120.6736),
    }
    if city not in coords:
        return f"不支援的城市：{city}"
    
    lat, lon = coords[city]
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        current = data.get("current_weather", {})
        temp = current.get("temperature", "N/A")
        desc = current.get("weathercode", 0)
        return f"{city}目前氣溫約 {temp}°C，天氣代碼 {desc}"
    except requests.RequestException as e:
        return f"查詢失敗：{str(e)}"
```

### 2.2 說明

- `timeout=10`：避免長時間等待
- `resp.raise_for_status()`：HTTP 錯誤時拋出例外
- 將例外轉成字串回傳，避免 MCP 呼叫失敗

---

## 三、股票查詢工具

若使用需 API Key 的服務（例如 Yahoo Finance、Twelve Data），可先以模擬回傳練習：

```python
@mcp.tool()
def get_stock(symbol: str) -> str:
    """查詢股票代號的即時價格（範例：TSM、2330）。"""
    # 實際串接請使用 yfinance、twelve_data 等
    mock_prices = {"TSM": 150.5, "2330": 580.0}
    if symbol in mock_prices:
        return f"{symbol} 模擬價格：{mock_prices[symbol]}"
    return f"未找到 {symbol} 的價格資料"
```

---

## 四、錯誤處理

建議模式：

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

Tool 應盡量回傳有意義的字串，而非拋出例外，讓 LLM 能向使用者說明狀況。

---

## 五、API Key 管理

### 5.1 使用環境變數

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

### 5.2 Docker 環境

在 docker-compose 中傳入：

```yaml
mcpo-custom:
  environment:
    - WEATHER_API_KEY=${WEATHER_API_KEY}
```

---

## 六、驗證與練習

完成後在 Open-WebUI 測試：

- 「台北明天天氣如何？」
- 「查詢台積電（TSM）股價」

### 練習題

1. 串接真實天氣 API（如 Open-Meteo 或 weatherapi.com）。
2. 使用 `yfinance` 套件查詢真實股價。
3. 新增 `get_exchange_rate(from_curr: str, to_curr: str)` 查詢匯率。

---

上一篇：[自訂MCP_01_第一個自訂工具](./自訂MCP_01_第一個自訂工具.md)  
下一篇：[自訂MCP_03_整合資料庫](./自訂MCP_03_整合資料庫.md)
