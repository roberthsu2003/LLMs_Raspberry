# test_tools.py - 直接呼叫工具函式測試（不透過 MCP 層）
from server import add, hello

print(add(3, 5))        # 應輸出 8
print(hello("小明"))    # 應輸出 Hello 小明, 這是自訂 MCP Server
