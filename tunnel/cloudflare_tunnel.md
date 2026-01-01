# Cloudflare Tunnel
Cloudflare Tunnel 是一種安全將內部資源連接到 Cloudflare 全球網路的工具，無需公開 IP 位址。 它透過輕量級守護程式 cloudflared 建立僅出站連線，讓流量雙向傳輸而不暴露伺服器。

## 申請個人網址流程
> 核心概念一句話：  
> 只要 Nameserver 已經指向 Cloudflare，這個網域就「不再由 GoDaddy 管理 DNS」了

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



## cloudflare專案內使用申請的`網址`
## godaddy.com改變Name Server位址
## cloudflare Tunnel
