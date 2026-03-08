# 整合 Cloudflare Pipeline

open-webui + pipelines + cloudflared 完整部署範例。

## 檔案結構

```
整合CloudflarePipeline/
├── README.md
├── docker-compose.yml
├── pipelines.yaml      # Pipeline 設定（可選）
└── .env               # CLOUDFLARE_TOKEN
```

## 啟動

```bash
# 確保 open-webui volume 已建立
docker volume create open-webui

# 設定 .env 中的 CLOUDFLARE_TOKEN
# 啟動服務
docker compose up -d
```

## 服務

| 服務 | Port | 說明 |
|------|------|------|
| open-webui | 8080 | Open WebUI 介面 |
| pipelines | 9099 | Pipeline Server |
| cloudflared | - | Cloudflare Tunnel |
