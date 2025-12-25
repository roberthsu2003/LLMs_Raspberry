將樹莓派（Raspberry Pi）變成一個簡單的 Web Server 是一項非常經典且有趣的實作。要顯示簡單的 HTML、CSS 和 JavaScript，最推薦且最穩定的方式是使用 **Apache** 或 **Nginx**。

使用 **Nginx** 來架設web server，因為它輕量、效能高，非常適合在樹莓派上運行。

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

### 進階建議

* **使用 FTP 上傳檔案：** 如果你想在電腦上寫好代碼再傳到樹莓派，建議安裝 **FileZilla** 並透過 SFTP（使用樹莓派的帳號密碼）連接，這樣管理檔案會方便很多。
* **固定 IP：** 建議在路由器設定中將樹莓派的 IP 固定，這樣下次開機時網址才不會變動。

你需要我進一步說明如何從**外部網路（家以外的地方）**連回你的樹莓派伺服器嗎？（這通常涉及「內網穿透」或「虛擬伺服器設定」）