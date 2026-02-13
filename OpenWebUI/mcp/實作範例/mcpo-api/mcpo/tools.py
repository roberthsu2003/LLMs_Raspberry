import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Custom Tools")

# Mapping of city to coordinates
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

# Tuple of supported city names for quick reference
CITY_NAMES = tuple(CITY_MAP.keys())


@mcp.tool()
def get_weather(city: str) -> str:
    """
    查詢指定城市的天氣概況。
    參數 `city`：要查詢的城市名稱，應為台灣內部城市之一。
    支援的城市列表可從 `CITY_NAMES` 取得。
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

    return f"Weather for {city}"


if __name__ == "__main__":
    mcp.run()
