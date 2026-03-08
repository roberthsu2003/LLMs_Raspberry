# Pipeline（第 1 章）：第一個 Pipeline

## 📋 目錄

- [範例檔](#範例檔)
- [快速開始：Docker Run](#快速開始docker-run)
- [進階部署：Docker Compose](#進階部署docker-compose)
- [在 Open-WebUI 中連接](#在-open-webui-中連接)
- [管理與啟用 Pipeline](#管理與啟用-pipeline)
- [常見問題](#常見問題)

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
| [docker-compose.yml](./範例檔/docker-compose.yml) | 單一 pipelines 服務，port 9099 |

---

## 快速開始：Docker Run

### 步驟 1：拉取映像

```bash
docker pull ghcr.io/open-webui/pipelines:main
```

### 步驟 2：啟動容器

```bash
docker run -d -p 9099:9099 \
  --add-host=host.docker.internal:host-gateway \
  -v pipelines:/app/pipelines \
  --name pipelines \
  --restart always \
  ghcr.io/open-webui/pipelines:main
```

### 步驟 3：確認運作

```bash
docker ps
curl http://localhost:9099/health
```

---

## 進階部署：Docker Compose

```bash
cd 範例檔
docker compose up -d
```

**參數說明：**

| 參數 | 說明 |
|------|------|
| `-p 9099:9099` | Pipeline API 埠號 |
| `-v pipelines:/app/pipelines` | 存放 pipeline 程式碼的 volume |
| `host.docker.internal:host-gateway` | 讓容器可訪問主機（如 Ollama） |

---

## 在 Open-WebUI 中連接

1. 前往 **Settings → Connections → OpenAI API**
2. 新增連線
3. **API URL：**
   - 都在 Docker：`http://host.docker.internal:9099`
   - 都在本機：`http://localhost:9099`
4. **API key：** `0p3n-w3bu!`（預設）

---

## 管理與啟用 Pipeline

1. 前往 **Settings → Pipelines**
2. 可從 GitHub URL 安裝範例，或上傳 Python 檔案
3. Pipeline 程式碼存放在 `/app/pipelines`，若用 bind mount 可直接修改

---

## 常見問題

### Python 檔改了要不要 rebuild？

- **只改 `pipelines/` 下的 .py 檔：** 不需要，會自動重新載入
- **改 requirements.txt 或 Dockerfile：** 需要 `docker compose up -d --build`

### 如何確認 Pipeline 正常運作？

```bash
curl http://localhost:9099/health
docker logs pipelines
```

---

上一篇：[Pipeline_00_認識Pipeline](../Pipeline_00_認識Pipeline/README.md)  
下一篇：[Pipeline_02_整合Cloudflare](../Pipeline_02_整合Cloudflare/README.md)
