# Cloudflare Tunnel
Cloudflare Tunnel 是一種安全將內部資源連接到 Cloudflare 全球網路的工具，無需公開 IP 位址。 它透過輕量級守護程式 cloudflared 建立僅出站連線，讓流量雙向傳輸而不暴露伺服器。

## 申請個人網址流程
> 核心概念一句話：  
> 只要 Nameserver 已經指向 Cloudflare，這個網域就「不再由 GoDaddy 管理 DNS」了

![網域管轄權的轉移](./images/網域管轄權的轉移.png)

### 申請流程:
- 步驟1: godaddy.com申請1年用的個人網址(NT:50元以內)
- 步驟2: 登入 cloudflare.com，以申請的`個人網址`建立專案，進入DNS(Domain Name Server)的設定頁面，查看Cloudflare名稱伺服器的網址(一般都是2組)
- 步驟3: 回到godaddy.com,的`DNS`頁面,進入`Nameservers`,將Cloudflare提供的2組伺服器填入至Nameservers內

### 驗證方式:
**GUI視覺方式**

1. 進入至Cloudflare專案,檢查專案狀態是否為`使用中`
2. 進入至Cloudflare內的`DNS->記錄`,確認是否可以編輯

**CLI方式**

使用DNS查詢工具,樹莓派DNS查詢工具預設沒有安裝,請安裝

```bash
sudo apt update
sudo apt install dnsutils
```

```bash
nslookup -type=NS 你的網址
```

```bash
dig NS 你的網址
```

> 如果有cloudflare提供的2組伺服器網址,代表正確

> [Cloudflare Tunnel Guide簡報檔下載](./Cloudflare_Tunnel_Guide.pptx)

## cloudflare Tunnel的設定

1. 在Cloudflare 建立隧道名稱(任意名稱),依據指示,安裝適當的軟體

有2種方式可以啟動Tunnel:

1. 在機器上安裝 cloudflared 後，可以安裝服務，以便在機器啟動時自動執行 Tunnel

2. 只在目前的終端工作階段中手動執行 Tunnel:

驗証方式:
檢查下方的Connectors是否已經有連接器連線

2. 設立主機名稱和服務

- 主機名稱:設定子網域,例如->open-webui.網域名稱
- 服務:本機端的網址,例如->http://localhost:8080



### 步驟 1: 安裝 cloudflared
在 Raspberry Pi 或伺服器上執行：

```

```
