# test_tools.py - 直接呼叫工具函式測試（不透過 MCP 層）
from server import get_weather

print(get_weather("台北"))   # 應輸出台北目前氣溫約 XX°C,天氣代碼 XX
print(get_weather("高雄"))   # 應輸出高雄目前氣溫約 XX°C,天氣代碼 XX
