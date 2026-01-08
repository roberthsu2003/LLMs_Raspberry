# 範例 B：JavaScript + npm（不打包）

## 教學重點

這個範例**故意失敗**，目的是：
- 展示 npm 套件存在，但瀏覽器「看不到」
- 理解 node_modules 是開發者的世界
- 自然引出：「那中間誰來翻譯？」

## 檔案結構

```
B_js-npm/
├── index.html          # 主 HTML 檔案
├── main.js             # 嘗試 import lodash（會失敗）
├── package.json        # npm 配置
├── node_modules/       # npm 安裝的套件（執行 npm install 後產生）
└── README.md           # 本文件
```

## 如何執行

### 步驟 1：安裝依賴

```bash
npm install
```

這會下載 lodash 到 `node_modules/` 資料夾。

### 步驟 2：嘗試在瀏覽器中執行

**方法 1：直接開啟**
- 雙擊 `index.html`
- 打開瀏覽器 Console（F12）
- 觀察錯誤訊息

**方法 2：使用本地伺服器**
```bash
python3 -m http.server 8000
```

然後訪問 `http://localhost:8000`

### 步驟 3：觀察錯誤

打開瀏覽器 Console，你會看到：

```
Failed to resolve module specifier "lodash". 
Relative references must start with either "/", "./", or "../".
```

## 為什麼會失敗？

### 問題 1：瀏覽器不認識套件名稱

```javascript
import _ from 'lodash';  // ❌ 瀏覽器不認識 'lodash'
```

瀏覽器只認識：
- 相對路徑：`./main.js`、`../utils.js`
- 絕對路徑：`/src/main.js`
- URL：`https://cdn.example.com/lib.js`

瀏覽器**不認識**：
- 套件名稱：`'lodash'`、`'react'`

### 問題 2：node_modules 的位置

即使 lodash 在 `node_modules/lodash/` 中，瀏覽器也不知道：
- `'lodash'` 對應到 `./node_modules/lodash/lodash.js`
- 需要工具來「解析」套件名稱

### 問題 3：模組格式

npm 套件可能是 CommonJS 格式：
```javascript
module.exports = { ... };
```

但瀏覽器需要 ES Module 格式：
```javascript
export { ... };
```

## 教學重點

### 1. npm 是開發階段工具

- npm 幫你下載套件到 `node_modules/`
- 但瀏覽器不認識 npm
- 瀏覽器無法直接使用 `node_modules/`

### 2. 需要 Bundler

這就是為什麼需要打包工具（Bundler）：
- 讀取 `import _ from 'lodash'`
- 找到 lodash 在 `node_modules/` 中的位置
- 轉換成瀏覽器能用的格式
- 打包成一個檔案

### 3. 這個錯誤是「故意的」

這個範例故意失敗，目的是：
- 讓學生體驗問題
- 理解為什麼需要工具
- 自然引出解決方案

## 學習目標

完成這個範例後，你應該能夠：
- ✅ 理解 npm 的角色是「開發階段工具」
- ✅ 知道瀏覽器無法直接使用 npm 套件
- ✅ 理解為什麼需要 Bundler

## 延伸思考

1. 為什麼 Node.js 可以直接使用 npm 套件，但瀏覽器不行？
2. 如果我想使用 npm 套件，需要什麼工具？
3. 這些工具做了什麼事？

## 對應章節

👉 [第 2 章：JavaScript 與 npm](../../chapters/02_JavaScript與npm.md)
