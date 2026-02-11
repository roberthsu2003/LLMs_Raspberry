# MCP

# **🧠 整體架構原理（從上到下）**

你現在的實際架構是：

```other
瀏覽器
   ↓
Open-WebUI (LLM UI)
   ↓
MCP Client (內建於 WebUI)
   ↓
mcpo (MCP → OpenAPI 轉換器)
   ↓
mcp-server-time
```

我們一層一層解釋。

---

# **第一層：為什麼要 MCP_ENABLE=true？**

Open-WebUI 內部其實有三種能力：

1. 模型連線（OpenAI / Ollama）
2. Pipeline
3. MCP Client

MCP_ENABLE=true 的作用是：

> 啟用 MCP Client 模組

如果沒開：

- UI 不會出現「外部工具」
- WebUI 不會有 MCP 呼叫能力

它只是「打開功能開關」。

---

# **第二層：為什麼要 mcpo？**

MCP 是一種協定（Model Context Protocol）。

但 Open-WebUI 的工具系統是：

> 基於 OpenAPI

兩種格式不同。

所以需要一個「翻譯器」。

mcpo 做的事就是：

```other
MCP 協定
   ↓
轉成 OpenAPI HTTP server
```

所以 WebUI 其實根本不知道 MCP 存在，

它只知道：

> 這是一個 OpenAPI 工具伺服器

---

# **第三層：為什麼 URL 填 http://mcpo:8000？**

因為 Docker bridge network 的原理是：

- 每個 container 都有 DNS 名稱
- service name = hostname

你兩個 container 都在：

```other
webui-net
```

所以：

```other
http://mcpo:8000
```

在 open-webui container 裡面可以直接解析。

這是 Docker 內部 DNS 機制。

---

# **第四層：為什麼不能填 localhost？**

在 container 裡：

```other
localhost = 自己
```

不是宿主機。

所以：

```other
open-webui 裡的 localhost ≠ mcpo
```

這是很多人會卡住的地方。

---

# **第五層：為什麼要選 OpenAPI？**

因為 WebUI 有兩種 server：

| **類型**            | **用途** |
| ----------------- | ------ |
| OpenAI-compatible | LLM    |
| OpenAPI           | Tool   |

mcpo 是工具。

如果你填在 LLM 那邊，

WebUI 會去找：

```other
GET /v1/models
```

當然會錯。

---

# **第六層：為什麼模型會「自己決定」要用工具？**

這是最核心原理。

當模型支援 function calling 時：

1. WebUI 把 OpenAPI schema 傳給模型
2. 模型看到可用工具：
    - get_current_time
    - convert_time
1. 當你問：

「現在台北時間幾點？」

1. 模型判斷：

→ 這需要呼叫工具

1. 模型輸出 tool call
2. WebUI 呼叫 mcpo
3. mcpo 呼叫 mcp-server-time
4. 回傳結果
5. 模型生成自然語言回答

---

# **🔥 真正的核心概念**

你現在完成的不是「接 API」。

你完成的是：

> 讓模型有「外部能力」

這是 Agent 的基礎。

---

# **🎓 用教學角度總結**

你可以這樣教學生：

### **第一步**

模型只能聊天

### **第二步**

模型透過 Tool 可以查時間

### **第三步**

模型透過 MCP 可以接任何外部系統

這是從 LLM → Agent 的過程。

---

# **🧠 最重要的一句話**

Pipeline 是「你寫流程」

MCP 是「模型決定要不要用工具」

兩個哲學完全不同。