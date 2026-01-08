# 部署至樹莓派的方式

本指南說明如何將前端專案部署到樹莓派，包括使用 FileZilla、SSH 指令等方式。

> 💡 **學習目標**：完成本指南後，你將能夠：
> - 將本地開發的前端專案上傳到樹莓派
> - 使用多種方式進行檔案傳輸
> - 驗證部署是否成功
> - 解決常見的部署問題

---

## 🚀 快速開始（5 分鐘完成第一次部署）

如果你是第一次部署，建議先完成這個快速開始，建立信心後再深入了解其他方法。

### 前置條件檢查

在開始之前，請確認：

1. **樹莓派已開機並連接到網路**
   ```bash
   # 在樹莓派上執行，查看 IP 位址
   hostname -I
   # 記下顯示的 IP，例如：192.168.1.100
   ```

2. **樹莓派已安裝 Nginx**（如果還沒安裝，請先參考 [建立web_server](../建立web_server/README.md)）

3. **你有一份前端專案**（建議使用 [1_javascript](../1_javascript/README.md) 範例專案）

### 快速部署步驟

**步驟 1：準備專案檔案**

```bash
# 在你的電腦上，進入專案目錄
cd 前端開發環境配置/1_javascript

# 確認 public 資料夾存在（這是我們要上傳的內容）
ls public/
# 應該看到：index.html, css/, js/ 等檔案
```

**步驟 2：使用 SCP 上傳（最簡單的方法）**

```bash
# 將 [樹莓派IP] 替換為你的樹莓派 IP
# 將 public 資料夾上傳到樹莓派
scp -r public pi@[樹莓派IP]:/home/pi/my-website

# 例如：
# scp -r public pi@192.168.1.100:/home/pi/my-website
```

**步驟 3：在樹莓派上設定 Nginx**

```bash
# SSH 連線到樹莓派
ssh pi@[樹莓派IP]

# 編輯 Nginx 設定檔
sudo nano /etc/nginx/sites-available/default
```

找到 `root` 這一行，修改為：
```nginx
root /home/pi/my-website/public;
```

儲存並離開（`Ctrl+O` 存檔，`Ctrl+X` 離開）

**步驟 4：重新載入 Nginx**

```bash
# 測試設定檔是否正確
sudo nginx -t

# 如果顯示 "syntax is ok"，重新載入 Nginx
sudo systemctl reload nginx
```

**步驟 5：驗證部署成功** ✅

1. 在瀏覽器中打開：`http://[樹莓派IP]`
2. 你應該能看到你的網頁！
3. 測試互動功能（點擊按鈕、檢查動畫等）

> 🎉 **恭喜！** 你已經成功完成第一次部署！

---

## 📋 前置準備（詳細說明）

### 1. 確認樹莓派連線資訊

在開始部署前，你需要知道以下資訊：

- **IP 位址**：例如 `192.168.1.100`
  ```bash
  # 在樹莓派上執行
  hostname -I
  ```
  
- **使用者名稱**：通常是 `pi` 或你設定的使用者名稱
- **SSH 埠號**：預設為 `22`
- **目標目錄**：例如 `/var/www/html` 或 `~/projects`

### 2. 確認樹莓派上已安裝的服務

- **Nginx** 或 **Apache**（用於網頁伺服器）
  ```bash
  # 檢查 Nginx 是否安裝
  nginx -v
  
  # 如果沒有安裝，請參考 [建立web_server](../建立web_server/README.md)
  ```
  
- **Node.js** 和 **npm**（如果專案需要，純 HTML/CSS/JS 專案不需要）

---

## 方法一：使用 FileZilla（圖形化界面）

FileZilla 是一個免費的 FTP/SFTP 客戶端軟體，適合不熟悉命令列的使用者。

### 步驟 1：下載並安裝 FileZilla

1. 前往 [FileZilla 官網](https://filezilla-project.org/)下載
2. 安裝完成後開啟 FileZilla

### 步驟 2：建立 SFTP 連線

1. 在 FileZilla 頂部輸入連線資訊：
   - **主機**：`sftp://樹莓派IP位址` 或直接輸入 IP（例如：`sftp://192.168.1.100`）
   - **使用者名稱**：樹莓派的使用者名稱（例如：`pi`）
   - **密碼**：樹莓派的使用者密碼
   - **埠號**：`22`

2. 點擊「快速連線」

### 步驟 3：上傳檔案

1. **左側視窗**：本地電腦的檔案
2. **右側視窗**：樹莓派的檔案系統

**上傳步驟：**
- 在左側找到要上傳的專案資料夾（例如：`public` 資料夾）
- 在右側導航到目標目錄（例如：`/home/pi/my-website`）
- 將檔案或資料夾從左側拖曳到右側
- 等待上傳完成（底部會顯示傳輸狀態）

**💡 提示：**
- 如果上傳失敗，檢查樹莓派是否有足夠的磁碟空間：`df -h`
- 大型專案可能需要幾分鐘，請耐心等待

### 步驟 4：設定檔案權限（如果需要）

在右鍵選單中選擇「檔案權限」，設定為 `755`（目錄）或 `644`（檔案）。

**或者使用 SSH 指令設定：**
```bash
# SSH 連線到樹莓派
ssh pi@[樹莓派IP]

# 設定權限
chmod -R 755 /home/pi/my-website
```

### 步驟 5：驗證上傳成功 ✅

在 FileZilla 右側視窗中，確認檔案已正確上傳：
- 檢查檔案數量是否正確
- 檢查檔案大小是否合理
- 確認資料夾結構完整（例如：`css/`, `js/` 資料夾都存在）

---

## 方法二：使用 SCP 指令（命令列）

SCP（Secure Copy）是透過 SSH 進行檔案傳輸的命令列工具。

### 基本語法

```bash
scp [選項] <來源路徑> <使用者名稱>@<主機IP>:<目標路徑>
```

### 範例 1：上傳單一檔案

```bash
# 上傳單一 HTML 檔案
scp /本地路徑/index.html pi@192.168.1.100:/var/www/html/
```

**實際操作範例：**
```bash
# 假設你在專案目錄中
cd 前端開發環境配置/1_javascript
scp public/index.html pi@192.168.1.100:/home/pi/my-website/
```

### 範例 2：上傳整個資料夾（推薦）

使用 `-r` 參數遞迴複製整個目錄：

```bash
# 上傳整個 public 資料夾
scp -r /本地路徑/專案資料夾 pi@192.168.1.100:/var/www/html/
```

**實際操作範例：**
```bash
# 假設你在專案目錄中
cd 前端開發環境配置/1_javascript
scp -r public pi@192.168.1.100:/home/pi/my-website/
```

**💡 提示：**
- 第一次連線時會詢問是否信任主機，輸入 `yes`
- 需要輸入樹莓派的密碼（預設通常是 `raspberry`）
- 上傳過程中會顯示進度

### 範例 3：指定 SSH 埠號

如果 SSH 使用非預設埠號（例如 2222）：

```bash
scp -P 2222 -r /本地路徑/專案資料夾 pi@192.168.1.100:/var/www/html/
```

### 範例 4：從樹莓派下載檔案

```bash
scp pi@192.168.1.100:/var/www/html/index.html /本地儲存路徑/
```

### 常用選項說明

- `-r`：遞迴複製整個目錄
- `-P`：指定 SSH 埠號（注意：大寫 P）
- `-v`：顯示詳細資訊
- `-C`：啟用壓縮傳輸

---

## 方法三：使用 rsync（推薦，適合大型專案）

`rsync` 可以只同步變更的檔案，適合重複部署和大型專案。

### 安裝 rsync

**macOS：**
```bash
# rsync 通常已預裝，如果沒有可以透過 Homebrew 安裝
brew install rsync
```

**Linux：**
```bash
sudo apt-get install rsync
```

### 基本語法

```bash
rsync [選項] <來源路徑> <使用者名稱>@<主機IP>:<目標路徑>
```

### 範例 1：同步整個專案資料夾

```bash
rsync -avz /本地路徑/專案資料夾/ pi@192.168.1.100:/var/www/html/專案資料夾/
```

**參數說明：**
- `-a`：歸檔模式，保留檔案權限、時間戳等
- `-v`：顯示詳細資訊
- `-z`：傳輸時壓縮，加快速度

### 範例 2：排除特定檔案或資料夾

```bash
rsync -avz --exclude 'node_modules' --exclude '.git' /本地路徑/專案資料夾/ pi@192.168.1.100:/var/www/html/
```

### 範例 3：使用 SSH 金鑰認證

如果你已設定 SSH 金鑰，不需要輸入密碼：

```bash
rsync -avz -e ssh /本地路徑/專案資料夾/ pi@192.168.1.100:/var/www/html/
```

### 範例 4：刪除目標目錄中多餘的檔案

使用 `--delete` 參數，確保目標目錄與來源目錄完全一致：

```bash
rsync -avz --delete /本地路徑/專案資料夾/ pi@192.168.1.100:/var/www/html/專案資料夾/
```

⚠️ **注意**：`--delete` 會刪除目標目錄中不存在的檔案，使用時要小心！

---

## 方法四：使用 Git（適合有版本控制的專案）

如果專案已經使用 Git 版本控制，可以在樹莓派上直接拉取最新版本。

### 步驟 1：在樹莓派上安裝 Git

```bash
sudo apt-get update
sudo apt-get install git
```

### 步驟 2：SSH 連線到樹莓派

```bash
ssh pi@192.168.1.100
```

### 步驟 3：克隆或更新專案

**首次部署（克隆）：**
```bash
cd /var/www/html
git clone https://github.com/使用者名稱/專案名稱.git
```

**更新現有專案：**
```bash
cd /var/www/html/專案名稱
git pull origin main
```

---

## 方法五：使用 SFTP 指令（互動式）

SFTP 提供互動式的檔案傳輸界面。

### 連線到樹莓派

```bash
sftp pi@192.168.1.100
```

### 常用 SFTP 指令

```
# 列出本地檔案
lls

# 列出遠端檔案
ls

# 切換本地目錄
lcd /本地路徑

# 切換遠端目錄
cd /var/www/html

# 上傳檔案
put 檔案名稱

# 上傳資料夾（需要先壓縮）
put -r 資料夾名稱

# 下載檔案
get 檔案名稱

# 退出
exit
```

---

## 📝 部署後續步驟

### 1. 設定檔案權限

SSH 連線到樹莓派後，設定適當的檔案權限：

```bash
ssh pi@192.168.1.100

# 進入專案目錄
cd /var/www/html/專案名稱

# 設定目錄權限
sudo chmod -R 755 .

# 設定檔案權限
sudo find . -type f -exec chmod 644 {} \;

# 設定目錄權限
sudo find . -type d -exec chmod 755 {} \;
```

### 2. 設定檔案擁有者（如果需要）

如果使用 Nginx，通常需要設定為 `www-data`：

```bash
sudo chown -R www-data:www-data /var/www/html/專案名稱
```

### 3. 重啟網頁伺服器

**Nginx：**
```bash
sudo systemctl restart nginx
```

**Apache：**
```bash
sudo systemctl restart apache2
```

### 4. 測試網站

在瀏覽器中訪問：`http://樹莓派IP位址`

**驗證清單：** ✅
- [ ] 網頁可以正常載入
- [ ] CSS 樣式正確顯示（檢查顏色、佈局）
- [ ] JavaScript 功能正常（點擊按鈕測試）
- [ ] 圖片和資源正確載入
- [ ] 沒有 404 錯誤（按 F12 打開開發者工具檢查）

**如果遇到問題，請參考下方的「常見問題」章節。**

---

## 🔧 針對不同專案類型的部署

### 純 HTML/CSS/JavaScript 專案

直接上傳專案資料夾到網頁伺服器目錄即可：

```bash
# 範例：上傳 1_javascript 專案
cd 前端開發環境配置/1_javascript
scp -r public pi@192.168.1.100:/home/pi/my-website/
```

**實際操作步驟：**
1. 確認專案中有 `public` 或 `dist` 資料夾
2. 使用 SCP 上傳整個資料夾
3. 在樹莓派上設定 Nginx 指向該資料夾
4. 重新載入 Nginx

### TypeScript 專案

需要先在本機編譯，然後上傳編譯後的檔案：

```bash
# 步驟 1：在本機編譯
cd 前端開發環境配置/2_typescript
npm run build

# 步驟 2：確認編譯結果
ls dist/
# 應該看到編譯後的 .js 檔案

# 步驟 3：上傳 dist 資料夾
scp -r dist pi@192.168.1.100:/home/pi/my-typescript-app/
```

**💡 重要提示：**
- 不要上傳 `src/` 資料夾，只上傳編譯後的 `dist/` 或 `build/` 資料夾
- 確認 `dist/` 資料夾中有 `index.html` 檔案

### React 專案

同樣需要先建置，然後上傳建置後的檔案：

```bash
# 步驟 1：在本機建置
cd 前端開發環境配置/3_typescript_react
npm run build

# 步驟 2：確認建置結果
ls build/
# 應該看到 index.html 和 static/ 資料夾

# 步驟 3：上傳 build 資料夾
scp -r build pi@192.168.1.100:/home/pi/my-react-app/
```

**💡 重要提示：**
- React 專案建置後會產生 `build/` 資料夾
- 確保上傳整個 `build/` 資料夾，包括 `static/` 子資料夾
- 如果使用路由（React Router），需要配置 Nginx 的 `try_files` 指令

---

## 🔐 使用 SSH 金鑰認證（免密碼登入）

為了方便和安全，建議設定 SSH 金鑰認證。

### 步驟 1：在本機生成 SSH 金鑰

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

### 步驟 2：將公鑰複製到樹莓派

```bash
ssh-copy-id pi@192.168.1.100
```

或者手動複製：

```bash
cat ~/.ssh/id_rsa.pub | ssh pi@192.168.1.100 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### 步驟 3：測試免密碼登入

```bash
ssh pi@192.168.1.100
```

如果成功，之後使用 SCP 或 rsync 時就不需要輸入密碼了。

---

## 📊 方法比較

| 方法 | 優點 | 缺點 | 適用場景 |
|------|------|------|---------|
| **FileZilla** | 圖形界面、操作簡單 | 需要手動操作、不適合自動化 | 不熟悉命令列的使用者 |
| **SCP** | 簡單快速、內建支援 | 每次都傳輸全部檔案 | 小專案或單次部署 |
| **rsync** | 只同步變更檔案、效率高 | 需要安裝 | 大型專案、頻繁部署 |
| **Git** | 版本控制、追蹤變更 | 需要公開或私有倉庫 | 有版本控制的專案 |
| **SFTP** | 互動式、可瀏覽檔案 | 需要手動操作 | 需要瀏覽遠端檔案系統 |

---

## ⚠️ 常見問題

### Q1: 連線被拒絕？

**A:** 檢查：
- 樹莓派是否開啟 SSH 服務：`sudo systemctl status ssh`
- 防火牆是否允許 SSH 連線
- IP 位址是否正確

### Q2: 上傳後網站無法顯示？

**A:** 檢查：
- 檔案權限是否正確
- 網頁伺服器是否有讀取權限
- 網頁伺服器設定檔是否指向正確目錄
- 檢查網頁伺服器錯誤日誌：`sudo tail -f /var/log/nginx/error.log`

### Q3: 上傳速度很慢？

**A:** 可以：
- 使用 `rsync -z` 啟用壓縮
- 排除不必要的檔案（如 `node_modules`）
- 檢查網路連線品質

### Q4: 如何自動化部署？

**A:** 可以建立部署腳本（deploy.sh）：

```bash
#!/bin/bash
# deploy.sh

REMOTE_USER="pi"
REMOTE_HOST="192.168.1.100"
REMOTE_PATH="/var/www/html/專案名稱"
LOCAL_PATH="./build"

echo "開始部署..."

# 使用 rsync 同步檔案
rsync -avz --delete $LOCAL_PATH/ $REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/

echo "部署完成！"
```

使用方式：
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 📚 相關資源

- [Nginx 網站伺服器配置](../建立web_server/README.md)
- [Node.js 和 npm 環境配置](../Node.js_npm_環境配置/README.md)

