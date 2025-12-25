# Next Gen Code Review - 純 JavaScript 網頁應用

> 🎨 使用純 HTML、CSS、JavaScript 打造的現代化網頁應用，無需 Node.js 或任何構建工具。

![專案預覽](創意發想圖片/index.png)

---

## 📋 目錄

- [👥 非開發者指南](#-非開發者指南) - 快速上手使用本專案
- [👨‍💻 開發者指南](#-開發者指南) - 深入了解技術細節
- [🚀 部署到樹莓派](#-部署到樹莓派) - 完整部署指南
- [📚 學習資源](#-學習資源) - 進階學習資料

---

# 👥 非開發者指南

> 💡 適合不需要修改程式碼，只想快速查看網頁效果的使用者。

## 🎯 專案簡介

這是一個模擬「下一世代程式碼審查平台」的網頁應用，展示了：
- ✅ 現代化的深色主題設計
- ✅ 純 JavaScript 實現（無需編譯）
- ✅ 流暢的動畫效果和視差滾動
- ✅ 響應式介面（支援各種螢幕尺寸）
- ✅ 互動式按鈕和彈窗
- ✅ 零依賴（無需 Node.js 或 npm）

## 🔧 系統需求

### 必備條件
- **現代瀏覽器**（Chrome、Firefox、Safari 或 Edge）
- 就這樣！不需要安裝任何其他軟體

### 選用工具（開發用）
- **Visual Studio Code** - 程式碼編輯器
- **Live Server 擴充功能** - 本地伺服器（VS Code）

## ⚙️ 快速開始

### 方法一：直接開啟檔案（最簡單）

```bash
# macOS
open public/index.html

# Windows
start public/index.html

# Linux
xdg-open public/index.html
```

雙擊 `public/index.html` 檔案即可在瀏覽器中開啟！

### 方法二：使用 Python 內建伺服器（推薦）

```bash
# Python 3
cd public
python3 -m http.server 8000

# Python 2
cd public
python -m SimpleHTTPServer 8000
```

然後在瀏覽器中訪問：`http://localhost:8000`

### 方法三：使用 VS Code Live Server

1. 安裝 VS Code 的 Live Server 擴充功能
2. 右鍵點擊 `public/index.html`
3. 選擇「Open with Live Server」

網頁會自動在瀏覽器中開啟，並支援即時重新載入！

## 🎮 互動功能

網頁包含以下互動功能：

### 1. 主要按鈕
- **「免費開始」**：顯示註冊資訊對話框
- **「申請 Demo」**：顯示預約展示對話框
- **「Log in」**：顯示登入對話框
- **「Sign up」**：顯示註冊對話框

### 2. 導航選單
- **Features**：查看功能說明
- **Docs**：查看文件
- **Pricing**：查看定價
- **Contact**：聯絡我們

### 3. 視覺效果
- **旋轉動畫**：三個發光形狀以不同速度旋轉
- **脈衝動畫**：發光效果的脈衝變化
- **滑鼠視差**：移動滑鼠時形狀會跟隨移動
- **滾動視差**：頁面滾動時的視差效果
- **淡入動畫**：頁面載入時的元素淡入

### 4. 品牌標誌互動
點擊任何品牌名稱查看使用案例提示。

## ❓ 常見問題

### Q1: 網頁無法正確顯示？
**A:** 確保使用現代瀏覽器（Chrome、Firefox、Safari、Edge）。避免使用 IE。

### Q2: 動畫效果不流暢？
**A:** 
- 關閉瀏覽器的其他分頁釋放資源
- 更新顯示卡驅動程式
- 使用硬體加速（瀏覽器設定中開啟）

### Q3: 如何修改網頁內容？
**A:** 請參考下方的「開發者指南」章節。

### Q4: 可以部署到網站嗎？
**A:** 可以！請參考本文件的「部署到樹莓派」章節。

### Q5: 需要安裝 Node.js 嗎？
**A:** 不需要！這是純 JavaScript 專案，直接開啟 HTML 檔案即可運行。

---

# 👨‍💻 開發者指南

> 💻 適合需要修改程式碼、理解架構、添加功能的開發者。

## 📋 技術棧

| 技術 | 版本 | 用途 |
|------|------|------|
| HTML5 | - | 網頁結構 |
| CSS3 | - | 樣式和動畫 |
| JavaScript (ES6+) | - | 互動邏輯 |
| 無需構建工具 | - | 直接在瀏覽器運行 |

## 📂 專案結構

```
1_javascript/
├── public/                     # 靜態資源（網頁根目錄）
│   ├── index.html             # 主 HTML 檔案
│   ├── css/
│   │   └── style.css          # 樣式表（深色主題）
│   └── js/
│       └── main.js            # JavaScript 主程式
│
├── 創意發想圖片/               # 設計參考圖片
│   └── index.png
│
├── index.html                  # 舊版檔案（保留參考）
└── README.md                   # 本文件
```

### 為什麼使用 `public/` 資料夾？

1. **清晰的結構**：將網頁檔案與專案文件分離
2. **部署方便**：直接將 `public/` 資料夾部署到伺服器
3. **專業標準**：符合業界最佳實踐
4. **Nginx 相容**：直接對應 Nginx 的 root 目錄

## 📝 核心檔案說明

### 1. `public/index.html` - 網頁結構

主要區塊：

```html
<header>           <!-- 導航欄 -->
<section class="hero">  <!-- 主視覺區域 -->
  <div class="hero-content">  <!-- 文字內容 -->
  <div class="glow-wrap">     <!-- 動畫形狀 -->
<section class="brands">     <!-- 品牌合作夥伴 -->
<footer>           <!-- 頁尾 -->
```

**重要特點：**
- 語義化 HTML5 標籤
- SEO 優化的 meta 標籤
- 響應式 viewport 設定
- 外部 CSS 和 JS 引用

### 2. `public/css/style.css` - 樣式設計

#### 設計系統

```css
/* CSS 變數 - 方便主題切換 */
:root {
  --bg: #0b0b0f;          /* 主背景色 */
  --text: #ffffff;        /* 主文字色 */
  --muted: #a0a0b2;       /* 次要文字色 */
  --accent: #b084ff;      /* 強調色（紫色）*/
  --card: #15151c;        /* 卡片背景 */
  --border: #262636;      /* 邊框色 */
}
```

#### 關鍵動畫

```css
/* 旋轉動畫 */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 淡入上升 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 淡入縮放 */
@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 脈衝效果 */
@keyframes pulse {
  0%, 100% { opacity: 0.6; }
  50% { opacity: 1; }
}
```

#### 響應式斷點

- **桌面**：`> 900px` - 雙欄佈局
- **平板**：`640px - 900px` - 單欄佈局，隱藏導航
- **手機**：`< 640px` - 完全優化的行動版

### 3. `public/js/main.js` - JavaScript 主程式

#### 核心功能模組

```javascript
// 主要功能
initButtons()        // 初始化按鈕互動
initNavigation()     // 初始化導航
initAnimations()     // 初始化動畫效果

// UI 元件
showModal()          // 顯示模態對話框
closeModal()         // 關閉模態對話框
showToast()          // 顯示 Toast 提示

// 特效
滾動視差效果          // window scroll 事件
滑鼠視差效果          // mousemove 事件
Intersection Observer // 滾動顯示動畫
```

#### 事件處理架構

```javascript
// 1. 等待 DOM 載入
document.addEventListener('DOMContentLoaded', () => {
  // 初始化所有功能
});

// 2. 按鈕事件委派
primaryButtons.forEach(btn => {
  btn.addEventListener('click', handlePrimaryAction);
});

// 3. 模態對話框管理
function showModal(title, message, buttons) {
  // 創建並顯示 modal
}

// 4. Toast 提示系統
function showToast(message, duration) {
  // 顯示並自動隱藏提示
}
```

## 🔨 開發工作流程

### 1. 設定開發環境

**VS Code 推薦擴充功能：**
```
- Live Server          # 即時預覽
- Prettier            # 程式碼格式化
- ESLint              # JavaScript 檢查
- HTML CSS Support    # CSS 智能提示
- Auto Rename Tag     # 自動重命名標籤
- Path Intellisense   # 路徑自動完成
```

**安裝步驟：**
1. 開啟 VS Code
2. 按 `Ctrl+Shift+X`（或 `Cmd+Shift+X`）
3. 搜尋並安裝上述擴充功能

### 2. 開發流程

```bash
# 1. 打開專案
cd 前端開發環境配置/1_javascript

# 2. 使用 VS Code 開啟
code .

# 3. 右鍵 public/index.html
# 選擇「Open with Live Server」

# 4. 修改檔案，自動重新載入
```

### 3. 修改網頁內容

**修改文字內容：**
```html
<!-- public/index.html -->
<h1>
  你的標題<br>
  第二行標題
</h1>

<p>
  你的描述文字
</p>
```

**修改配色：**
```css
/* public/css/style.css */
:root {
  --bg: #你的背景色;
  --accent: #你的強調色;
  /* ... 其他顏色 */
}
```

**修改互動邏輯：**
```javascript
// public/js/main.js
function handlePrimaryAction(e) {
  // 你的自訂邏輯
  showToast('你的提示訊息');
}
```

### 4. 除錯技巧

**使用瀏覽器開發者工具：**

```javascript
// 在程式碼中添加斷點
debugger;

// 輸出日誌
console.log('變數值：', variable);
console.table(arrayData);
console.time('效能測試');
// ... 程式碼 ...
console.timeEnd('效能測試');

// 監控事件
monitorEvents(document.querySelector('.btn'));
```

**開啟開發者工具：**
- Windows/Linux：`F12` 或 `Ctrl+Shift+I`
- macOS：`Cmd+Option+I`

**常用面板：**
- **Elements**：檢查 HTML 和 CSS
- **Console**：查看日誌和錯誤
- **Network**：檢查資源載入
- **Performance**：分析效能

## 🎨 自訂與擴充

### 修改主題配色

**方法一：修改 CSS 變數**

```css
/* public/css/style.css */
:root {
  /* 藍色主題 */
  --accent: #3B82F6;
  --accent-soft: rgba(59, 130, 246, 0.2);
  
  /* 綠色主題 */
  --accent: #10B981;
  --accent-soft: rgba(16, 185, 129, 0.2);
  
  /* 紅色主題 */
  --accent: #EF4444;
  --accent-soft: rgba(239, 68, 68, 0.2);
}
```

**方法二：添加主題切換功能**

```javascript
// public/js/main.js
function switchTheme(theme) {
  const root = document.documentElement;
  
  const themes = {
    purple: {
      accent: '#b084ff',
      accentSoft: 'rgba(176, 132, 255, 0.2)'
    },
    blue: {
      accent: '#3B82F6',
      accentSoft: 'rgba(59, 130, 246, 0.2)'
    },
    green: {
      accent: '#10B981',
      accentSoft: 'rgba(16, 185, 129, 0.2)'
    }
  };
  
  const selectedTheme = themes[theme];
  root.style.setProperty('--accent', selectedTheme.accent);
  root.style.setProperty('--accent-soft', selectedTheme.accentSoft);
}

// 使用
switchTheme('blue');
```

### 新增互動功能

**範例：添加「返回頂部」按鈕**

```html
<!-- public/index.html -->
<button id="backToTop" class="btn" style="position: fixed; bottom: 30px; right: 30px; display: none;">
  ↑
</button>
```

```css
/* public/css/style.css */
#backToTop {
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

#backToTop:hover {
  opacity: 1;
}
```

```javascript
// public/js/main.js
const backToTopBtn = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
  if (window.pageYOffset > 300) {
    backToTopBtn.style.display = 'block';
  } else {
    backToTopBtn.style.display = 'none';
  }
});

backToTopBtn.addEventListener('click', () => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});
```

### 新增頁面區塊

**範例：添加「功能介紹」區塊**

```html
<!-- public/index.html -->
<!-- 在 brands 和 footer 之間添加 -->
<section class="features">
  <div class="features-container">
    <h2>核心功能</h2>
    
    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">🤖</div>
        <h3>AI 驅動</h3>
        <p>使用機器學習自動檢測程式碼問題</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>即時反饋</h3>
        <p>在 PR 階段立即獲得審查意見</p>
      </div>
      
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>深度分析</h3>
        <p>全面的程式碼品質報告</p>
      </div>
    </div>
  </div>
</section>
```

```css
/* public/css/style.css */
.features {
  padding: 80px 60px;
  text-align: center;
}

.features h2 {
  font-size: 42px;
  margin-bottom: 60px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px;
  transition: transform 0.3s ease, border-color 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
  border-color: var(--accent);
}

.feature-icon {
  font-size: 48px;
  margin-bottom: 20px;
}

.feature-card h3 {
  font-size: 24px;
  margin-bottom: 12px;
}

.feature-card p {
  color: var(--muted);
  line-height: 1.6;
}
```

## 🐛 常見開發問題

### Q: CSS 樣式沒有載入？

**檢查清單：**
```bash
# 1. 確認檔案路徑
ls public/css/style.css

# 2. 檢查 HTML 中的引用
<link rel="stylesheet" href="css/style.css">
<!-- 注意：相對於 index.html 的路徑 -->

# 3. 清除瀏覽器快取
Ctrl+Shift+R (Windows/Linux)
Cmd+Shift+R (macOS)
```

### Q: JavaScript 沒有執行？

**除錯步驟：**
```javascript
// 1. 檢查 Console 是否有錯誤
F12 → Console 標籤

// 2. 確認 script 載入順序
<script src="js/main.js"></script>
<!-- 應該在 </body> 之前 -->

// 3. 確認 DOM 已載入
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM ready!');
  // 你的程式碼
});
```

### Q: 動畫效果在某些瀏覽器不正常？

**解決方案：**
```css
/* 添加瀏覽器前綴 */
.glow-shape {
  -webkit-animation: spin 20s linear infinite;
  -moz-animation: spin 20s linear infinite;
  animation: spin 20s linear infinite;
}

/* 使用 transform 而非 top/left */
.element {
  /* ✅ 好 - 硬體加速 */
  transform: translateX(100px);
  
  /* ❌ 差 - 觸發重排 */
  left: 100px;
}
```

### Q: 手機版佈局跑版？

**檢查響應式設定：**
```html
<!-- 確認 viewport meta 標籤 -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

```css
/* 使用相對單位 */
.container {
  width: 100%;        /* ✅ 好 */
  max-width: 1200px;
  padding: 0 20px;
}

.fixed-width {
  width: 800px;       /* ❌ 差 - 會在小螢幕溢出 */
}
```

## 📦 檔案大小優化

### 1. 壓縮 CSS

**使用線上工具：**
- [CSS Minifier](https://cssminifier.com/)
- 將壓縮後的 CSS 儲存為 `style.min.css`

```html
<!-- 生產環境使用壓縮版 -->
<link rel="stylesheet" href="css/style.min.css">
```

### 2. 壓縮 JavaScript

**使用線上工具：**
- [JavaScript Minifier](https://javascript-minifier.com/)
- 將壓縮後的 JS 儲存為 `main.min.js`

```html
<!-- 生產環境使用壓縮版 -->
<script src="js/main.min.js"></script>
```

### 3. 優化圖片

- 使用 WebP 格式
- 壓縮 PNG/JPG
- 使用適當的尺寸

---

# 🚀 部署到樹莓派

> 🍓 完整的樹莓派 Nginx 部署指南。

## 🎯 部署概覽

本專案是**純靜態網頁應用**，無需任何後端或 Node.js，非常適合部署到樹莓派。

**優點：**
- ✅ 零依賴 - 無需安裝 Node.js
- ✅ 超輕量 - 檔案大小小於 50KB
- ✅ 高效能 - Nginx 直接提供靜態檔案
- ✅ 低功耗 - 適合樹莓派 24/7 運行
- ✅ 快速部署 - 5 分鐘內完成

## 📋 部署前準備

### 檢查檔案完整性

```bash
# 在本機執行
cd 前端開發環境配置/1_javascript

# 確認檔案存在
ls -R public/
# 應該看到：
# public/index.html
# public/css/style.css
# public/js/main.js
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

看到 `active (running)` 表示成功！

### 步驟 3：測試 Nginx

```bash
# 查看樹莓派 IP
hostname -I
```

在瀏覽器中訪問：`http://[樹莓派IP]`

應該會看到 Nginx 歡迎頁面。

## 📤 上傳專案到樹莓派

### 方法一：使用 SCP（推薦）

```bash
# 在您的電腦上執行
# 上傳整個 public 資料夾
scp -r 前端開發環境配置/1_javascript/public pi@[樹莓派IP]:/home/pi/code-review-app

# 如果需要輸入密碼，預設是 raspberry
```

### 方法二：使用 Git

```bash
# 在樹莓派上執行
cd ~
git clone [您的 Git 儲存庫 URL]
cd LLMs_Raspberry/前端開發環境配置/1_javascript
```

### 方法三：使用 USB 隨身碟

```bash
# 1. 將專案複製到 USB
# 2. 插入樹莓派
# 3. 在樹莓派上執行

# 查看 USB 掛載點
lsblk

# 複製檔案
sudo cp -r /media/pi/[USB名稱]/public /home/pi/code-review-app
```

## ⚙️ 配置 Nginx

### 步驟 1：建立網站配置

```bash
# 在樹莓派上執行
sudo nano /etc/nginx/sites-available/code-review
```

輸入以下配置：

```nginx
server {
    listen 80;
    server_name [您的樹莓派IP或域名];
    
    # 網站根目錄
    root /home/pi/code-review-app/public;
    index index.html;
    
    # 字元編碼
    charset utf-8;
    
    # 主頁面
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # 靜態資源快取
    location ~* \.(css|js|jpg|jpeg|png|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Gzip 壓縮
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types 
        text/plain 
        text/css 
        text/xml 
        text/javascript 
        application/javascript 
        application/xml+rss 
        application/json;
    
    # 安全性標頭
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    
    # 錯誤頁面
    error_page 404 /index.html;
    error_page 500 502 503 504 /index.html;
    
    # 存取日誌
    access_log /var/log/nginx/code-review-access.log;
    error_log /var/log/nginx/code-review-error.log;
}
```

### 步驟 2：啟用網站

```bash
# 建立符號連結
sudo ln -s /etc/nginx/sites-available/code-review /etc/nginx/sites-enabled/

# 移除預設網站（選用）
sudo rm /etc/nginx/sites-enabled/default

# 測試配置
sudo nginx -t
```

看到 `syntax is ok` 和 `test is successful` 表示配置正確！

### 步驟 3：設定檔案權限

```bash
# 確保 Nginx 可以讀取檔案
sudo chown -R pi:www-data /home/pi/code-review-app
sudo chmod -R 755 /home/pi/code-review-app

# 驗證權限
ls -la /home/pi/code-review-app
```

### 步驟 4：重新載入 Nginx

```bash
sudo systemctl reload nginx

# 或重啟 Nginx
sudo systemctl restart nginx
```

## ✅ 測試部署

在瀏覽器中訪問：
```
http://[樹莓派IP]
```

您應該會看到「下一世代程式碼審查平台」網頁！🎉

### 測試清單

- [ ] 網頁正常載入
- [ ] CSS 樣式正確顯示
- [ ] JavaScript 互動正常（點擊按鈕）
- [ ] 動畫效果流暢
- [ ] 手機版佈局正常
- [ ] 所有按鈕和連結都能點擊

## 🔒 進階配置（選用）

### 1. 設定自訂域名

**編輯 Nginx 配置：**
```bash
sudo nano /etc/nginx/sites-available/code-review
```

修改 `server_name`：
```nginx
server_name your-domain.com www.your-domain.com;
```

**設定 DNS：**
在您的域名供應商設定 A 記錄指向樹莓派 IP。

### 2. 設定 HTTPS（Let's Encrypt）

```bash
# 安裝 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 取得 SSL 憑證（需要有域名）
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 測試自動續約
sudo certbot renew --dry-run

# 設定自動續約（每天檢查）
sudo crontab -e
# 添加以下行：
0 3 * * * certbot renew --quiet
```

**HTTPS 後配置：**
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL 優化
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # ... 其他配置
}

# HTTP 重新導向到 HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### 3. 設定防火牆

```bash
# 安裝 UFW
sudo apt install ufw -y

# 允許 SSH（重要！避免被鎖在外面）
sudo ufw allow 22/tcp

# 允許 HTTP 和 HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 或使用 Nginx 預設規則
sudo ufw allow 'Nginx Full'

# 啟用防火牆
sudo ufw enable

# 檢查狀態
sudo ufw status verbose
```

### 4. 效能優化

**Nginx 全域配置：**
```bash
sudo nano /etc/nginx/nginx.conf
```

優化設定：
```nginx
http {
    # 工作進程數（根據 CPU 核心數調整）
    worker_processes auto;
    worker_connections 1024;
    
    # 檔案快取
    open_file_cache max=1000 inactive=20s;
    open_file_cache_valid 30s;
    open_file_cache_min_uses 2;
    open_file_cache_errors on;
    
    # 連線優化
    keepalive_timeout 65;
    keepalive_requests 100;
    
    # 緩衝區優化
    client_body_buffer_size 16k;
    client_header_buffer_size 1k;
    client_max_body_size 8m;
    large_client_header_buffers 4 8k;
    
    # Gzip 優化
    gzip on;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
    gzip_min_length 1024;
    gzip_vary on;
    gzip_proxied any;
    
    # 其他配置...
}
```

### 5. 設定日誌輪替

```bash
sudo nano /etc/logrotate.d/nginx
```

```
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        if [ -f /var/run/nginx.pid ]; then
            kill -USR1 `cat /var/run/nginx.pid`
        fi
    endscript
}
```

## 📝 部署檢查清單

部署前請確認：

- [ ] 樹莓派系統已更新
- [ ] Nginx 已安裝並運行
- [ ] 專案檔案已上傳到樹莓派
- [ ] Nginx 網站配置已建立
- [ ] 檔案權限正確設定（755）
- [ ] Nginx 配置測試通過（`nginx -t`）
- [ ] Nginx 已重新載入
- [ ] 可以在瀏覽器中訪問網站
- [ ] 所有功能正常運作
- [ ] CSS 和 JS 正確載入
- [ ] （選用）已設定 HTTPS
- [ ] （選用）已設定防火牆
- [ ] （選用）已設定域名

## 🐛 部署疑難排解

### 問題 1：無法訪問網站（顯示 Nginx 預設頁面）

**原因：** 網站配置未正確啟用

**解決方案：**
```bash
# 檢查符號連結
ls -la /etc/nginx/sites-enabled/

# 確認 code-review 存在
# 如果不存在，重新建立
sudo ln -s /etc/nginx/sites-available/code-review /etc/nginx/sites-enabled/

# 移除預設網站
sudo rm /etc/nginx/sites-enabled/default

# 重新載入
sudo systemctl reload nginx
```

### 問題 2：CSS/JS 沒有載入（404 錯誤）

**檢查步驟：**
```bash
# 1. 確認檔案存在
ls -la /home/pi/code-review-app/public/css/
ls -la /home/pi/code-review-app/public/js/

# 2. 檢查檔案權限
# 應該是 755（資料夾）和 644（檔案）
chmod 755 /home/pi/code-review-app/public/css
chmod 644 /home/pi/code-review-app/public/css/style.css

# 3. 檢查 Nginx 錯誤日誌
sudo tail -50 /var/log/nginx/code-review-error.log

# 4. 檢查 HTML 中的路徑
# 應該是相對路徑：css/style.css 而非 /css/style.css
```

### 問題 3：403 Forbidden 錯誤

**原因：** 權限問題

**解決方案：**
```bash
# 設定正確的擁有者和權限
sudo chown -R pi:www-data /home/pi/code-review-app
sudo chmod -R 755 /home/pi/code-review-app

# 檢查 home 目錄權限
chmod 755 /home/pi

# 檢查 Nginx 使用者
ps aux | grep nginx
# 應該是 www-data

# 確認 Nginx 配置中的 user
grep user /etc/nginx/nginx.conf
```

### 問題 4：Nginx 無法啟動

**除錯步驟：**
```bash
# 1. 測試配置
sudo nginx -t

# 2. 查看詳細錯誤
sudo systemctl status nginx -l

# 3. 查看日誌
sudo tail -50 /var/log/nginx/error.log

# 4. 檢查 80 埠是否被佔用
sudo netstat -tunlp | grep :80

# 5. 如果被佔用，停止佔用的服務
sudo systemctl stop apache2  # 如果是 Apache
```

### 問題 5：動畫效果在樹莓派上很卡

**優化方案：**

**1. 降低動畫複雜度：**
```css
/* public/css/style.css */
/* 減少旋轉形狀數量或降低模糊效果 */
.glow-shape {
  filter: blur(0.2px);  /* 從 0.3px 降低 */
}

/* 或禁用某些動畫 */
.glow-wrap::after {
  animation: none;  /* 停用脈衝動畫 */
}
```

**2. 使用硬體加速：**
```css
.glow-shape {
  will-change: transform;
  transform: translateZ(0);
}
```

**3. 提升樹莓派效能：**
```bash
# 超頻（謹慎使用）
sudo raspi-config
# Performance Options → Overclock

# 分配更多 GPU 記憶體
sudo raspi-config
# Performance Options → GPU Memory → 128
```

### 問題 6：從外部網路無法訪問

**檢查步驟：**
```bash
# 1. 確認本地網路可訪問
# 在樹莓派同網段的設備測試
curl http://[樹莓派IP]

# 2. 檢查路由器設定
# 需要設定埠轉發：
# 外部埠 80 → 內部 IP [樹莓派IP]:80

# 3. 檢查 ISP 是否封鎖 80 埠
# 嘗試使用其他埠（如 8080）

# 4. 使用 DynDNS 服務
# 如果沒有固定 IP，使用動態 DNS
```

## 🔄 更新部署

當您修改了網頁後：

```bash
# 方法一：SCP 更新
scp -r public/* pi@[樹莓派IP]:/home/pi/code-review-app/public/

# 方法二：Git 更新（如果使用 Git）
# 在樹莓派上
cd ~/LLMs_Raspberry/前端開發環境配置/1_javascript
git pull

# 不需要重啟 Nginx（靜態檔案自動更新）
# 但建議清除瀏覽器快取後重新整理
```

## 📊 監控與維護

### 查看訪問統計

```bash
# 即時查看訪問日誌
sudo tail -f /var/log/nginx/code-review-access.log

# 統計訪問量
sudo cat /var/log/nginx/code-review-access.log | wc -l

# 查看最常訪問的頁面
sudo awk '{print $7}' /var/log/nginx/code-review-access.log | sort | uniq -c | sort -rn | head -10

# 查看訪問來源 IP
sudo awk '{print $1}' /var/log/nginx/code-review-access.log | sort | uniq -c | sort -rn | head -10
```

### 監控系統資源

```bash
# CPU 和記憶體
top
htop  # 需要安裝：sudo apt install htop

# 磁碟使用
df -h

# Nginx 狀態
sudo systemctl status nginx

# 網路連線
sudo netstat -tunlp | grep nginx
```

### 自動化備份

```bash
# 建立備份腳本
nano ~/backup-website.sh
```

```bash
#!/bin/bash
# 網站備份腳本

BACKUP_DIR="/home/pi/backups"
DATE=$(date +%Y%m%d_%H%M%S)
SITE_DIR="/home/pi/code-review-app"

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/website_backup_$DATE.tar.gz $SITE_DIR

# 只保留最近 7 天的備份
find $BACKUP_DIR -name "website_backup_*.tar.gz" -mtime +7 -delete

echo "備份完成：$BACKUP_DIR/website_backup_$DATE.tar.gz"
```

```bash
# 設定執行權限
chmod +x ~/backup-website.sh

# 設定 cron 自動備份（每天凌晨 2 點）
crontab -e
# 添加：
0 2 * * * /home/pi/backup-website.sh >> /home/pi/backup.log 2>&1
```

---

# 📚 學習資源

## 🎓 HTML/CSS/JavaScript 資源

### 官方文件
- [MDN Web Docs](https://developer.mozilla.org/zh-TW/) - 最權威的網頁技術文件
- [W3Schools](https://www.w3schools.com/) - 初學者友善的教學
- [Can I Use](https://caniuse.com/) - 檢查瀏覽器相容性

### 線上課程
- [freeCodeCamp](https://www.freecodecamp.org/chinese/) - 免費中文課程
- [Codecademy](https://www.codecademy.com/) - 互動式學習
- [Udemy](https://www.udemy.com/) - 付費專業課程

### YouTube 頻道
- [Traversy Media](https://www.youtube.com/user/TechGuyWeb)
- [The Net Ninja](https://www.youtube.com/channel/UCW5YeuERMmlnqo4oq8vwUpg)
- [Kevin Powell](https://www.youtube.com/kepowob) - CSS 專家

### 中文資源
- [前端大全](https://www.qianduan.net/)
- [iT 邦幫忙](https://ithelp.ithome.com.tw/)
- [六角學院](https://www.hexschool.com/)

## 🛠️ 開發工具

### 線上工具
- [CodePen](https://codepen.io/) - 線上程式碼測試
- [JSFiddle](https://jsfiddle.net/) - 快速測試
- [CSS Gradient](https://cssgradient.io/) - 漸層產生器
- [Google Fonts](https://fonts.google.com/) - 免費字型

### CSS 工具
- [Flexbox Froggy](https://flexboxfroggy.com/) - Flexbox 遊戲學習
- [Grid Garden](https://cssgridgarden.com/) - CSS Grid 遊戲學習
- [Animista](https://animista.net/) - CSS 動畫產生器

### JavaScript 工具
- [JavaScript.info](https://javascript.info/) - 深入 JavaScript
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS) - 深入理解 JS
- [30 Days of JavaScript](https://github.com/Asabeneh/30-Days-Of-JavaScript) - 30 天挑戰

## 📖 進階主題

### 網頁效能優化
- [Web.dev](https://web.dev/) - Google 的效能指南
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - 效能分析工具

### 響應式設計
- [Responsive Design Patterns](https://responsivedesign.is/patterns/) - 設計模式
- [Mobile First Design](https://www.uxpin.com/studio/blog/a-hands-on-guide-to-mobile-first-design/) - 行動優先

### 無障礙設計
- [WebAIM](https://webaim.org/) - 無障礙設計指南
- [A11y Project](https://www.a11yproject.com/) - 無障礙資源

---

## 📞 支援與回饋

遇到問題或有建議？

- 📧 Email: [您的 Email]
- 🐛 Issues: [GitHub Issues 連結]
- 💬 Discussions: [GitHub Discussions 連結]
- 📱 社群: [Discord/Slack 連結]

---

## 📄 授權

本專案採用 MIT 授權。

---

## 🙏 致謝

- 設計靈感來自 [Graphite](https://graphite.dev/)
- 使用純 HTML、CSS、JavaScript 打造
- 無依賴、無構建工具、開箱即用

---

## 🎉 專案特色

### ✨ 優點

1. **零依賴** - 無需 Node.js 或任何套件管理器
2. **超輕量** - 總檔案大小 < 50KB
3. **即時預覽** - 直接開啟 HTML 即可查看
4. **易於維護** - 程式碼簡單清晰
5. **效能優異** - 純靜態檔案，載入迅速
6. **跨平台** - 任何現代瀏覽器都能運行
7. **SEO 友善** - 純 HTML 結構
8. **部署簡單** - 複製檔案即可部署

### 🚀 適用場景

- ✅ 個人作品集網站
- ✅ 公司官網（靜態頁面）
- ✅ Landing Page
- ✅ 產品展示頁
- ✅ 活動宣傳頁
- ✅ 學習網頁開發
- ✅ 樹莓派專案
- ✅ 低成本部署需求

---

**🎊 恭喜！您已成功建立純 JavaScript 網頁應用！**

祝您開發愉快！Happy Coding! 🚀
