# open-webui如何安裝和使用MCP工具

## 📋 目錄

- [🧠 整體架構原理（從上到下）](#-整體架構原理從上到下)
- [第一層：為什麼要 MCP_ENABLE=true？](#第一層為什麼要-mcp_enabletrue)
- [第二層：為什麼要 mcpo？](#第二層為什麼要-mcpo)
- [第三層：為什麼 URL 填 http://mcpo:8000？](#第三層為什麼-url-填-httpmcpo8000)
- [第四層：為什麼模型會「自己決定」要用工具？](#第四層為什麼模型會自己決定要用工具)
- [🔥 真正的核心概念](#-真正的核心概念)

---

## 測試現在的模型

詢問模型現在的時間
```
現在台北時間幾點？
```

模型會回傳：

```

抱歉，作為一個語言模型，我沒有實時的時鐘資訊，無法直接告訴你「現在」台北的精確時間。不過你可以很方便地自己查詢：

1. **手機或電腦**：大部分智慧型手機、筆電或桌機都會自動顯示正確的地理時區時間。只要確認你已設置「台北」或「台灣」的時區（UTC+8），就能看到即時時間。
2. **網路搜尋**：在瀏覽器搜尋「台北現在時間」即可取得正確結果。
3. **手動計算**  
   - 先查到你所在地的時間與時區，例如若你在 **香港（UTC+8）**，則台北的時間與你相同。  
   - 若你在 **紐約（UTC-4）**，台北時間比它快 12 小時；如果你在 **倫敦（UTC+0）**，台北時間比倫敦快 8 小時。  
   - 記得夏令時間（DST）會影響你所在地的時區偏移。

如果你想讓我幫忙計算某個已知時間點在台北的對應時間，歡迎告訴我（例如「2024 年 2 月 10 日 15:30（東京）換算成台北時間是？」）。祝你順利查到正確時間！
```

---

## 透過MCP取得現在的時間

### **🧠 整體架構原理（從上到下）**

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

### **第一層：為什麼要 MCP_ENABLE=true？**

MCP_ENABLE=true 的作用是：

> 啟用 MCP Client 模組

如果沒開：

- UI 不會出現「外部工具」
- WebUI 不會有 MCP 呼叫能力

它只是「打開功能開關」。

**docker compose內的設定必需增加環境變數: MCP_ENABLE=true**

---

### **第二層：為什麼要 mcpo？**

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

### **第三層：為什麼 URL 填 http://mcpo:8000？**

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

### **第四層：為什麼模型會「自己決定」要用工具？**

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

### **🔥 真正的核心概念**

你現在完成的不是「接 API」。

你完成的是：

> 讓模型有「外部能力」

這是 Agent 的基礎。

---