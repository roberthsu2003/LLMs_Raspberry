# 第 3 章：TypeScript 的本質（不碰框架）

## 🎯 教學目標

完成本章後，你應該能夠：

- 明確知道 TypeScript 只是 JavaScript 的超集
- 理解 tsc 的角色是「轉譯器」
- 知道 TypeScript 的錯誤只存在於「開發期」
- 理解 TypeScript → JavaScript 的轉換流程
- 知道為什麼 TypeScript 永遠不會在瀏覽器執行

---

## 📖 核心觀念

### TypeScript 是什麼？

> **TypeScript 不是新語言，只是 JavaScript 的超集（Superset）**

這意味著：
- 所有合法的 JavaScript 程式碼都是合法的 TypeScript
- TypeScript = JavaScript + 型別系統
- TypeScript 最終會轉換成 JavaScript

### 核心一句話

> **TypeScript 永遠不會在瀏覽器執行**

瀏覽器只能執行 JavaScript，所以 TypeScript 必須先轉換成 JavaScript。

---

## 🔄 TypeScript → JavaScript 的流程

### 轉譯（Transpilation）

```
TypeScript 檔案         轉譯器 (tsc)          JavaScript 檔案
  (.ts)        →        (TypeScript          →      (.js)
                        Compiler)                      
```

### 實際範例

#### TypeScript 原始碼（main.ts）

```typescript
function add(a: number, b: number): number {
    return a + b;
}

const result = add(1, 2);
console.log(result);
```

#### 轉譯後的 JavaScript（main.js）

```javascript
function add(a, b) {
    return a + b;
}

const result = add(1, 2);
console.log(result);
```

**觀察**：
- 型別註解（`: number`）被移除了
- 其他程式碼保持不變
- 這就是「轉譯」的過程

---

## 🛠️ TypeScript Compiler (tsc)

### tsc 是什麼？

**tsc** = **T**ype**S**cript **C**ompiler（TypeScript 編譯器）

它的工作：
1. 檢查型別錯誤
2. 把 TypeScript 轉換成 JavaScript
3. 產生型別定義檔（.d.ts）

### 安裝 TypeScript

```bash
npm install -D typescript
```

### 使用 tsc

```bash
# 編譯單一檔案
tsc main.ts

# 編譯整個專案（使用 tsconfig.json）
tsc
```

---

## 📁 最小 TypeScript 專案結構

### 範例 C：TypeScript（無框架、無 Vite）

```
ts-basic/
├── src/
│   └── main.ts          # TypeScript 原始碼
├── dist/
│   └── main.js          # 編譯後的 JavaScript（自動產生）
├── tsconfig.json        # TypeScript 配置
└── package.json
```

### 檔案內容

#### `src/main.ts`

```typescript
// TypeScript 原始碼
function add(a: number, b: number): number {
    return a + b;
}

function greet(name: string): void {
    console.log(`Hello, ${name}!`);
}

const result = add(1, 2);
console.log(result);  // 3

greet('World');  // Hello, World!

// ❌ 型別錯誤（開發時就會發現）
// const error = add('1', '2');  // TypeScript 會報錯
```

#### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",        // 編譯目標版本
    "module": "ES2020",         // 模組系統
    "outDir": "./dist",        // 輸出目錄
    "rootDir": "./src",        // 原始碼目錄
    "strict": true,            // 嚴格模式
    "esModuleInterop": true,   // ES 模組相容性
    "skipLibCheck": true       // 跳過函式庫檢查
  },
  "include": ["src/**/*"],     // 包含的檔案
  "exclude": ["node_modules"]  // 排除的檔案
}
```

#### `package.json`

```json
{
  "name": "ts-basic",
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

### 編譯流程

```bash
# 1. 安裝依賴
npm install

# 2. 編譯 TypeScript
npm run build

# 3. 查看編譯結果
ls dist/
# 應該看到 main.js
```

### 編譯後的檔案（dist/main.js）

```javascript
// 注意：型別註解都被移除了
function add(a, b) {
    return a + b;
}

function greet(name) {
    console.log(`Hello, ${name}!`);
}

const result = add(1, 2);
console.log(result);

greet('World');
```

---

## 🎯 TypeScript 的價值

### 1. 型別安全（Type Safety）

**開發時發現錯誤**：

```typescript
function add(a: number, b: number): number {
    return a + b;
}

// ❌ TypeScript 會報錯（開發時）
const result = add('1', '2');  
// Error: Argument of type 'string' is not assignable to parameter of type 'number'.
```

**如果沒有 TypeScript**：
- 錯誤要到執行時才會發現
- 可能在使用者環境中才出現問題

### 2. 更好的開發體驗

**IDE 智能提示**：

```typescript
interface User {
    name: string;
    age: number;
}

function getUser(): User {
    return { name: 'John', age: 30 };
}

const user = getUser();
// IDE 會自動提示 user.name 和 user.age
console.log(user.name);  // ✅ 有提示
console.log(user.xxx);   // ❌ TypeScript 會報錯
```

### 3. 程式碼文件化

**型別就是文件**：

```typescript
// 一看就知道這個函數需要什麼參數，回傳什麼
function calculateTotal(price: number, tax: number): number {
    return price * (1 + tax);
}
```

---

## 🔍 深入理解：tsconfig.json

### 重要配置選項

#### target（編譯目標）

```json
{
  "compilerOptions": {
    "target": "ES2020"  // 編譯成 ES2020 語法
  }
}
```

**說明**：決定編譯後的 JavaScript 使用哪個版本的語法。

#### module（模組系統）

```json
{
  "compilerOptions": {
    "module": "ES2020"  // 使用 ES Module
  }
}
```

**選項**：
- `"ES2020"`：ES Module（`import/export`）
- `"CommonJS"`：CommonJS（`require/module.exports`）

#### strict（嚴格模式）

```json
{
  "compilerOptions": {
    "strict": true  // 啟用所有嚴格檢查
  }
}
```

**效果**：
- 變數必須明確宣告型別
- 不允許 `null` 和 `undefined`
- 更嚴格的型別檢查

---

## 💡 TypeScript 的錯誤只在開發期

### 開發期錯誤

當你寫 TypeScript 時，IDE 和 tsc 會立即顯示錯誤：

```typescript
// ❌ TypeScript 錯誤
const x: number = 'hello';
// Error: Type 'string' is not assignable to type 'number'.
```

### 執行期

瀏覽器執行的是編譯後的 JavaScript，不會有型別錯誤：

```javascript
// 編譯後的 JavaScript（沒有型別）
const x = 'hello';  // 可以執行，不會報錯
```

**重點**：TypeScript 的錯誤只在開發時出現，不會影響執行期的程式碼。

---

## ✅ 優點與缺點

### ✅ 優點

1. **型別安全**
   - 開發時發現錯誤
   - 減少執行期錯誤

2. **更好的開發體驗**
   - IDE 智能提示
   - 自動完成

3. **程式碼文件化**
   - 型別就是文件
   - 更容易理解程式碼

### ❌ 缺點

1. **一定要編譯**
   - 不能直接執行
   - 需要編譯步驟

2. **設定成本高**
   - 需要配置 `tsconfig.json`
   - 學習型別系統

3. **編譯時間**
   - 大型專案編譯較慢
   - 需要等待編譯完成

---

## 🎓 關鍵理解

### TypeScript 不是新語言

> **TypeScript = JavaScript + 型別系統**

- 所有 JavaScript 都是合法的 TypeScript
- TypeScript 只是加上型別註解

### TypeScript 永遠不會在瀏覽器執行

> **瀏覽器只能執行 JavaScript**

- TypeScript 必須先轉換成 JavaScript
- tsc 就是做這個轉換的工具

### 型別錯誤只在開發期

> **TypeScript 的錯誤不會出現在執行期**

- 開發時：TypeScript 檢查型別
- 執行時：瀏覽器執行 JavaScript（沒有型別）

---

## ⚠️ 學生常見迷思

### ❌ 迷思 1：「瀏覽器可以直接跑 TypeScript」

**事實**：不行，瀏覽器只能執行 JavaScript。

**為什麼**：TypeScript 需要先轉換成 JavaScript。

### ❌ 迷思 2：「TypeScript 會讓程式跑得比較快」

**事實**：不會，執行的是編譯後的 JavaScript，速度一樣。

**為什麼**：TypeScript 只是開發時的工具，不影響執行效能。

### ❌ 迷思 3：「沒寫型別就不是 TypeScript」

**事實**：TypeScript 可以推斷型別，不一定需要明確寫型別。

**為什麼**：
```typescript
// 這也是 TypeScript（型別推斷）
const x = 10;  // TypeScript 知道 x 是 number
```

### ❌ 迷思 4：「tsconfig.json 很神秘，不能亂動」

**事實**：tsconfig.json 只是配置檔案，可以根據需求調整。

**為什麼**：它是用來告訴 tsc 如何編譯的設定檔。

---

## 🎓 本章重點回顧

1. **TypeScript 是 JavaScript 的超集**
   - 不是新語言
   - 只是加上型別系統

2. **TypeScript 永遠不會在瀏覽器執行**
   - 必須先轉換成 JavaScript
   - tsc 是轉譯器

3. **型別錯誤只在開發期**
   - 開發時：TypeScript 檢查
   - 執行時：瀏覽器執行 JavaScript

4. **tsconfig.json 的角色**
   - 告訴 tsc 如何編譯
   - 可以根據需求調整

---

## 🚀 下一章預告

在下一章，我們將學習 **為什麼需要 Vite**。

你會學到：
- Vite 解決了哪些問題
- 開發伺服器 vs 正式建置的差異
- Vite 如何整合所有工具

👉 [前往第 4 章：為什麼需要 Vite](./04_為什麼需要Vite.md)

---

## 💪 練習建議

1. **實作題**：建立一個 TypeScript 專案
   - 寫幾個有型別的函數
   - 編譯成 JavaScript
   - 比較編譯前後的差異

2. **實驗題**：故意寫一些型別錯誤，看看 TypeScript 如何提示

3. **研究題**：查看 `tsconfig.json` 的各種選項，了解它們的作用
