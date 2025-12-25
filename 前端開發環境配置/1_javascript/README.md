# HTML、CSS、JavaScript 開發環境配置

## 目錄
- [簡介](#簡介)
- [開發工具](#開發工具)
- [專案結構](#專案結構)
- [標準配置檔案](#標準配置檔案)
- [開發流程](#開發流程)
- [測試與除錯](#測試與除錯)
- [免費部署空間](#免費部署空間)
- [最佳實踐](#最佳實踐)

## 簡介

本指南介紹如何建立純 HTML、CSS、JavaScript 的開發環境，**不使用 Node.js** 和 **不使用 Vite** 等構建工具。適合初學者或需要快速開發靜態網頁的專案。

## 開發工具

### 必備工具

1. **程式碼編輯器**
   - [Visual Studio Code](https://code.visualstudio.com/)（推薦）
   - [Sublime Text](https://www.sublimetext.com/)
   - [Notepad++](https://notepad-plus-plus.org/)

2. **瀏覽器**
   - Google Chrome（推薦用於開發）
   - Firefox Developer Edition
   - Safari（Mac）
   - Microsoft Edge

3. **版本控制**
   - [Git](https://git-scm.com/)

### VS Code 推薦擴充功能

```plaintext
- Live Server：即時預覽網頁
- HTML CSS Support：CSS 類別名稱智能提示
- Auto Rename Tag：自動重命名配對標籤
- Prettier：程式碼格式化
- ESLint：JavaScript 語法檢查
- Path Intellisense：路徑自動完成
- IntelliSense for CSS：CSS 智能提示
- JavaScript (ES6) code snippets：JavaScript 程式碼片段
```

## 專案結構

### 基本結構

```
project-name/
│
├── index.html              # 主頁面
├── about.html              # 關於頁面
├── contact.html            # 聯絡頁面
│
├── css/
│   ├── style.css          # 主樣式表
│   ├── reset.css          # CSS 重置
│   └── responsive.css     # 響應式設計
│
├── js/
│   ├── main.js            # 主要 JavaScript
│   ├── utils.js           # 工具函式
│   └── components/        # 元件 JavaScript
│       ├── navbar.js
│       └── footer.js
│
├── images/                # 圖片資源
│   ├── logo.png
│   ├── banner.jpg
│   └── icons/
│
├── assets/                # 其他資源
│   ├── fonts/            # 字型檔案
│   ├── videos/           # 影片檔案
│   └── documents/        # 文件檔案
│
├── .gitignore            # Git 忽略檔案
├── README.md             # 專案說明
└── LICENSE               # 授權文件
```


## 標準配置檔案

### 必要的配置檔案

以下是純 HTML、CSS、JavaScript 專案應該包含的標準配置檔案：

### 1. `.gitignore`

```gitignore
# 作業系統檔案
.DS_Store
Thumbs.db
desktop.ini

# 編輯器檔案
.vscode/
.idea/
*.swp
*.swo
*~

# 臨時檔案
*.log
*.tmp
*.bak

# 環境變數
.env
.env.local

# 依賴套件（如果之後需要使用）
node_modules/
vendor/

# 建置檔案
dist/
build/

# 其他
*.zip
*.rar
```

### 2. `README.md`

每個專案都應該有一個清楚的 README.md 檔案，說明專案的目的、使用方式和技術細節。

```markdown
# 專案名稱

簡短描述專案的目的和功能

## 功能特色

- 功能 1
- 功能 2
- 功能 3

## 使用技術

- HTML5
- CSS3
- JavaScript (ES6+)

## 安裝與執行

1. 克隆專案
   ```bash
   git clone [repository-url]
   ```

2. 使用 Live Server 或直接開啟 `index.html`

## 專案結構

（說明專案的檔案結構）

## 瀏覽器支援

- Chrome（最新版本）
- Firefox（最新版本）
- Safari（最新版本）
- Edge（最新版本）

## 授權

MIT License
```

### 3. `LICENSE`

選擇適合的開源授權，常見選項：
- **MIT License**：最常用、最寬鬆，適合大多數專案
- **Apache License 2.0**：提供專利保護
- **GPL-3.0**：要求衍生作品也要開源
- **BSD License**：類似 MIT，但有更多變體



## 開發流程

### 1. 建立專案

```bash
# 建立專案資料夾
mkdir my-project
cd my-project

# 初始化 Git
git init

# 建立基本結構
mkdir css js images assets
touch index.html css/style.css js/main.js .gitignore README.md
```

### 2. 開始開發

使用 VS Code 的 Live Server 擴充功能：
1. 在 VS Code 中開啟專案資料夾
2. 安裝 Live Server 擴充功能
3. 在 `index.html` 上按右鍵
4. 選擇「Open with Live Server」
5. 瀏覽器會自動開啟並即時重載

### 3. 版本控制

```bash
# 第一次提交
git add .
git commit -m "Initial commit"

# 建立遠端儲存庫並推送
git remote add origin [repository-url]
git branch -M main
git push -u origin main
```

## 測試與除錯

### 1. 瀏覽器開發者工具

- **Chrome DevTools**：`F12` 或 `Cmd+Option+I`（Mac）
- 主要功能：
  - **Elements**：檢查和修改 HTML/CSS
  - **Console**：查看 JavaScript 錯誤和輸出
  - **Network**：監控網路請求
  - **Sources**：除錯 JavaScript 程式碼
  - **Performance**：效能分析和優化

### 2. 程式碼驗證工具

- **HTML 驗證**：[W3C Markup Validation](https://validator.w3.org/)
- **CSS 驗證**：[W3C CSS Validation](https://jigsaw.w3.org/css-validator/)
- **JavaScript 檢查**：使用 ESLint 或瀏覽器 Console
- **效能測試**：[Google PageSpeed Insights](https://pagespeed.web.dev/)
- **SEO 檢查**：[Google Search Console](https://search.google.com/search-console)

### 3. 跨瀏覽器測試

建議在多個瀏覽器中測試您的網站：
- **本機測試**：Chrome、Firefox、Safari、Edge
- **線上測試工具**：
  - [BrowserStack](https://www.browserstack.com/)（付費，有免費試用）
  - [LambdaTest](https://www.lambdatest.com/)（部分功能免費）

## 免費部署空間

以下是適合部署純 HTML、CSS、JavaScript 專案的免費平台，依推薦程度排序：

### 1. GitHub Pages ⭐ 推薦

**優點：**
- 完全免費
- 與 GitHub 無縫整合
- 支援自訂網域
- 自動 HTTPS
- 更新方便（推送程式碼即部署）

**部署步驟：**

```bash
# 1. 推送程式碼到 GitHub
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main

# 2. 在 GitHub 儲存庫設定
# Settings → Pages → Source → main branch → Save
```

**網址格式：** `https://username.github.io/repository-name/`

**注意事項：**
- 公開儲存庫完全免費
- 私有儲存庫需要 GitHub Pro（學生可免費申請）

---

### 2. Netlify ⭐ 推薦

**優點：**
- 免費方案功能強大
- 拖放部署
- 持續部署（CI/CD）
- 自訂網域
- 表單處理
- 無伺服器函式（Functions）

**部署方式：**

**方法一：拖放部署**
1. 訪問 [Netlify](https://www.netlify.com/)
2. 註冊/登入
3. 拖放專案資料夾到 Netlify

**方法二：Git 連接**
1. 連接 GitHub/GitLab/Bitbucket
2. 選擇儲存庫
3. 自動部署

**免費額度：**
- 100 GB 頻寬/月
- 300 分鐘建置時間/月
- 無限網站數量

---

### 3. Vercel

**優點：**
- 極快的部署速度
- 優秀的開發者體驗
- 自動 HTTPS
- 全球 CDN
- 預覽部署

**部署步驟：**
1. 訪問 [Vercel](https://vercel.com/)
2. 連接 GitHub 帳號
3. 匯入專案
4. 自動部署

**免費額度：**
- 100 GB 頻寬/月
- 無限網站
- 個人專案完全免費

---

### 4. Cloudflare Pages

**優點：**
- 無限頻寬
- 全球 CDN
- 快速部署
- 與 Cloudflare 生態系統整合

**部署步驟：**
1. 訪問 [Cloudflare Pages](https://pages.cloudflare.com/)
2. 連接 Git 儲存庫
3. 配置建置設定
4. 部署

**免費額度：**
- 無限頻寬
- 無限請求
- 500 次建置/月

---

### 5. Render

**優點：**
- 支援靜態網站
- 自動 SSL
- 全球 CDN
- 持續部署

**部署步驟：**
1. 訪問 [Render](https://render.com/)
2. 新增靜態網站
3. 連接 Git 儲存庫
4. 部署

**免費額度：**
- 100 GB 頻寬/月
- 自動 SSL

---

### 6. Firebase Hosting

**優點：**
- Google 支持
- 快速 CDN
- 與 Firebase 服務整合
- 自動 SSL

**部署步驟：**

```bash
# 1. 安裝 Firebase CLI（需要 Node.js）
npm install -g firebase-tools

# 2. 登入
firebase login

# 3. 初始化專案
firebase init hosting

# 4. 部署
firebase deploy
```

**免費額度：**
- 10 GB 儲存空間
- 360 MB/天 下載量

**注意事項：**
- Firebase Hosting 需要安裝 Node.js 環境來使用 CLI 工具
- 適合需要與其他 Firebase 服務整合的專案

---

## 各平台比較表

| 平台 | 頻寬 | 部署方式 | 自訂網域 | HTTPS | 推薦度 |
|------|------|----------|----------|-------|--------|
| **GitHub Pages** | 100 GB/月 | Git | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Netlify** | 100 GB/月 | 拖放/Git | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Vercel** | 100 GB/月 | Git | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Cloudflare Pages** | 無限 | Git | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| **Render** | 100 GB/月 | Git | ✅ | ✅ | ⭐⭐⭐⭐ |
| **Firebase Hosting** | 360 MB/天 | CLI | ✅ | ✅ | ⭐⭐⭐⭐ |

---

## 部署建議

### 初學者推薦
1. **GitHub Pages**：最簡單，與學習 Git 完美結合
2. **Netlify**：支援拖放部署，無需複雜設定

### 專業開發者推薦
1. **Vercel**：效能優秀，開發者體驗極佳
2. **Cloudflare Pages**：無限頻寬，全球 CDN 加速
3. **Netlify**：功能完整，生態系統豐富

### 快速測試推薦
- **Netlify**：拖放資料夾即可部署
- **Vercel**：連接 GitHub 後自動部署

---

## 透過AI快速開發
1. [創意圖片](./創意發想圖片/index.png)
2. [AI產生HTML](./AI產生HTML/index.html)

