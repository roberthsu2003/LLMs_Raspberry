# TypeScript 開發環境配置

> 本專案示範如何建立一個完整的 TypeScript 開發環境，包含 ES6 模組、型別定義、Source Maps 等專業配置。

---

# 📋 目錄

- [👥 非開發者指南](#-非開發者指南) - 如何使用本專案
- [👨‍💻 開發者指南](#-開發者指南) - 如何開發和維護本專案
- [🚀 部署到樹莓派](#-部署到樹莓派) - Nginx 部署完整指南

---

# 👥 非開發者指南

> 💡 這部分適合不需要修改程式碼，只需要執行和使用本專案的使用者。

## 🚀 快速開始

### 🎯 本專案是什麼？

這是一個 TypeScript 示範專案，包含簡單的數學運算功能。即使您不懂程式設計，也可以按照以下步驟快速執行。

**功能說明：**
- ✅ 執行數學運算（加法、減法、乘法）
- ✅ 顯示計算結果
- ✅ 可部署到樹莓派網頁伺服器

### 📂 資料夾說明

```
2_typescript/
├── src/           # 程式源碼（TypeScript）
├── dist/          # 編譯後的檔案（自動產生）
├── package.json   # 專案設定檔
└── README.md      # 說明文件（本檔案）
```

## 🔧 系統需求

在開始之前，請確保已安裝：
- **Node.js**（版本 18 以上）- [下載連結](https://nodejs.org/)
- **npm**（隨 Node.js 一起安裝）

**檢查是否已安裝：**
```bash
node --version    # 應顯示 v18.x.x 或更高
npm --version     # 應顯示版本號
```

## ⚙️ 安裝步驟

### 步驟 1：進入專案資料夾

```bash
cd 前端開發環境配置/2_typescript
```

### 步驟 2：安裝必要套件

```bash
npm install
```

> 💡 **說明：** 這個指令會自動安裝所有需要的套件。

## ▶️ 執行專案

### 方法一：編譯後執行（推薦）

```bash
# 1. 編譯程式
npm run build

# 2. 執行程式
npm run start
```

**您會看到：**
```
加法:10 + 5 = 15
減法:10 - 5 = 5
```

### 方法二：一鍵編譯並執行

```bash
npm run dev
```

> 💡 **說明：** 這個指令會自動完成編譯和執行兩個步驟。

## 🧹 清理編譯檔案

如果需要清除編譯產生的檔案：

```bash
npm run clean
```

## ❓ 常見問題

### Q1: 執行時出現「找不到模組」錯誤？
**A:** 請先執行 `npm install` 安裝必要套件。

### Q2: `dist/` 資料夾是空的？
**A:** 需要先執行 `npm run build` 進行編譯。

### Q3: 如何修改計算的數字？
**A:** 請參考下方的「開發者指南」章節。

### Q4: 可以在樹莓派上執行嗎？
**A:** 可以！請參考本文件最下方的「部署到樹莓派」章節。

---

# 👨‍💻 開發者指南

> 💻 這部分適合需要修改程式碼、添加功能的開發者。

## 📋 技術架構

本專案使用的技術：
- ✅ **TypeScript 5.9.3** - 靜態型別檢查
- ✅ **ES6 模組系統** - `import`/`export` 語法
- ✅ **Node.js** - 執行環境
- ✅ **嚴格型別檢查** - 提前發現錯誤
- ✅ **Source Map** - 方便除錯
- ✅ **型別定義檔** - 自動生成 `.d.ts`

## 📂 詳細專案結構

```
2_typescript/
├── src/                    # TypeScript 源碼
│   ├── index.ts           # 程式進入點
│   └── utils/             # 工具函式模組
│       └── math.ts        # 數學運算函式
├── dist/                   # 編譯輸出（自動生成）
│   ├── index.js           # 編譯後的 JS
│   ├── index.js.map       # Source Map
│   ├── index.d.ts         # 型別定義檔
│   ├── index.d.ts.map     # 型別定義 Source Map
│   └── utils/
│       ├── math.js
│       ├── math.js.map
│       ├── math.d.ts
│       └── math.d.ts.map
├── node_modules/          # 依賴套件
├── package.json           # npm 專案配置
├── package-lock.json      # 套件版本鎖定
├── tsconfig.json          # TypeScript 編譯器配置
└── README.md              # 本文件
```

## 📝 程式碼說明

### `src/utils/math.ts` - 數學運算模組

```typescript
export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}
```

### `src/index.ts` - 主程式

```typescript
import { add, subtract } from './utils/math.js';

const result1 = add(10, 5);
const result2 = subtract(10, 5);

console.log(`加法:10 + 5 = ${result1}`);
console.log(`減法:10 - 5 = ${result2}`);
```

## ⚙️ 重要配置檔案

### `package.json` - npm 專案配置

```json
{
  "name": "2_typescript",
  "version": "1.0.0",
  "type": "module",          // ⚠️ 重要：使用 ES6 模組
  "scripts": {
    "build": "tsc",          // 編譯 TypeScript
    "start": "node dist/index.js",  // 執行編譯後的程式
    "dev": "tsc && node dist/index.js",  // 編譯並執行
    "clean": "rm -rf dist"   // 清理編譯輸出
  },
  "devDependencies": {
    "typescript": "^5.9.3",
    "@types/node": "^25.0.3"
  }
}
```

**關鍵設定說明：**
- `"type": "module"` - 啟用 ES6 模組系統，這是為什麼 import 路徑要用 `.js`

### `tsconfig.json` - TypeScript 編譯器配置

```json
{
  "compilerOptions": {
    // 檔案配置
    "rootDir": "./src",          // 源碼目錄
    "outDir": "./dist",          // 輸出目錄
    
    // 模組系統
    "module": "nodenext",        // Node.js ES 模組
    "target": "esnext",          // 編譯目標（最新 ECMAScript）
    
    // 型別檢查（嚴格模式）
    "strict": true,              // 啟用所有嚴格檢查
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    
    // 輸出檔案
    "sourceMap": true,           // 生成 Source Map（除錯用）
    "declaration": true,         // 生成 .d.ts 型別定義檔
    "declarationMap": true,      // 生成型別定義 Source Map
    
    // 其他
    "verbatimModuleSyntax": true,  // 嚴格模組語法
    "skipLibCheck": true          // 跳過函式庫檢查（加快編譯）
  }
}
```

## 🔨 開發工作流程

### 1. 修改程式碼

```bash
# 使用任何編輯器開啟檔案
code src/index.ts
```

### 2. 編譯檢查

```bash
npm run build
```

### 3. 測試執行

```bash
npm run start
```

### 4. 開發模式（自動編譯+執行）

```bash
npm run dev
```

## 🐛 常見開發問題

### Q: 為什麼 import 路徑要用 `.js` 而不是 `.ts`？

```typescript
// ✅ 正確
import { add } from './utils/math.js';

// ❌ 錯誤
import { add } from './utils/math.ts';
import { add } from './utils/math';
```

**原因：**
- `"type": "module"` 使用 ES6 模組
- ES6 模組的 import 路徑必須明確指定副檔名
- TypeScript 編譯後是 `.js` 檔案，所以要寫 `.js`

### Q: 出現「verbatimModuleSyntax」錯誤？

**錯誤訊息：**
```
ECMAScript imports and exports cannot be written in a CommonJS file
```

**解決方案：**
確保 `package.json` 中有 `"type": "module"`。

### Q: 如何新增功能模組？

1. 在 `src/` 下建立新檔案，例如 `src/utils/string.ts`
2. 匯出函式：

```typescript
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}
```

3. 在 `src/index.ts` 中匯入：

```typescript
import { capitalize } from './utils/string.js';
```

## 📦 可用的 npm 指令

| 指令 | 說明 | 使用時機 |
|------|------|---------|
| `npm install` | 安裝依賴套件 | 首次使用或套件更新後 |
| `npm run build` | 編譯 TypeScript | 修改程式碼後 |
| `npm run start` | 執行編譯後的程式 | 測試功能 |
| `npm run dev` | 編譯並執行 | 開發時快速測試 |
| `npm run clean` | 清理編譯輸出 | 重新編譯前 |

---

# 🚀 部署到樹莓派

> 🍓 完整的樹莓派部署指南，包含 Nginx 網頁伺服器配置。

## ⚠️ 重要說明

本專案目前是 **Node.js CLI 應用程式**，有兩種部署方式：

### 方式一：在樹莓派上直接執行（無需 Nginx）
適合：命令列執行、定時任務、後端處理

### 方式二：改造成網頁應用並用 Nginx 部署
適合：瀏覽器訪問、Web 介面

下面將詳細說明兩種方式。

---

## 🔧 方式一：樹莓派上直接執行 Node.js

### 步驟 1：在樹莓派上安裝 Node.js

```bash
# 更新系統
sudo apt update && sudo apt upgrade -y

# 安裝 Node.js（LTS 版本）
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# 驗證安裝
node --version    # 應顯示 v18.x.x 或更高
npm --version
```

### 步驟 2：上傳專案到樹莓派

**方法 A：使用 Git（推薦）**

```bash
# 在樹莓派上
cd ~
git clone [您的專案 Git URL]
cd LLMs_Raspberry/前端開發環境配置/2_typescript
```

**方法 B：使用 SCP 上傳**

```bash
# 在您的電腦上執行
scp -r 前端開發環境配置/2_typescript pi@[樹莓派IP]:/home/pi/
```

### 步驟 3：安裝依賴並執行

```bash
# 在樹莓派上
cd ~/2_typescript
npm install
npm run build
npm run start
```

### 步驟 4：設定為系統服務（開機自動執行）

建立 systemd 服務檔案：

```bash
sudo nano /etc/systemd/system/typescript-app.service
```

輸入以下內容：

```ini
[Unit]
Description=TypeScript Demo Application
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/2_typescript
ExecStart=/usr/bin/node /home/pi/2_typescript/dist/index.js
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

啟用並啟動服務：

```bash
# 重新載入 systemd
sudo systemctl daemon-reload

# 啟用服務（開機自動啟動）
sudo systemctl enable typescript-app.service

# 立即啟動服務
sudo systemctl start typescript-app.service

# 查看服務狀態
sudo systemctl status typescript-app.service

# 查看日誌
sudo journalctl -u typescript-app.service -f
```

---

## 🌐 方式二：改造成網頁應用 + Nginx 部署

### 為什麼需要改造？

目前的專案是 CLI 應用，輸出到終端機。要在瀏覽器中顯示，需要：
1. 建立 HTML 介面
2. 將 TypeScript 編譯成瀏覽器可執行的 JavaScript
3. 使用 Nginx 提供網頁服務

### 步驟 1：改造專案為網頁應用

#### 1.1 修改 TypeScript 配置

編輯 `tsconfig.json`：

```json
{
  "compilerOptions": {
    "rootDir": "./src",
    "outDir": "./dist",
    "module": "ES2020",           // 改為瀏覽器支援的模組
    "target": "ES2020",
    "lib": ["ES2020", "DOM"],     // 添加 DOM API
    "strict": true,
    "sourceMap": true,
    "declaration": false,          // 瀏覽器不需要型別定義檔
    "moduleResolution": "node",
    "skipLibCheck": true
  }
}
```

#### 1.2 修改源碼以支援瀏覽器

**修改 `src/utils/math.ts`：**（保持不變）

```typescript
export function add(a: number, b: number): number {
  return a + b;
}

export function subtract(a: number, b: number): number {
  return a - b;
}

export function multiply(a: number, b: number): number {
  return a * b;
}
```

**修改 `src/index.ts`：**

```typescript
import { add, subtract, multiply } from './utils/math.js';

// 建立結果顯示函式
function displayResult(operation: string, a: number, b: number, result: number) {
  const resultDiv = document.getElementById('results');
  if (resultDiv) {
    const p = document.createElement('p');
    p.textContent = `${operation}: ${a} 和 ${b} = ${result}`;
    resultDiv.appendChild(p);
  }
}

// 等待 DOM 載入完成
document.addEventListener('DOMContentLoaded', () => {
  console.log('TypeScript 網頁應用已啟動！');
  
  // 執行計算
  const num1 = 10;
  const num2 = 5;
  
  displayResult('加法', num1, num2, add(num1, num2));
  displayResult('減法', num1, num2, subtract(num1, num2));
  displayResult('乘法', num1, num2, multiply(num1, num2));
});
```

#### 1.3 建立 HTML 檔案

在專案根目錄建立 `public/index.html`：

```bash
mkdir -p public
nano public/index.html
```

輸入以下內容：

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TypeScript 數學運算示範</title>
    <style>
        body {
            font-family: 'Arial', 'Microsoft JhengHei', sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            color: #333;
        }
        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 30px;
        }
        #results {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            min-height: 100px;
        }
        #results p {
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-left: 4px solid #667eea;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .info {
            margin-top: 20px;
            padding: 15px;
            background: #e3f2fd;
            border-radius: 8px;
            border-left: 4px solid #2196f3;
        }
        footer {
            text-align: center;
            margin-top: 20px;
            color: rgba(255,255,255,0.8);
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧮 TypeScript 數學運算示範</h1>
        
        <div class="info">
            <strong>📌 專案說明：</strong>
            本網頁展示 TypeScript 編譯後在瀏覽器中執行的效果。
            所有計算都在您的瀏覽器中本地執行。
        </div>
        
        <h2>📊 計算結果</h2>
        <div id="results">
            <p>⏳ 正在載入...</p>
        </div>
    </div>
    
    <footer>
        🍓 部署在樹莓派 Nginx | TypeScript Demo Application
    </footer>
    
    <!-- 載入 TypeScript 編譯後的 JavaScript -->
    <script type="module" src="../dist/index.js"></script>
</body>
</html>
```

#### 1.4 更新 package.json

```json
{
  "name": "2_typescript",
  "version": "1.0.0",
  "description": "學習用",
  "license": "ISC",
  "author": "",
  "type": "module",
  "main": "index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsc && node dist/index.js",
    "clean": "rm -rf dist",
    "build:web": "tsc && cp -r public dist/"
  },
  "devDependencies": {
    "@types/node": "^25.0.3",
    "typescript": "^5.9.3"
  }
}
```

### 步驟 2：編譯專案

```bash
npm run build
```

### 步驟 3：在樹莓派上安裝 Nginx

```bash
# 安裝 Nginx
sudo apt update
sudo apt install nginx -y

# 啟動 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 檢查狀態
sudo systemctl status nginx
```

### 步驟 4：上傳檔案到樹莓派

```bash
# 在您的電腦上
scp -r 前端開發環境配置/2_typescript pi@[樹莓派IP]:/home/pi/
```

### 步驟 5：設定 Nginx

建立網站配置：

```bash
sudo nano /etc/nginx/sites-available/typescript-app
```

輸入以下配置：

```nginx
server {
    listen 80;
    server_name [您的樹莓派IP或域名];

    # 網站根目錄
    root /home/pi/2_typescript;
    index public/index.html;

    # 主頁面
    location / {
        try_files $uri $uri/ =404;
    }

    # 靜態檔案（JS, CSS）
    location ~* \.(js|css|map)$ {
        expires 1d;
        add_header Cache-Control "public, immutable";
    }

    # 錯誤頁面
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
}
```

啟用網站：

```bash
# 建立符號連結
sudo ln -s /etc/nginx/sites-available/typescript-app /etc/nginx/sites-enabled/

# 測試配置
sudo nginx -t

# 重新載入 Nginx
sudo systemctl reload nginx
```

### 步驟 6：設定檔案權限

```bash
# 確保 Nginx 可以讀取檔案
sudo chown -R pi:www-data /home/pi/2_typescript
sudo chmod -R 755 /home/pi/2_typescript
```

### 步驟 7：測試網站

在瀏覽器中訪問：
```
http://[樹莓派IP]
```

您應該會看到美觀的網頁介面，顯示數學運算結果！

---

## 🔒 進階配置（選用）

### 1. 設定 HTTPS（使用 Let's Encrypt）

```bash
# 安裝 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 取得 SSL 憑證
sudo certbot --nginx -d your-domain.com

# 自動更新憑證
sudo certbot renew --dry-run
```

### 2. 設定防火牆

```bash
# 允許 HTTP 和 HTTPS
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 3. 效能優化

編輯 Nginx 配置以啟用 Gzip 壓縮：

```nginx
# 在 server 區塊中添加
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;
```

---

## 📝 部署檢查清單

- [ ] 樹莓派已安裝 Node.js
- [ ] 樹莓派已安裝 Nginx
- [ ] 專案已上傳到樹莓派
- [ ] 執行 `npm install` 安裝依賴
- [ ] 執行 `npm run build` 編譯專案
- [ ] Nginx 配置檔案已設定
- [ ] 檔案權限已正確設定
- [ ] Nginx 已重新載入
- [ ] 可以在瀏覽器中訪問網站
- [ ] （選用）已設定 HTTPS
- [ ] （選用）已設定防火牆

---

## 🐛 部署疑難排解

### 問題 1：Nginx 無法啟動

```bash
# 檢查配置錯誤
sudo nginx -t

# 查看錯誤日誌
sudo tail -f /var/log/nginx/error.log
```

### 問題 2：無法訪問網站

```bash
# 檢查 Nginx 狀態
sudo systemctl status nginx

# 檢查防火牆
sudo ufw status

# 檢查樹莓派 IP
hostname -I
```

### 問題 3：JavaScript 檔案 404 錯誤

- 確認 `dist/` 資料夾存在且包含 `.js` 檔案
- 檢查 HTML 中的 script 路徑是否正確
- 確認檔案權限：`ls -la /home/pi/2_typescript/dist/`

### 問題 4：TypeScript 編譯錯誤

```bash
# 清理並重新編譯
npm run clean
npm run build

# 檢查 Node.js 版本
node --version  # 應該是 v18+ 
```

---

## 📚 詳細教學文件

以下是完整的 TypeScript 學習指南，適合想深入了解 TypeScript 的開發者。

## 目錄
- [簡介](#簡介)
- [什麼是 TypeScript](#什麼是-typescript)
- [環境準備](#環境準備)
- [開發工具](#開發工具)
- [建立 TypeScript 專案](#建立-typescript-專案)
- [專案結構](#專案結構)
- [TypeScript 配置檔案](#typescript-配置檔案)
- [開發流程](#開發流程)
- [常見問題與解決方案](#常見問題與解決方案)
- [進階功能](#進階功能)
- [最佳實踐](#最佳實踐)

## 簡介

本指南將帶領你從零開始建立 TypeScript 開發環境，適合剛接觸 TypeScript 的初學者，以及想要建立標準化開發流程的開發者。

## 什麼是 TypeScript

TypeScript 是由 Microsoft 開發的 JavaScript 超集（Superset），主要特點：

- **靜態型別檢查**：在編譯時期就能發現型別錯誤
- **更好的 IDE 支援**：提供智能提示、自動完成
- **物件導向特性**：支援類別、介面、泛型等
- **最終編譯成 JavaScript**：可在任何支援 JavaScript 的環境執行
- **向下相容**：所有 JavaScript 程式碼都是有效的 TypeScript 程式碼

### TypeScript vs JavaScript

| 特性 | JavaScript | TypeScript |
|------|-----------|-----------|
| 型別系統 | 動態型別 | 靜態型別 |
| 錯誤檢測 | 執行時期 | 編譯時期 |
| IDE 支援 | 基本 | 優秀 |
| 學習曲線 | 較平緩 | 較陡峭 |
| 檔案副檔名 | .js | .ts |

## 環境準備

### 系統需求

- **作業系統**：Windows、macOS 或 Linux
- **記憶體**：建議至少 4 GB RAM
- **硬碟空間**：至少 500 MB 可用空間

### 安裝 Node.js

TypeScript 需要 Node.js 環境才能執行編譯器。

#### 1. 下載並安裝 Node.js

訪問 [Node.js 官網](https://nodejs.org/)，下載 **LTS（長期支援版）**。

- **Windows / macOS**：下載安裝檔並執行
- **Linux（Ubuntu/Debian）**：

```bash
# 使用 NodeSource 安裝最新 LTS 版本
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### 2. 驗證安裝

打開終端機（Terminal）或命令提示字元（Command Prompt），輸入：

```bash
node --version
npm --version
```

應該會看到類似以下的版本號：
```
v20.11.0
10.2.4
```

### 安裝 TypeScript

#### 全域安裝（推薦用於學習）

```bash
npm install -g typescript
```

#### 驗證 TypeScript 安裝

```bash
tsc --version
```

應該會顯示類似：
```
Version 5.3.3
```

> **注意**：`tsc` 是 TypeScript Compiler（TypeScript 編譯器）的縮寫。

## 開發工具

### 必備工具

#### 1. 程式碼編輯器

**Visual Studio Code**（強烈推薦）
- [下載 VS Code](https://code.visualstudio.com/)
- 內建 TypeScript 支援
- 最佳的 TypeScript 開發體驗

**其他選擇**：
- WebStorm（付費，功能強大）
- Sublime Text + TypeScript 外掛
- Atom + TypeScript 外掛

#### 2. 瀏覽器

開發 Web 應用時需要：
- **Google Chrome**（推薦）
- **Firefox Developer Edition**
- **Microsoft Edge**

#### 3. 版本控制

- **Git**：[下載 Git](https://git-scm.com/)

### VS Code 推薦擴充功能

建議安裝以下擴充功能以提升開發效率：

```plaintext
必裝：
- ESLint：程式碼品質檢查
- Prettier：程式碼格式化
- Error Lens：即時顯示錯誤訊息

推薦：
- Path Intellisense：路徑自動完成
- TypeScript Importer：自動匯入型別
- Pretty TypeScript Errors：美化錯誤訊息顯示
- JavaScript and TypeScript Nightly：最新 TS 功能
- Code Spell Checker：拼字檢查
- GitLens：Git 增強功能
- Auto Rename Tag：自動重命名配對標籤
- Bracket Pair Colorizer 2：括號配對顏色
```

#### 安裝擴充功能步驟

1. 打開 VS Code
2. 點擊左側的擴充功能圖示（或按 `Ctrl+Shift+X` / `Cmd+Shift+X`）
3. 搜尋擴充功能名稱
4. 點擊「Install」安裝

## 建立 TypeScript 專案

### 方法一：手動建立（推薦初學者）

#### 步驟 1：建立專案資料夾

```bash
# 建立專案目錄
mkdir my-typescript-project
cd my-typescript-project
```

#### 步驟 2：初始化 npm 專案

```bash
npm init -y
```

這會建立 `package.json` 檔案。

#### 步驟 3：初始化 TypeScript 配置

```bash
tsc --init
```

這會建立 `tsconfig.json` 檔案（TypeScript 編譯器配置檔）。

#### 步驟 4：建立基本目錄結構

```bash
# 建立目錄
mkdir src dist

# 建立第一個 TypeScript 檔案
touch src/index.ts
```

#### 步驟 5：編寫第一個 TypeScript 程式

使用 VS Code 或任何文字編輯器打開 `src/index.ts`：

```typescript
// src/index.ts
function greet(name: string): string {
    return `你好，${name}！歡迎學習 TypeScript！`;
}

const userName: string = "學生";
console.log(greet(userName));

// 這會產生錯誤：類型 'number' 不能指派給類型 'string'
// const wrongType: string = 123;
```

#### 步驟 6：編譯 TypeScript

```bash
tsc
```

或者指定檔案：

```bash
tsc src/index.ts
```

編譯成功後，會在 `dist` 目錄下產生 `index.js` 檔案。

#### 步驟 7：執行編譯後的 JavaScript

```bash
node dist/index.js
```

你應該會看到輸出：
```
你好，學生！歡迎學習 TypeScript！
```

### 方法二：使用 npm scripts（推薦進階使用）

編輯 `package.json`，在 `scripts` 區塊中加入：

```json
{
  "name": "my-typescript-project",
  "version": "1.0.0",
  "description": "我的 TypeScript 專案",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsc --watch",
    "clean": "rm -rf dist"
  },
  "keywords": ["typescript"],
  "author": "你的名字",
  "license": "MIT",
  "devDependencies": {
    "typescript": "^5.3.3"
  }
}
```

現在可以使用以下指令：

```bash
npm run build   # 編譯 TypeScript
npm start       # 執行程式
npm run dev     # 監看模式（檔案變更時自動編譯）
npm run clean   # 清除編譯輸出
```

### 方法三：安裝 ts-node（即時執行）

如果想要直接執行 TypeScript 檔案而不用先編譯：

```bash
# 安裝 ts-node
npm install -D ts-node @types/node

# 直接執行 TypeScript 檔案
npx ts-node src/index.ts
```

在 `package.json` 中加入快速執行腳本：

```json
{
  "scripts": {
    "dev": "ts-node src/index.ts",
    "watch": "ts-node-dev --respawn src/index.ts"
  }
}
```

## 專案結構

### 基本結構

```
my-typescript-project/
│
├── src/                    # TypeScript 原始碼
│   ├── index.ts           # 主程式進入點
│   ├── utils/             # 工具函式
│   │   └── helpers.ts
│   ├── models/            # 資料模型/介面
│   │   └── User.ts
│   ├── services/          # 業務邏輯
│   │   └── UserService.ts
│   └── types/             # 型別定義
│       └── custom.d.ts
│
├── dist/                   # 編譯後的 JavaScript（自動產生）
│   └── index.js
│
├── node_modules/          # npm 套件（自動產生）
│
├── tests/                 # 測試檔案
│   └── index.test.ts
│
├── .gitignore            # Git 忽略檔案
├── package.json          # npm 專案配置
├── package-lock.json     # npm 依賴鎖定檔案
├── tsconfig.json         # TypeScript 編譯器配置
├── README.md             # 專案說明
└── LICENSE               # 授權文件
```

### Web 應用專案結構

如果是開發 Web 前端應用：

```
typescript-web-app/
│
├── src/
│   ├── ts/                # TypeScript 檔案
│   │   ├── main.ts
│   │   ├── components/
│   │   └── utils/
│   │
│   ├── css/               # 樣式檔案
│   │   └── style.css
│   │
│   └── assets/            # 靜態資源
│       └── images/
│
├── dist/                  # 輸出目錄（用於部署）
│   ├── js/               # 編譯後的 JS
│   ├── css/              # 複製的 CSS
│   └── index.html        # HTML 檔案
│
├── public/                # 公開資源
│   └── index.html
│
├── tsconfig.json
├── package.json
└── README.md
```

## TypeScript 配置檔案

### tsconfig.json 詳解

`tsconfig.json` 是 TypeScript 專案的核心配置檔案。

#### 基礎配置（推薦初學者）

```json
{
  "compilerOptions": {
    /* 語言與環境 */
    "target": "ES2020",                    // 編譯目標 JavaScript 版本
    "lib": ["ES2020"],                     // 包含的標準函式庫
    
    /* 模組 */
    "module": "commonjs",                  // 模組系統（Node.js 使用 commonjs）
    "rootDir": "./src",                    // 原始碼根目錄
    "outDir": "./dist",                    // 編譯輸出目錄
    
    /* JavaScript 支援 */
    "allowJs": false,                      // 是否允許編譯 JS 檔案
    "checkJs": false,                      // 是否檢查 JS 檔案中的錯誤
    
    /* 型別檢查 */
    "strict": true,                        // 啟用所有嚴格型別檢查選項
    "noImplicitAny": true,                 // 不允許隱式的 any 型別
    "strictNullChecks": true,              // 嚴格的 null 檢查
    
    /* 模組解析 */
    "esModuleInterop": true,               // 支援 ES 模組互通
    "moduleResolution": "node",            // 使用 Node.js 模組解析策略
    "resolveJsonModule": true,             // 允許匯入 JSON 檔案
    
    /* 輸出 */
    "sourceMap": true,                     // 產生 .map 檔案（用於除錯）
    "removeComments": true,                // 移除註解
    
    /* 其他 */
    "skipLibCheck": true,                  // 跳過函式庫型別檢查（加快編譯）
    "forceConsistentCasingInFileNames": true  // 確保檔案名稱大小寫一致
  },
  "include": [
    "src/**/*"                            // 包含 src 目錄下所有檔案
  ],
  "exclude": [
    "node_modules",                       // 排除 node_modules
    "dist",                               // 排除輸出目錄
    "**/*.test.ts"                        // 排除測試檔案
  ]
}
```

#### Web 專案配置

如果是開發瀏覽器端應用：

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],  // 加入 DOM API
    "module": "ES2020",                         // 使用 ES 模組
    "moduleResolution": "node",
    "rootDir": "./src/ts",
    "outDir": "./dist/js",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "sourceMap": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["src/ts/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### package.json 配置

完整的 `package.json` 範例：

```json
{
  "name": "my-typescript-project",
  "version": "1.0.0",
  "description": "TypeScript 專案範本",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "watch": "tsc --watch",
    "clean": "rm -rf dist",
    "lint": "eslint src/**/*.ts",
    "format": "prettier --write \"src/**/*.ts\""
  },
  "keywords": [
    "typescript",
    "nodejs"
  ],
  "author": "你的名字",
  "license": "MIT",
  "devDependencies": {
    "@types/node": "^20.10.0",
    "typescript": "^5.3.3",
    "ts-node": "^10.9.2",
    "eslint": "^8.55.0",
    "prettier": "^3.1.0"
  }
}
```

### .gitignore 配置

建立 `.gitignore` 檔案以排除不必要的檔案：

```gitignore
# 依賴套件
node_modules/

# 編譯輸出
dist/
build/
*.js
*.js.map

# TypeScript 快取
*.tsbuildinfo

# 作業系統檔案
.DS_Store
Thumbs.db

# 編輯器檔案
.vscode/
.idea/
*.swp
*.swo

# 環境變數
.env
.env.local

# 日誌檔案
*.log
npm-debug.log*

# 測試覆蓋率
coverage/
```

## 開發流程

### 標準開發流程

#### 1. 建立新專案

```bash
# 建立專案目錄
mkdir my-project && cd my-project

# 初始化 npm 專案
npm init -y

# 安裝 TypeScript
npm install -D typescript @types/node

# 初始化 TypeScript 配置
npx tsc --init

# 建立目錄結構
mkdir src dist
```

#### 2. 設定開發環境

編輯 `tsconfig.json`，調整適合你的配置。

#### 3. 開發程式碼

在 `src` 目錄下撰寫 TypeScript 程式碼。

**範例：建立一個簡單的模組**

```typescript
// src/utils/math.ts
export function add(a: number, b: number): number {
    return a + b;
}

export function subtract(a: number, b: number): number {
    return a - b;
}
```

```typescript
// src/index.ts
import { add, subtract } from './utils/math';

const result1 = add(10, 5);
const result2 = subtract(10, 5);

console.log(`加法：10 + 5 = ${result1}`);
console.log(`減法：10 - 5 = ${result2}`);
```

#### 4. 編譯與執行

```bash
# 編譯
npm run build

# 執行
npm start
```

或使用監看模式自動編譯：

```bash
npm run watch
```

#### 5. 版本控制

```bash
# 初始化 Git
git init

# 加入 .gitignore
echo "node_modules/" > .gitignore
echo "dist/" >> .gitignore

# 第一次提交
git add .
git commit -m "Initial commit: TypeScript project setup"
```

### 開發技巧

#### 使用 VS Code 的整合終端機

1. 在 VS Code 中按 `` Ctrl+` ``（或 `` Cmd+` ``）開啟終端機
2. 執行 `npm run watch` 保持編譯器運行
3. 在另一個終端機視窗執行程式

#### 即時預覽（Web 應用）

如果是開發網頁應用：

1. 安裝 Live Server 擴充功能
2. 在 `public/index.html` 中引入編譯後的 JS
3. 右鍵選擇「Open with Live Server」

```html
<!-- public/index.html -->
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TypeScript Web App</title>
</head>
<body>
    <h1>我的 TypeScript 應用</h1>
    <div id="app"></div>
    
    <!-- 引入編譯後的 JavaScript -->
    <script src="../dist/js/main.js"></script>
</body>
</html>
```

## 常見問題與解決方案

### 問題 1：找不到 tsc 指令

**錯誤訊息：**
```
tsc: command not found
```

**解決方案：**

```bash
# 全域安裝 TypeScript
npm install -g typescript

# 或使用 npx
npx tsc --version
```

### 問題 2：無法找到模組

**錯誤訊息：**
```
Cannot find module './utils/math'
```

**解決方案：**

1. 檢查檔案路徑是否正確
2. 確認 `tsconfig.json` 中的 `rootDir` 設定
3. 使用相對路徑，並省略 `.ts` 副檔名

```typescript
// 正確
import { add } from './utils/math';

// 錯誤
import { add } from './utils/math.ts';
```

### 問題 3：型別錯誤

**錯誤訊息：**
```
Type 'string' is not assignable to type 'number'
```

**解決方案：**

確保變數的型別與賦值一致：

```typescript
// 錯誤
let age: number = "25";

// 正確
let age: number = 25;
```

### 問題 4：隱式 any 型別

**錯誤訊息：**
```
Parameter 'x' implicitly has an 'any' type
```

**解決方案：**

為參數明確指定型別：

```typescript
// 錯誤
function greet(name) {
    return `Hello, ${name}`;
}

// 正確
function greet(name: string): string {
    return `Hello, ${name}`;
}
```

### 問題 5：編譯很慢

**解決方案：**

在 `tsconfig.json` 中加入：

```json
{
  "compilerOptions": {
    "skipLibCheck": true,
    "incremental": true
  }
}
```

## 進階功能

### 型別定義檔（.d.ts）

如果使用第三方 JavaScript 函式庫，可能需要安裝型別定義：

```bash
# 安裝 lodash 及其型別定義
npm install lodash
npm install -D @types/lodash
```

### 路徑別名（Path Mapping）

在 `tsconfig.json` 中設定路徑別名，避免複雜的相對路徑：

```json
{
  "compilerOptions": {
    "baseUrl": "./",
    "paths": {
      "@utils/*": ["src/utils/*"],
      "@models/*": ["src/models/*"],
      "@services/*": ["src/services/*"]
    }
  }
}
```

使用方式：

```typescript
// 原本
import { Helper } from '../../../utils/helper';

// 使用別名
import { Helper } from '@utils/helper';
```

### 程式碼檢查（ESLint）

安裝並設定 ESLint：

```bash
# 安裝 ESLint 與 TypeScript 相關套件
npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

建立 `.eslintrc.json`：

```json
{
  "parser": "@typescript-eslint/parser",
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "plugins": ["@typescript-eslint"],
  "env": {
    "node": true,
    "es6": true
  },
  "rules": {
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

在 `package.json` 中加入腳本：

```json
{
  "scripts": {
    "lint": "eslint src/**/*.ts",
    "lint:fix": "eslint src/**/*.ts --fix"
  }
}
```

### 程式碼格式化（Prettier）

安裝 Prettier：

```bash
npm install -D prettier
```

建立 `.prettierrc`：

```json
{
  "semi": true,
  "trailingComma": "all",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2
}
```

在 `package.json` 中加入腳本：

```json
{
  "scripts": {
    "format": "prettier --write \"src/**/*.ts\""
  }
}
```

## 最佳實踐

### 1. 型別優先

始終明確定義型別，避免使用 `any`：

```typescript
// ❌ 不好
function process(data: any) {
    return data;
}

// ✅ 好
interface User {
    id: number;
    name: string;
    email: string;
}

function processUser(user: User): User {
    return user;
}
```

### 2. 使用介面和型別別名

```typescript
// 介面（適合物件結構）
interface Product {
    id: number;
    name: string;
    price: number;
}

// 型別別名（適合聯合型別、交叉型別）
type Status = 'pending' | 'approved' | 'rejected';
type ID = string | number;
```

### 3. 善用泛型

```typescript
// 泛型函式
function getFirstElement<T>(arr: T[]): T | undefined {
    return arr[0];
}

const firstNumber = getFirstElement([1, 2, 3]); // number | undefined
const firstString = getFirstElement(['a', 'b']); // string | undefined
```

### 4. 啟用嚴格模式

在 `tsconfig.json` 中設定：

```json
{
  "compilerOptions": {
    "strict": true
  }
}
```

### 5. 組織專案結構

將程式碼按功能模組化：

```
src/
├── models/         # 資料模型
├── services/       # 業務邏輯
├── utils/          # 工具函式
├── types/          # 型別定義
└── index.ts        # 進入點
```

### 6. 編寫清晰的型別註解

```typescript
/**
 * 計算兩個數字的和
 * @param a - 第一個數字
 * @param b - 第二個數字
 * @returns 兩數之和
 */
function add(a: number, b: number): number {
    return a + b;
}
```

### 7. 使用 readonly 和 const

```typescript
// 常數
const MAX_SIZE = 100;

// 唯讀屬性
interface Config {
    readonly apiUrl: string;
    readonly timeout: number;
}

// 唯讀陣列
const numbers: readonly number[] = [1, 2, 3];
// numbers.push(4); // 錯誤：不能修改唯讀陣列
```

### 8. 避免過度使用型別斷言

```typescript
// ❌ 不好（除非確定型別）
const value = someValue as string;

// ✅ 好（使用型別守衛）
if (typeof someValue === 'string') {
    const value = someValue;
}
```

---

## 總結

恭喜你完成 TypeScript 開發環境的建立！現在你已經具備：

✅ TypeScript 開發環境  
✅ 專案結構與配置  
✅ 編譯與執行流程  
✅ 開發工具與擴充功能  
✅ 最佳實踐與常見問題解決

### 下一步學習

1. **深入學習 TypeScript 語法**：介面、類別、泛型、裝飾器
2. **實作專案**：Todo List、API 客戶端、CLI 工具
3. **學習框架**：React + TypeScript、Vue + TypeScript、Node.js + TypeScript
4. **進階主題**：型別體操、編譯器 API、模組打包

### 推薦資源

- [TypeScript 官方文件](https://www.typescriptlang.org/docs/)
- [TypeScript 線上練習](https://www.typescriptlang.org/play)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)

---

**祝你學習愉快！有任何問題歡迎隨時詢問！** 🚀