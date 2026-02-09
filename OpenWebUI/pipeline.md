# OpenWebUI Pipeline 完整教學指南

## 📋 目錄
- [Pipeline Server 章節導入：什麼時候該用？](#pipeline-server-章節導入什麼時候該用)
- [什麼是 Pipeline](#什麼是-pipeline)
- [快速開始：使用 Docker Run](#快速開始使用-docker-run)
- [進階部署：使用 Docker Compose](#進階部署使用-docker-compose)
- [在 OpenWebUI 中連接 Pipelines](#在-openwebui-中連接-pipelines)
- [管理與啟用 Pipeline](#管理與啟用-pipeline)
- [重要觀念釐清](#重要觀念釐清)
- [專案結構建議](#專案結構建議)
- [常見問題](#常見問題)
- [教學比喻](#教學比喻)
- [參考資源](#參考資源)
- [下一步](#下一步)

---

## Pipeline Server 章節導入：什麼時候該用？

### 本章目標

在前面的章節中，你已經學會如何使用 **Open-WebUI 內建的 Filter 與 Tools** 來擴充模型能力。本章要回答一個實務上一定會遇到的問題：

> **什麼情況下，內建 Filter / Tools 已經不夠，我應該改用 Pipeline Server？**

本章不急著寫程式，而是先建立「判斷時機」與「架構視角」，幫助你在對的時候選對工具。

---

### 先給結論：什麼情況需要 Pipeline Server？

如果你遇到下面「任何一種」情況，就非常適合引入 Pipeline Server：

* 🔁 **流程不只一個步驟**，而是多步驟、可重組的處理流程
* 🌐 **需要和 Open-WebUI 以外的系統共用**（API、n8n、後端服務）
* 🧠 **模型前後都要動手腳**（前處理 + 後處理）
* 🧩 **想把 AI 行為做成「一個服務」而不是「一個設定」**

如果你只是在「單一請求 → 單一回應」中加點邏輯，那 Filter / Tools 會更簡單；但只要你開始「設計流程」，Pipeline Server 就會變成主角。

---

### 為什麼 Filter / Tools 會開始不夠用？

#### 1️⃣ Filter：適合「輕量、就地修改」

Filter 非常適合：

* 改 prompt
* 加系統訊息
* 做輸入／輸出的小調整

但它的限制也很明確：

* 執行順序固定
* 不適合複雜狀態管理
* 很難拆成可重用的流程模組

👉 **Filter 的角色是「即時加工」，不是「流程設計」**。

---

#### 2️⃣ Tools：適合「單次能力擴充」

Tools 很適合：

* 查資料
* 呼叫 API
* 做一次明確任務

但當你開始遇到這些需求時，Tools 就會變得卡手：

* 一個回應需要呼叫多個工具
* 工具之間有順序與條件判斷
* 想控制「什麼情況一定要走某個流程」

👉 **Tools 解決的是「會不會做」，不是「怎麼串」**。

---

### Pipeline Server 在做什麼？（一句話版）

> **Pipeline Server = 把「和模型互動的整個流程」獨立成一個 API 服務**

它讓你可以：

* **明確定義：**
  * 輸入怎麼處理
  * prompt 怎麼組
  * 模型怎麼選
  * 輸出怎麼加工
* **把這套邏輯：**
  * 給 Open-WebUI 用
  * 給其他系統用

---

### 教學視角：什麼時候該教學生 Pipeline Server？

在課程設計上，Pipeline Server 非常適合放在：

> **「學生開始想做自己的 AI 服務」的那一刻**

典型的學員轉折點包括：

* 「我不想每個專案都重寫 Filter / Tool」
* 「我想把這個 AI 功能接給別人用」
* 「我想控制整個 AI 行為，而不只是補強模型」

這時候，Pipeline Server 不只是新技術，而是**架構升級**。

---

## 什麼是 Pipeline

**Pipeline** 是一個**模組化、自訂的工作流程框架**，讓你可以把流程拆成步驟，擴展自訂邏輯，例如：

- ✅ 自訂函數、外部 API 調用
- ✅ 自訂訊息過濾器（例如內容過濾）
- ✅ 整合 RAG、Langfuse、搜尋工具等
- ✅ 利用 Python 庫做更複雜的處理流程

Pipeline 會提供一個 **OpenAI 相容的 API server**，所以 Open-WebUI 可以將它當成一個 API 來源來使用。

**與 Filter / Tools 的關係：**

* Pipeline 可以**整合** Filter 和 Tools 的功能
* Pipeline 提供**更完整的流程控制**能力
* Pipeline 讓你的 AI 邏輯**獨立成服務**，可重複使用

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

### Q5: 什麼時候該用 Pipeline，什麼時候用 Filter / Tools？

**A:** 
- **使用 Filter / Tools：** 單一請求的簡單調整、單次能力擴充
- **使用 Pipeline：** 多步驟流程、需要流程控制、要獨立成服務、需要與其他系統整合

---

## 教學比喻

> **Docker image** 是「已裝好軟體的電腦」  
> **pipelines 資料夾**是「我每天在改的程式碼」  
> **套件裝在電腦裡，不是丟在程式碼資料夾」

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
