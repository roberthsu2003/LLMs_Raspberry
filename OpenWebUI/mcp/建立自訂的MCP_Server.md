# 建立自訂的MCP Server

這一步才是你課程真正有價值的地方：

> 不只是「使用」MCP

> 而是「自己做一個 MCP Server」

我幫你設計一個**標準教學架構**，可以直接放進你現在的 Open-WebUI + Docker 環境。

---

# **🎯 一、整體架構**

假設我們要做一個：

👉 自訂 MCP Server：mcp-custom

例如功能：

- get_time
- get_weather
- get_stock

架構會變成：

```other
Open-WebUI
   ├── mcpo-time
   ├── mcpo-weather
   └── mcpo-custom   ← 你自己寫的
```

---

# **🧱 二、專案目錄建議**

建議目錄：

```other
project-root/
│
├── docker-compose.yml
│
├── mcpo/                 # 共用 mcpo image
│   └── Dockerfile
│
└── mcp-custom/
    ├── Dockerfile
    ├── requirements.txt
    └── server.py
```

---

# **🧠 三、自訂 MCP Server（server.py 範例）**

這是最小可用版本（stdio 模式）：

```other
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Custom Tools")

@mcp.tool()
def hello(name: str) -> str:
    return f"Hello {name}, 這是自訂 MCP Server"

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    mcp.run()
```

這會自動：

- 註冊 tool schema
- 支援 stdio transport

---

# **📦 四、mcp-custom/Dockerfile**

```other
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

CMD ["python", "server.py"]
```

---

# **📦 五、requirements.txt**

```other
mcp
```

如果你要呼叫外部 API：

```other
mcp
requests
```

---

# **🧱 六、docker-compose.yml 加入自訂 MCP**

加入一個 service：

```other
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
```

---

# **🔥 重要說明**

這行：

```other
mcpo --port 8000 -- python /custom/server.py
```

代表：

mcpo 啟動

→ 用 stdio 模式

→ 啟動你自己寫的 MCP server

---

# **🚀 啟動**

```other
docker compose up --build -d
```

測試：

```other
http://localhost:8003/docs
```

---

# **🔗 Open-WebUI 設定**

新增 MCP Provider：

```other
http://mcpo-custom:8000
```

然後測試：

> 請幫我用工具加總 3 + 5

---

# **🧠 教學升級方向（你會很適合教這個）**

你可以分三階段教：

### **第一階段：靜態工具**

- hello
- add

### **第二階段：外部 API 工具**

- weather
- 股票

### **第三階段：資料庫工具**

- 查詢 ChromaDB
- 查詢 SQLite

這時學生會真正理解：

> MCP = LLM 與外部世界的橋樑

---

# **🏗 七、如果你想更專業（正式部署版）**

正式環境會改成：

```other
mcp.run(transport="http")
```

然後：

```other
mcpo 不需要
```

因為你自己的 MCP server 就直接開 HTTP。

但教學我建議：

👉 先 stdio + mcpo

👉 再教 HTTP transport

這樣理解層次會很清楚。

---

# **🎯 最終總結**

如果你要自訂 MCP Server：

✔ 寫 server.py

✔ Dockerfile 安裝 mcp

✔ docker-compose 用 mcpo 啟動

✔ Open-WebUI 加 provider

架構不變，只是多一個 container。

---

如果你願意，我可以幫你設計一個：

🧩「完整 6 小時 MCP Server 開發章節」

包含練習題、錯誤排除、架構圖

這會非常適合你的課程。