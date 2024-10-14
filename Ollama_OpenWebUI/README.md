# Ollama 和 OpenWebUI應用
- **Ollama安裝於raspberry**
- **OpenWebUI安裝於container**

## 1. 樹莓派安裝Docker
###  [1.1官網說明](https://docs.docker.com/engine/install/debian/)
  - 請使用Install using the apt repository章節步驟
  - 注意完成後要將user pi 加入至 docker group
  - `sudo usermod -aG docker pi`

## 2. 安裝Ollama
- [**2.1官網說明**](https://github.com/ollama/ollama)
	- **使用Linux安裝**

### 2.1 修改環境變數
- 主要目的是讓ollama接受外部主機的呼叫
**2.1.1 步驟1:**
透過呼叫 systemctl edit ollama.service 編輯 systemd 服務。這將打開一個編輯器。

```
sudo vim /etc/systemd/system/ollama.service
```

**2.1.2步驟2:**
對於每個環境變量，在 [Service] 部分下新增一行 Environment：

```
[Service]
Environment="OLLAMA_HOST=0.0.0.0"
```

**2.1.3步驟3:**

```
systemctl daemon-reload
systemctl restart ollama
```


### 2.1 Ollama安裝Open LLMs
- [**官網支援LLMs清單**](https://ollama.com/library)
- 安裝方法
	- `ollama run llama3.1`

## 3. 安裝OpenWebUI
- 使用docker安裝
- **由於我們的ollam是直接安裝在raspberry上,OpenWebUI是安裝在docker上,所以要下的Docker command不一樣,以下有2種安裝方式**

### 3.1 安裝方式1

```
docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

#### 說明1. Docker 中的 `--network=host` 選項允許容器共用主機的網路命名空間，這表示容器沒有自己的 IP 位址，而是直接使用主機的 IP 位址。此模式對於需要高效能或需要存取網路服務而無需網路位址轉換 (NAT) 開銷的應用程式特別有用。

#### 說明2. 呼叫方式將會改變,port 從3000改為8080,例如:**http://localhost:8080**

#### 說明3. `-d` 需要讓 Docker 容器在後臺以常駐（Daemonized）形式執行。
#### 說明4. `-v open-webui:/app/backend/data`

-v 標誌會將名為 open-webui 的磁碟區掛載到容器內的路徑 /app/backend/data。這允許持久性儲存，意即即使容器停止或移除，寫入此路徑的資料仍會被儲存

以下指令是在主機端找尋目錄

```
docker volume inspect open-webui
```

```bash
cd /var/lib/docker/volumes/
ls
```

#### 說明5. `-e OLLAMA_BASE_URL=http://127.0.0.1:11434`

-e 標誌在容器內設定一個名為 OLLAMA_BASE_URL 的環境變量，容器內執行的應用程式可以使用該變數來引用外部服務或配置

#### 說明6. `--name open-webui`

此選項為容器指派一個自訂名稱（open-webui），以便以後使用其他 Docker 命令更輕鬆地管理和引用

#### 說明7. `--restart always:`

此重啟策略可確保容器在因任何原因（包括系統重新啟動或危機）停止時自動重啟，這對於保持服務持續運作至關重要

#### 說明8. `ghcr.io/open-webui/open-webui:main`
這指定用於建立容器的 Docker 映像，包括其儲存庫 (ghcr.io/open-webui) 和標籤 (main)。如果本機不存在此映像，Docker 將嘗試從指定的登錄中提取它





### 3.2 安裝方式2-(目前有錯誤!尚未解決)

```
docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

>  呼叫方式**http://localhost:3000**


#### 說明
http://host.docker.internal 是 Docker 環境中使用的特殊 DNS 名稱，主要用於從 Docker 容器中存取在主機上執行的服務。以下是其功能和用法的詳細說明：

- 目地: host.docker.internal 的主要功能是允許 Docker 容器與在主機上執行的服務通訊。這在開發過程中特別有用，當您需要存取資料庫、API 或其他本機託管的服務時，您的應用程式會在容器中執行
- 
- 解決方案：當容器嘗試連線到 host.docker.internal 時，它會解析為主機的內部 IP 位址。這允許容器直接向綁定到主機網路介面的服務發送請求

### 手動更新

- 移除

```
docker stop open-webui
docker rm open-webui
docker rmi ghcr.io/open-webui/open-webui:main
```

- 重新安裝