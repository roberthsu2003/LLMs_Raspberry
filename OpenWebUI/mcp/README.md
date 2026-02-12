# MCP

## 名詞解釋：什麼是「MCP」？

MCP 是一種協定（Model Context Protocol）。
它是一種用於在模型和外部工具之間傳遞上下文的協定。

---

## 目錄

### 第一篇：使用現有 MCP（環境建置與入門）

- [open-webui如何使用MCP](./open-webui如何使用MCP.md)
- [使用Dockerfile建立MCPO](./使用Dockerfile建立MCPO.md)
- [使用docker_compose整合Dockerfile](./使用docker_compose整合Dockerfile.md)
- [整合使用open-webui和cloudflare tunnel](./整合使用open-webui和cloudflare_tunnel.md)
- [同時安裝多個MCP Server](./同時安裝多個MCP_Server.md)

### 第二篇：自訂 MCP Server（由淺至深）

| 階段 | 主題 | 說明 |
|------|------|------|
| 1 | [撰寫第一個自訂工具](./自訂MCP_01_第一個自訂工具.md) | FastMCP 入門、`hello`、`add` 等靜態工具 |
| 2 | [呼叫外部 API](./自訂MCP_02_呼叫外部API.md) | `get_weather`、`get_stock`、錯誤處理、API Key 管理 |
| 3 | [整合資料庫](./自訂MCP_03_整合資料庫.md) | ChromaDB、SQLite 查詢，RAG 整合概念 |
| 4 | [整合 mcpo 部署](./自訂MCP_04_整合mcpo部署.md) | docker-compose 設定、volume 掛載、Open-WebUI 連線驗證 |

> 原有總覽：[建立自訂的MCP Server](./建立自訂的MCP_Server.md)


