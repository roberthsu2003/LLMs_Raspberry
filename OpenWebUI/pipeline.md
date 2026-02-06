# OpenWebUI Pipeline 完整教學指南

## 📋 目錄
- [什麼是 Pipeline](#什麼是-pipeline)
- [快速開始：使用 Docker Run](#快速開始使用-docker-run)
- [進階部署：使用 Docker Compose](#進階部署使用-docker-compose)
- [在 OpenWebUI 中連接 Pipelines](#在-openwebui-中連接-pipelines)
- [管理與啟用 Pipeline](#管理與啟用-pipeline)
- [重要觀念釐清](#重要觀念釐清)
- [專案結構建議](#專案結構建議)

---

## 什麼是 Pipeline

**Pipeline** 是一個**模組化、自訂的工作流程框架**，讓你可以把流程拆成步驟，擴展自訂邏輯，例如：

- ✅ 自訂函數、外部 API 調用
- ✅ 自訂訊息過濾器（例如內容過濾）
- ✅ 整合 RAG、Langfuse、搜尋工具等
- ✅ 利用 Python 庫做更複雜的處理流程

Pipeline 會提供一個 **OpenAI 相容的 API server**，所以 Open-WebUI 可以將它當成一個 API 來源來使用。

---

## 快速開始：使用 Docker Run

### 步驟 1：拉取 Pipelines 映像

```bash
docker pull ghcr.io/open-webui/pipelines:main
```

這是官方提供的 Pipeline 伺服器映像，可以直接啟動一個 OpenAI 規格的 API server。

### 步驟 2：啟動 Pipeline Docker 容器

#### 方式 A：使用 Named Volume（適合正式部署）

```bash
docker run -d -p 9099:9099 \
  --add-host=host.docker.internal:host-gateway \
  -v pipelines:/app/pipelines \
  --name pipelines \
  --restart always \
  ghcr.io/open-webui/pipelines:main
```

**說明：**
- `-p 9099:9099`：將本機 9099 埠暴露出來做 API 存取
- `--add-host=host.docker.internal:host-gateway`：允許容器訪問主機服務
- `-v pipelines:/app/pipelines`：使用 named volume 存放 pipeline 設定與程式碼
- `--restart always`：容器自動重啟

#### 方式 B：使用 Bind Mount（適合教學與開發）

```bash
# 先建立 pipelines 目錄
mkdir -p pipelines

# 啟動容器
docker run -d -p 9099:9099 \
  --add-host=host.docker.internal:host-gateway \
  -v $(pwd)/pipelines:/app/pipelines \
  --name pipelines \
  --restart always \
  ghcr.io/open-webui/pipelines:main
```

**優點：**
- ✅ 可以直接用編輯器修改 pipeline 程式碼
- ✅ 適合教學與開發階段
- ✅ 樹莓派上更容易 debug

---

## 進階部署：使用 Docker Compose

### 專案結構建議

```
project/
├── docker-compose.yml
├── Dockerfile          # 如果需要自訂 Python 套件
└── pipelines/
    ├── my_pipeline.py
    └── requirements.txt
```

### Dockerfile（如果需要安裝額外的 Python 套件）

```dockerfile
FROM ghcr.io/open-webui/pipelines:main

# 複製 requirements.txt 並安裝套件
COPY pipelines/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
```

**重要觀念：**
- Python 套件是裝在 **Docker image 裡**，不是放在 pipelines volume
- pipelines 資料夾只存放**你的程式碼**（如 `my_pipeline.py`）

### docker-compose.yml

```yaml
version: '3.8'

services:
  pipelines:
    # 如果有 Dockerfile，使用 build
    build: .
    # 或直接使用官方映像
    # image: ghcr.io/open-webui/pipelines:main
    
    ports:
      - "9099:9099"
    
    volumes:
      # 使用 bind mount，方便開發與教學
      - ./pipelines:/app/pipelines
    
    extra_hosts:
      - "host.docker.internal:host-gateway"
    
    restart: always
    
    container_name: pipelines
```

### 啟動服務

```bash
# 建立並啟動服務
docker compose up -d --build

# 查看日誌
docker compose logs -f pipelines

# 停止服務
docker compose down
```

---

## 在 OpenWebUI 中連接 Pipelines

### 步驟 1：登入 Open-WebUI 後台

開啟瀏覽器，前往 Open-WebUI 介面（例如 `http://localhost:3000`）

### 步驟 2：設定連線

1. 前往 **Settings → Connections → OpenAI API**
2. 新增一個連線，設定如下：
   - **API URL:**
     - 如果 Open-WebUI 與 Pipelines 都在 Docker 裡：`http://host.docker.internal:9099`
     - 如果 Open-WebUI 在 Docker，Pipelines 在主機：`http://host.docker.internal:9099`
     - 如果都在主機上：`http://localhost:9099`
   - **API key:** `0p3n-w3bu!`（預設金鑰，可自訂）
3. 儲存設定

### 步驟 3：驗證連線

若成功連線，Open-WebUI 會在 API Base URL 欄位顯示一個 **Pipelines 標識**。

---

## 管理與啟用 Pipeline

連線設定完成後，可以在 Open-WebUI 介面中：

1. 前往 **Settings → Pipelines** 頁籤
2. 查看已安裝的 pipelines
3. 安裝或上傳你自己的 pipeline 程式
   - 可以從 GitHub URL 安裝範例 pipeline
   - 也可以直接上傳 Python 檔案

---

## 重要觀念釐清

### Volume vs Python 環境

| **項目** | **正確位置** | **說明** |
|---------|------------|---------|
| `my_pipeline.py` | `/app/pipelines`（volume） | 你的程式碼檔案 |
| `requirements.txt` | Image build 階段 | 套件清單檔案 |
| `pip install pandas` | Dockerfile | 套件安裝指令 |
| Python runtime | Container image | Python 執行環境 |

**關鍵觀念：**
- 🔴 **pipelines volume 裡放的是「你的程式」**
- 🔴 **Python 套件是「裝在容器 image 裡」**
- 🔴 **Volume ≠ Python 環境**

### Named Volume vs Bind Mount

#### Named Volume（適合正式部署）

**優點：**
- ✅ 資料由 Docker 管理，更安全
- ✅ 適合正式部署環境
- ✅ Pipeline 程式不常修改時使用

**缺點：**
- ❌ 不適合教學與開發
- ❌ 需要進入容器才能修改檔案
- ❌ 樹莓派上 debug 較困難

**實體路徑：**
```bash
/var/lib/docker/volumes/pipelines/_data
```

#### Bind Mount（適合教學與開發）

**優點：**
- ✅ 可以直接用編輯器修改程式碼
- ✅ 適合教學與開發階段
- ✅ 樹莓派上更容易 debug
- ✅ 檔案修改立即生效

**缺點：**
- ❌ 需要確保主機路徑存在
- ❌ 權限設定需要注意

**使用方式：**
```bash
-v $(pwd)/pipelines:/app/pipelines
```

---

## 專案結構建議

### 完整的教學專案結構

```
project/
├── docker-compose.yml          # Docker Compose 設定
├── Dockerfile                  # 自訂映像（如需安裝套件）
├── README.md                   # 專案說明
└── pipelines/
    ├── requirements.txt        # Python 套件清單
    ├── my_pipeline.py          # 你的 Pipeline 程式
    └── examples/               # 範例程式
        └── example_pipeline.py
```

### requirements.txt 範例

```txt
pandas
numpy
requests
chromadb
```

### Pipeline 程式範例

```python
# pipelines/my_pipeline.py
from typing import Dict, Any

def process_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    處理訊息的 Pipeline 函數
    """
    # 你的自訂邏輯
    processed = message.copy()
    processed['processed'] = True
    return processed
```

---

## 常見問題

### Q1: Pipeline reload 要不要重啟容器？

**A:** 通常不需要。Pipeline 伺服器會自動偵測檔案變更並重新載入。如果沒有自動載入，可以重啟容器：

```bash
docker compose restart pipelines
```

### Q2: Python 檔改了，需不需要 rebuild？

**A:** 
- 如果只修改 `pipelines/` 目錄下的 Python 檔案：**不需要 rebuild**
- 如果修改了 `requirements.txt` 或 `Dockerfile`：**需要 rebuild**

```bash
docker compose up -d --build
```

### Q3: 如何確認 Pipeline 是否正常運作？

**A:** 檢查容器日誌：

```bash
docker compose logs -f pipelines
```

或測試 API：

```bash
curl http://localhost:9099/health
```

### Q4: 樹莓派上效能如何？

**A:** 
- Pipeline 伺服器本身資源需求不高
- 建議使用 bind mount 方便 debug
- 如果 Pipeline 需要大量運算，考慮使用外部服務

---

## 教學比喻

> **Docker image** 是「已裝好軟體的電腦」  
> **pipelines 資料夾**是「我每天在改的程式碼」  
> **套件裝在電腦裡，不是丟在程式碼資料夾**

---

## 參考資源

- [Open-WebUI Pipelines GitHub](https://github.com/open-webui/pipelines)
- [Open-WebUI 官方文件](https://docs.openwebui.com/)

---

## 下一步

- 📝 建立你的第一個 Pipeline
- 🔧 整合 RAG 功能
- 🎯 實作自訂訊息過濾器
- 🚀 部署到生產環境
