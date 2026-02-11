# 使用Dockerfile建立MCPO的工具伺服器

```other
docker run -d \
  --name mcpo \
  --network webui-net \
  -p 8000:8000 \
  python:3.11 \
  sh -c "pip install --no-cache-dir mcpo mcp-server-time && \
         mcpo --port 8000 -- mcp-server-time --local-timezone=Asia/Taipei"
```

你這段 docker run 指令其實做了三件事：

1. 使用 python:3.11
2. 安裝 mcpo 與 mcp-server-time
3. 啟動 mcpo，並掛載 mcp-server-time

我們把它改成「可重複建置」的 Dockerfile 方式，會更專業，也更適合教學。

---

# **一、改寫成 Dockerfile**

建立一個資料夾，例如：

```other
mcpo-server/
 ├── Dockerfile
```

---

## **Dockerfile 內容**

```other
FROM python:3.11-slim

WORKDIR /app

# 安裝套件
RUN pip install --no-cache-dir mcpo mcp-server-time

# 開放 8000 port
EXPOSE 8000

# 啟動指令
CMD ["mcpo", "--port", "8000", "--", "mcp-server-time", "--local-timezone=Asia/Taipei"]
```

---

# **二、建置 Image**

在該目錄執行：

```other
docker build -t mcpo-server .
```

---

# **三、執行 Container**

```other
docker run -d \
  --name mcpo \
  --network webui-net \
  -p 8000:8000 \
  mcpo-server
```

---

# **四、執行流程說明（教學重點）**

這段流程非常適合你在 MCP 課程中講解「容器啟動流程」👇

---

## **Step 1：Docker 啟動 Container**

Docker 讀取 image：

```other
mcpo-server
```

---

## **Step 2：執行 CMD**

Docker 會執行：

```other
mcpo --port 8000 -- mcp-server-time --local-timezone=Asia/Taipei
```

---

## **Step 3：mcpo 的角色**

mcpo 是一個：

👉 OpenAI-compatible wrapper

👉 把 MCP server 包裝成 REST API

流程是：

```other
HTTP Request
   ↓
mcpo
   ↓
MCP protocol
   ↓
mcp-server-time
   ↓
回傳 JSON
```

---

## **Step 4：Port 對應**

```other
-p 8000:8000
```

代表：

```other
Host:8000  →  Container:8000
```

---

# **五、為什麼 Dockerfile 比 docker run 好？**

| **docker run** | **Dockerfile** |
| -------------- | -------------- |
| 一次性            | 可版本控制          |
| 不可重建           | 可重複建置          |
| 不好教學           | 架構清楚           |
| 不好維護           | 可上傳 GitHub     |

---

# **六、如果你想更專業（進階版）**

可以加上：

```other
ENV TZ=Asia/Taipei
```

或改成：

```other
FROM python:3.11-slim

WORKDIR /app

ENV TZ=Asia/Taipei

RUN pip install --no-cache-dir mcpo mcp-server-time

EXPOSE 8000

ENTRYPOINT ["mcpo"]
CMD ["--port", "8000", "--", "mcp-server-time", "--local-timezone=Asia/Taipei"]
```

這樣可以讓學生理解：

- ENTRYPOINT 是主程式
- CMD 是預設參數

---

# **七、你課程可以這樣講（很有感）**

你現在在教 MCP，這個範例其實可以變成：

> 🔥「如何把一個 MCP Server 變成 OpenAI-compatible API」

然後再接：

- Open-WebUI 連線
- Pipeline Server 連線
- n8n 連線

這會讓學生突然理解：

> MCP ≠ API

> mcpo = 協定轉換器

---

如果你要，我可以幫你畫一張：

```other
Open-WebUI
     ↓
OpenAI API
     ↓
mcpo
     ↓
MCP
     ↓
mcp-server-time
```

這張圖超適合放講義。