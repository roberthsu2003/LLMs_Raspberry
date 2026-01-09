# 範例 C：TypeScript 基礎（無框架、無 Vite）

> 💡 **學習目標**：透過實際操作，理解 TypeScript 如何轉換成 JavaScript，以及為什麼 TypeScript 永遠不會在瀏覽器執行。

## 🎯 這個範例要教什麼？

這個範例展示：
- ✅ TypeScript 編譯流程（`.ts` → `.js`）
- ✅ tsc（TypeScript Compiler）的作用
- ✅ TypeScript → JavaScript 的轉換過程
- ✅ **TypeScript 永遠不會在瀏覽器執行**（重要！）
- ✅ 型別註解在編譯時被移除
- ✅ 開發時檢查 vs 執行時執行

---

## 📂 檔案結構

```
C_ts-basic/
├── src/
│   └── main.ts          # TypeScript 原始碼（你寫的）
├── dist/                # 編譯輸出（自動產生，不要手動修改）
│   ├── main.js          # 編譯後的 JavaScript（瀏覽器執行這個）
│   ├── main.js.map      # Source Map（除錯用）
│   └── main.d.ts        # 型別定義檔
├── index.html           # HTML 檔案（引用 dist/main.js）
├── tsconfig.json        # TypeScript 配置
├── package.json         # 專案配置
└── README.md            # 本檔案
```

**💡 關鍵理解：**
- `src/main.ts`：你寫的 TypeScript 程式碼
- `dist/main.js`：編譯後的 JavaScript（瀏覽器實際執行這個）
- `index.html`：引用 `dist/main.js`，**不是** `src/main.ts`

---

## 🚀 快速開始（從零建立 TypeScript 專案）

### 方法一：使用現有範例專案（快速體驗）

如果你想快速體驗，可以直接使用現有的範例專案：

```bash
# 進入專案目錄
cd examples/C_ts-basic

# 安裝依賴
npm install

# 編譯 TypeScript
npm run build
```

---

### 方法二：從零開始建立（推薦學習）

如果你想完整理解 TypeScript 專案的建立過程，讓我們從零開始：

#### 步驟 1：建立專案資料夾

```bash
# 建立專案資料夾
mkdir my-typescript-project
cd my-typescript-project
```

#### 步驟 2：初始化 npm 專案

```bash
# 初始化 npm 專案
npm init -y
```

**這會建立 `package.json` 檔案：**
```json
{
  "name": "my-typescript-project",
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

**💡 關鍵理解：**
- `npm init` 建立 `package.json`，這是專案的配置檔案
- 記錄專案資訊和依賴套件

#### 步驟 3：安裝 TypeScript

```bash
# 安裝 TypeScript（作為開發依賴）
npm install -D typescript
```

**這會：**
- 下載 TypeScript 到 `node_modules/` 資料夾
- 更新 `package.json`，加入 `devDependencies`：
  ```json
  {
    "devDependencies": {
      "typescript": "^5.0.0"
    }
  }
  ```

**💡 關鍵理解：**
- `-D` 或 `--save-dev`：安裝到 `devDependencies`（開發時需要）
- TypeScript 是開發工具，不會出現在最終的程式碼中

#### 步驟 4：建立專案結構

```bash
# 建立原始碼資料夾
mkdir src

# 建立輸出資料夾（編譯後的檔案會放在這裡）
mkdir dist
```

**專案結構：**
```
my-typescript-project/
├── src/              # TypeScript 原始碼
├── dist/             # 編譯後的 JavaScript（自動產生）
└── package.json      # 專案配置
```

#### 步驟 5：建立 TypeScript 配置檔

```bash
# 建立 tsconfig.json
npx tsc --init
```

**或者手動建立 `tsconfig.json`：**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ES2020",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "sourceMap": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

**💡 關鍵配置說明：**
- `target`：編譯後的 JavaScript 版本
- `outDir`：輸出目錄（編譯後的檔案放在哪裡）
- `rootDir`：原始碼目錄（TypeScript 檔案在哪裡）
- `strict`：啟用嚴格模式

#### 步驟 6：建立 TypeScript 程式碼

**建立 `src/main.ts`：**
```typescript
// TypeScript 原始碼
function add(a: number, b: number): number {
    return a + b;
}

function greet(name: string): void {
    console.log(`Hello, ${name}!`);
}

// 使用函數
const result = add(1, 2);
console.log(`1 + 2 = ${result}`);

greet('World');

// 在瀏覽器中顯示結果
if (typeof document !== 'undefined') {
    const app = document.querySelector('#app');
    if (app) {
        app.textContent = `計算結果：${result}`;
    }
}
```

#### 步驟 7：建立 HTML 檔案

**建立 `index.html`：**
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TypeScript 基礎範例</title>
</head>
<body>
    <h1>TypeScript 基礎</h1>
    <div id="app"></div>
    
    <!-- 注意：引用編譯後的 JavaScript，不是 TypeScript -->
    <script type="module" src="./dist/main.js"></script>
</body>
</html>
```

**💡 關鍵點：**
- 引用的是 `./dist/main.js`（編譯後的 JavaScript）
- **不是** `./src/main.ts`（TypeScript）

#### 步驟 8：設定 npm scripts

**修改 `package.json`，加入 scripts：**
```json
{
  "name": "my-typescript-project",
  "version": "1.0.0",
  "scripts": {
    "build": "tsc",
    "watch": "tsc --watch"
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```

**💡 scripts 說明：**
- `build`：編譯一次 TypeScript
- `watch`：監聽檔案變更，自動編譯

#### 步驟 9：編譯 TypeScript

```bash
# 編譯 TypeScript
npm run build
```

**這會執行：**
- `tsc`（TypeScript Compiler）
- 讀取 `src/main.ts`
- 轉換成 JavaScript
- 輸出到 `dist/main.js`

**✅ 成功標誌：**
- 看到 `dist/` 資料夾被建立
- `dist/main.js` 檔案存在
- 沒有錯誤訊息

---

## 📝 查看原始 TypeScript 程式碼（現有範例）

如果你想查看現有範例的程式碼，打開 `src/main.ts`，你會看到：

打開 `src/main.ts`，你會看到：

```typescript
// TypeScript 原始碼
function add(a: number, b: number): number {
    return a + b;
}

function greet(name: string): void {
    console.log(`Hello, ${name}!`);
}

// 使用函數
const result = add(1, 2);
console.log(`1 + 2 = ${result}`);

greet('World');
```

**觀察重點：**
- `: number`、`: string`：型別註解
- `: void`：函數不回傳值
- 這些是 TypeScript 的語法

### 步驟 10：查看編譯後的 JavaScript

編譯完成後，打開 `dist/main.js`，你會看到：

打開 `dist/main.js`，你會看到：

```javascript
// 注意：型別註解都被移除了！
function add(a, b) {
    return a + b;
}

function greet(name) {
    console.log(`Hello, ${name}!`);
}

const result = add(1, 2);
console.log(`1 + 2 = ${result}`);

greet('World');
```

**🔍 對比觀察：**

| TypeScript (`src/main.ts`) | JavaScript (`dist/main.js`) |
|---------------------------|----------------------------|
| `function add(a: number, b: number): number` | `function add(a, b)` |
| `function greet(name: string): void` | `function greet(name)` |
| 有型別註解 | **型別註解被移除了** |

**💡 關鍵理解：**
- 型別註解（`: number`、`: string`、`: void`）**全部被移除**
- 其他程式碼保持不變
- 這就是「轉譯（Transpilation）」的過程

### 步驟 11：在瀏覽器中執行

**方法 1：直接開啟**
```bash
# 雙擊 index.html，或在瀏覽器中打開
open index.html  # macOS
start index.html  # Windows
```

**方法 2：使用本地伺服器（推薦）**
```bash
npm run serve
```

這會啟動一個本地伺服器，自動打開瀏覽器。

**在瀏覽器中：**
- 打開開發者工具（F12）
- 查看 Console
- 你會看到：
  ```
  1 + 2 = 3
  Hello, World!
  計算結果：3
  ```

**🔍 重要觀察：**
- 瀏覽器執行的是 `dist/main.js`（JavaScript）
- 瀏覽器**不執行** `src/main.ts`（TypeScript）
- HTML 中引用的是：`<script src="./dist/main.js"></script>`

---

## 📋 完整建立流程總結

讓我們回顧一下完整的建立流程：

```
1. 建立專案資料夾
   mkdir my-typescript-project
   ↓
2. 初始化 npm
   npm init -y
   ↓
3. 安裝 TypeScript
   npm install -D typescript
   ↓
4. 建立專案結構
   mkdir src dist
   ↓
5. 建立 tsconfig.json
   npx tsc --init 或手動建立
   ↓
6. 寫 TypeScript 程式碼
   建立 src/main.ts
   ↓
7. 建立 HTML 檔案
   建立 index.html
   ↓
8. 設定 npm scripts
   修改 package.json
   ↓
9. 編譯 TypeScript
   npm run build
   ↓
10. 在瀏覽器中執行
    打開 index.html
```

**💡 關鍵理解：**
- 每個步驟都有其目的
- `npm init` 建立專案配置
- `npm install -D typescript` 安裝開發工具
- `tsconfig.json` 告訴 TypeScript 如何編譯
- `npm run build` 執行編譯

---

## 🔍 深入理解：編譯流程

### 完整的開發流程

```
1. 寫 TypeScript
   src/main.ts
   ↓
2. 編譯（tsc）
   npm run build
   ↓
3. 產生 JavaScript
   dist/main.js
   ↓
4. 瀏覽器執行
   index.html → dist/main.js
```

### 視覺化對比

**TypeScript（開發時）：**
```typescript
// src/main.ts
function add(a: number, b: number): number {
    return a + b;
}
```

**JavaScript（執行時）：**
```javascript
// dist/main.js（瀏覽器執行這個）
function add(a, b) {
    return a + b;
}
```

**💡 關鍵點：**
- 開發時：寫 TypeScript，有型別保護
- 編譯時：tsc 移除型別，轉換成 JavaScript
- 執行時：瀏覽器執行 JavaScript（沒有型別）

---

## 📝 檔案詳細說明

### `src/main.ts` - TypeScript 原始碼

```typescript
// TypeScript 原始碼
function add(a: number, b: number): number {
    return a + b;
}

function greet(name: string): void {
    console.log(`Hello, ${name}!`);
}

// 使用函數
const result = add(1, 2);
console.log(`1 + 2 = ${result}`);

greet('World');

// ❌ 如果取消註解，TypeScript 會報錯（開發時）
// const error = add('1', '2');  
// Error: Type 'string' is not assignable to type 'number'

// 在瀏覽器中顯示結果
if (typeof document !== 'undefined') {
    const app = document.querySelector('#app');
    if (app) {
        app.textContent = `計算結果：${result}`;
    }
}
```

**說明：**
- `add(a: number, b: number): number`：函數接受兩個數字，回傳數字
- `greet(name: string): void`：函數接受字串，不回傳值
- 型別錯誤會在開發時被發現（取消註解那行會報錯）

### `tsconfig.json` - TypeScript 配置

```json
{
  "compilerOptions": {
    "target": "ES2020",        // 編譯成 ES2020 語法
    "module": "ES2020",         // 使用 ES Module
    "outDir": "./dist",        // 輸出目錄
    "rootDir": "./src",        // 原始碼目錄
    "strict": true,            // 嚴格模式
    "esModuleInterop": true,   // ES 模組相容性
    "skipLibCheck": true,      // 跳過函式庫檢查
    "lib": ["ES2020", "DOM", "DOM.Iterable"],  // 可用的 API
    "sourceMap": true,         // 產生 Source Map（除錯用）
    "declaration": true        // 產生型別定義檔（.d.ts）
  },
  "include": ["src/**/*"],     // 包含的檔案
  "exclude": ["node_modules"]  // 排除的檔案
}
```

**重要配置說明：**
- `target`：編譯後的 JavaScript 版本
- `outDir`：編譯後的檔案放在哪裡
- `rootDir`：原始碼在哪裡
- `strict`：啟用嚴格型別檢查

### `package.json` - 專案配置

```json
{
  "name": "ts-basic",
  "version": "1.0.0",
  "description": "TypeScript 基礎範例（無框架、無 Vite）",
  "type": "module",
  "scripts": {
    "build": "tsc",                    // 編譯 TypeScript
    "watch": "tsc --watch",            // 監聽檔案變更，自動編譯
    "serve": "npx http-server . -p 8080 -o"  // 啟動本地伺服器
  },
  "devDependencies": {
    "typescript": "^5.0.0"
  }
}
```

**可用指令：**
- `npm run build`：編譯一次
- `npm run watch`：監聽檔案變更，自動編譯（推薦開發時使用）
- `npm run serve`：啟動本地伺服器

### `index.html` - HTML 入口

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TypeScript 基礎範例</title>
</head>
<body>
    <h1>TypeScript 基礎</h1>
    <div id="app"></div>
    
    <!-- 注意：引用編譯後的 JavaScript，不是 TypeScript -->
    <script type="module" src="./dist/main.js"></script>
</body>
</html>
```

**💡 關鍵點：**
- 引用的是 `./dist/main.js`（編譯後的 JavaScript）
- **不是** `./src/main.ts`（TypeScript）
- 瀏覽器無法直接執行 TypeScript

---

## 🎓 實際操作練習

### 練習 1：觀察型別錯誤

1. **打開 `src/main.ts`**
2. **取消註解這行：**
   ```typescript
   const error = add('1', '2');
   ```
3. **執行編譯：**
   ```bash
   npm run build
   ```
4. **觀察錯誤訊息：**
   ```
   error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
   ```

**💡 學習重點：**
- TypeScript 在**開發時**就發現錯誤
- 如果沒有型別檢查，這個錯誤要到**執行時**才會發現

### 練習 2：使用 watch 模式

1. **啟動 watch 模式：**
   ```bash
   npm run watch
   ```
2. **修改 `src/main.ts`**（例如改變數字）
3. **觀察：** 檔案會自動重新編譯
4. **重新載入瀏覽器**，看到更新

**💡 學習重點：**
- `watch` 模式會自動監聽檔案變更
- 每次儲存 TypeScript 檔案，就會自動編譯
- 這是開發時的常用模式

### 練習 3：比較編譯前後

1. **打開 `src/main.ts`**（TypeScript）
2. **打開 `dist/main.js`**（JavaScript）
3. **並排比較：**
   - 型別註解在哪裡？
   - 哪些被移除了？
   - 哪些保持不變？

**💡 學習重點：**
- TypeScript → JavaScript 的轉換過程
- 型別註解在編譯時被移除
- 執行時沒有型別資訊

### 練習 4：修改 tsconfig.json

1. **修改 `tsconfig.json`：**
   ```json
   {
     "compilerOptions": {
       "target": "ES5",  // 從 ES2020 改成 ES5
       // ... 其他設定
     }
   }
   ```
2. **重新編譯：**
   ```bash
   npm run build
   ```
3. **查看 `dist/main.js`**，觀察語法的變化

**💡 學習重點：**
- `target` 決定編譯後的 JavaScript 版本
- ES5 語法更舊，但相容性更好
- ES2020 語法更新，但需要較新的瀏覽器

---

## 🔍 常見問題

### Q1：為什麼瀏覽器不能直接執行 TypeScript？

**A：** 瀏覽器只能執行 JavaScript。TypeScript 需要先轉換成 JavaScript。

**類比：**
- TypeScript = 中文（你寫的）
- JavaScript = 英文（瀏覽器懂的）
- tsc = 翻譯器（把中文翻譯成英文）

### Q2：每次修改都要重新編譯嗎？

**A：** 是的，但有 `watch` 模式可以自動編譯。

```bash
# 開發時使用 watch 模式
npm run watch

# 這樣每次儲存檔案，就會自動編譯
```

### Q3：`dist/` 資料夾可以刪除嗎？

**A：** 可以，但需要重新編譯。

```bash
# 刪除 dist 資料夾
rm -rf dist

# 重新編譯
npm run build
```

### Q4：為什麼 `dist/main.js` 沒有型別註解？

**A：** 因為型別註解在編譯時被移除了。瀏覽器不需要型別資訊，只需要可執行的程式碼。

### Q5：可以同時開啟 `src/main.ts` 和 `dist/main.js` 對比嗎？

**A：** 當然可以！這是學習的好方法。

**建議：**
- 左側視窗：`src/main.ts`（你寫的）
- 右側視窗：`dist/main.js`（編譯後的）
- 對比觀察型別註解的變化

---

## 📊 學習檢查清單

完成這個範例後，請確認你理解：

- [ ] TypeScript 需要編譯才能執行
- [ ] 瀏覽器執行的是 `dist/main.js`，不是 `src/main.ts`
- [ ] 型別註解在編譯時被移除
- [ ] TypeScript 的錯誤只在開發時出現
- [ ] `tsc` 是 TypeScript 編譯器
- [ ] `tsconfig.json` 控制編譯行為
- [ ] `watch` 模式可以自動編譯
- [ ] TypeScript 永遠不會在瀏覽器執行

---

## 🎯 關鍵理解總結

### 1. TypeScript → JavaScript 的轉換

```
TypeScript（開發時）
  ↓ tsc 編譯
JavaScript（執行時）
  ↓ 瀏覽器執行
實際運作
```

### 2. 型別註解的作用

- **開發時**：TypeScript 檢查型別，發現錯誤
- **編譯時**：tsc 移除型別註解
- **執行時**：瀏覽器執行 JavaScript（沒有型別）

### 3. 開發流程

```
1. 寫 TypeScript（src/main.ts）
2. 編譯（npm run build）
3. 產生 JavaScript（dist/main.js）
4. 瀏覽器執行（index.html → dist/main.js）
```

---

## 🚀 延伸學習

### 下一步建議

1. **嘗試寫更多 TypeScript 程式碼**
   - 定義介面（interface）
   - 使用類別（class）
   - 泛型（generics）

2. **實驗不同的 tsconfig.json 設定**
   - 修改 `target` 版本
   - 啟用/停用 `strict` 模式
   - 觀察編譯結果的變化

3. **學習 TypeScript 進階特性**
   - 聯合型別（Union Types）
   - 型別推斷（Type Inference）
   - 型別守衛（Type Guards）

---

## 📚 相關資源

- [TypeScript 官方文件](https://www.typescriptlang.org/docs/)
- [TypeScript Playground](https://www.typescriptlang.org/play)（線上試玩）
- [第 3 章：TypeScript 的本質](../../chapters/03_TypeScript的本質.md)

---

## 💪 練習題

1. **實作題**：在 `src/main.ts` 中新增一個函數，計算兩個數字的乘積
   ```typescript
   function multiply(a: number, b: number): number {
       // 你的實作
   }
   ```

2. **實驗題**：故意寫一個型別錯誤，觀察 TypeScript 如何提示

3. **研究題**：修改 `tsconfig.json` 的 `target`，比較編譯結果的差異

---

**🎉 恭喜！你已經理解 TypeScript 的基本運作方式了！**

下一步：學習 [第 4 章：為什麼需要 Vite](../../chapters/04_為什麼需要Vite.md)，了解如何讓開發更順暢。
