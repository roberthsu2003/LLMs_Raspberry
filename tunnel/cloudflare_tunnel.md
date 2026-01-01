# Cloudflare Tunnel

Cloudflare Tunnel 是一種能夠安全地將您的內部服務連接到 Cloudflare 全球網路的工具，而無需對外暴露公開的 IP 位址。它透過在您的伺服器上運行的輕量級代理程式 `cloudflared`，建立一個僅限對外的安全連線，讓內外部流量可以雙向傳輸。

## 前置作業：設定個人網域

> 核心觀念：**一旦將網域的名稱伺服器 (Nameserver) 指向 Cloudflare，DNS 的管理權限即由 Cloudflare 接管，而非原註冊商（如 GoDaddy）。**

![網域管轄權的轉移](./images/網域管轄權的轉移.png)

### 步驟一：註冊網域並更新名稱伺服器

1.  **註冊網域**：於網域註冊商（如 [GoDaddy](https://godaddy.com)）申請一個個人網域。
2.  **新增網站至 Cloudflare**：登入 [Cloudflare](https://cloudflare.com)，將您剛申請的網域新增為一個站點。進入該站點的 DNS 設定頁面，Cloudflare 會提供兩組專屬的名稱伺服器 (Nameserver) 位址。
3.  **更新名稱伺服器**：回到 GoDaddy 的 DNS 管理頁面，找到「名稱伺服器 (Nameservers)」設定，將其從 GoDaddy 預設值更改為 Cloudflare 提供的那兩組位址。

### 步驟二：驗證網域設定

您可以透過以下任一方式，確認您的網域是否已成功交由 Cloudflare 管理。

**圖形化介面 (GUI) 驗證**

1.  登入 Cloudflare，檢查您網域專案的狀態是否顯示為 **`使用中 (Active)`**。
2.  導覽至專案內的 **`DNS > 記錄 (Records)`** 頁面，確認您有權限新增或編輯 DNS 記錄。

**命令列介面 (CLI) 驗證**

您可以使用 `nslookup` 或 `dig` 等 DNS 查詢工具。若您的系統（如 Raspberry Pi）尚未安裝，請執行以下指令：
```bash
sudo apt update
sudo apt install dnsutils
```

接著，查詢您網域的 NS (Name Server) 記錄：
```bash
# 使用 nslookup
nslookup -type=NS your-domain.com

# 或使用 dig
dig NS your-domain.com
```
如果回傳的結果是 Cloudflare 提供的那兩組伺服器位址，即代表設定正確。

> **相關資源**：[Cloudflare Tunnel 簡報檔下載](./Cloudflare_Tunnel_Guide.pptx)

## 設定 Cloudflare Tunnel

> 核心觀念：**建立一個 Tunnel 通道，並在您的裝置上執行 `cloudflared` 程式來連接它。接著，設定一個公開的主機名稱 (例如 `app.yourdomain.com`)，並將其對應到您本機的服務 (例如 `http://localhost:8080`)。**

### 步驟一：建立 Tunnel

1.  在 Cloudflare 儀表板，導覽至 **`Zero Trust`**。
2.  在左側選單中，選擇 **`網路 (Network) > 連接器`**。
3.  點擊 **`建立 Tunnel (Create a Tunnel)`**，並為您的 Tunnel 設定一個易於識別的名稱。

### 步驟二：安裝並執行 Connector

Cloudflare 會提供對應您作業系統的安裝指令。安裝後，有兩種執行 `cloudflared` 的方式：

*   **作為服務執行 (建議用於正式環境)**：
    安裝並設定為系統服務，讓 `cloudflared` 能在開機時自動啟動，確保 Tunnel 連線持續在線。
*   **手動執行 (適用於開發與測試)**：
    直接在終端機中執行指令，Tunnel 將只在當前的終端機工作階段中運行，關閉即中斷。

**連線驗證**：執行指令後，回到 Cloudflare 的 Tunnel 設定頁面，檢查下方的 **`Connectors`** 區塊是否出現新的連線紀錄，並顯示為健康狀態。

### 步驟三：設定公開主機名稱 (Public Hostname)

這是最後一步，將公開的網址指向您本機的服務。

-   **主機名稱 (Hostname)**：設定您要公開的子網域 (subdomain)。例如，`open-webui.your-domain.com`。
-   **服務 (Service)**：選擇協定 (HTTP/HTTPS等) 並填寫本機服務的位址。例如，`http://localhost:8080`。

儲存後，任何人即可透過您設定的主機名稱，安全地存取您本機的服務。

之後，您可以在 Cloudflare 的 Tunnel 設定頁面，透過 **通道名稱** 區塊的狀態來判斷連線是否成功。正常連線時會顯示 **`連線`**，若中斷則會顯示 **`關閉`**。
