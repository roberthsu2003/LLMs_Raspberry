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

> 1. Docker 中的 --network=host 選項允許容器共用主機的網路命名空間，這表示容器沒有自己的 IP 位址，而是直接使用主機的 IP 位址。此模式對於需要高效能或需要存取網路服務而無需網路位址轉換 (NAT) 開銷的應用程式特別有用。

> 2. ## 呼叫方式將會改變,port 從3000改為8080,例如:http://localhost:8080

### 3.2 安裝方式2

```
docker run -d -p 3000:8080 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

> ## 呼叫方式http://localhost:3000

#### 說明
http://host.docker.internal 是 Docker 環境中使用的特殊 DNS 名稱，主要用於從 Docker 容器中存取在主機上執行的服務。以下是其功能和用法的詳細說明：

- 目地: host.docker.internal 的主要功能是允許 Docker 容器與在主機上執行的服務通訊。這在開發過程中特別有用，當您需要存取資料庫、API 或其他本機託管的服務時，您的應用程式會在容器中執行
- 
- 解決方案：當容器嘗試連線到 host.docker.internal 時，它會解析為主機的內部 IP 位址。這允許容器直接向綁定到主機網路介面的服務發送請求
