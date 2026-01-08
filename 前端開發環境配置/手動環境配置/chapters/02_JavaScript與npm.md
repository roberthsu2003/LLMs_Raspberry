# 第 2 章：JavaScript + npm（套件的世界）

## 🎯 教學目標

完成本章後，你應該能夠：

- 理解 npm 的角色是「開發階段的套件管理」
- 分清楚 dependencies 與 devDependencies
- 知道 node_modules 為什麼不該上傳
- 理解為什麼瀏覽器不能直接讀 node_modules
- 自然引出「所以我們需要 Bundler」的概念

---

## 📖 核心觀念

### npm 是什麼？

**npm** = **N**ode **P**ackage **M**anager（Node 套件管理器）

它是：
- 世界上最大的程式碼庫（registry）
- 管理 JavaScript 套件的工具
- **開發階段**使用的工具

### 關鍵理解

> **npm 是「開發階段工具」，瀏覽器根本不認識 npm**

---

## 🎬 實際體驗：npm 的引入

### 情境：你想使用 lodash

假設你想在專案中使用 `lodash`（一個實用的 JavaScript 工具函式庫）。

### 步驟 1：初始化 npm 專案

```bash
# 在專案目錄下執行
npm init -y
```

這會建立 `package.json` 檔案：

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

### 步驟 2：安裝 lodash

```bash
npm install lodash
```

這會：
1. 下載 lodash 到 `node_modules/` 資料夾
2. 更新 `package.json`，加入依賴：

```json
{
  "dependencies": {
    "lodash": "^4.17.21"
  }
}
```

### 步驟 3：嘗試在瀏覽器中使用

**main.js**
```javascript
// ❌ 這樣不行！
import _ from 'lodash';

console.log(_.add(1, 2));
```

**index.html**
```html
<!DOCTYPE html>
<html>
<body>
    <script type="module" src="./main.js"></script>
</body>
</html>
```

### 步驟 4：瀏覽器報錯

打開瀏覽器 Console，你會看到：

```
Failed to resolve module specifier "lodash". 
Relative references must start with either "/", "./", or "../".
```

**為什麼會這樣？**

因為瀏覽器不認識 `'lodash'` 這個「套件名稱」，它只認識相對路徑（如 `./main.js`）。

---

## 🔍 深入理解：node_modules 是什麼？

### node_modules 的結構

當你執行 `npm install lodash` 後，會產生：

```
node_modules/
├── lodash/
│   ├── package.json
│   ├── lodash.js
│   └── ... (很多檔案)
└── ... (其他依賴)
```

### 瀏覽器為什麼不認識？

1. **路徑問題**
   - 瀏覽器不知道 `'lodash'` 對應到 `./node_modules/lodash/lodash.js`
   - 瀏覽器只認識相對路徑（`./`、`../`）或絕對路徑（`/`）

2. **格式問題**
   - npm 套件可能是 CommonJS 格式（`module.exports`）
   - 瀏覽器需要 ES Module 格式（`export`）

3. **依賴問題**
   - lodash 可能依賴其他套件
   - 瀏覽器不知道如何解析這些依賴

---

## 📦 package.json 詳解

### dependencies vs devDependencies

#### dependencies（生產依賴）

**用途**：專案執行時需要的套件

**範例**：
```json
{
  "dependencies": {
    "lodash": "^4.17.21",
    "axios": "^1.0.0"
  }
}
```

**說明**：這些套件會被打包進最終的程式碼中。

#### devDependencies（開發依賴）

**用途**：只在開發時需要的工具

**範例**：
```json
{
  "devDependencies": {
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

**說明**：這些工具不會出現在最終的程式碼中。

### 安裝方式

```bash
# 安裝到 dependencies
npm install lodash

# 安裝到 devDependencies
npm install --save-dev typescript
# 或簡寫
npm install -D typescript
```

---

## 🚫 為什麼 node_modules 不該上傳？

### 原因 1：檔案太大

`node_modules` 可能包含：
- 數千個檔案
- 數百 MB 甚至數 GB 的大小
- 上傳/下載非常慢

### 原因 2：可以重新產生

只要有 `package.json` 和 `package-lock.json`，就可以：

```bash
npm install
```

這會重新下載所有依賴。

### 原因 3：平台差異

- Windows、macOS、Linux 的檔案系統不同
- 某些套件可能有平台特定的版本

### 解決方案：.gitignore

建立 `.gitignore` 檔案：

```
node_modules/
*.log
.DS_Store
```

這樣 Git 就不會追蹤 `node_modules`。

---

## 💡 自然引出：所以我們需要 Bundler

### 問題總結

我們現在有：
- ✅ JavaScript 程式碼
- ✅ npm 套件（在 node_modules 中）
- ❌ 但瀏覽器無法直接使用

### 解決方案：Bundler（打包工具）

**Bundler 的工作**：
1. 讀取你的程式碼（`import _ from 'lodash'`）
2. 找到 lodash 在 `node_modules` 中的位置
3. 把 lodash 的程式碼轉換成瀏覽器能用的格式
4. 把所有檔案打包成一個（或幾個）檔案
5. 輸出到 `dist/` 或 `build/` 資料夾

### 常見的 Bundler

- **Webpack**：最流行，功能強大但配置複雜
- **Vite**：新興工具，速度快，配置簡單
- **Rollup**：適合函式庫
- **Parcel**：零配置

---

## 🎓 關鍵理解

### npm 的角色

> **npm 是「開發階段的套件管理」，不是「執行階段的套件載入」**

- 開發階段：npm 幫你下載、管理套件
- 執行階段：瀏覽器需要打包工具把套件轉換成可用格式

### 瀏覽器 vs Node.js

| 環境 | 能否直接使用 npm 套件？ |
|------|----------------------|
| Node.js | ✅ 可以（因為 Node.js 知道如何解析 `node_modules`） |
| 瀏覽器 | ❌ 不行（瀏覽器不認識套件名稱） |

### 為什麼需要工具？

因為：
- 瀏覽器不認識 `'lodash'` 這種套件名稱
- 需要工具把套件名稱轉換成實際檔案路徑
- 需要工具把 CommonJS 轉換成 ES Module
- 需要工具處理依賴關係

---

## ⚠️ 學生常見迷思

### ❌ 迷思 1：「npm 套件可以直接被瀏覽器 import」

**事實**：不行，瀏覽器不認識套件名稱。

**為什麼**：瀏覽器只認識相對路徑，不認識 `'lodash'` 這種套件名稱。

### ❌ 迷思 2：「node_modules 是程式碼的一部分」

**事實**：不是，它是依賴套件，可以重新產生。

**為什麼**：只要有 `package.json`，就可以用 `npm install` 重新產生。

### ❌ 迷思 3：「沒有 node_modules 專案就壞掉了」

**事實**：不會，執行 `npm install` 就能恢復。

**為什麼**：`package.json` 記錄了所有依賴，可以重新下載。

### ❌ 迷思 4：「npm = 前端框架」

**事實**：npm 是套件管理器，不是框架。

**為什麼**：npm 只是工具，React、Vue 才是框架。

---

## 🎓 本章重點回顧

1. **npm 是開發階段工具**
   - 幫你下載、管理套件
   - 瀏覽器不認識 npm

2. **瀏覽器無法直接使用 npm 套件**
   - 不認識套件名稱
   - 不知道如何解析 `node_modules`

3. **需要 Bundler**
   - 把套件轉換成瀏覽器能用的格式
   - 打包所有檔案

4. **dependencies vs devDependencies**
   - dependencies：執行時需要
   - devDependencies：開發時需要

---

## 🚀 下一章預告

在下一章，我們將學習 **TypeScript 的本質**。

你會學到：
- TypeScript 不是新語言，只是 JavaScript 的超集
- TypeScript 永遠不會在瀏覽器執行
- tsc 的角色是「轉譯器」

👉 [前往第 3 章：TypeScript 的本質](./03_TypeScript的本質.md)

---

## 💪 練習建議

1. **實作題**：建立一個 npm 專案，安裝 lodash，嘗試在瀏覽器中直接使用（會失敗，但這是學習過程）

2. **研究題**：查看 `node_modules/lodash/package.json`，了解套件的結構

3. **思考題**：列出你目前專案中使用的 npm 套件，分類它們是 dependencies 還是 devDependencies
