# 範例 D：TypeScript + Vite

> 💡 **學習目標**：體驗 Vite 如何整合 TypeScript、npm 套件和瀏覽器，理解現代前端開發工具鏈。

## 🎯 這個範例要教什麼？

這個範例展示：
- ✅ Vite 的便利性和整合能力
- ✅ 開發伺服器（Dev Server）的作用
- ✅ 熱更新（HMR）的體驗
- ✅ 自動編譯 TypeScript
- ✅ 開發 vs 建置的差異
- ✅ **一個工具整合所有功能**

---

## 📂 檔案結構

```
D_ts-vite/
├── index.html          # 入口 HTML（直接引用 .ts 檔案！）
├── src/
│   └── main.ts         # TypeScript 原始碼
├── vite.config.ts      # Vite 配置（可選）
├── tsconfig.json        # TypeScript 配置
├── package.json         # 專案配置
├── dist/               # 建置輸出（自動產生）
└── README.md           # 本文件
```

**💡 關鍵理解：**
- `index.html` 直接引用 `.ts` 檔案（Vite 會自動處理）
- 不需要手動編譯 TypeScript
- Vite 整合了所有工具

---

## 🛠️ 建立新專案

### 方式一：使用 `npm create` 快速建立（推薦）

最快速的方式是使用 Vite 官方提供的腳手架工具：

```bash
# 建立新專案
npm create vite@latest my-vite-project

# 在建立過程中選擇：
# ✓ Select a framework: › Vanilla
# ✓ Select a variant: › TypeScript
```

**完整步驟：**

1. **執行建立命令：**
   ```bash
   npm create vite@latest my-vite-project
   ```

2. **選擇專案模板：**
   - 選擇 `Vanilla`（純 JavaScript/TypeScript，不使用框架）
   - 選擇 `TypeScript` 變體

3. **進入專案目錄並安裝依賴：**
   ```bash
   cd my-vite-project
   npm install
   ```

4. **啟動開發伺服器：**
   ```bash
   npm run dev
   ```

**✅ 優點：**
- 快速建立，幾秒鐘完成
- 自動配置好所有必要的檔案（`vite.config.ts`、`tsconfig.json`、`package.json` 等）
- 使用官方推薦的配置
- 適合快速開始新專案

**💡 其他可用的模板：**
- `vanilla`：純 JavaScript 或 TypeScript
- `vue`：Vue.js
- `react`：React（JavaScript）
- `react-ts`：React（TypeScript）
- `preact`：Preact
- `lit`：Lit
- `svelte`：Svelte

### 方式二：手動建立專案（學習用）

如果你想深入了解每個檔案的用途和配置，可以參考這個範例的檔案結構手動建立：

1. 建立專案目錄和基本檔案
2. 初始化 `package.json`
3. 安裝依賴套件
4. 建立配置檔案（`vite.config.ts`、`tsconfig.json`）
5. 建立原始碼檔案

這種方式適合想要深入理解 Vite 配置的學習者。

---

## 🚀 快速開始（5 分鐘體驗）

### 步驟 1：安裝依賴

```bash
# 進入專案目錄
cd examples/D_ts-vite

# 安裝依賴
npm install
```

**這會安裝：**
- `vite`：開發工具
- `typescript`：TypeScript 編譯器

### 步驟 2：啟動開發伺服器

```bash
npm run dev
```

**✅ 成功標誌：**
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**瀏覽器會自動打開：** `http://localhost:5173`

**你會看到：**
- 網頁正常顯示
- Console 顯示：`🚀 Vite + TypeScript 已啟動！`

### 步驟 3：體驗熱更新（HMR）

1. **打開 `src/main.ts`**
2. **修改內容：**
   ```typescript
   const msg: string = "Hello Vite! 我修改了！";
   ```
3. **儲存檔案**
4. **觀察瀏覽器：** 自動更新，不需要手動重新整理！

**💡 這就是熱更新（HMR）！**

### 步驟 4：查看檔案內容

**`index.html`** - 直接引用 TypeScript！
```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TypeScript + Vite</title>
</head>
<body>
    <div id="app"></div>
    
    <!-- 注意：直接引用 .ts 檔案！Vite 會自動處理 -->
    <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

**💡 關鍵點：**
- 直接引用 `/src/main.ts`（TypeScript 檔案）
- Vite 自動編譯成 JavaScript
- 瀏覽器收到的是編譯後的 JavaScript

**`src/main.ts`** - TypeScript 原始碼
```typescript
const msg: string = "Hello Vite!";
const app = document.querySelector('#app');

if (app) {
    app.innerHTML = `
        <h1>${msg}</h1>
        <p>✅ Vite + TypeScript 運作正常！</p>
        <p>修改這個檔案，觀察自動重新載入（HMR）</p>
    `;
    console.log('🚀 Vite + TypeScript 已啟動！');
}
```

**`vite.config.ts`** - Vite 配置
```typescript
import { defineConfig } from 'vite';

export default defineConfig({
    // 預設配置就很好用了
    // 可以根據需求添加自訂配置
    server: {
        port: 5173,
        open: true,  // 自動打開瀏覽器
    },
});
```

**`package.json`** - 專案配置
```json
{
  "name": "ts-vite",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",              // 開發模式
    "build": "tsc && vite build", // 建置模式
    "preview": "vite preview"    // 預覽建置結果
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

---

## 🔍 深入理解：Vite 做了什麼？

### 開發階段（`npm run dev`）

當你執行 `npm run dev` 時：

1. **Vite 啟動開發伺服器**
   - 監聽檔案變更
   - 提供 HTTP 服務

2. **處理 TypeScript**
   ```typescript
   // src/main.ts（你寫的）
   const msg: string = "Hello";
   ```
   - Vite 看到 `.ts` 檔案
   - 自動編譯成 JavaScript
   - 即時提供給瀏覽器

3. **處理 npm 套件**
   ```typescript
   import _ from 'lodash';  // ✅ 現在可以用了！
   ```
   - Vite 解析 `'lodash'`
   - 找到 `node_modules/lodash/`
   - 轉換成瀏覽器能用的格式

4. **熱更新（HMR）**
   - 修改檔案後自動重新載入
   - 保持應用狀態（某些情況下）
   - 快速看到變更

### 建置階段（`npm run build`）

當你執行 `npm run build` 時：

1. **編譯 TypeScript**
   - 使用 `tsc` 編譯所有 `.ts` 檔案
   - 產生 `.js` 檔案

2. **打包所有檔案**
   - 讀取所有 import
   - 解析依賴關係
   - 打包成一個（或幾個）檔案

3. **優化**
   - 壓縮程式碼
   - Tree Shaking（移除未使用的程式碼）
   - 產生 Source Map

4. **輸出到 `dist/`**
   ```
   dist/
   ├── index.html
   └── assets/
       └── main-abc123.js
   ```

---

## 📊 對照：沒有 Vite vs 有 Vite

### ❌ 沒有 Vite

**開發流程：**
1. 寫 TypeScript
2. 手動執行 `tsc` 編譯
3. 手動重新整理瀏覽器
4. 重複步驟 2-3

**問題：**
- 每次修改都要手動編譯
- 每次修改都要手動重新整理
- 開發效率低
- 容易出錯

### ✅ 有 Vite

**開發流程：**
1. 寫 TypeScript
2. 自動編譯、自動重新載入
3. 完成！

**優點：**
- 自動編譯 TypeScript
- 自動重新載入
- 即時錯誤提示
- 開發效率高

---

## 🎓 實際操作練習

### 練習 1：體驗熱更新

1. **啟動開發伺服器：**
   ```bash
   npm run dev
   ```

2. **修改 `src/main.ts`：**
   ```typescript
   const msg: string = "我修改了！";
   ```

3. **儲存檔案**
4. **觀察：** 瀏覽器自動更新，不需要手動重新整理

### 練習 2：使用 npm 套件

1. **安裝 lodash：**
   ```bash
   npm install lodash
   ```

2. **在 `src/main.ts` 中使用：**
   ```typescript
   import _ from 'lodash';
   
   const numbers = [1, 2, 3, 4, 5];
   console.log('總和：', _.sum(numbers));
   ```

3. **觀察：** Vite 自動處理 npm 套件！

### 練習 3：建置專案

1. **執行建置：**
   ```bash
   npm run build
   ```

2. **查看 `dist/` 資料夾：**
   - 編譯後的 JavaScript
   - 打包後的檔案
   - 優化後的程式碼

3. **預覽建置結果：**
   ```bash
   npm run preview
   ```

### 練習 4：比較開發和建置

1. **開發模式：**
   - 啟動 `npm run dev`
   - 觀察檔案結構（沒有 `dist/`）
   - 觀察網路請求（很多小檔案）

2. **建置模式：**
   - 執行 `npm run build`
   - 觀察 `dist/` 資料夾
   - 觀察打包後的檔案（一個大檔案）

---

## 🔍 常見問題

### Q1：為什麼可以直接引用 `.ts` 檔案？

**A：** Vite 在背後自動處理。當瀏覽器請求 `.ts` 檔案時，Vite 會：
1. 讀取 TypeScript 檔案
2. 編譯成 JavaScript
3. 返回給瀏覽器

**瀏覽器收到的實際上是 JavaScript！**

### Q2：開發和建置有什麼不同？

**A：**
- **開發**：即時編譯，不打包，快速啟動
- **建置**：完整編譯，打包優化，適合部署

### Q3：可以不用 `vite.config.ts` 嗎？

**A：** 可以！Vite 有預設配置，大部分情況下不需要自訂配置。

### Q4：Vite 只能用在 TypeScript 嗎？

**A：** 不是！Vite 支援：
- JavaScript
- TypeScript
- JSX
- Vue
- React
- 等等

### Q5：熱更新會丟失狀態嗎？

**A：** 大部分情況下不會。Vite 的 HMR 會盡量保持應用狀態，只有在無法保持時才會完整重新載入。

---

## 📊 學習檢查清單

完成這個範例後，請確認你理解：

- [ ] Vite 整合了 TypeScript、npm 套件、瀏覽器
- [ ] 開發時可以直接引用 `.ts` 檔案
- [ ] 熱更新（HMR）讓開發更順暢
- [ ] 開發和建置使用相同的工具鏈
- [ ] Vite 不是框架，是工具鏈整合器

---

## 🎯 關鍵理解總結

### 1. Vite 是工具鏈整合器

> **Vite 整合了所有工具，提供統一的開發體驗**

- TypeScript 編譯
- npm 套件處理
- 開發伺服器
- 熱更新
- 建置優化

### 2. 開發 vs 建置

- **開發**：快速啟動，即時編譯，不打包
- **建置**：完整編譯，打包優化，適合部署

### 3. 一個工具解決所有問題

不需要：
- ❌ 手動配置 TypeScript
- ❌ 手動配置打包工具
- ❌ 手動配置開發伺服器

只需要：
- ✅ Vite（一個工具搞定所有）

---

## 🚀 延伸學習

### 下一步建議

1. **學習 React**
   - 了解為什麼需要框架
   - 學習 Component 思維
   - 參考：[第 5 章：React 出現的理由](../../chapters/05_React出現的理由.md)

2. **學習 React + Vite**
   - 了解如何整合 React 和 Vite
   - 學習 JSX 編譯
   - 參考：[第 6 章：React 與 JavaScript](../../chapters/06_React與JavaScript.md)

3. **完整現代環境**
   - React + TypeScript + Vite
   - 參考：[範例 F：完整現代環境](../F_react-ts-vite/README.md)

---

## 📚 相關資源

- [Vite 官方文件](https://vitejs.dev/)
- [TypeScript 官方文件](https://www.typescriptlang.org/)
- [第 4 章：為什麼需要 Vite](../../chapters/04_為什麼需要Vite.md)

---

## 💪 練習題

1. **實作題**：在專案中新增一個 TypeScript 模組，觀察 Vite 如何處理

2. **實驗題**：安裝並使用不同的 npm 套件，觀察 Vite 如何處理

3. **研究題**：修改 `vite.config.ts`，嘗試不同的配置選項

---

**🎉 恭喜！你已經理解 Vite 的強大之處了！**

下一步：學習 [第 5 章：React 出現的理由](../../chapters/05_React出現的理由.md)，了解為什麼需要框架。
