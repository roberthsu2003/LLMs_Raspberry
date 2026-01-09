# 第 1 章：純 JavaScript 最小前端環境（Baseline）

## 🎯 教學目標

完成本章後，你應該能夠：

- 理解現代瀏覽器已內建 ES Module 機制
- 知道沒有任何工具時，前端可以做到哪些事
- 建立「原生做得到 vs 工具幫你做」的對照基準
- 理解為什麼即使瀏覽器很強，仍需要工具

---

## 📖 核心觀念

### 建立基準線（Baseline）

在學習工具之前，我們先建立一個「基準線」：**沒有任何工具時，瀏覽器能做什麼？**

這很重要，因為：
- 讓你知道「工具的價值」在哪裡
- 讓你知道「什麼是瀏覽器原生能力」
- 讓你知道「什麼是工具額外提供的」

---

## 🌐 現代瀏覽器的能力

### ES Module（ES6 模組系統）

現代瀏覽器（Chrome 61+、Firefox 60+、Safari 11+）已經支援 ES Module！

這意味著你可以：

```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>ES Module 範例</title>
</head>
<body>
    <h1>Hello ES Module</h1>
    <script type="module" src="./main.js"></script>
</body>
</html>
```

```javascript
// main.js
import { msg } from './msg.js';
console.log(msg);
```

```javascript
// msg.js
export const msg = 'Hello from module!';
```

**關鍵點**：注意 `type="module"`，這告訴瀏覽器這是一個 ES Module。

---

## 📁 最小專案結構

> 💡 **實際範例**：完整的範例專案請參考 [範例 A：純 JavaScript](../examples/A_js-basic/README.md)

### 範例 A：純 JavaScript（無任何工具）

```
js-basic/
├── index.html
├── main.js
├── msg.js
└── utils.js
```

**📂 完整範例專案：** [examples/A_js-basic](../examples/A_js-basic/)

### 檔案內容

#### `index.html`

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>純 JavaScript 範例</title>
</head>
<body>
    <h1>JS Basic</h1>
    <div id="app"></div>
    
    <!-- 關鍵：type="module" -->
    <script type="module" src="./main.js"></script>
</body>
</html>
```

#### `main.js`

```javascript
// 可以 import 其他模組
import { msg } from './msg.js';
import { greet } from './utils.js';

// 使用 import 的內容
console.log(msg);
greet('World');

// DOM 操作
document.querySelector('#app').textContent = msg;
```

#### `msg.js`

```javascript
// 可以 export 變數、函數、類別
export const msg = 'Hello from module!';

export function getMessage() {
    return msg;
}
```

#### `utils.js`

```javascript
// 可以 export 多個東西
export function greet(name) {
    console.log(`Hello, ${name}!`);
}

export function add(a, b) {
    return a + b;
}
```

---

## ✅ 瀏覽器原生能做到的事

### 1. ES Module 系統

✅ 可以使用 `import/export`  
✅ 可以模組化程式碼  
✅ 可以組織檔案結構

### 2. 現代 JavaScript 語法

✅ `const`、`let`、`arrow function`  
✅ `class`、`async/await`  
✅ `template literal`、`destructuring`

### 3. Web API

✅ DOM 操作  
✅ Fetch API  
✅ LocalStorage  
✅ WebSocket

---

## ❌ 瀏覽器原生「做不到」的事

### 1. 無法使用 npm 套件

```javascript
// ❌ 這樣不行！
import _ from 'lodash';  // 瀏覽器不認識 'lodash'
```

**為什麼**：瀏覽器不知道 `lodash` 在哪裡，它只認識相對路徑（如 `./msg.js`）。

### 2. 無法處理 TypeScript

```typescript
// ❌ 瀏覽器不認識 TypeScript
function add(a: number, b: number): number {
    return a + b;
}
```

**為什麼**：瀏覽器只能執行 JavaScript，不認識 TypeScript 的型別語法。

### 3. 無法處理 JSX

```jsx
// ❌ 瀏覽器不認識 JSX
function App() {
    return <h1>Hello</h1>;
}
```

**為什麼**：JSX 不是標準 JavaScript 語法，需要轉換。

### 4. 沒有開發伺服器功能

❌ 沒有自動重新載入（需要手動 F5）  
❌ 沒有熱更新（修改程式碼後要手動刷新）  
❌ 沒有錯誤提示（只能在瀏覽器 Console 看）

### 5. 不支援舊瀏覽器

❌ IE 11 不支援 ES Module  
❌ 舊版 Safari 不支援某些新語法

---

## 🔍 實際體驗

### 步驟 1：建立檔案

建立以下檔案結構：

```
my-project/
├── index.html
├── main.js
└── utils.js
```

### 步驟 2：寫程式碼

**index.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>我的專案</title>
</head>
<body>
    <div id="app"></div>
    <script type="module" src="./main.js"></script>
</body>
</html>
```

**main.js**
```javascript
import { greet, add } from './utils.js';

greet('World');
console.log(add(1, 2));

document.querySelector('#app').textContent = 'Hello!';
```

**utils.js**
```javascript
export function greet(name) {
    console.log(`Hello, ${name}!`);
}

export function add(a, b) {
    return a + b;
}
```

### 步驟 3：開啟檔案

**方法 1：直接開啟**
- 雙擊 `index.html` 檔案
- 或右鍵 → 開啟方式 → 瀏覽器

**方法 2：使用本地伺服器（推薦）**

```bash
# Python 3
python3 -m http.server 8000

# 然後在瀏覽器訪問
# http://localhost:8000
```

**為什麼需要伺服器？**

因為 ES Module 有 CORS 限制，直接用 `file://` 開啟可能會遇到錯誤。

---

## 💡 優點與缺點

### ✅ 優點

1. **最貼近瀏覽器原生**
   - 沒有額外的轉換步驟
   - 程式碼就是瀏覽器執行的程式碼

2. **幾乎沒有魔法**
   - 沒有複雜的配置檔案
   - 容易理解程式碼流程

3. **快速開始**
   - 不需要安裝任何工具
   - 寫完就能跑

### ❌ 缺點

1. **不支援舊瀏覽器**
   - IE 11 無法使用
   - 需要考慮相容性

2. **無法處理 npm 套件**
   - 無法使用 lodash、axios 等套件
   - 需要手動下載並管理

3. **開發體驗差**
   - 沒有自動重新載入
   - 沒有錯誤提示
   - 需要手動刷新

4. **無法使用新語法**
   - 無法使用 TypeScript
   - 無法使用 JSX

---

## 🎓 關鍵理解

### 瀏覽器「其實已經很強」

現代瀏覽器已經內建：
- ES Module 系統
- 現代 JavaScript 語法
- 豐富的 Web API

### 但「只能用自己寫的檔案」

瀏覽器只能：
- 載入相對路徑的檔案（`./main.js`）
- 無法直接使用 npm 套件
- 無法處理需要轉換的語法

### 這就是為什麼需要工具

工具幫你：
- 把 npm 套件轉換成瀏覽器能用的格式
- 把 TypeScript/JSX 轉換成 JavaScript
- 提供開發伺服器和熱更新

---

## ⚠️ 學生常見迷思

### ❌ 迷思 1：「一定要 npm 才能寫前端」

**事實**：簡單的專案不需要 npm，瀏覽器原生就能跑。

**為什麼**：ES Module 已經內建在現代瀏覽器中。

### ❌ 迷思 2：「import 一定要搭配打包工具」

**事實**：現代瀏覽器原生支援 `import/export`。

**為什麼**：ES Module 是標準，不需要打包工具也能用。

### ❌ 迷思 3：「module 是 Node.js 才有的東西」

**事實**：ES Module 是 JavaScript 標準，瀏覽器和 Node.js 都支援。

**為什麼**：ES6 引入了模組系統，成為 JavaScript 標準的一部分。

### ❌ 迷思 4：「這樣就已經是完整專案了」

**事實**：這只是最基礎的環境，現代專案通常需要更多工具。

**為什麼**：當專案變大、需要第三方套件、需要使用新語法時，就需要工具。

---

## 🎓 本章重點回顧

1. **現代瀏覽器已內建 ES Module**
   - 可以使用 `import/export`
   - 不需要打包工具也能模組化

2. **瀏覽器原生能做到**
   - ES Module 系統
   - 現代 JavaScript 語法
   - Web API

3. **瀏覽器原生做不到**
   - 使用 npm 套件
   - 處理 TypeScript/JSX
   - 提供開發伺服器功能

4. **建立基準線**
   - 知道「原生能力」的邊界
   - 理解「工具價值」在哪裡

---

## 🚀 下一章預告

在下一章，我們將引入 **npm**，看看當你想使用第三方套件時會發生什麼事。

你會發現：
- npm 套件存在，但瀏覽器「看不到」
- 自然引出「那中間誰來翻譯？」的問題

👉 [前往第 2 章：JavaScript 與 npm](./02_JavaScript與npm.md)

---

## 💪 練習建議

1. **實作題**：建立一個純 JavaScript 專案，使用 ES Module 組織程式碼
   - 建立 3-5 個模組檔案
   - 使用 `import/export` 連接它們
   - 在瀏覽器中執行
   - **推薦**：參考 [範例 A：純 JavaScript](../examples/A_js-basic/README.md)

2. **思考題**：列出你目前專案中「瀏覽器原生能做到」和「需要工具才能做到」的功能

3. **挑戰題**：試著在純 JavaScript 專案中使用一個 npm 套件（例如 lodash），看看會發生什麼錯誤

**📂 完整範例專案：** [examples/A_js-basic](../examples/A_js-basic/)
