# 範例 A：純 JavaScript（無任何工具）

## 教學重點

這個範例展示：
- 現代瀏覽器已內建 ES Module 機制
- 沒有任何工具時，前端可以做到哪些事
- 建立「原生做得到 vs 工具幫你做」的對照基準

## 檔案結構

```
A_js-basic/
├── index.html      # 主 HTML 檔案
├── main.js         # 主程式（使用 import）
├── msg.js          # 模組 1（使用 export）
├── utils.js        # 模組 2（使用 export）
└── README.md       # 本文件
```

## 如何執行

### 方法 1：直接開啟（可能會有 CORS 問題）

雙擊 `index.html` 檔案，在瀏覽器中開啟。

**注意**：如果遇到 CORS 錯誤，請使用方法 2。

### 方法 2：使用本地伺服器（推薦）

```bash
# Python 3
python3 -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000

# Node.js (需要安裝 http-server)
npx http-server -p 8000
```

然後在瀏覽器中訪問：`http://localhost:8000`

## 關鍵點

### 1. type="module"

在 `index.html` 中：

```html
<script type="module" src="./main.js"></script>
```

**`type="module"`** 告訴瀏覽器這是一個 ES Module，可以使用 `import/export`。

### 2. ES Module 語法

**import**：
```javascript
import { msg } from './msg.js';
import { greet, add } from './utils.js';
```

**export**：
```javascript
export const msg = 'Hello from module!';
export function greet(name) { ... }
```

### 3. 相對路徑

注意：import 時必須使用相對路徑（`./msg.js`），不能省略 `.js` 副檔名。

## 觀察重點

1. **瀏覽器原生支援**：現代瀏覽器已經能跑 ES Module
2. **模組化**：可以用 `import/export` 組織程式碼
3. **但有限制**：只能用相對路徑，無法使用 npm 套件

## 學習目標

完成這個範例後，你應該能夠：
- ✅ 理解現代瀏覽器已內建 ES Module
- ✅ 知道如何使用 `import/export`
- ✅ 理解瀏覽器原生的限制

## 延伸練習

1. 嘗試新增更多模組檔案
2. 嘗試在模組之間互相引用
3. 思考：如果我想使用 npm 套件（例如 lodash），會發生什麼事？

## 對應章節

👉 [第 1 章：純 JavaScript 最小環境](../../chapters/01_純JavaScript最小環境.md)
