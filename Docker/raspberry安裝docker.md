# 樹莓派安裝 Docker 完整指南

歡迎來到 Docker 的世界！

這份文件是為初學者設計的，旨在幫助你輕鬆地在你的電腦或 Raspberry Pi 上安裝並開始使用 Docker。別擔心，我們會用最簡單的方式帶你入門！

---

## 1. Docker 是什麼？

![host_image_container關係圖](./images/host_image_container關係圖.png)

想像一下，你正在做一個很酷的專案（例如一個網站），它需要在特定的環境和一堆軟體上才能運行。當你把專案交給同學或老師時，他們可能因為環境不同而無法順利運行。

**Docker 就是來解決這個問題的！**

-   **就像一個「軟體貨櫃」**：Docker 可以將你的應用程式，連同它需要的所有東西（函式庫、設定、環境變數等）全部打包在一起，放進一個標準化的「貨櫃 (Container)」裡。
-   **到處都能跑**：這個貨櫃可以在任何安裝了 Docker 的機器上運行，無論是 Windows、macOS 還是 Linux (像你的 Raspberry Pi)，都能保證環境完全一致。
-   **輕量且快速**：跟傳統的虛擬機比起來，Docker 容器更小、啟動更快，也更節省資源。

簡單來說，Docker 讓軟體開發、分享和部署變得超級簡單又可靠。

---

## 📋 目錄
- [系統需求](#系統需求)
- [前置準備](#前置準備)
- [安裝步驟](#安裝步驟)
- [驗證安裝](#驗證安裝)
- [常見問題排除](#常見問題排除)
- [基本使用範例](#基本使用範例)

---

## 🖥️ 系統需求

### 硬體需求
- **Raspberry Pi 5** (推薦) 或 Raspberry Pi 4,3B+
- **記憶體**: 至少 4GB RAM (Docker 需要足夠記憶體)
- **儲存空間**: 至少 32GB microSD 卡
- **網路連線**: 穩定的網際網路連線

### 軟體需求
- **作業系統**: Raspberry Pi OS (64-bit) 或 Ubuntu 20.04+
- **架構**: ARM64 (aarch64) 或 ARMv7

---

## 🔧 前置準備

### 1. 更新系統套件
```bash
# 更新套件清單
sudo apt update

# 升級系統套件
sudo apt upgrade -y

# 安裝必要的工具
sudo apt install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

### 2. 檢查系統架構

請先確認您的作業系統與架構，這樣才能在 Docker Hub 上找到相容且正確的映像檔。

> aarch64 代表 "ARM Architecture 64-bit"。
> aarch64 是 ARM 公司推出的 ARMv8-A 指令集架構 中 64 位元執行狀態的名稱。

```bash
# 檢查系統架構
uname -m #aarch64

# 檢查作業系統版本
lsb_release -a
```

---

## 📦 安裝步驟

### 方法：使用官方安裝腳本 (推薦)

#### 1. 下載並執行 Docker 官方安裝腳本
```bash
# 下載安裝腳本
curl -fsSL https://get.docker.com -o get-docker.sh

# 執行安裝腳本
sudo sh get-docker.sh
```

#### 2. 將使用者加入 docker 群組
```bash
# 將目前使用者加入 docker 群組
sudo usermod -aG docker $USER

# 立即讓群組設定生效（執行後，無需登出即可讓 $USER 擁有 docker 權限）
newgrp docker
```


## ✅ 驗證安裝

### 1. 檢查 Docker 版本
```bash
# 檢查 Docker 版本
docker --version

# 檢查 Docker Compose 版本 (新版語法)
docker compose version
```

### 2. 執行 Hello World 測試 Docker 是否正常運作
執行一個簡單的 `hello-world` 容器，這是驗證 Docker 是否安裝成功並能正常運作的最基本方法。
```bash
# 執行 hello-world 容器
docker run hello-world
```
如果看到 "Hello from Docker!" 的訊息，代表您的 Docker 環境已準備就緒！

接著，您可以檢查更詳細的 Docker 系統資訊。
```bash
# 檢查 Docker 系統資訊
docker system info
```

### 3. 檢查 Docker 服務狀態
```bash
# 檢查 Docker 服務狀態
sudo systemctl status docker

# 檢查 Docker 是否正在執行
sudo systemctl is-active docker
```

---

## 🔍 常見問題排除

### 問題 1: 權限不足錯誤
**錯誤訊息**: `permission denied while trying to connect to the Docker daemon socket`

**解決方案**:
```bash
# 確認使用者已加入 docker 群組
groups $USER

# 如果沒有看到 docker 群組，重新加入
sudo usermod -aG docker $USER

# 重新登入或重新載入群組
newgrp docker
```

### 問題 2: 記憶體不足
**錯誤訊息**: `no space left on device` 或容器無法啟動

**解決方案**:
```bash
# 清理 Docker 系統
docker system prune -a

# 檢查磁碟使用量
df -h

# 清理未使用的映像檔
docker image prune -a
```

### 問題 3: 網路連線問題
**錯誤訊息**: 無法拉取映像檔

**解決方案**:
```bash
# 檢查網路連線
ping google.com

# 檢查 Docker 網路設定
docker network ls

# 重設 Docker 網路
sudo systemctl restart docker
```

### 問題 4: ARM 架構相容性
**解決方案**:
```bash
# 搜尋 ARM 相容的映像檔
docker search --filter is-official=true nginx

# 使用多平台映像檔
docker pull --platform linux/arm64 nginx:latest
```

---

## 🚀 基本使用範例

### 1. 執行簡單的 Web 伺服器
```bash
# 使用 Nginx
docker run -d -p 8080:80 --name my-nginx nginx:alpine

# 檢查容器狀態
docker ps

# 測試網頁
curl http://localhost:8080
```

### 2. 建立並執行 Python 應用程式
```bash
# 建立 Python 應用程式目錄
mkdir ~/python-app
cd ~/python-app

# 建立 app.py
cat > app.py << EOF
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello from Raspberry Pi Docker!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

# 建立 Dockerfile
cat > Dockerfile << EOF
FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
EOF

# 建立 requirements.txt (建議使用較新版本)
echo "Flask>=3.0.0" > requirements.txt

# 建構映像檔
docker build -t my-python-app .

# 執行容器
docker run -d -p 5000:5000 --name my-app my-python-app
```

### 3. 使用 Docker Compose
```bash
# 建立 compose.yaml (新版 Docker Compose 建議的檔名)
# 注意：新版的 Compose 檔案不再需要頂層的 'version' 標籤
cat > compose.yaml << EOF
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
EOF

# 啟動服務 (Docker 會自動尋找 compose.yaml)
docker compose up -d

# 停止服務
docker compose down
```

---

## 📊 效能優化建議

### 1. 限制容器的記憶體使用
Raspberry Pi 記憶體有限，直接限制每個容器可以使用的資源，是更直接有效的優化方式。現代的 Raspberry Pi OS 預設已啟用記憶體管理功能 (cgroups)，您無需手動修改系統啟動設定。

您可以在執行容器時，透過參數來限制其記憶體用量：
```bash
# 執行一個 Nginx 容器，並限制其最多使用 256MB 記憶體
docker run -d -p 8080:80 --name my-limited-nginx --memory="256m" nginx:alpine
```
- `--memory="256m"`: 設定容器可使用的最大記憶體。
- 您也可以加上 `--memory-swap` 來限制 Swap 空間。

### 2. 儲存空間優化
```bash
# 定期清理 Docker 系統，包含未使用的容器、網路、映像檔和建置快取
docker system prune -a

# 若要連同未使用的 volume 一起刪除，請加上 --volumes 旗標 (請謹慎使用)
docker system prune -a --volumes

# 設定自動清理 (建立 cron 工作)，例如在每天凌晨 2 點執行
# 注意：-f 會強制執行，不會跳出確認訊息
(sudo crontab -l 2>/dev/null; echo "0 2 * * * /usr/bin/docker system prune -af") | sudo crontab -
```

### 3. 網路優化
```bash
# 使用本地映像檔快取
docker pull hello-world
```

---

## 🔗 相關資源

- [Docker 官方文件](https://docs.docker.com/)
- [Raspberry Pi 官方文件](https://www.raspberrypi.org/documentation/)
- [Docker Hub](https://hub.docker.com/)
- [ARM 映像檔清單](https://github.com/docker-library/official-images)

---

## 📝 注意事項

1. **記憶體限制**: Raspberry Pi 的記憶體有限，建議只執行必要的容器
2. **ARM 架構**: 確保使用的映像檔支援 ARM 架構
3. **效能考量**: Docker 在樹莓派上的效能會比在 x86 系統上慢
4. **儲存空間**: 定期清理未使用的映像檔和容器以節省空間
5. **安全性**: 避免在生產環境中執行有安全風險的容器

---

**🎉 恭喜！您已成功在 Raspberry Pi 上安裝並設定 Docker！**

如有任何問題，請參考上述的常見問題排除章節，或查閱 Docker 官方文件。
