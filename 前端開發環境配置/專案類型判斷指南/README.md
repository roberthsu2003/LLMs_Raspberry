# 🎯 專案類型判斷指南

> **重要**：從外部 AI 網站下載的前端專案可能包含不同技術棧，本指南幫助你快速判斷專案類型並選擇正確的開發工具。

### 📋 快速判斷流程圖

```
下載專案後
    ↓
檢查是否有 package.json？
    ├─ 否 → 【類型 1】純 HTML/CSS/JavaScript
    │         → 直接開啟 HTML 檔案即可
    │
    └─ 是 → 檢查 package.json 內容
            ├─ 有 next → 【類型 4】Next.js
            │            → 需要：Node.js, npm（內建建置工具）
            │
            ├─ 有 react/react-dom → 【類型 3】TypeScript + React
            │                       → 需要：Node.js, npm, Vite/Webpack
            │
            └─ 有 typescript → 【類型 2】TypeScript
                               → 需要：Node.js, npm, TypeScript 編譯器
```

---

## 🔍 詳細判斷方法

### 步驟 1：檢查專案根目錄的檔案

打開下載的專案資料夾，查看根目錄有哪些檔案：

#### ✅ 檢查清單

- [ ] 是否有 `package.json`？
- [ ] 是否有 `next` 在 dependencies？（Next.js 專案）
- [ ] 是否有 `next.config.js` 或 `next.config.ts`？（Next.js 專案）
- [ ] 是否有 `app/` 或 `pages/` 資料夾？（Next.js 路由結構）
- [ ] 是否有 `tsconfig.json`？
- [ ] 是否有 `vite.config.ts` 或 `webpack.config.js`？
- [ ] 是否有 `src/` 資料夾？
- [ ] 是否有 `node_modules/` 資料夾？
- [ ] 是否有 `.js` 或 `.ts` 檔案？

---

## 📦 類型 1：HTML + CSS + JavaScript（純前端）

### 識別特徵

**檔案結構：**
```
專案資料夾/
├── index.html          # 主 HTML 檔案
├── css/
│   └── style.css      # 樣式檔案
├── js/
│   └── main.js        # JavaScript 檔案（.js 結尾）
└── images/            # 圖片資源（選用）
```

**關鍵指標：**
- ✅ 沒有 `package.json`，或 `package.json` 中沒有 `dependencies` 和 `devDependencies`
- ✅ 只有 `.html`、`.css`、`.js` 檔案
- ✅ 沒有 `tsconfig.json`
- ✅ 沒有 `src/` 資料夾（或 `src/` 中只有 `.js` 檔案）

**package.json 範例：**
```json
{
  "name": "my-project",
  "scripts": {
    "serve": "python3 -m http.server 8000"
  }
}
```
（注意：沒有 `dependencies` 或 `devDependencies`）

### 需要的工具

- ✅ **不需要任何工具**！直接開啟 HTML 檔案即可
- 選用：VS Code + Live Server 擴充功能（方便開發）

### 如何運行

**方法一：直接開啟（最簡單）**
```bash
# 雙擊 index.html 檔案，或在瀏覽器中開啟
open index.html
```

**方法二：使用 Python 內建伺服器**
```bash
# Python 3
python3 -m http.server 8000

# 然後在瀏覽器訪問：http://localhost:8000
```

**方法三：使用 VS Code Live Server**
1. 安裝 Live Server 擴充功能
2. 右鍵點擊 `index.html`
3. 選擇「Open with Live Server」

### 相關文件

👉 [詳細的 JavaScript 專案配置指南](../1_javascript/README.md)

---

## 📘 類型 2：HTML + CSS + TypeScript

### 識別特徵

**檔案結構：**
```
專案資料夾/
├── package.json        # 有 TypeScript 相關依賴
├── tsconfig.json       # TypeScript 配置檔案 ⭐
├── src/                # 原始碼資料夾
│   ├── index.ts        # TypeScript 檔案（.ts 結尾）⭐
│   └── utils/
│       └── math.ts
├── dist/               # 編譯後的 JavaScript（選用）
│   └── index.js
└── public/             # 靜態資源
    ├── index.html
    └── css/
        └── style.css
```

**關鍵指標：**
- ✅ 有 `tsconfig.json` 檔案 ⭐
- ✅ 有 `.ts` 檔案（TypeScript 原始碼）⭐
- ✅ `package.json` 中有 `typescript` 在 `devDependencies`
- ✅ 可能有 `@types/*` 套件（型別定義）
- ✅ 沒有 `react` 或 `react-dom` 在 `dependencies`

**package.json 範例：**
```json
{
  "name": "my-typescript-project",
  "scripts": {
    "build": "tsc",
    "dev": "tsc && node dist/index.js"
  },
  "devDependencies": {
    "typescript": "^5.9.3",
    "@types/node": "^25.0.3"
  }
}
```

### 需要的工具

- ✅ **Node.js**（安裝 npm）
- ✅ **TypeScript**（透過 npm 安裝）
- ✅ 程式碼編輯器（VS Code 推薦）

### 如何設置和運行

**步驟 1：安裝 Node.js**
```bash
# 檢查是否已安裝
node --version
npm --version

# 如果沒有，請到 https://nodejs.org/ 下載安裝
```

**步驟 2：安裝專案依賴**
```bash
cd 專案資料夾
npm install
```

**步驟 3：編譯 TypeScript**
```bash
# 編譯 TypeScript 為 JavaScript
npm run build

# 或使用開發模式（自動編譯）
npm run dev
```

**步驟 4：開啟網頁**
```bash
# 編譯後，開啟 public/index.html
# 或使用開發伺服器
npm run serve
```

### 相關文件

👉 [詳細的 TypeScript 專案配置指南](../2_typescript/README.md)  
👉 [Node.js 和 npm 環境配置](../Node.js_npm_環境配置/README.md)

---

## ⚛️ 類型 3：HTML + CSS + TypeScript + React

### 識別特徵

**檔案結構：**
```
專案資料夾/
├── package.json        # 有 React 和 TypeScript 相關依賴
├── tsconfig.json       # TypeScript 配置
├── vite.config.ts      # 或 webpack.config.js（建置工具配置）⭐
├── src/                # React 原始碼
│   ├── App.tsx         # React 元件（.tsx 結尾）⭐
│   ├── main.tsx        # 入口檔案
│   └── components/
│       └── Button.tsx
├── public/             # 靜態資源
│   ├── index.html
│   └── css/
│       └── style.css
└── node_modules/       # 依賴套件
```

**關鍵指標：**
- ✅ 有 `react` 和 `react-dom` 在 `package.json` 的 `dependencies` ⭐
- ✅ 有 `.tsx` 或 `.jsx` 檔案（React 元件）⭐
- ✅ 有 `vite.config.ts`、`webpack.config.js` 或 `create-react-app` 相關配置
- ✅ `package.json` 中有 `@vitejs/plugin-react` 或類似 React 外掛
- ✅ 有 `tsconfig.json`（TypeScript 配置）

**package.json 範例：**
```json
{
  "name": "my-react-app",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "typescript": "^5.2.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.9",
    "vite": "^4.4.5"
  }
}
```

### 需要的工具

- ✅ **Node.js**（安裝 npm）
- ✅ **React** 和相關套件（透過 npm 安裝）
- ✅ **TypeScript**（透過 npm 安裝）
- ✅ **Vite** 或 **Webpack**（建置工具，透過 npm 安裝）
- ✅ 程式碼編輯器（VS Code 推薦）

### 如何設置和運行

**步驟 1：安裝 Node.js**
```bash
# 檢查是否已安裝
node --version
npm --version
```

**步驟 2：安裝專案依賴**
```bash
cd 專案資料夾
npm install
```

**步驟 3：啟動開發伺服器**
```bash
# 使用 Vite（常見）
npm run dev

# 或使用其他建置工具
npm start
```

**步驟 4：建置生產版本**
```bash
# 編譯並打包專案
npm run build

# 預覽建置結果
npm run preview
```

### 相關文件

👉 [詳細的 TypeScript + React 專案配置指南](../3_typescript_react/README.md)  
👉 [Node.js 和 npm 環境配置](../Node.js_npm_環境配置/README.md)

---

## ▲ 類型 4：Next.js（React 全端框架）

### 識別特徵

**檔案結構：**
```
專案資料夾/
├── package.json        # 有 next 依賴 ⭐
├── next.config.js      # 或 next.config.ts、next.config.mjs ⭐
├── tsconfig.json       # TypeScript 配置（選用）
├── app/                # App Router（Next.js 13+）⭐
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
│   # 或 pages/         # Pages Router（舊版）
│   #   ├── _app.tsx
│   #   ├── index.tsx
│   #   └── api/        # API 路由
├── public/             # 靜態資源
└── node_modules/       # 依賴套件
```

**關鍵指標：**
- ✅ 有 `next` 在 `package.json` 的 `dependencies` ⭐
- ✅ 有 `next.config.js`、`next.config.ts` 或 `next.config.mjs` ⭐
- ✅ 有 `app/` 資料夾（App Router）或 `pages/` 資料夾（Pages Router）
- ✅ 通常同時有 `react` 和 `react-dom`（Next.js 基於 React）
- ✅ 可能有 `app/page.tsx`、`app/layout.tsx` 或 `pages/index.tsx`

**package.json 範例：**
```json
{
  "name": "my-next-app",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0"
  }
}
```

### 需要的工具

- ✅ **Node.js**（安裝 npm，建議 18.17 以上）
- ✅ **Next.js**（透過 npm 安裝，內建建置工具）
- ✅ 程式碼編輯器（VS Code 推薦）

### 如何設置和運行

**步驟 1：安裝 Node.js**
```bash
# 檢查是否已安裝
node --version
npm --version
```

**步驟 2：安裝專案依賴**
```bash
cd 專案資料夾
npm install
```

**步驟 3：啟動開發伺服器**
```bash
# 開發模式（熱重載）
npm run dev

# 瀏覽器訪問：http://localhost:3000
```

**步驟 4：建置生產版本**
```bash
# 編譯專案
npm run build

# 啟動生產伺服器
npm run start
```

### Next.js 與 React（Vite/Webpack）的差異

| 特徵 | Next.js | React（類型 3） |
|------|---------|-----------------|
| **建置工具** | 內建，無需額外配置 | 需 Vite 或 Webpack |
| **路由** | 檔案系統路由（`app/` 或 `pages/`） | 需 react-router 等 |
| **SSR/SSG** | 內建支援 | 需額外配置 |
| **API 路由** | 內建（`app/api/` 或 `pages/api/`） | 需額外後端 |
| **配置檔** | `next.config.js` | `vite.config.ts` 或 `webpack.config.js` |

### 相關文件

👉 [Node.js 和 npm 環境配置](../Node.js_npm_環境配置/README.md)

---

## 🔧 快速檢查指令

在專案根目錄執行以下指令，快速判斷專案類型：

### 檢查 package.json

```bash
# 檢查是否有 Next.js（應優先於 React 檢查）
cat package.json | grep -i '"next"'

# 檢查是否有 React
cat package.json | grep -i react

# 檢查是否有 TypeScript
cat package.json | grep -i typescript

# 查看所有依賴
cat package.json | grep -A 20 "dependencies"
```

### 檢查檔案類型

```bash
# 檢查是否有 .tsx 檔案（React + TypeScript）
find . -name "*.tsx" -type f

# 檢查是否有 .ts 檔案（TypeScript）
find . -name "*.ts" -type f ! -name "*.tsx"

# 檢查是否有 .jsx 檔案（React）
find . -name "*.jsx" -type f

# 檢查是否有 tsconfig.json
ls -la tsconfig.json
```

### 檢查建置工具

```bash
# 檢查是否有 Next.js
ls -la next.config.* 2>/dev/null
ls -d app pages 2>/dev/null

# 檢查是否有 Vite
ls -la vite.config.* 2>/dev/null

# 檢查是否有 Webpack
ls -la webpack.config.* 2>/dev/null

# 檢查是否有 Create React App
cat package.json | grep -i "react-scripts"
```

---

## 📊 對照表

| 特徵 | 類型 1<br>JavaScript | 類型 2<br>TypeScript | 類型 3<br>React + TypeScript | 類型 4<br>Next.js |
|------|:-------------------:|:-------------------:|:---------------------------:|:-----------------:|
| **package.json** | 無或極簡 | ✅ 有 | ✅ 有 | ✅ 有 |
| **tsconfig.json** | ❌ 無 | ✅ 有 | ✅ 有 | ✅ 通常有 |
| **.ts 檔案** | ❌ 無 | ✅ 有 | ✅ 有 | ✅ 有 |
| **.tsx/.jsx 檔案** | ❌ 無 | ❌ 無 | ✅ 有 | ✅ 有 |
| **next** | ❌ 無 | ❌ 無 | ❌ 無 | ✅ 有 |
| **react/react-dom** | ❌ 無 | ❌ 無 | ✅ 有 | ✅ 有 |
| **app/ 或 pages/** | ❌ 無 | ❌ 無 | ❌ 無 | ✅ 有 |
| **建置工具** | ❌ 不需要 | TypeScript 編譯器 | Vite/Webpack | 內建 |
| **需要 Node.js** | ❌ 不需要 | ✅ 需要 | ✅ 需要 | ✅ 需要 |
| **運行方式** | 直接開啟 HTML | 編譯後開啟 | `npm run dev` | `npm run dev` |

---

## ❓ 常見問題

### Q1: 專案同時有 .js 和 .ts 檔案，是哪種類型？

**A:** 通常是**類型 2（TypeScript）**。`.js` 檔案可能是：
- 編譯後的輸出檔案（在 `dist/` 資料夾）
- 舊的 JavaScript 檔案（正在遷移到 TypeScript）
- 配置檔案（如 `webpack.config.js`）

**判斷方法：** 查看 `src/` 資料夾，如果主要是 `.ts` 檔案，就是 TypeScript 專案。

### Q2: 有 package.json 但沒有 node_modules，怎麼辦？

**A:** 需要先安裝依賴：
```bash
npm install
```

這會根據 `package.json` 安裝所有需要的套件。

### Q3: 執行 `npm install` 時出現錯誤？

**A:** 可能的原因：
1. **沒有安裝 Node.js** → 到 [nodejs.org](https://nodejs.org/) 下載安裝
2. **Node.js 版本太舊** → 更新到 LTS 版本
3. **網路問題** → 檢查網路連線，或使用國內鏡像：
   ```bash
   npm config set registry https://registry.npmmirror.com
   ```

### Q4: 如何知道專案使用哪個建置工具？

**A:** 檢查以下檔案或依賴（**建議依序檢查，Next.js 優先**）：
- `package.json` 中有 `next` + `next.config.js/ts` → 使用 **Next.js**（內建建置）
- `vite.config.ts` 或 `vite.config.js` → 使用 **Vite**
- `webpack.config.js` → 使用 **Webpack**
- `package.json` 中有 `react-scripts` → 使用 **Create React App**

### Q5: 專案同時有 React 和 Next.js，怎麼判斷？

**A:** 若 `package.json` 中有 `next` 依賴，應視為 **Next.js 專案（類型 4）**。Next.js 基於 React，但有自己的建置與路由系統。運行時使用 `npm run dev`，會啟動 Next.js 開發伺服器（預設 port 3000），而非 Vite 或 Webpack。

### Q6: 專案下載後無法運行？

**A:** 按照以下步驟檢查：

1. **確認專案類型**（使用本指南）
2. **安裝必要工具**（Node.js、npm）
3. **安裝專案依賴**：`npm install`
4. **查看 package.json 的 scripts**：了解如何運行專案
5. **閱讀專案的 README.md**：通常有詳細說明

---

## 🎓 學習路徑建議

### 初學者
1. 先從**類型 1（純 JavaScript）**開始
2. 熟悉 HTML、CSS、JavaScript 基礎
3. 再學習**類型 2（TypeScript）**

### 進階學習
1. 掌握 TypeScript 後
2. 學習 **類型 3（React + TypeScript）**
3. 學習 **類型 4（Next.js）**：全端框架、SSR、檔案路由
4. 了解現代前端開發工具鏈

