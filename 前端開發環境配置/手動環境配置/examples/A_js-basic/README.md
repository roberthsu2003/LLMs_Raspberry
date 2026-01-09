# 範例 A：純 JavaScript（無任何工具）

> 💡 **學習目標**：理解現代瀏覽器已內建 ES Module 機制，體驗「沒有任何工具時」的前端開發。

## 🎯 這個範例要教什麼？

這個範例展示：
- ✅ 現代瀏覽器已內建 ES Module 機制
- ✅ 不需要任何工具就能使用 `import/export`
- ✅ 瀏覽器原生的模組化能力
- ✅ **瀏覽器原生能做到 vs 做不到**的對照基準
- ✅ 為什麼即使瀏覽器很強，仍需要工具

---

## 📂 檔案結構

```
A_js-basic/
├── index.html      # 主 HTML 檔案（入口）
├── main.js         # 主程式（使用 import）
├── msg.js          # 模組 1（使用 export）
├── utils.js        # 模組 2（使用 export）
└── README.md       # 本文件
```

**💡 關鍵理解：**
- 只有 4 個檔案，沒有任何配置檔案
- 不需要 `package.json`、不需要 `node_modules`
- 瀏覽器直接執行這些檔案

---

## 🚀 快速開始（3 分鐘體驗）

### 步驟 1：查看檔案結構

確認你有以下檔案：
- `index.html`
- `main.js`
- `msg.js`
- `utils.js`

### 步驟 2：查看程式碼

**`index.html`** - HTML 入口檔案
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
    
    <!-- 關鍵：type="module" 告訴瀏覽器這是 ES Module -->
    <script type="module" src="./main.js"></script>
</body>
</html>
```

**💡 關鍵點：** `type="module"` 告訴瀏覽器這是一個 ES Module，可以使用 `import/export`。

**`main.js`** - 主程式檔案
```javascript
// 可以 import 其他模組
import { msg } from './msg.js';
import { greet, add } from './utils.js';

// 使用 import 的內容
console.log(msg);
greet('World');

const result = add(1, 2);
console.log(`1 + 2 = ${result}`);

// DOM 操作
const app = document.querySelector('#app');
if (app) {
    app.textContent = `${msg} - 計算結果：${result}`;
}
```

**`msg.js`** - 模組 1
```javascript
// 可以 export 變數、函數、類別
export const msg = 'Hello from module!';

export function getMessage() {
    return msg;
}
```

**`utils.js`** - 模組 2
```javascript
// 可以 export 多個東西
export function greet(name) {
    console.log(`Hello, ${name}!`);
}

export function add(a, b) {
    return a + b;
}
```

### 步驟 3：執行專案

**方法 1：直接開啟（可能會有 CORS 問題）**

```bash
# 雙擊 index.html，或在瀏覽器中打開
open index.html  # macOS
start index.html  # Windows
```

**⚠️ 注意：** 如果遇到 CORS 錯誤，請使用方法 2。

**方法 2：使用本地伺服器（推薦）**

```bash
# Python 3（推薦）
python3 -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js（需要安裝 http-server）
npx http-server -p 8000
```

**然後在瀏覽器中訪問：** `http://localhost:8000`

**✅ 成功標誌：**
- 網頁正常顯示
- 瀏覽器 Console 顯示：
  ```
  Hello from module!
  Hello, World!
  1 + 2 = 3
  ```
- 頁面上顯示：`Hello from module! - 計算結果：3`

---

## 🔍 深入理解：ES Module 機制

### 什麼是 ES Module？

ES Module（ES6 Module）是 JavaScript 的標準模組系統，現代瀏覽器已經原生支援。

### 關鍵語法

**export（匯出）：**
```javascript
// 匯出變數
export const msg = 'Hello';

// 匯出函數
export function greet(name) {
    console.log(`Hello, ${name}!`);
}

// 匯出多個
export function add(a, b) {
    return a + b;
}
```

**import（匯入）：**
```javascript
// 匯入單個
import { msg } from './msg.js';

// 匯入多個
import { greet, add } from './utils.js';

// 匯入全部（不推薦）
import * as utils from './utils.js';
```

### 重要規則

1. **必須使用相對路徑**
   ```javascript
   // ✅ 正確
   import { msg } from './msg.js';
   
   // ❌ 錯誤（瀏覽器不認識）
   import { msg } from 'msg';
   ```

2. **必須包含副檔名**
   ```javascript
   // ✅ 正確
   import { msg } from './msg.js';
   
   // ❌ 錯誤
   import { msg } from './msg';
   ```

3. **必須使用 `type="module"`**
   ```html
   <!-- ✅ 正確 -->
   <script type="module" src="./main.js"></script>
   
   <!-- ❌ 錯誤（無法使用 import/export） -->
   <script src="./main.js"></script>
   ```

---

## 📊 瀏覽器原生能做到的事

### ✅ 1. ES Module 系統

- ✅ 可以使用 `import/export`
- ✅ 可以模組化程式碼
- ✅ 可以組織檔案結構
- ✅ 不需要任何工具

### ✅ 2. 現代 JavaScript 語法

- ✅ `const`、`let`、`arrow function`
- ✅ `class`、`async/await`
- ✅ `template literal`、`destructuring`
- ✅ `Promise`、`fetch`

### ✅ 3. Web API

- ✅ DOM 操作
- ✅ Fetch API
- ✅ LocalStorage
- ✅ WebSocket
- ✅ Canvas API

---

## ❌ 瀏覽器原生做不到的事

### ❌ 1. 無法使用 npm 套件

```javascript
// ❌ 這樣不行！
import _ from 'lodash';  // 瀏覽器不認識 'lodash'
```

**為什麼？**
- 瀏覽器不知道 `lodash` 在哪裡
- 瀏覽器只認識相對路徑（如 `./msg.js`）
- npm 套件名稱不是檔案路徑

**錯誤訊息：**
```
Failed to resolve module specifier "lodash". 
Relative references must start with either "/", "./", or "../".
```

### ❌ 2. 無法處理 TypeScript

```typescript
// ❌ 瀏覽器不認識 TypeScript
function add(a: number, b: number): number {
    return a + b;
}
```

**為什麼？**
- 瀏覽器只能執行 JavaScript
- 不認識 TypeScript 的型別語法（`: number`）

### ❌ 3. 無法處理 JSX

```jsx
// ❌ 瀏覽器不認識 JSX
function App() {
    return <h1>Hello</h1>;
}
```

**為什麼？**
- JSX 不是標準 JavaScript 語法
- 需要轉換成 `React.createElement()`

### ❌ 4. 沒有開發伺服器功能

- ❌ 沒有自動重新載入（需要手動 F5）
- ❌ 沒有熱更新（修改程式碼後要手動刷新）
- ❌ 沒有錯誤提示（只能在瀏覽器 Console 看）
- ❌ 沒有 Source Map（除錯困難）

### ❌ 5. 不支援舊瀏覽器

- ❌ IE 11 不支援 ES Module
- ❌ 舊版 Safari 不支援某些新語法
- ❌ 需要考慮相容性

---

## 🎓 實際操作練習

### 練習 1：新增一個模組

1. **建立新檔案 `math.js`：**
   ```javascript
   export function multiply(a, b) {
       return a * b;
   }
   
   export function divide(a, b) {
       return a / b;
   }
   ```

2. **在 `main.js` 中匯入：**
   ```javascript
   import { multiply, divide } from './math.js';
   
   console.log(multiply(3, 4));  // 12
   console.log(divide(10, 2));   // 5
   ```

3. **重新載入瀏覽器，查看結果**

### 練習 2：模組之間互相引用

1. **在 `msg.js` 中引用 `utils.js`：**
   ```javascript
   import { greet } from './utils.js';
   
   export const msg = 'Hello from module!';
   
   export function showMessage() {
       greet('World');
       return msg;
   }
   ```

2. **在 `main.js` 中使用：**
   ```javascript
   import { showMessage } from './msg.js';
   
   showMessage();
   ```

### 練習 3：嘗試使用 npm 套件（會失敗）

1. **嘗試在 `main.js` 中匯入 lodash：**
   ```javascript
   // ❌ 這會失敗
   import _ from 'lodash';
   ```

2. **觀察錯誤訊息：**
   ```
   Failed to resolve module specifier "lodash"
   ```

3. **思考：** 為什麼會失敗？需要什麼工具才能解決？

---

## 🔍 常見問題

### Q1：為什麼需要本地伺服器？直接開啟 HTML 不行嗎？

**A：** ES Module 有 CORS（跨來源資源共用）限制，直接用 `file://` 開啟可能會遇到錯誤。

**解決方法：**
- 使用本地伺服器（`python3 -m http.server`）
- 或使用 VS Code 的 Live Server 擴充功能

### Q2：為什麼 import 時要加 `.js` 副檔名？

**A：** 這是 ES Module 的規範，瀏覽器需要明確知道檔案類型。

```javascript
// ✅ 正確
import { msg } from './msg.js';

// ❌ 錯誤
import { msg } from './msg';
```

### Q3：可以省略 `type="module"` 嗎？

**A：** 不行！沒有 `type="module"`，瀏覽器不會把檔案當作 ES Module，`import/export` 會報錯。

```html
<!-- ✅ 正確 -->
<script type="module" src="./main.js"></script>

<!-- ❌ 錯誤 -->
<script src="./main.js"></script>
```

### Q4：這樣就已經是完整專案了嗎？

**A：** 這只是最基礎的環境。當你需要：
- 使用 npm 套件
- 使用 TypeScript
- 使用 JSX
- 更好的開發體驗

就需要引入工具了。

### Q5：IE 11 可以執行嗎？

**A：** 不行。IE 11 不支援 ES Module，需要：
- 使用打包工具（如 Webpack）
- 轉換成舊版 JavaScript
- 或使用 polyfill

---

## 📊 學習檢查清單

完成這個範例後，請確認你理解：

- [ ] ES Module 是瀏覽器原生支援的
- [ ] 不需要任何工具就能使用 `import/export`
- [ ] `type="module"` 是必需的
- [ ] import 必須使用相對路徑和 `.js` 副檔名
- [ ] 瀏覽器無法直接使用 npm 套件
- [ ] 瀏覽器無法處理 TypeScript 和 JSX
- [ ] 需要本地伺服器才能正常執行（避免 CORS）

---

## 🎯 關鍵理解總結

### 1. 瀏覽器「其實已經很強」

現代瀏覽器已經內建：
- ✅ ES Module 系統
- ✅ 現代 JavaScript 語法
- ✅ 豐富的 Web API

### 2. 但「只能用自己寫的檔案」

瀏覽器只能：
- ✅ 載入相對路徑的檔案（`./main.js`）
- ❌ 無法直接使用 npm 套件
- ❌ 無法處理需要轉換的語法

### 3. 這就是為什麼需要工具

工具幫你：
- 🔧 把 npm 套件轉換成瀏覽器能用的格式
- 🔧 把 TypeScript/JSX 轉換成 JavaScript
- 🔧 提供開發伺服器和熱更新

---

## 🚀 延伸學習

### 下一步建議

1. **學習 npm 和套件管理**
   - 了解為什麼需要 npm
   - 學習如何安裝和使用套件
   - 參考：[第 2 章：JavaScript 與 npm](../../chapters/02_JavaScript與npm.md)

2. **學習 TypeScript**
   - 了解為什麼需要編譯
   - 學習型別系統
   - 參考：[第 3 章：TypeScript 的本質](../../chapters/03_TypeScript的本質.md)

3. **學習開發工具**
   - 了解 Vite 的作用
   - 學習開發伺服器
   - 參考：[第 4 章：為什麼需要 Vite](../../chapters/04_為什麼需要Vite.md)

---

## 📚 相關資源

- [MDN: ES Modules](https://developer.mozilla.org/zh-TW/docs/Web/JavaScript/Guide/Modules)
- [ES6 Modules 完整指南](https://www.freecodecamp.org/chinese/news/javascript-modules-explained-with-examples/)
- [第 1 章：純 JavaScript 最小環境](../../chapters/01_純JavaScript最小環境.md)

---

## 💪 練習題

1. **實作題**：建立一個計算器專案
   - 建立 `calculator.js` 模組
   - 包含加、減、乘、除函數
   - 在 `main.js` 中使用這些函數

2. **實驗題**：嘗試在 `main.js` 中匯入一個 npm 套件（例如 lodash），觀察錯誤訊息

3. **思考題**：列出你的專案中「瀏覽器原生能做到」和「需要工具才能做到」的功能

---

**🎉 恭喜！你已經理解瀏覽器原生的模組化能力了！**

下一步：學習 [第 2 章：JavaScript 與 npm](../../chapters/02_JavaScript與npm.md)，了解如何使用第三方套件。
