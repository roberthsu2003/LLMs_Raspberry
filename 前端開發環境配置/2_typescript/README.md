# Customer Feedback Platform - TypeScript 示範專案

> 🎨 一個現代化的深色主題網頁應用，展示 TypeScript 在前端開發中的強大功能。

![專案預覽](創意發想圖片/創意發想圖片.png)

---

## 📋 目錄

- [👥 非開發者指南](#-非開發者指南) - 快速上手使用本專案
- [👨‍💻 開發者指南](#-開發者指南) - 深入了解技術細節
- [🚀 部署到樹莓派](#-部署到樹莓派) - 完整部署指南
- [📚 TypeScript 學習資源](#-typescript-學習資源) - 進階學習資料

---

# 👥 非開發者指南

> 💡 適合不需要修改程式碼，只想快速查看網頁效果的使用者。

## 🎯 專案簡介

這是一個模擬「客戶回饋整合平台」的網頁應用，展示了：
- ✅ 現代化的深色主題設計
- ✅ 流暢的動畫效果
- ✅ 響應式介面（支援各種螢幕尺寸）
- ✅ 互動式卡片和按鈕
- ✅ TypeScript 型別安全

## 🔧 系統需求

開始前請確保已安裝：
- **Node.js**（版本 18 以上）- [下載連結](https://nodejs.org/)
- **現代瀏覽器**（Chrome、Firefox、Safari 或 Edge）

**檢查是否已安裝：**
```bash
node --version    # 應顯示 v18.x.x 或更高
npm --version     # 應顯示版本號
```

## ⚙️ 快速開始

### 步驟 1：進入專案資料夾

```bash
cd 前端開發環境配置/2_typescript
```

### 步驟 2：安裝依賴套件

```bash
npm install
```

### 步驟 3：編譯專案

```bash
npm run build:web
```

看到 ✅ 訊息表示編譯成功！

### 步驟 4：在瀏覽器中開啟

**方法一：直接開啟檔案**
```bash
# macOS
open public/index.html

# Windows
start public/index.html

# Linux
xdg-open public/index.html
```

**方法二：使用本地伺服器（推薦）**
```bash
npm run serve
```

這會自動在瀏覽器中開啟 `http://localhost:8080`

## 🎮 互動功能

網頁包含以下互動功能：

### 1. 功能卡片
- **滑鼠懸停**：卡片會放大並顯示光暈效果
- **點擊卡片**：顯示該功能的詳細說明
  - 📞 **CALLS**：通話功能說明
  - 🎫 **TICKETS**：工單系統說明
  - ⭐ **REVIEWS**：評論管理說明
  - 📊 **SURVEYS**：問卷調查說明

### 2. 按鈕互動
- **Contact sales**：顯示聯絡銷售對話框
- **Try Dovetail free**：顯示免費試用資訊
- **Watch Keynote**：點擊藍色標籤查看發表會資訊

### 3. 動畫效果
- 頁面載入時的淡入動畫
- 滑鼠移動時的視差效果
- 圖標的浮動動畫

## ❓ 常見問題

### Q1: 網頁無法正確顯示？
**A:** 確保已執行 `npm run build:web` 編譯專案。

### Q2: 樣式跑版或不美觀？
**A:** 請使用現代瀏覽器（Chrome、Firefox、Safari、Edge），避免使用 IE。

### Q3: 如何修改網頁內容？
**A:** 請參考下方的「開發者指南」章節。

### Q4: 可以部署到網站嗎？
**A:** 可以！請參考本文件的「部署到樹莓派」章節。

---

# 👨‍💻 開發者指南

> 💻 適合需要修改程式碼、理解架構、添加功能的開發者。

## 📋 技術棧

| 技術 | 版本 | 用途 |
|------|------|------|
| TypeScript | 5.9.3 | 型別安全的 JavaScript |
| HTML5 | - | 網頁結構 |
| CSS3 | - | 樣式和動畫 |
| ES2020 Modules | - | 模組系統 |

## 📂 專案結構

```
2_typescript/
├── public/                     # 靜態資源
│   ├── index.html             # 主 HTML 檔案
│   └── css/
│       └── style.css          # 樣式表（深色主題）
│
├── src/                        # TypeScript 源碼
│   ├── index.ts               # 主程式（DOM 操作、互動邏輯）
│   └── utils/
│       └── math.ts            # 工具函式模組
│
├── dist/                       # 編譯輸出（自動生成）
│   ├── index.js               # 編譯後的 JS
│   ├── index.js.map           # Source Map
│   └── utils/
│       ├── math.js
│       └── math.js.map
│
├── 創意發想圖片/               # 設計參考圖片
│   └── 創意發想圖片.png
│
├── package.json                # npm 專案配置
├── tsconfig.json               # TypeScript 編譯器配置
└── README.md                   # 本文件
```

## 📝 核心程式碼說明

### 1. `public/index.html` - 網頁結構

主要區塊：
- **導航欄**：頂部導航選單
- **Hero Section**：主要內容區，包含：
  - 左側：標題、描述、按鈕、合作夥伴
  - 右側：四個功能卡片（CALLS、TICKETS、REVIEWS、SURVEYS）
- **Footer**：頁尾資訊

### 2. `public/css/style.css` - 樣式設計

設計特點：
```css
/* 深色主題配色 */
--bg-primary: #0a0a0a;        /* 主背景色 */
--bg-secondary: #1a1a1a;      /* 次要背景色 */
--text-primary: #ffffff;       /* 主文字色 */
--text-secondary: #a0a0a0;     /* 次要文字色 */
--accent-blue: #3B82F6;        /* 強調色（藍色）*/
--accent-purple: #8B5CF6;      /* 強調色（紫色）*/
```

關鍵動畫：
- `fadeInUp`：淡入上升效果
- `fadeInScale`：淡入縮放效果
- `iconFloat`：圖標浮動效果

### 3. `src/index.ts` - TypeScript 主程式

核心功能：

```typescript
// 介面定義
interface FeatureCard {
  element: HTMLElement;
  category: string;
}

// 主要函式
function initFeatureCards(): void    // 初始化功能卡片
function initButtons(): void         // 初始化按鈕互動
function initAnimations(): void      // 初始化動畫
function initConnectionLines(): void // 初始化連接線
function showModal(): void           // 顯示對話框
function showFeatureInfo(): void     // 顯示功能資訊
```

## ⚙️ 配置檔案詳解

### `package.json` - npm 專案配置

```json
{
  "name": "2_typescript",
  "version": "1.0.0",
  "type": "module",              // ⚠️ 使用 ES6 模組
  "scripts": {
    "build": "tsc",              // 編譯 TypeScript
    "build:web": "npm run build && echo '...'",  // 編譯並提示
    "serve": "npx http-server public -p 8080 -o", // 啟動本地伺服器
    "clean": "rm -rf dist"       // 清理編譯輸出
  },
  "devDependencies": {
    "typescript": "^5.9.3",
    "@types/node": "^25.0.3"
  }
}
```

### `tsconfig.json` - TypeScript 編譯器配置

```json
{
  "compilerOptions": {
    // 檔案配置
    "rootDir": "./src",              // 源碼目錄
    "outDir": "./dist",              // 輸出目錄
    
    // 環境配置（支援瀏覽器）
    "module": "ES2020",              // 使用 ES2020 模組
    "target": "ES2020",              // 編譯目標
    "lib": ["ES2020", "DOM", "DOM.Iterable"],  // 包含 DOM API
    
    // 型別檢查（嚴格模式）
    "strict": true,                  // 啟用所有嚴格檢查
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    
    // 輸出設定
    "sourceMap": true,               // 生成 Source Map（除錯用）
    "declaration": true,             // 生成型別定義檔
    "declarationMap": true,
    
    // 其他
    "verbatimModuleSyntax": true,    // 嚴格模組語法
    "skipLibCheck": true             // 跳過函式庫檢查
  }
}
```

## 🔨 開發工作流程

### 1. 開發環境設定

```bash
# 安裝依賴
npm install

# 安裝開發工具（選用）
npm install -D http-server
```

### 2. 開發流程

```bash
# 方式一：手動編譯+測試
npm run build        # 編譯
npm run serve        # 啟動本地伺服器

# 方式二：一鍵編譯
npm run build:web    # 編譯並提示
# 然後手動開啟 public/index.html
```

### 3. 修改程式碼

**修改 HTML：**
```bash
# 編輯 public/index.html
code public/index.html
```

**修改樣式：**
```bash
# 編輯 public/css/style.css
code public/css/style.css
```

**修改 TypeScript：**
```bash
# 編輯 src/index.ts
code src/index.ts

# 編譯後刷新瀏覽器查看效果
npm run build
```

### 4. 除錯技巧

**使用瀏覽器開發者工具：**
1. 開啟網頁後按 `F12` 或 `Cmd+Option+I`（macOS）
2. 切換到 `Console` 標籤查看日誌
3. 切換到 `Sources` 標籤設定中斷點
4. 因為有 Source Map，可以直接除錯 TypeScript 原始碼！

**常用 console 輸出：**
```typescript
console.log('變數值：', variable);
console.table(arrayData);
console.time('效能測試');
// ... 程式碼 ...
console.timeEnd('效能測試');
```

## 🎨 自訂與擴充

### 修改配色

編輯 `public/css/style.css`：

```css
:root {
    --bg-primary: #0a0a0a;      /* 改成你想要的主背景色 */
    --accent-blue: #3B82F6;     /* 改成你想要的強調色 */
    /* ... 其他變數 */
}
```

### 新增功能卡片

1. 在 `public/index.html` 中添加新卡片：

```html
<div class="feature-card" data-category="newfeature">
    <div class="card-header">NEW FEATURE</div>
    <div class="card-icons">
        <!-- 添加圖標 -->
    </div>
</div>
```

2. 在 `src/index.ts` 中添加對應訊息：

```typescript
const messages: Record<string, string> = {
    // ... 現有訊息
    newfeature: '🎉 新功能：您的功能說明'
};
```

### 新增動畫效果

在 `public/css/style.css` 中定義新動畫：

```css
@keyframes yourAnimation {
    from {
        /* 起始狀態 */
    }
    to {
        /* 結束狀態 */
    }
}

.your-element {
    animation: yourAnimation 1s ease;
}
```

## 🐛 常見開發問題

### Q: TypeScript 編譯錯誤？

**問題：**
```
error TS2304: Cannot find name 'document'.
```

**解決方案：**
確認 `tsconfig.json` 中包含 DOM 函式庫：
```json
{
  "compilerOptions": {
    "lib": ["ES2020", "DOM", "DOM.Iterable"]
  }
}
```

### Q: 模組匯入錯誤？

**問題：**
```
Uncaught SyntaxError: Cannot use import statement outside a module
```

**解決方案：**
確保 HTML 中使用 `type="module"`：
```html
<script type="module" src="../dist/index.js"></script>
```

### Q: CSS 樣式沒有載入？

**檢查清單：**
- [ ] 檔案路徑是否正確？
- [ ] CSS 檔案是否存在？
- [ ] 瀏覽器 Console 有錯誤訊息嗎？
- [ ] 快取問題？試試 `Ctrl+Shift+R` 強制重新整理

### Q: 動畫效果不流暢？

**優化建議：**
1. 使用 `transform` 而非 `top/left`
2. 使用 `will-change` 提示瀏覽器
3. 減少同時運行的動畫數量

```css
.smooth-animation {
    will-change: transform;
    transform: translateX(0);
    transition: transform 0.3s ease;
}
```

## 📦 可用的 npm 指令

| 指令 | 說明 | 使用時機 |
|------|------|---------|
| `npm install` | 安裝依賴套件 | 首次使用或更新套件 |
| `npm run build` | 編譯 TypeScript | 修改 TS 檔案後 |
| `npm run build:web` | 編譯並顯示完成訊息 | 準備查看網頁 |
| `npm run serve` | 啟動本地伺服器 | 開發測試時 |
| `npm run clean` | 清理編譯輸出 | 重新編譯前 |

---

# 🚀 部署到樹莓派

> 🍓 完整的樹莓派 Nginx 部署指南。

## 🎯 部署概覽

本專案是**純前端網頁應用**，可以直接部署到 Nginx 網頁伺服器。

**優點：**
- ✅ 無需 Node.js 執行環境
- ✅ 靜態檔案部署簡單快速
- ✅ Nginx 效能優異
- ✅ 適合樹莓派等低功耗設備

## 📋 部署前準備

### 在本機編譯專案

```bash
# 1. 進入專案目錄
cd 前端開發環境配置/2_typescript

# 2. 安裝依賴（如果還沒安裝）
npm install

# 3. 編譯專案
npm run build:web

# 4. 確認編譯成功
ls dist/        # 應該看到 index.js 等檔案
ls public/      # 應該看到 index.html 和 css/ 資料夾
```

## 🔧 樹莓派環境設定

### 步驟 1：更新系統

```bash
# 在樹莓派上執行
sudo apt update && sudo apt upgrade -y
```

### 步驟 2：安裝 Nginx

```bash
# 安裝 Nginx
sudo apt install nginx -y

# 啟動 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 檢查狀態
sudo systemctl status nginx
```

看到 `active (running)` 表示 Nginx 已成功啟動。

### 步驟 3：測試 Nginx

在瀏覽器中訪問樹莓派的 IP：
```
http://[樹莓派IP]
```

應該會看到 Nginx 歡迎頁面。

**查看樹莓派 IP：**
```bash
hostname -I
```

## 📤 上傳專案到樹莓派

### 方法一：使用 SCP（推薦）

```bash
# 在您的電腦上執行
# 上傳整個專案資料夾
scp -r 前端開發環境配置/2_typescript pi@[樹莓派IP]:/home/pi/

# 或者只上傳必要檔案
scp -r 前端開發環境配置/2_typescript/public pi@[樹莓派IP]:/home/pi/typescript-web/
scp -r 前端開發環境配置/2_typescript/dist pi@[樹莓派IP]:/home/pi/typescript-web/
```

### 方法二：使用 Git

```bash
# 在樹莓派上執行
cd ~
git clone [您的 Git 儲存庫 URL]
cd LLMs_Raspberry/前端開發環境配置/2_typescript
```

### 方法三：使用 USB 隨身碟

1. 將專案複製到 USB 隨身碟
2. 插入樹莓派
3. 複製檔案：
```bash
sudo cp -r /media/pi/[USB名稱]/2_typescript /home/pi/
```

## ⚙️ 配置 Nginx

### 步驟 1：建立網站配置

```bash
# 在樹莓派上執行
sudo nano /etc/nginx/sites-available/typescript-app
```

輸入以下配置：

```nginx
server {
    listen 80;
    server_name [您的樹莓派IP或域名];
    
    # 網站根目錄
    root /home/pi/2_typescript/public;
    index index.html;
    
    # 字元編碼
    charset utf-8;
    
    # 主頁面
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # dist 目錄（編譯後的 JS）
    location /dist/ {
        alias /home/pi/2_typescript/dist/;
        expires 1d;
        add_header Cache-Control "public, immutable";
    }
    
    # 靜態資源（CSS、JS、圖片等）
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot|map)$ {
        expires 7d;
        add_header Cache-Control "public, immutable";
    }
    
    # Gzip 壓縮
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript 
               application/javascript application/xml+rss application/json;
    
    # 錯誤頁面
    error_page 404 /index.html;
    error_page 500 502 503 504 /index.html;
    
    # 安全性設定
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### 步驟 2：啟用網站

```bash
# 建立符號連結
sudo ln -s /etc/nginx/sites-available/typescript-app /etc/nginx/sites-enabled/

# 移除預設網站（選用）
sudo rm /etc/nginx/sites-enabled/default

# 測試配置是否正確
sudo nginx -t
```

看到 `syntax is ok` 和 `test is successful` 表示配置正確。

### 步驟 3：設定檔案權限

```bash
# 確保 Nginx 可以讀取檔案
sudo chown -R pi:www-data /home/pi/2_typescript
sudo chmod -R 755 /home/pi/2_typescript
```

### 步驟 4：重新載入 Nginx

```bash
sudo systemctl reload nginx
```

## ✅ 測試部署

在瀏覽器中訪問：
```
http://[樹莓派IP]
```

您應該會看到漂亮的客戶回饋平台網頁！🎉

## 🔒 進階配置（選用）

### 1. 設定自訂域名

如果您有域名，可以配置 DNS：

```bash
# 編輯配置
sudo nano /etc/nginx/sites-available/typescript-app

# 修改 server_name
server_name your-domain.com www.your-domain.com;
```

### 2. 設定 HTTPS（Let's Encrypt）

```bash
# 安裝 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 取得 SSL 憑證（需要有域名）
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自動續約測試
sudo certbot renew --dry-run
```

### 3. 設定防火牆

```bash
# 安裝 UFW
sudo apt install ufw -y

# 允許 SSH（重要！）
sudo ufw allow 22/tcp

# 允許 HTTP 和 HTTPS
sudo ufw allow 'Nginx Full'

# 啟用防火牆
sudo ufw enable

# 檢查狀態
sudo ufw status
```

### 4. 效能優化

編輯 Nginx 主配置：

```bash
sudo nano /etc/nginx/nginx.conf
```

添加或修改：

```nginx
http {
    # 增加工作進程數
    worker_processes auto;
    
    # 啟用 Gzip
    gzip on;
    gzip_comp_level 6;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    
    # 快取設定
    open_file_cache max=1000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
}
```

### 5. 設定日誌

查看訪問日誌：
```bash
sudo tail -f /var/log/nginx/access.log
```

查看錯誤日誌：
```bash
sudo tail -f /var/log/nginx/error.log
```

## 📝 部署檢查清單

部署前請確認：

- [ ] 專案已在本機編譯完成
- [ ] `dist/` 資料夾包含編譯後的 JS 檔案
- [ ] `public/` 資料夾包含 HTML 和 CSS 檔案
- [ ] 樹莓派已安裝 Nginx
- [ ] 專案檔案已上傳到樹莓派
- [ ] Nginx 配置檔案已建立
- [ ] Nginx 配置測試通過（`nginx -t`）
- [ ] 檔案權限已正確設定
- [ ] Nginx 已重新載入
- [ ] 可以在瀏覽器中訪問網站
- [ ] 所有互動功能正常運作
- [ ] （選用）已設定 HTTPS
- [ ] （選用）已設定防火牆

## 🐛 部署疑難排解

### 問題 1：Nginx 無法啟動

```bash
# 檢查配置錯誤
sudo nginx -t

# 查看詳細錯誤
sudo systemctl status nginx -l

# 查看錯誤日誌
sudo tail -50 /var/log/nginx/error.log
```

**常見原因：**
- 配置檔案語法錯誤
- 80 埠被佔用
- 權限問題

### 問題 2：網頁顯示 403 Forbidden

**原因：** 檔案權限問題

**解決方案：**
```bash
# 重新設定權限
sudo chown -R pi:www-data /home/pi/2_typescript
sudo chmod -R 755 /home/pi/2_typescript

# 檢查 SELinux（如果適用）
sudo setenforce 0
```

### 問題 3：網頁顯示 404 Not Found

**檢查清單：**
```bash
# 1. 確認檔案路徑
ls -la /home/pi/2_typescript/public/index.html

# 2. 檢查 Nginx 配置中的 root 路徑
sudo nano /etc/nginx/sites-available/typescript-app

# 3. 確認符號連結
ls -la /etc/nginx/sites-enabled/
```

### 問題 4：JavaScript 無法載入

**問題：** 瀏覽器 Console 顯示 MIME type 錯誤

**解決方案：**
確保 Nginx 配置包含：
```nginx
types {
    text/html html;
    text/css css;
    application/javascript js;
}
```

或使用 Nginx 預設的 mime.types：
```nginx
include /etc/nginx/mime.types;
```

### 問題 5：樣式沒有載入

```bash
# 1. 檢查 CSS 檔案是否存在
ls -la /home/pi/2_typescript/public/css/style.css

# 2. 檢查瀏覽器 Console 的錯誤訊息

# 3. 清除瀏覽器快取並重新整理（Ctrl+Shift+R）
```

### 問題 6：無法從外部網路訪問

```bash
# 1. 檢查樹莓派防火牆
sudo ufw status

# 2. 檢查路由器防火牆和埠轉發設定

# 3. 確認樹莓派 IP
hostname -I

# 4. 測試本地網路訪問
# 在樹莓派上
curl http://localhost

# 在同網段的其他設備上
curl http://[樹莓派IP]
```

## 🔄 更新部署

當您修改了專案程式碼後：

```bash
# 1. 在本機重新編譯
npm run build:web

# 2. 上傳更新的檔案到樹莓派
scp -r dist/ pi@[樹莓派IP]:/home/pi/2_typescript/
scp -r public/ pi@[樹莓派IP]:/home/pi/2_typescript/

# 3. 在樹莓派上重新載入 Nginx（通常不需要）
sudo systemctl reload nginx

# 4. 清除瀏覽器快取並重新整理頁面
```

## 📊 效能監控

### 查看 Nginx 狀態

```bash
# 即時查看訪問日誌
sudo tail -f /var/log/nginx/access.log

# 統計訪問量
sudo cat /var/log/nginx/access.log | wc -l

# 查看最常訪問的頁面
sudo awk '{print $7}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -10
```

### 監控系統資源

```bash
# CPU 和記憶體使用情況
top

# 磁碟使用情況
df -h

# 網路連線
sudo netstat -tunlp | grep nginx
```

---

# 📚 TypeScript 學習資源

## 🎓 官方資源

- [TypeScript 官方網站](https://www.typescriptlang.org/)
- [TypeScript 官方文件](https://www.typescriptlang.org/docs/)
- [TypeScript Playground](https://www.typescriptlang.org/play) - 線上練習

## 📖 推薦教學

- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/) - 深入理解 TypeScript
- [TypeScript Tutorial](https://www.typescripttutorial.net/) - 系統化教學
- [TypeScript 中文教學](https://willh.gitbook.io/typescript-tutorial/)

## 🎬 影片教學

- [TypeScript Crash Course](https://www.youtube.com/results?search_query=typescript+crash+course)
- [Net Ninja TypeScript](https://www.youtube.com/playlist?list=PL4cUxeGkcC9gUgr39Q_yD6v-bSyMwKPUI)

## 🛠️ 進階主題

- [TypeScript Design Patterns](https://refactoring.guru/design-patterns/typescript)
- [React + TypeScript](https://react-typescript-cheatsheet.netlify.app/)
- [Node.js + TypeScript](https://nodejs.dev/learn/nodejs-with-typescript)

---

## 📞 支援與回饋

遇到問題或有建議？

- 📧 Email: [您的 Email]
- 🐛 Issues: [GitHub Issues 連結]
- 💬 Discussions: [GitHub Discussions 連結]

---

## 📄 授權

本專案採用 ISC 授權。

---

## 🙏 致謝

- 設計靈感來自 [Dovetail](https://dovetail.com/)
- 由 [Mobbin](https://mobbin.com/) 精選設計
- 使用 TypeScript 和現代網頁技術打造

---

**🎉 恭喜！您已成功建立並部署 TypeScript 網頁應用！**

祝您開發愉快！ Happy Coding! 🚀
