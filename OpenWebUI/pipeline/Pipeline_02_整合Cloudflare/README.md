# Pipeline（第 2 章）：整合 Cloudflare

## 📋 目錄

- [範例檔](#範例檔)
- [架構說明](#架構說明)
- [啟動與連線](#啟動與連線)
- [Open-WebUI 設定](#open-webui-設定)

---

## 範例檔

本範例完整檔案位於 [範例檔](./範例檔/) 資料夾：

```
範例檔/
├── docker-compose.yml
└── .env
```

| 檔案 | 說明 |
|------|------|
| [docker-compose.yml](./範例檔/docker-compose.yml) | 整合 open-webui、pipelines、cloudflared |
| [.env](./範例檔/.env) | Cloudflare Tunnel token |

---

## 架構說明

| 服務 | 說明 |
|------|------|
| open-webui | Open WebUI 介面，port 8080 |
| pipelines | Pipeline Server，port 9099 |
| cloudflared | Cloudflare Tunnel，對外曝光 |

---

## 啟動與連線

### 前置條件

- 已建立 `open-webui` volume：`docker volume create open-webui`
- 已取得 Cloudflare Tunnel token，填入 `.env` 的 `CLOUDFLARE_TOKEN`

### 啟動

```bash
cd 範例檔
docker compose up -d
```

---

## Open-WebUI 設定

1. 前往 **Settings → Connections → OpenAI API**
2. 新增連線
3. **API URL：** `http://pipelines:9099`（同一 Docker 網路內用容器名稱）
4. **API key：** `0p3n-w3bu!`

---

上一篇：[Pipeline_01_第一個Pipeline](../Pipeline_01_第一個Pipeline/README.md)  
下一篇：[Pipeline_03_程式碼實作](../Pipeline_03_程式碼實作/README.md)
