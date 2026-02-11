# OpenWebUI Pipeline 完整教學指南

> **給同學們的話：**  
> 這份講義是為 Raspberry Pi 教學環境設計的，我們會用 Docker 來實作 Pipeline Server。  
> 如果你還沒學過 Docker，別擔心，我們會一步步帶你走過。  
> 重點不是「記住指令」，而是「理解為什麼這樣做」。

---

## 📋 目錄

### 名詞解釋
- [什麼是「符合 OpenAI 規格（OpenAI-compatible）」？](#什麼是符合-openai-規格openai-compatible)
- [什麼是「符合 OpenAI 規格的模型（OpenAI-compatible models）」？](#什麼是符合-openai-規格的模型openai-compatible-models)

### 第一部分：理解 Pipeline Server
- [為什麼需要 Pipeline Server？](#為什麼需要-pipeline-server)
- [什麼是 Pipeline？](#什麼是-pipeline)
- [教學環境設定：為什麼用 Docker？](#教學環境設定為什麼用-docker)

### 第二部分：實作 Pipeline Server
- [快速開始：使用 Docker Run](#快速開始使用-docker-run)
- [進階部署：使用 Docker Compose](#進階部署使用-docker-compose)
- [在 OpenWebUI 中連接 Pipelines](#在-openwebui-中連接-pipelines)
- [管理與啟用 Pipeline](#管理與啟用-pipeline)

### 第三部分：深入理解與實務
- [重要觀念釐清](#重要觀念釐清)
- [專案結構建議](#專案結構建議)
- [常見問題與排錯](#常見問題與排錯)
- [教學比喻與記憶法](#教學比喻與記憶法)

### 第四部分：延伸學習
- [參考資源](#參考資源)
- [下一步學習方向](#下一步學習方向)

---

## 什麼是「符合 OpenAI 規格（OpenAI-compatible）」？

### 一、為什麼在 Open-WebUI 裡一直看到「符合 OpenAI 規格」？

在使用 Open-WebUI 的過程中，我們常會看到文件、設定或教學提到：

> This API is OpenAI-compatible  
> 符合 OpenAI 規格

這並不是指「一定要使用 OpenAI 的模型」，  
而是指 API 的設計方式，遵循 OpenAI API 的介面規格。

Open-WebUI 本身並不關心你「實際用的是哪個模型」，  
它只關心一件事：

> 我送出的請求，你聽不聽得懂？  
> 你回來的結果，我解不解得開？

---

### 二、什麼叫「符合 OpenAI 規格」？

在技術上，「符合 OpenAI 規格」只需要滿足 **三個條件**。

#### 1️⃣ API endpoint 一樣

例如常見的：

```
POST /v1/chat/completions
GET  /v1/models
```

只要 Open-WebUI 發送請求的 URL 存在，  
它就能正常與你的 API Server 溝通。

---

#### 2️⃣ Request JSON 結構一樣

Open-WebUI 送給模型的資料格式，基本上長這樣：

```json
{
  "model": "gpt-4",
  "messages": [
    { "role": "user", "content": "你好" }
  ]
}
```

重點不是模型名稱是不是 `gpt-4`，  
而是：
- 有 `model`
- 有 `messages`
- `messages` 裡有 `role` 與 `content`

👉 **你的 API Server 必須能解析這種結構**

---

#### 3️⃣ Response JSON 結構一樣

API 回傳的結果，必須長得像這樣（簡化版）：

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "你好！"
      }
    }
  ]
}
```

Open-WebUI 只會從這個位置讀取模型輸出：

```
choices[0].message.content
```

👉 **只要回傳格式正確，內容來自誰都沒關係**

---

### 三、常見誤解澄清（非常重要）

#### ❌ 錯誤理解
- 一定要使用 OpenAI 的雲端模型
- 一定要付費給 OpenAI
- 一定要有 OpenAI API Key

#### ✅ 正確理解
- 只要 API 的「外觀」符合 OpenAI 規格即可
- 背後可以是：
  - 本地模型
  - 校內伺服器
  - 私有模型
  - 自己寫的 API

---

### 四、為什麼 Open-WebUI 要用這種設計？

這是一種非常聰明、也非常實務導向的設計。

**好處包含：**
1. 不被單一模型或廠商綁死
2. 本地模型、私有模型都能接
3. 教學只要教一套 API 規格，就能通用
4. 學生未來換平台，也能快速上手

從教學角度來看，這代表：

> 你不是在教某一個模型，  
> 而是在教一個「通用的 AI API 介面概念」。

---

### 五、生活化比喻：USB 插頭

可以用這個比喻幫學生快速理解：
- **Open-WebUI：**  
  「我只插 USB-C」
- **OpenAI API：**  
  「我是 USB-C」
- **其他模型或伺服器：**  
  「我雖然不是原廠，但我也做成 USB-C」

👉 **只要插得進去，就能用**

---

### 六、課堂重點一句話總結（考試版）

> 所謂「符合 OpenAI 規格（OpenAI-compatible）」是指：  
> 一個 API Server 只要提供與 OpenAI API 相同的 endpoint、  
> request JSON 與 response JSON 結構，  
> 即使背後使用的是本地或自架模型，  
> 仍可被 Open-WebUI 當作 OpenAI API 來使用。

---

## 什麼是「符合 OpenAI 規格的模型（OpenAI-compatible models）」？

### 一、先破除一個最常見的誤會

很多同學第一次看到這個名詞，會以為：

> 「OpenAI-compatible models」  
> 是不是指「OpenAI 做的模型」？

👉 **這是錯的。**

OpenAI-compatible 跟「模型是誰做的」沒有直接關係。

---

### 二、正確定義（請記住這一句）

> 「模型符合 OpenAI 規格（OpenAI-compatible）」  
> 指的是：模型服務提供的 API 介面，  
> 是否遵守 OpenAI 所定義的 API 規格。

重點有三個字一定要畫線：  
👉 **API 規格**

---

### 三、為什麼要強調「API」，而不是「模型」？

在實務上：
- 我們的程式 **不是直接呼叫模型**
- 而是 **呼叫一個「模型服務 API」**

所以真正影響你程式能不能用的，不是：
- 模型名稱
- 模型參數
- 模型公司

而是：

> 你送出的請求，  
> 跟對方 API 要的格式，一不一樣

---

### 四、什麼叫「符合 OpenAI 規格」？（三個必要條件）

一個模型服務 **同時符合以下三點**，  
我們才稱它是 OpenAI-compatible。

---

#### ① Endpoint（網址）一樣

OpenAI 最常見的聊天 API 路徑是：

```
POST /v1/chat/completions
```

如果一個服務也提供這個路徑，  
第一關才算過。

---

#### ② Request JSON 結構一樣

OpenAI 的典型請求格式是：

```json
{
  "model": "模型名稱",
  "messages": [
    { "role": "system", "content": "你是助理" },
    { "role": "user", "content": "你好" }
  ]
}
```

重點不是模型名稱，而是一定要有：
- `messages`
- `role`
- `content`

---

#### ③ Response JSON 結構一樣（最重要）

OpenAI 回傳資料的結構（簡化）：

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "回覆內容"
      }
    }
  ]
}
```

只要你的程式 **可以用同一套方式解析回應**，  
那就算相容。

---

### 五、所以「OpenAI-compatible models」真正的意思是什麼？

正確理解是：

> **「提供 OpenAI API 規格的模型服務」**

而不是：
- ❌ 模型能力等同 OpenAI
- ❌ 模型一定是 GPT
- ❌ 模型一定來自 OpenAI

---

### 六、為什麼大家都想「符合 OpenAI 規格」？

因為 **工具生態系最大**。

只要 API 相容，你就可以：
- 不改程式碼
- 不換 UI
- 不改工作流程
- 直接換模型

這也是為什麼很多系統、平台、框架  
都「以 OpenAI API 當標準介面」。

---

### 七、一個學生一定要懂的重點整理

請牢記這三句話：
1. OpenAI-compatible 描述的是 **API**，不是模型
2. 模型可以不同，只要 **API 一樣就能互換**
3. 能不能用 OpenAI API 語法，取決於服務是否相容

---

### 八、一句話總結（考試 / 面試 / 上課都好用）

> OpenAI-compatible models 指的不是模型本身，  
> 而是「模型服務是否遵守 OpenAI API 規格」。

---

## 為什麼需要 Pipeline Server？

### 學習目標

在開始之前，讓我們先回答一個關鍵問題：

> **什麼時候，Open-WebUI 內建的 Filter 和 Tools 已經不夠用了？**

這不是技術問題，而是**架構設計**的問題。理解這個問題，你就能在對的時候選對工具。

---

### 先給結論：什麼情況需要 Pipeline Server？

同學們，如果你遇到下面**任何一種**情況，就該考慮使用 Pipeline Server 了：

* 🔁 **流程不只一個步驟**  
  你需要多步驟、可重組的處理流程，而不是單次操作

* 🌐 **需要和 Open-WebUI 以外的系統共用**  
  你想把 AI 功能接給其他系統用（API、n8n、後端服務）

* 🧠 **模型前後都要動手腳**  
  你需要在模型推理前做前處理，推理後做後處理

* 🧩 **想把 AI 行為做成「一個服務」**  
  你不想每次都在 Open-WebUI 裡調設定，而是想建立一個可重複使用的服務

**簡單判斷原則：**  
如果你只是在「單一請求 → 單一回應」中加點邏輯，Filter / Tools 會更簡單。  
但只要你開始「設計流程」，Pipeline Server 就會變成主角。

---

### 為什麼 Filter / Tools 會開始不夠用？

讓我們先理解現有工具的定位，這樣你才知道什麼時候該升級。

#### Filter：適合「輕量、就地修改」

**Filter 很適合做這些事：**
* 修改 prompt
* 加入系統訊息
* 對輸入或輸出做小調整

**但 Filter 的限制也很明顯：**
* 執行順序是固定的，很難改變
* 不適合複雜的狀態管理
* 很難拆成可重用的流程模組

**老師的建議：**  
Filter 的角色是「即時加工」，不是「流程設計」。  
當你開始需要「設計流程」時，就是該考慮 Pipeline Server 的時候了。

---

#### Tools：適合「單次能力擴充」

**Tools 很適合做這些事：**
* 查資料
* 呼叫外部 API
* 執行一次明確的任務

**但當你遇到這些需求時，Tools 就會變得卡手：**
* 一個回應需要呼叫多個工具
* 工具之間有順序與條件判斷
* 想控制「什麼情況一定要走某個流程」

**老師的建議：**  
Tools 解決的是「會不會做」，不是「怎麼串」。  
當你需要「串流程」時，Pipeline Server 會是更好的選擇。

---

### Pipeline Server 在做什麼？（一句話版）

> **Pipeline Server = 把「和模型互動的整個流程」獨立成一個 API 服務**

**它讓你可以：**

* **明確定義整個流程：**
  * 輸入怎麼處理
  * prompt 怎麼組裝
  * 模型怎麼選擇
  * 輸出怎麼加工

* **把這套邏輯分享給：**
  * Open-WebUI 使用
  * 其他系統使用
  * 未來的專案使用

**簡單說：**  
Pipeline Server 讓你把 AI 邏輯從「設定」升級成「服務」。

---

### 教學視角：什麼時候該學 Pipeline Server？

同學們，在課程設計上，Pipeline Server 非常適合放在：

> **「你開始想做自己的 AI 服務」的那一刻**

**典型的學習轉折點包括：**

* 「我不想每個專案都重寫 Filter / Tool」
* 「我想把這個 AI 功能接給別人用」
* 「我想控制整個 AI 行為，而不只是補強模型」

這時候，Pipeline Server 不只是新技術，而是**架構升級**。

---

## 什麼是 Pipeline？

### 定義

**Pipeline** 是一個**模組化、可自訂的工作流程框架**，讓你可以：

* ✅ 把複雜流程拆成多個步驟
* ✅ 自訂函數、呼叫外部 API
* ✅ 實作訊息過濾器（例如內容過濾）
* ✅ 整合 RAG、Langfuse、搜尋工具等
* ✅ 利用 Python 庫做更複雜的處理

**最重要的特性：**  
Pipeline 會提供一個 **OpenAI 相容的 API server**，所以 Open-WebUI 可以將它當成一個 API 來源來使用。

---

### Pipeline 與 Filter / Tools 的關係

同學們常問：「那我之前學的 Filter 和 Tools 怎麼辦？」

**答案是：** Pipeline 可以**整合** Filter 和 Tools 的功能，並且提供：

* **更完整的流程控制**能力
* **獨立成服務**，可重複使用
* **更好的模組化**設計

**簡單說：**  
Filter / Tools 是「功能」，Pipeline 是「架構」。  
你可以用 Pipeline 來組織和管理 Filter / Tools 的功能。

---

## 教學環境設定：為什麼用 Docker？

### 本課程的實作環境

同學們，在開始實作之前，我們先來理解為什麼選擇這個環境：

* **硬體：** Raspberry Pi
* **執行方式：** Docker Container
* **角色定位：** Pipeline Server = 一個獨立的 API 服務

**這個選擇不是為了炫技，而是為了讓大家建立正確的系統觀念。**

---

### 為什麼「一定要用 Docker」來教 Pipeline Server？

#### 1️⃣ Pipeline Server 本質上就是一個 Server

同學們，一旦進入 Pipeline Server 階段，你其實已經在做這件事：

> **把 AI 流程，變成一個可以被呼叫的服務**

這代表你必然會遇到：

* **Port（埠號）**：服務要開在哪個埠？
* **啟動 / 停止**：服務怎麼啟動和關閉？
* **環境變數**：服務需要哪些設定？
* **相依套件**：服務需要哪些 Python 套件？

**老師的教學考量：**  
用 Docker 教，可以一次把這些「Server 該有的概念」教對。  
你不用先學一堆 Linux 服務管理的細節，就能理解 Server 的運作方式。

---

#### 2️⃣ Docker 讓 Raspberry Pi 的環境「可複製、可重現」

同學們，在 Raspberry Pi 教學現場，老師最怕的是：

* 套件版本不同
* Python 環境亂掉
* 一台可以跑，一台不能跑
* 「老師，我的為什麼不行？」

**Docker 可以解決這些問題：**

* 不管哪一顆 Pi
* 不管之前裝過什麼
* 只要 `docker run` 或 `docker compose up`
* 行為就一致

**老師的教學考量：**  
這是**教學穩定度**，而不是部署炫技。  
我們希望每個同學都能成功，而不是花時間在環境問題上。

---

#### 3️⃣ Docker 幫你理解「Open-WebUI 與 Pipeline 是不同服務」

同學們，很多初學者會混淆：

* Open-WebUI 是什麼？
* Pipeline Server 是什麼？
* Ollama（模型）是什麼？

**用 Docker 分開跑，你會很清楚看到：**

* **Open-WebUI：**
  * 負責 UI（使用者介面）
  * 管理對話歷史
  * 提供聊天介面

* **Pipeline Server：**
  * 提供 API 服務
  * 處理流程控制
  * 執行自訂邏輯

* **Ollama：**
  * 執行模型推論
  * 提供模型能力

**老師的教學考量：**  
這一步是在教「系統邊界」，不是指令操作。  
理解每個服務的職責，你才能設計出好的系統架構。

---

### 本章實作目標

完成本章後，同學們應該能夠：

* ✅ 用 Docker 啟動一個 Pipeline API Server
* ✅ 理解這個 Server：
  * 有自己的 Port（埠號）
  * 有自己的 API endpoint（端點）
* ✅ 讓 Open-WebUI 把請求「轉交」給這個 Pipeline Server
* ✅ 理解「服務」和「設定」的差別

**重點：**  
不是只停留在「Open-WebUI 裡面調設定」，而是真的建立一個獨立的服務。

---

### 下一個目標：建立一個最小 Pipeline Server

接下來的內容，我們會：

1. **建立一個最小 Pipeline Server**（使用官方映像）
2. **用 `docker run` 啟動 Pipeline API**
3. **從 Open-WebUI 指向這個 Pipeline Server**
4. **理解服務之間的溝通方式**
5. **直接下載openwebui的wiki單一py檔範例**

> 官網網址:  
> `https://raw.githubusercontent.com/open-webui/pipelines/main/examples/pipelines/integrations/wikipedia_pipeline.py`  
> [官方範例目錄 GitHub Repo](https://github.com/open-webui/pipelines/tree/main/examples)  

**整個流程的重點只有一個：**

> **讓同學們親手做出「我真的有一個 AI API 服務」的感覺**

---

## 快速開始：使用 Docker Run

### 學習目標

在這個章節，我們會用最簡單的方式啟動 Pipeline Server。  
重點是「理解流程」，而不是「記住指令」。

---

### 步驟 1：拉取 Pipelines 映像

首先，我們需要取得 Pipeline Server 的 Docker 映像：

```bash
docker pull ghcr.io/open-webui/pipelines:main
```

**老師說明：**  
這是官方提供的 Pipeline 伺服器映像，已經幫你準備好：
* Python 環境
* Pipeline Server 程式
* OpenAI 相容的 API 介面

你不需要自己寫 Server 程式，直接用這個映像就可以了。

**同學們可能會問：**  
「為什麼要用 `main` 這個標籤？」  
→ 這是開發版本，會持續更新。正式環境可以用特定版本號。

---

### 步驟 2：啟動 Pipeline Docker 容器

我們使用 Named Volume 來啟動容器，這種方式適合正式部署。

```bash
docker run -d -p 9099:9099 \
  --add-host=host.docker.internal:host-gateway \
  -v pipelines:/app/pipelines \
  --name pipelines \
  --restart always \
  ghcr.io/open-webui/pipelines:main
```

**參數說明：**

* `-d`：背景執行（detached mode）
* `-p 9099:9099`：把容器的 9099 埠對應到主機的 9099 埠
* `--add-host=host.docker.internal:host-gateway`：讓容器可以訪問主機上的服務（例如 Ollama）
* `-v pipelines:/app/pipelines`：使用 named volume 存放 pipeline 程式碼
* `--name pipelines`：給容器一個名字，方便管理
* `--restart always`：容器自動重啟（重開機後也會自動啟動）

**關於 `host-gateway` 在 Raspberry Pi 上的使用：**

* ✅ **Docker 20.10+ 版本：** 完全支援 `host-gateway`，可以直接使用
* ⚠️ **Docker 較舊版本：** 如果遇到問題，可以使用替代方案（見下方）

**檢查 Docker 版本：**
```bash
docker --version
```



**使用 Docker Compose（單一服務版本）：**

如果你偏好使用 Docker Compose，可以建立一個 `docker-compose.yml` 檔案：

```yaml
version: '3.8'

services:
  pipelines:
    image: ghcr.io/open-webui/pipelines:main
    
    ports:
      - "9099:9099"
    
    volumes:
      # 使用 named volume
      - pipelines:/app/pipelines
    
    extra_hosts:
      - "host.docker.internal:host-gateway"
    
    restart: always
    
    container_name: pipelines

volumes:
  pipelines:
```

**啟動方式：**

```bash
# 啟動服務
docker compose up -d

# 查看日誌
docker compose logs -f pipelines

# 停止服務
docker compose down

# 停止服務並刪除 volume（小心使用，會刪除資料）
docker compose down -v
```

**說明：**  
Named Volume 的資料由 Docker 管理，適合正式部署。資料會儲存在 Docker 管理的位置，即使容器刪除也不會遺失。

---

### 步驟 3：確認容器正常運作

啟動後，我們來確認一下容器是否正常：

```bash
# 查看容器狀態
docker ps

# 查看容器日誌
docker logs pipelines
```

**應該會看到：**  
Pipeline Server 啟動的訊息，通常會顯示 API 服務已經在 9099 埠上運行。

**如果出問題：**  
* 檢查日誌：`docker logs pipelines`
* 檢查埠號是否被占用：`netstat -tuln | grep 9099`
* 檢查容器狀態：`docker ps -a`

---

## 進階部署：使用 Docker Compose

### 學習目標

當你開始建立自己的 Pipeline 專案時，Docker Compose 會讓管理變得更簡單。  
這個章節會教你如何用 `docker-compose.yml` 來管理整個專案。

---

### 為什麼要用 Docker Compose？

**同學們可能會問：**  
「我已經會用 `docker run` 了，為什麼還要學 Docker Compose？」

**答案是：**

* **管理更方便**：一個檔案就能管理整個專案
* **設定更清楚**：所有參數都寫在 `docker-compose.yml` 裡
* **擴展更容易**：未來要加其他服務（例如資料庫）很容易
* **團隊協作**：其他人拿到你的 `docker-compose.yml` 就能直接跑

**老師建議：**  
小專案可以用 `docker run`，但正式專案建議用 Docker Compose。

---

### 專案結構建議

在開始之前，讓我們先建立一個清楚的專案結構：

```
project/
├── docker-compose.yml          # Docker Compose 設定
├── Dockerfile                  # 自訂映像（如果需要安裝額外套件）
└── pipelines/                  # Pipeline 程式碼目錄
    ├── my_pipeline.py          # 你的 Pipeline 程式
    └── requirements.txt        # Python 套件清單（如果需要）
```

**老師說明：**  
這個結構很清楚：
* `docker-compose.yml`：服務設定
* `Dockerfile`：如果需要自訂映像
* `pipelines/`：你的程式碼

---

### Dockerfile（如果需要安裝額外的 Python 套件）

**什麼時候需要 Dockerfile？**  
當你的 Pipeline 需要額外的 Python 套件時（例如 pandas、numpy）。

```dockerfile
FROM ghcr.io/open-webui/pipelines:main

# 複製 requirements.txt 並安裝套件
COPY pipelines/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
```

**重要觀念（同學們一定要理解）：**

* Python 套件是裝在 **Docker image 裡**，不是放在 pipelines volume
* pipelines 資料夾只存放**你的程式碼**（如 `my_pipeline.py`）
* `requirements.txt` 是在 **build 階段**使用的，不是執行階段

**老師提醒：**  
如果不需要額外套件，可以不用 Dockerfile，直接用官方映像。

---

### docker-compose.yml

這是整個專案的核心設定檔：

```yaml
version: '3.8'

services:
  pipelines:
    # 如果有 Dockerfile，使用 build
    build: .
    # 或直接使用官方映像（註解掉 build，取消註解下面這行）
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

**參數說明：**

* `build: .`：使用當前目錄的 Dockerfile 建立映像
* `ports`：埠號對應
* `volumes`：資料卷掛載（bind mount）
* `extra_hosts`：讓容器可以訪問主機服務
* `restart: always`：自動重啟
* `container_name`：容器名稱

**Raspberry Pi 特別注意：**

如果 `host-gateway` 在你的 Docker Compose 版本不支援，可以這樣修改：

```yaml
extra_hosts:
  # 方法 1：使用 host-gateway（Docker 20.10+）
  - "host.docker.internal:host-gateway"
  
  # 方法 2：如果 host-gateway 不支援，使用實際 IP
  # 先執行 hostname -I 取得 IP，然後替換下面的 IP
  # - "host.docker.internal:192.168.1.100"
```

**老師提醒：**  
`./pipelines` 是相對路徑，會對應到專案目錄下的 `pipelines/` 資料夾。

---

### 啟動服務

設定好後，啟動就變得很簡單：

```bash
# 建立並啟動服務
docker compose up -d --build

# 查看日誌（持續監看）
docker compose logs -f pipelines

# 查看日誌（只看一次）
docker compose logs pipelines

# 停止服務
docker compose down

# 停止服務並刪除 volume（小心使用）
docker compose down -v
```

**老師說明：**

* `-d`：背景執行
* `--build`：重新建立映像（如果修改了 Dockerfile）
* `-f`：持續監看日誌（類似 `tail -f`）
* `-v`：同時刪除 volume（資料會不見，要小心）

**同學們常問：**  
「什麼時候需要 `--build`？」  
→ 只有修改 Dockerfile 或 requirements.txt 時才需要。

---

## 在 OpenWebUI 中連接 Pipelines

### 學習目標

這個章節會教你如何讓 Open-WebUI 和 Pipeline Server 溝通。  
重點是理解「服務之間的連接方式」。

---

### 步驟 1：登入 Open-WebUI 後台

開啟瀏覽器，前往 Open-WebUI 介面（例如 `http://localhost:3000` 或你的樹莓派 IP）

**老師提醒：**  
如果 Open-WebUI 也在 Docker 裡，記得確認它已經啟動：
```bash
docker ps | grep open-webui
```

---

### 步驟 2：設定連線

1. 前往 **Settings → Connections → OpenAI API**
2. 點擊「新增連線」或「Add Connection」
3. 設定如下：

   **API URL：**  
   根據你的部署方式選擇：
   
   * 如果 Open-WebUI 與 Pipelines **都在 Docker 裡**：  
     `http://host.docker.internal:9099`
   
   * 如果 Open-WebUI **在 Docker**，Pipelines **在主機**：  
     `http://host.docker.internal:9099`
   
   * 如果**都在主機上**：  
     `http://localhost:9099`
   
   * 如果 Open-WebUI **在主機**，Pipelines **在 Docker**：  
     `http://localhost:9099`

   **API key：**  
   `0p3n-w3bu!`（這是預設金鑰，可以自訂）

4. 點擊「儲存」或「Save」

**老師說明：**  
`host.docker.internal` 是 Docker 提供的特殊主機名，讓容器可以訪問主機上的服務。  
如果兩個容器在同一個 Docker network 裡，也可以用容器名稱。

---

### 步驟 3：驗證連線

**成功連線的標誌：**

* Open-WebUI 會在 API Base URL 欄位顯示一個 **Pipelines 標識**
* 連線狀態顯示為「已連接」或「Connected」

**如果連線失敗：**

1. **檢查 Pipeline Server 是否運行：**
   ```bash
   docker ps | grep pipelines
   curl http://localhost:9099/health
   ```

2. **檢查網路連線：**
   * 確認埠號 9099 是否正確
   * 確認防火牆設定

3. **查看 Open-WebUI 日誌：**
   ```bash
   docker logs open-webui
   ```

**老師提醒：**  
最常見的問題是 URL 設定錯誤，特別是 `host.docker.internal` 的使用時機。

---

## 管理與啟用 Pipeline

### 學習目標

連線設定完成後，我們來學習如何在 Open-WebUI 中管理 Pipeline。

---

### 在 Open-WebUI 中管理 Pipeline

連線設定完成後，可以在 Open-WebUI 介面中：

1. **前往 Settings → Pipelines 頁籤**
2. **查看已安裝的 pipelines**
3. **安裝或上傳你自己的 pipeline 程式：**
   * 可以從 GitHub URL 安裝範例 pipeline
   * 也可以直接上傳 Python 檔案

**老師說明：**  
Pipeline 程式碼實際上是存放在 Pipeline Server 的 `/app/pipelines` 目錄裡。  
Open-WebUI 只是提供一個管理介面，讓你可以方便地上傳和管理。

**同學們可能會問：**  
「我可不可以直接修改 `/app/pipelines` 裡的檔案？」  
→ 可以！如果你用 bind mount，直接改主機上的檔案就可以了。

---

## 重要觀念釐清

### 學習目標

這個章節會釐清一些容易混淆的概念，幫助同學們建立正確的觀念。

---

### Volume vs Python 環境

這是同學們最常搞混的地方，讓我們用表格來釐清：

| **項目** | **正確位置** | **說明** |
|---------|------------|---------|
| `my_pipeline.py` | `/app/pipelines`（volume） | 你的程式碼檔案 |
| `requirements.txt` | Image build 階段 | 套件清單檔案 |
| `pip install pandas` | Dockerfile | 套件安裝指令 |
| Python runtime | Container image | Python 執行環境 |

**關鍵觀念（同學們一定要記住）：**

* 🔴 **pipelines volume 裡放的是「你的程式」**
* 🔴 **Python 套件是「裝在容器 image 裡」**
* 🔴 **Volume ≠ Python 環境**

**老師的比喻：**  
Volume 是「你的筆記本」（程式碼），  
Image 是「裝好軟體的電腦」（Python 環境）。  
你不能把軟體裝在筆記本裡，要把軟體裝在電腦裡。

---

### Named Volume vs Bind Mount

這是另一個重要的觀念，讓我們來比較兩種方式：

#### Named Volume（適合正式部署）

**優點：**
* ✅ 資料由 Docker 管理，更安全
* ✅ 適合正式部署環境
* ✅ Pipeline 程式不常修改時使用

**缺點：**
* ❌ 不適合教學與開發
* ❌ 需要進入容器才能修改檔案
* ❌ 樹莓派上 debug 較困難

**實體路徑：**
```bash
/var/lib/docker/volumes/pipelines/_data
```

**老師說明：**  
Named Volume 的資料存在 Docker 管理的目錄裡，你通常不會直接去改它。  
適合程式碼已經穩定，不需要頻繁修改的情況。

---

#### Bind Mount（適合教學與開發）

**優點：**
* ✅ 可以直接用編輯器修改程式碼
* ✅ 適合教學與開發階段
* ✅ 樹莓派上更容易 debug
* ✅ 檔案修改立即生效

**缺點：**
* ❌ 需要確保主機路徑存在
* ❌ 權限設定需要注意

**使用方式：**
```bash
-v $(pwd)/pipelines:/app/pipelines
```

**老師建議：**  
同學們在學習階段，**強烈建議使用 Bind Mount**。  
這樣你可以直接看到和修改程式碼，學習效果會更好。

---

## 專案結構建議

### 學習目標

這個章節會教你如何組織一個 Pipeline 專案，讓程式碼更容易管理和維護。

---

### 完整的教學專案結構

```
project/
├── docker-compose.yml          # Docker Compose 設定
├── Dockerfile                  # 自訂映像（如需安裝套件）
├── README.md                   # 專案說明
└── pipelines/                  # Pipeline 程式碼目錄
    ├── requirements.txt        # Python 套件清單
    ├── my_pipeline.py          # 你的 Pipeline 程式
    └── examples/               # 範例程式
        └── example_pipeline.py
```

**老師說明：**  
這個結構很清楚，每個檔案都有明確的用途。  
`examples/` 目錄可以放一些範例程式，方便參考。

---

### requirements.txt 範例

如果你的 Pipeline 需要額外的 Python 套件：

```txt
pandas
numpy
requests
chromadb
```

**老師提醒：**  
* 每個套件一行
* 可以指定版本：`pandas==2.0.0`
* 不需要的套件不要加，會讓映像變大

---

### Pipeline 程式範例

一個最簡單的 Pipeline 程式範例：

```python
# pipelines/my_pipeline.py
from typing import Dict, Any

def process_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    處理訊息的 Pipeline 函數
    
    這是 Pipeline Server 會呼叫的主要函數
    你可以在這裡實作你的自訂邏輯
    """
    # 你的自訂邏輯
    processed = message.copy()
    processed['processed'] = True
    
    return processed
```

**老師說明：**  
這是最基本的範例，實際的 Pipeline 會更複雜。  
重點是理解「Pipeline Server 會呼叫這個函數」的概念。

---

## 常見問題與排錯

### 學習目標

這個章節整理了同學們最常遇到的問題，幫助你快速排錯。

---

### Q1: Pipeline reload 要不要重啟容器？

**A:** 通常不需要。

Pipeline 伺服器會自動偵測檔案變更並重新載入。  
如果沒有自動載入，可以重啟容器：

```bash
docker compose restart pipelines
# 或
docker restart pipelines
```

**老師說明：**  
這是 Pipeline Server 的貼心設計，讓開發更方便。  
但如果修改了 `requirements.txt` 或 `Dockerfile`，就需要 rebuild。

---

### Q2: Python 檔改了，需不需要 rebuild？

**A:** 看情況。

* **如果只修改 `pipelines/` 目錄下的 Python 檔案：**  
  **不需要 rebuild**，Pipeline Server 會自動重新載入

* **如果修改了 `requirements.txt` 或 `Dockerfile`：**  
  **需要 rebuild**，因為這些是在 build 階段處理的

```bash
docker compose up -d --build
```

**老師提醒：**  
這是同學們最常搞混的地方。  
記住：**程式碼改動不用 rebuild，環境改動才要 rebuild**。

---

### Q3: 如何確認 Pipeline 是否正常運作？

**A:** 有幾個方法可以檢查：

**方法 1：檢查容器日誌**
```bash
docker compose logs -f pipelines
# 或
docker logs pipelines
```

**方法 2：測試 API**
```bash
curl http://localhost:9099/health
```

**方法 3：在 Open-WebUI 中測試**
* 建立一個新的對話
* 選擇 Pipeline Server 作為模型來源
* 發送一個測試訊息

**老師說明：**  
如果 API 回應正常，但 Open-WebUI 連不上，通常是連線設定問題。

---

### Q4: 樹莓派上效能如何？

**A:** Pipeline Server 本身資源需求不高。

* Pipeline Server 主要是做流程控制，運算量不大
* 建議使用 bind mount 方便 debug
* 如果 Pipeline 需要大量運算（例如 RAG），考慮使用外部服務

**老師建議：**  
樹莓派上跑 Pipeline Server 沒問題，但要注意：
* 如果同時跑 Open-WebUI、Ollama、Pipeline Server，記憶體可能會不夠
* 建議至少 4GB RAM 的樹莓派

---

### Q5: 什麼時候該用 Pipeline，什麼時候用 Filter / Tools？

**A:** 簡單判斷原則：

* **使用 Filter / Tools：**
  * 單一請求的簡單調整
  * 單次能力擴充
  * 不需要複雜流程控制

* **使用 Pipeline：**
  * 多步驟流程
  * 需要流程控制
  * 要獨立成服務
  * 需要與其他系統整合

**老師的建議：**  
先從 Filter / Tools 開始，當你發現「不夠用」的時候，就是該用 Pipeline 的時候了。

---

### Q6: 容器啟動失敗怎麼辦？

**A:** 按照以下步驟檢查：

1. **查看容器日誌：**
   ```bash
   docker logs pipelines
   ```

2. **檢查埠號是否被占用：**
   ```bash
   netstat -tuln | grep 9099
   # 或
   lsof -i :9099
   ```

3. **檢查 Docker 是否正常：**
   ```bash
   docker ps
   docker info
   ```

4. **檢查權限問題：**
   ```bash
   ls -la pipelines/
   ```

**老師提醒：**  
最常見的問題是：
* 埠號被占用（改個埠號試試）
* 權限問題（檢查檔案權限）
* 路徑不存在（確認 `pipelines/` 目錄存在）
* `host-gateway` 不支援（見下方 Q7）

---

### Q7: 在 Raspberry Pi 上 `host-gateway` 不支援怎麼辦？

**A:** 這是因為 Docker 版本較舊（需要 Docker 20.10+）。

**解決方法：**

1. **檢查 Docker 版本：**
   ```bash
   docker --version
   ```

2. **如果版本太舊，升級 Docker：**
   ```bash
   # 更新套件列表
   sudo apt update
   
   # 安裝最新版本的 Docker（建議）
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

3. **如果無法升級，使用實際 IP：**
   ```bash
   # 先取得 Raspberry Pi 的 IP
   PI_IP=$(hostname -I | awk '{print $1}')
   echo "你的 Pi IP: $PI_IP"
   
   # 使用實際 IP 替代 host-gateway
   docker run -d -p 9099:9099 \
     --add-host=host.docker.internal:$PI_IP \
     -v $(pwd)/pipelines:/app/pipelines \
     --name pipelines \
     --restart always \
     ghcr.io/open-webui/pipelines:main
   ```

**老師說明：**  
`host-gateway` 是 Docker 20.10+ 才支援的功能，它會自動解析為主機的 IP。  
如果 Docker 版本較舊，手動指定 IP 也能達到同樣的效果。

---

## 教學比喻與記憶法

### Docker Image vs Volume

> **Docker image** 是「已裝好軟體的電腦」  
> **pipelines 資料夾**是「我每天在改的程式碼」  
> **套件裝在電腦裡，不是丟在程式碼資料夾」

**老師的延伸比喻：**

* **Docker Container** = 開機後的電腦
* **Volume** = 外接硬碟（資料可以保留）
* **Port** = 電腦的網路埠（讓別人可以連進來）

---

### Pipeline Server 的角色

> **Open-WebUI** = 餐廳的服務生（接待客人）  
> **Pipeline Server** = 廚師（處理食材，做菜）  
> **Ollama** = 食材供應商（提供原料）

**老師說明：**  
服務生（Open-WebUI）接收客人的點單，  
交給廚師（Pipeline Server）處理，  
廚師需要時會向供應商（Ollama）要食材。

---

## 參考資源

### 官方資源

* [Open-WebUI Pipelines GitHub](https://github.com/open-webui/pipelines)
* [Open-WebUI 官方文件](https://docs.openwebui.com/)

### 延伸學習

* Docker 基礎教學
* Python API 開發（FastAPI）
* 微服務架構設計

---

## 下一步學習方向

完成這個章節後，同學們可以：

* 📝 **建立你的第一個 Pipeline**  
  從簡單的訊息處理開始，逐步增加複雜度

* 🔧 **整合 RAG 功能**  
  讓 Pipeline 能夠檢索外部資料

* 🎯 **實作自訂訊息過濾器**  
  根據需求過濾或修改訊息

* 🚀 **部署到生產環境**  
  學習如何優化和部署 Pipeline Server

* 🌐 **整合其他服務**  
  讓 Pipeline 與其他系統（例如資料庫、API）整合

**老師的建議：**  
不要急著做複雜的功能，先把基礎打穩。  
理解「為什麼這樣做」比「記住怎麼做」更重要。

---

## 給同學們的最後提醒

1. **理解比記憶重要**  
   不要只是記住指令，要理解為什麼這樣做

2. **多動手實作**  
   理論讀再多，不如實際做一次

3. **遇到問題先思考**  
   先理解問題，再找解決方法

4. **善用日誌和錯誤訊息**  
   大部分問題都可以從日誌中找到線索

5. **不要害怕犯錯**  
   錯誤是最好的學習機會

**祝同學們學習順利！** 🎉
‌