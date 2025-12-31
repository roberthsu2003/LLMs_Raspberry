# Ngrok Tunnel

## Ngrok Tunnel是什麼

ngrok tunnel 是一種反向隧道工具，用來將本機 localhost 的服務暴露到公網，讓外部使用者能透過臨時網址存取。

## 運作原理

ngrok 透過建立安全的反向代理通道，將遠端公網請求轉發到本地指定端口，例如將 ngrok.io 的流量 forwarding 到 localhost:3000。它支援穿透 NAT 或防火牆，無需設定路由器或公開端口。

![ngrok連線示意圖](./images/ngrok.png)

## 常見用途

- 開發階段 demo 本地 web 伺服器給團隊或客戶測試。
- 測試第三方 API 回調，如支付金流或 webhook。
- 產生 公網的HTTPS 網址，支援基本認證保護（如 ngrok http --auth=user:pass 3000）。

## 安裝流程

1. 申請ngrok網址
   - 訪問 [ngrok 網站](https://ngrok.com/)，註冊帳號並獲取 token。
   
   - 安裝ngrok應用程式
   
```bash 
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz
tar xvzf ngrok-v3-stable-linux-arm64.tgz
sudo mv ngrok /usr/local/bin/
ngrok version
rm ngrok-v3-stable-linux-arm64.tgz
  ```
  
   - 保留認證token
   - 記得你的公用網址
   

2. 配置 ngrok token
   - 下載 ngrok 後，執行 `ngrok config add-authtoken <YOUR_TOKEN>`，將 token 設定到 ngrok。

下載 ngrok 後，執行 `ngrok http 3000` 即可產生公網網址，如 [https://abc123.ngrok.io](https://abc123.ngrok.io) 指向本地 3000 端口。免費版有流量限制，付費版提供自訂域名與更多功能。

### 第二部分：學習範例 (Learning Example)

這裡我們使用 **Local Port Forwarding (本地通訊埠轉發)** 作為最經典的入門範例。

#### 步驟 1：在 Raspberry Pi 上製造一個「情境」

我們需要一個「只有 Pi 自己看得到」的服務。使用 Python 內建的 HTTP 伺服器最快。

請學生在 Raspberry Pi 上輸入：

Bash

```other
# 在 Pi 上建立一個簡單的測試資料夾
mkdir tunnel_test
cd tunnel_test
echo "<h1>Hello from the Secret Tunnel!</h1>" > index.html

# 啟動網頁伺服器，限定只能由 localhost (127.0.0.1) 存取，Port 為 8080
# 進入tunnel_test的資料夾
python3 -m http.server --bind 127.0.0.1 8080
```

#### 步驟 2：在 Windows 上使用 ngrok 連接 Pi 的服務

請學生在 Windows 上輸入：

Bash

```other
ngrok http 8080
```

> **驗證點：** 嘗試直接用手機連線到`你的公用網址`
