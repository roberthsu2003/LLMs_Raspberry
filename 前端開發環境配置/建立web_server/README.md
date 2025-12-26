將樹莓派（Raspberry Pi）變成一個簡單的 Web Server 是一項非常經典且有趣的實作。要顯示簡單的 HTML、CSS 和 JavaScript，最推薦且最穩定的方式是使用 **Apache** 或 **Nginx**。

使用 **Nginx** 來架設web server，因為它輕量、效能高，非常適合在樹莓派上運行。

---

## 什麼是 Nginx？

Nginx (發音為 "Engine-X") 是一個高性能的 HTTP 和反向代理伺服器。它以「事件驅動（Event-driven）」的架構聞名，這意味著它可以用非常少的記憶體資源處理大量的連線，非常適合硬體資源有限的樹莓派。

### 核心功能與優勢
1.  **高併發處理**：相比傳統的 Apache，Nginx 在處理大量同時連線時表現更優異。
2.  **反向代理 (Reverse Proxy)**：可以作為前端伺服器，將流量轉發給後端的應用程式（如 Node.js, Python Flask/Django）。
3.  **負載均衡 (Load Balancing)**：如果有服務集群，Nginx 可以協助分配流量。
4.  **靜態檔案服務**：處理圖片、CSS、JS 等靜態檔案的速度極快。

---

---

### 第一步：更新系統

在開始安裝任何軟體之前，請先確保你的樹莓派系統是最新的。打開終端機（Terminal）並輸入：

```bash
sudo apt update
sudo apt upgrade -y

```

### 第二步：安裝 Nginx

Nginx 是一個高效能的 HTTP 伺服器，安裝指令如下：

```bash
sudo apt install nginx -y

```

安裝完成後，伺服器會自動啟動。

### 第三步：測試伺服器是否運行

你可以從同一個區域網路（Wi-Fi）下的另一台電腦或手機，在瀏覽器網址列輸入**樹莓派的 IP 位址**。

> **如何查看 IP？** 在終端機輸入 `hostname -I`。

如果你看到「Welcome to nginx!」的畫面，代表你的伺服器已經成功上線了！

---

### 第四步：放置你的 HTML、CSS 和 JS 檔案

Nginx 預設存放網頁檔案的路徑是 `/var/www/html`。

1. **進入該目錄：**
```bash
cd /var/www/html

```


2. **建立你的網頁檔案：**
你可以刪除預設的 `index.nginx-debian.html`，並建立自己的 `index.html`。
```bash
sudo rm index.nginx-debian.html
sudo nano index.html

```


3. **輸入簡單的範例代碼：**
在編輯器中貼上這段簡單的程式碼：
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: sans-serif; text-align: center; background-color: #f4f4f4; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>我的樹莓派伺服器</h1>
    <p id="demo">這是一個簡單的網頁。</p>
    <button onclick="changeText()">點我試試 JS</button>

    <script>
        function changeText() {
            document.getElementById("demo").innerHTML = "JavaScript 運作正常！";
        }
    </script>
</body>
</html>

```


*按下 `Ctrl + O` 存檔，`Ctrl + X` 離開。*

---

### 第五步：瀏覽器重新載入

現在回到你的瀏覽器並重新載入頁面，你就能看到你自己寫的 HTML 內容，並且點擊按鈕也能觸發 JavaScript 效果了。

### nginx的控制指令

```bash
sudo systemctl restart nginx #重新啟動nginx
sudo systemctl stop nginx #停止nginx
sudo systemctl start nginx #啟動nginx
sudo systemctl status nginx #查看nginx狀態
sudo systemctl reload nginx #重新載入nginx
```

---

## Nginx 設定檔結構說明書

Nginx 的強大來自於其靈活的設定檔。了解其結構對未來進行進階設定（如綁定網域、HTTPS）非常重要。

### 主要設定檔位置
*   **主設定檔**：`/etc/nginx/nginx.conf` (全域設定)
*   **站點設定檔**：`/etc/nginx/sites-available/` (存放所有設定) 與 `/etc/nginx/sites-enabled/` (存放已啟用設定)

### 設定檔層級結構 (`nginx.conf`)
Nginx 設定檔由「區塊 (Block)」組成，層級如下：

```nginx
# 全域區塊 (Global Block)：設定 user, worker_processes 等
user www-data;
worker_processes auto;

events {
    # events 區塊：設定最大連線數
    worker_connections 768;
}

http {
    # http 區塊：設定 web 相關參數，如 mime types, log format
    
    server {
        # server 區塊：定義一個虛擬主機 (Virtual Host)
        listen 80;
        server_name example.com; # 網域名稱

        location / {
            # location 區塊：URL 匹配規則
            root /var/www/html;
            index index.html;
        }

        location /api {
            # 反向代理範例
            proxy_pass http://localhost:3000;
        }
    }
}
```

### 常用指令速查
| 指令 | 說明 | 範例 |
| :--- | :--- | :--- |
| `worker_processes` | 工作進程數，通常設為 `auto` (與 CPU 核心數相同) | `worker_processes auto;` |
| `listen` | 監聽的端口 (Port) | `listen 80;` |
| `server_name` | 該站點綁定的網域名稱 | `server_name mypi.local;` |
| `root` | 靜態檔案的根目錄路徑 | `root /var/www/my-site;` |
| `index` | 預設首頁檔案名稱 | `index index.html;` |
| `proxy_pass` | 將請求轉發給其他伺服器 (反向代理) | `proxy_pass http://127.0.0.1:5000;` |

---

## Nginx 靜態網頁部署設定：預設目錄 vs 自訂目錄

在配置 Nginx serving 靜態檔案時，主要有兩種檔案放置策略：

### 1. 使用預設目錄 (Default Directory)
Nginx 安裝後會預設一個網頁根目錄，通常位於 `/var/www/html`。

*   **特點**：
    *   **快速上手**：無需修改 Nginx 的主要設定檔，服務啟動即可看到內容。
    *   **結構單純**：適合單一專案或是剛開始學習伺服器部署時使用。
*   **操作方式**：如上述「第四步」所示，直接將檔案放入 `/var/www/html` 即可。

### 2. 使用自訂目錄 (Custom Directory)
實際開發中，我們通常會希望將網站檔案放在自己規劃的專案路徑下（例如 `/home/pi/projects/my-web`），而不是系統預設路徑。

*   **特點**：
    *   **管理靈活**：可以將不同專案分開管理，便於版本控制（Git）與備份。
    *   **多站點支援**：透過設定不同的 `server` block，可以在同一台伺服器上同時運行多個網站。

*   **Nginx 設定檔架構說明**：
    
    在了解如何修改設定之前，先認識 Nginx 的兩種設定檔類型：

    **🎯 主設定檔 (`/etc/nginx/nginx.conf`)**：
    - **比喻**：就像一間餐廳的「總管理規則手冊」，定義整間餐廳的運作原則
    - **功能**：設定 Nginx 的全域參數，例如：
        - 工作進程數量（`worker_processes`）
        - 記錄檔位置（`error_log`、`access_log`）
        - 系統層級的設定
    - **特點**：通常不需要頻繁修改，除非要調整伺服器效能或進階功能
    - **情境**：就像餐廳規定「所有員工都要遵守衛生標準」、「每桌服務時間不超過30分鐘」這類全餐廳通用的規則

    **📋 站點設定檔 (`/etc/nginx/sites-available/` 目錄下的檔案)**：
    - **比喻**：就像每個「分店的營運手冊」，定義每個網站的具體運作方式
    - **功能**：設定特定網站的參數，例如：
        - 網站檔案的位置（`root`）
        - 監聽的端口（`listen`）
        - 網域名稱（`server_name`）
        - 網站的處理規則（`location` blocks）
    - **特點**：每個網站可以有獨立的設定檔，便於管理多個網站
    - **情境**：就像 A 分店規定「我們的招牌菜單在這個文件夾裡」、「顧客從80號門進入」，而 B 分店可能有不同的規則
    
    **📂 檔案結構**：
    ```
    /etc/nginx/
    ├── nginx.conf                    # 主設定檔（總規則）
    ├── sites-available/              # 可用的站點設定檔（所有分店手冊）
    │   ├── default                   # 預設站點（主要分店）
    │   └── my-website                # 自訂站點（另一間分店）
    └── sites-enabled/                # 啟用的站點設定檔（正在營業的分店）
        └── default -> ../sites-available/default  # 符號連結
    ```
    
    **💡 工作流程**：
    1. 在 `sites-available/` 中建立或編輯站點設定檔（就像寫好分店手冊）
    2. 建立符號連結到 `sites-enabled/` 來啟用網站（就像把分店手冊放到「正在營業」資料夾）
    3. 測試設定：`sudo nginx -t`（檢查手冊有沒有錯誤）
    4. 重新載入：`sudo systemctl reload nginx`（讓新規則生效）

*   **配置範例**：
    需要修改 Nginx 的站點設定檔 (通常位於 `/etc/nginx/sites-available/default`)，將 `root` 指令指向你的自訂資料夾路徑。

    1. 編輯設定檔：
       `sudo nano /etc/nginx/sites-available/default`

    2. 修改 `root` 路徑：
       ```nginx
       server {
           listen 80 default_server;
           listen [::]:80 default_server;

           # 將 root 指向你的自訂專案資料夾 (例如 /home/pi/my-website)
           root /home/pi/my-website; 
           
           index index.html index.htm index.nginx-debian.html;

           server_name _;

           location / {
               try_files $uri $uri/ =404;
           }
       }
       ```

### 注意事項
*   **檔案權限 (Permissions)**：使用自訂目錄時，最常遇到的問題是 `403 Forbidden`。這通常是因為 Nginx 的執行使用者（通常是 `www-data`）沒有權限讀取你的 `home` 目錄。
    *   **解決方式**：確保你的專案資料夾和其上層目錄對其他使用者有讀取/執行權限。
    *   指令範例：`chmod 755 /home/pi`
*   **設定生效**：修改設定檔後，務必測試語法並重啟 Nginx：
    *   `sudo nginx -t` (檢查語法)
    *   `sudo systemctl reload nginx` (重啟)

---

### 進階建議

* **使用 FTP 上傳檔案：** 如果你想在電腦上寫好代碼再傳到樹莓派，建議安裝 **FileZilla** 並透過 SFTP（使用樹莓派的帳號密碼）連接，這樣管理檔案會方便很多。
* **固定 IP：** 建議在路由器設定中將樹莓派的 IP 固定，這樣下次開機時網址才不會變動。

你需要我進一步說明如何從**外部網路（家以外的地方）**連回你的樹莓派伺服器嗎？（這通常涉及「內網穿透」或「虛擬伺服器設定」）