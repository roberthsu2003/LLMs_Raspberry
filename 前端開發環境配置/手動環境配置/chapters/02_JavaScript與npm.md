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

> 💡 **實際範例**：完整的範例專案請參考 [範例 B：JavaScript + npm](../examples/B_js-npm/README.md)

### 情境：你想使用 lodash

假設你想在專案中使用 `lodash`（一個實用的 JavaScript 工具函式庫）。

**📂 完整範例專案：** [examples/B_js-npm](../examples/B_js-npm/)

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
- **Vite**：新興工具，速度快，配置簡單（推薦初學者）
- **Rollup**：適合函式庫
- **Parcel**：零配置

---

## ⚡ 快速開始：使用 npm 建立 Vite 專案

> 💡 **兩種學習方式**：
> - **快速方法**（本節）：使用官方工具快速建立，適合想立即開始的學生
> - **手動方法**（下一節）：從零開始建立，適合想深入了解的學生

Vite 提供了官方工具，可以快速建立一個完整的開發環境，只需要一個指令！

### 步驟 1：使用 create-vite 建立專案

```bash
# 使用 npm create 指令（推薦）
npm create vite@latest my-vite-project

# 或使用 npx
npx create-vite@latest my-vite-project
```

**執行後會詢問：**
```
✔ Select a framework: › Vanilla
✔ Select a variant: › JavaScript
```

**選擇說明：**
- **Vanilla**：純 JavaScript（不包含框架）
- **JavaScript**：使用 JavaScript（不是 TypeScript）

### 步驟 2：進入專案並安裝依賴

```bash
# 進入專案資料夾
cd my-vite-project

# 安裝所有依賴套件
npm install
```

**這會自動安裝：**
- `vite`（開發工具）
- 其他必要的依賴

### 步驟 3：查看專案結構

建立完成後，專案結構如下：

```
my-vite-project/
├── index.html          # 入口 HTML 檔案
├── package.json        # 專案配置
├── vite.config.js      # Vite 設定檔
├── node_modules/       # 依賴套件（自動產生）
├── public/             # 靜態資源資料夾
│   └── vite.svg
└── src/                # 原始碼資料夾
    ├── main.js         # 主程式檔案
    ├── style.css       # 樣式檔案
    └── counter.js      # 範例程式（可選）
```

### 步驟 4：啟動開發伺服器

```bash
npm run dev
```

**你會看到：**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**在瀏覽器中打開：** `http://localhost:5173`

### 步驟 5：安裝並使用 npm 套件

現在你可以安裝任何 npm 套件並使用：

```bash
# 安裝 lodash
npm install lodash
```

**修改 src/main.js：**
```javascript
import './style.css'
import _ from 'lodash'  // ✅ 現在可以正常使用！

// 使用 lodash
const numbers = [1, 2, 3, 4, 5];
console.log('總和：', _.sum(numbers));  // 15
console.log('最大值：', _.max(numbers)); // 5

// 更新頁面內容
document.querySelector('#app').innerHTML = `
  <h1>Vite + JavaScript</h1>
  <p>總和：${_.sum(numbers)}</p>
  <p>最大值：${_.max(numbers)}</p>
`
```

**重新載入瀏覽器，你會看到：**
- ✅ 網頁正常顯示
- ✅ lodash 正常運作
- ✅ 沒有錯誤訊息

### 步驟 6：建置生產版本

```bash
npm run build
```

這會建立一個 `dist/` 資料夾，包含所有打包和優化後的檔案。

### 步驟 7：預覽生產版本

```bash
npm run preview
```

這會啟動一個本地伺服器，預覽建置後的結果。

---

### 📋 可用的 npm scripts

建立專案後，`package.json` 中會自動包含這些指令：

```json
{
  "scripts": {
    "dev": "vite",           // 啟動開發伺服器
    "build": "vite build",   // 建置生產版本
    "preview": "vite preview" // 預覽生產版本
  }
}
```

**使用方式：**
```bash
npm run dev      # 開發模式
npm run build    # 建置專案
npm run preview  # 預覽建置結果
```

---

### 🎯 快速開始 vs 手動建立

| 方式 | 優點 | 缺點 | 適合對象 |
|------|------|------|---------|
| **快速建立**（本節） | 速度快、配置完整、官方推薦 | 可能包含不需要的檔案 | 想快速開始的學生 |
| **手動建立**（下一節） | 完全控制、了解每個步驟 | 需要手動配置 | 想深入學習的學生 |

**建議：**
- 第一次學習：使用**快速建立**，先體驗完整流程
- 深入理解：參考**手動建立**，了解每個步驟的意義

---

## 🛠️ 實作：手動建立 Vite 專案（深入了解）

> 💡 **學習目標**：從零開始建立 Vite 專案，了解每個步驟的意義和配置

如果你想要完全理解 Vite 的工作原理，或者想要更精簡的專案結構，可以手動建立專案。

### 情境：建立一個使用 lodash 的專案

假設我們要建立一個計算器，使用 lodash 的數學函式。

### 步驟 1：建立專案結構

```bash
# 建立專案資料夾
mkdir my-calculator
cd my-calculator

# 初始化 npm
npm init -y
```

### 步驟 2：安裝依賴套件

```bash
# 安裝 lodash（我們要使用的套件）
npm install lodash

# 安裝 Vite（開發工具，放在 devDependencies）
npm install -D vite
```

**檢查 package.json：**
```json
{
  "name": "my-calculator",
  "version": "1.0.0",
  "dependencies": {
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
```

### 步驟 3：建立專案檔案

**index.html**
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>計算器</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .calculator {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { color: #333; }
        .result {
            font-size: 24px;
            color: #667eea;
            margin: 20px 0;
            padding: 15px;
            background: #f0f0f0;
            border-radius: 5px;
        }
        button {
            padding: 10px 20px;
            margin: 5px;
            font-size: 16px;
            cursor: pointer;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
        }
        button:hover {
            background: #5568d3;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <h1>🧮 數學計算器</h1>
        <div class="result" id="result">結果會顯示在這裡</div>
        <div>
            <button onclick="calculateSum()">計算總和</button>
            <button onclick="calculateMax()">找出最大值</button>
            <button onclick="calculateAverage()">計算平均</button>
            <button onclick="shuffleArray()">隨機排序</button>
        </div>
    </div>
    <script type="module" src="./main.js"></script>
</body>
</html>
```

**main.js**
```javascript
// ✅ 現在可以正常使用 lodash 了！
import _ from 'lodash';

// 範例資料
const numbers = [10, 5, 20, 15, 30, 25];

// 計算總和
window.calculateSum = function() {
    const sum = _.sum(numbers);
    document.getElementById('result').textContent = 
        `總和：${sum} (數字：${numbers.join(', ')})`;
};

// 找出最大值
window.calculateMax = function() {
    const max = _.max(numbers);
    document.getElementById('result').textContent = 
        `最大值：${max} (數字：${numbers.join(', ')})`;
};

// 計算平均
window.calculateAverage = function() {
    const avg = _.mean(numbers);
    document.getElementById('result').textContent = 
        `平均值：${avg.toFixed(2)} (數字：${numbers.join(', ')})`;
};

// 隨機排序
window.shuffleArray = function() {
    const shuffled = _.shuffle(numbers);
    document.getElementById('result').textContent = 
        `隨機排序：${shuffled.join(', ')}`;
};

console.log('✅ lodash 載入成功！');
console.log('可用的函式：', Object.keys(_).slice(0, 10));
```

### 步驟 4：設定 Vite

**建立 vite.config.js**（可選，Vite 有預設設定）
```javascript
import { defineConfig } from 'vite';

export default defineConfig({
  // 專案根目錄
  root: '.',
  
  // 開發伺服器設定
  server: {
    port: 3000,
    open: true  // 自動打開瀏覽器
  },
  
  // 建置設定
  build: {
    outDir: 'dist',  // 輸出目錄
    sourcemap: true  // 產生 source map（方便除錯）
  }
});
```

### 步驟 5：設定 npm scripts

**修改 package.json**，加入 scripts：
```json
{
  "name": "my-calculator",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "lodash": "^4.17.21"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
```

### 步驟 6：啟動開發伺服器

```bash
npm run dev
```

**你會看到：**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**在瀏覽器中打開：** `http://localhost:3000`

**✅ 成功標誌：**
- 網頁正常顯示
- 點擊按鈕可以正常運作
- 瀏覽器 Console 沒有錯誤
- 可以看到 "✅ lodash 載入成功！" 的訊息

### 步驟 7：建置生產版本

```bash
npm run build
```

**Vite 會：**
1. 讀取所有檔案
2. 解析 `import _ from 'lodash'`
3. 找到 lodash 在 `node_modules` 中的位置
4. 把 lodash 轉換成瀏覽器能用的格式
5. 把所有程式碼打包並優化
6. 輸出到 `dist/` 資料夾

**查看建置結果：**
```bash
ls dist/
# 應該看到：
# index.html
# assets/
#   ├── index-[hash].js
#   └── index-[hash].css
```

### 步驟 8：預覽生產版本

```bash
npm run preview
```

這會啟動一個本地伺服器，預覽建置後的結果。

---

## 🔍 深入理解：Vite 做了什麼？

### 開發模式（`npm run dev`）

當你執行 `npm run dev` 時：

1. **Vite 啟動開發伺服器**
   - 監聽檔案變更
   - 提供熱模組替換（HMR）

2. **處理 import 語句**
   ```javascript
   import _ from 'lodash';
   ```
   - Vite 看到 `'lodash'`
   - 自動找到 `node_modules/lodash/` 
   - 轉換成瀏覽器能理解的格式
   - 即時提供給瀏覽器

3. **瀏覽器收到的是轉換後的程式碼**
   - 不再是 `import _ from 'lodash'`
   - 而是實際的 lodash 程式碼（已經轉換成 ES Module）

### 建置模式（`npm run build`）

當你執行 `npm run build` 時：

1. **讀取所有檔案**
   - `index.html`
   - `main.js`
   - 所有 import 的套件

2. **解析依賴關係**
   ```
   main.js
   └── lodash (從 node_modules)
       └── (lodash 的依賴，如果有)
   ```

3. **打包和優化**
   - 合併多個檔案
   - 移除未使用的程式碼（Tree Shaking）
   - 壓縮程式碼
   - 產生 source map

4. **輸出到 dist/**
   ```
   dist/
   ├── index.html
   └── assets/
       ├── index-abc123.js  (包含 main.js + lodash)
       └── index-def456.css (如果有 CSS)
   ```

### 對比：沒有 Bundler vs 有 Bundler

**❌ 沒有 Bundler（直接開啟 HTML）：**
```html
<script type="module" src="./main.js"></script>
```
- 瀏覽器看到 `import _ from 'lodash'`
- 瀏覽器不知道 `'lodash'` 是什麼
- **結果：錯誤**

**✅ 有 Bundler（使用 Vite）：**
```html
<script type="module" src="./main.js"></script>
```
- Vite 在背後處理 `import _ from 'lodash'`
- 轉換成實際的檔案路徑和程式碼
- 瀏覽器收到的是可執行的程式碼
- **結果：成功！**

---

## 📊 實際範例：比較不同情況

### 範例 1：簡單的數學運算

**main.js**
```javascript
import _ from 'lodash';

// 使用 lodash 的數學函式
const numbers = [1, 2, 3, 4, 5];

console.log('總和：', _.sum(numbers));        // 15
console.log('最大值：', _.max(numbers));       // 5
console.log('最小值：', _.min(numbers));       // 1
console.log('平均值：', _.mean(numbers));      // 3
```

**使用 Vite 後：**
- ✅ 可以正常執行
- ✅ 所有 lodash 函式都能使用
- ✅ 瀏覽器 Console 顯示正確結果

### 範例 2：陣列操作

**main.js**
```javascript
import _ from 'lodash';

const users = [
  { name: 'Alice', age: 25 },
  { name: 'Bob', age: 30 },
  { name: 'Charlie', age: 20 }
];

// 找出年齡最大的使用者
const oldest = _.maxBy(users, 'age');
console.log('最年長：', oldest.name);  // Bob

// 依年齡排序
const sorted = _.sortBy(users, 'age');
console.log('排序後：', sorted);

// 取得所有名字
const names = _.map(users, 'name');
console.log('名字列表：', names);  // ['Alice', 'Bob', 'Charlie']
```

### 範例 3：字串處理

**main.js**
```javascript
import _ from 'lodash';

const text = '  hello world  ';

// 移除前後空白
const trimmed = _.trim(text);
console.log(trimmed);  // 'hello world'

// 轉換成駝峰式
const camelCase = _.camelCase('hello world');
console.log(camelCase);  // 'helloWorld'

// 轉換成大寫
const upper = _.upperCase('hello world');
console.log(upper);  // 'HELLO WORLD'
```

---

## 🎯 驗證學習成果

完成以上步驟後，請確認：

- [ ] 可以成功執行 `npm run dev`
- [ ] 瀏覽器可以正常顯示網頁
- [ ] lodash 的函式可以正常使用
- [ ] 點擊按鈕可以正常運作
- [ ] 瀏覽器 Console 沒有錯誤
- [ ] 可以成功執行 `npm run build`
- [ ] `dist/` 資料夾中有建置後的檔案
- [ ] 理解 Vite 在開發和建置時的不同行為

---

## 💡 進階提示

### 1. 查看打包後的程式碼

建置後，打開 `dist/assets/index-xxx.js`，你會看到：
- lodash 的程式碼已經被打包進去
- 程式碼已經被壓縮和優化
- 不再有 `import` 語句，而是實際的程式碼

### 2. 使用其他 Bundler

如果你想嘗試其他 Bundler：

**Webpack：**
```bash
npm install -D webpack webpack-cli webpack-dev-server
```

**Parcel：**
```bash
npm install -D parcel
```

但對於初學者，**Vite 是最簡單的選擇**。

### 3. 除錯技巧

如果遇到問題：

```bash
# 清除快取
rm -rf node_modules package-lock.json
npm install

# 檢查 Vite 版本
npx vite --version

# 查看詳細的建置資訊
npm run build -- --debug
```

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
   - **推薦**：參考 [範例 B：JavaScript + npm](../examples/B_js-npm/README.md)

2. **研究題**：查看 `node_modules/lodash/package.json`，了解套件的結構

3. **思考題**：列出你目前專案中使用的 npm 套件，分類它們是 dependencies 還是 devDependencies

**📂 完整範例專案：** [examples/B_js-npm](../examples/B_js-npm/)
