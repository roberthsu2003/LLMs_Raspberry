# 第 4 章：為什麼需要 Vite（工具的誕生）

## 🎯 教學目標

完成本章後，你應該能夠：

- 理解 Vite 解決的是「開發體驗」與「工具整合」問題
- 分清楚「開發伺服器」與「正式建置」的差異
- 知道 Vite 不是框架，也不是 React 專屬
- 理解 Vite 如何整合 TypeScript、npm 套件、瀏覽器
- 知道為什麼 Vite 能提供更好的開發體驗

---

## 📖 核心觀念

### 這一章是「轉折點」

到目前為止，我們學到了：

- ✅ JavaScript（瀏覽器原生）
- ✅ npm（套件管理）
- ✅ TypeScript（型別系統）

但還缺什麼？

### 我們還缺什麼？

1. **開發伺服器**（Dev Server）
   - 自動重新載入
   - 熱更新（HMR）

2. **打包工具**（Bundler）
   - 處理 npm 套件
   - 轉換 TypeScript
   - 打包所有檔案

3. **工具整合**
   - TypeScript + npm + 瀏覽器的橋樑
   - 統一的開發流程

---

## 🚀 Vite 是什麼？

### 一句話定義

> **Vite 是「前端工具鏈整合器」，不是框架**

### Vite 解決的問題

#### 問題 1：開發體驗差

**沒有 Vite 時**：
- 修改程式碼 → 手動重新整理瀏覽器
- 修改 TypeScript → 手動執行 `tsc`
- 沒有即時錯誤提示

**有 Vite 時**：
- 修改程式碼 → 自動重新載入
- 修改 TypeScript → 自動編譯
- 即時錯誤提示

#### 問題 2：工具零散

**沒有 Vite 時**：
- 需要自己配置 TypeScript
- 需要自己配置打包工具
- 需要自己配置開發伺服器
- 需要自己處理 npm 套件

**有 Vite 時**：
- 一個工具整合所有功能
- 預設配置就能用
- 幾乎零設定

#### 問題 3：開發 vs 建置不一致

**沒有 Vite 時**：
- 開發時：手動編譯、手動重新整理
- 建置時：需要另外配置打包工具
- 兩個環境可能不一致

**有 Vite 時**：
- 開發時：Vite Dev Server
- 建置時：Vite Build
- 使用相同的工具鏈

---

## 🔄 Vite 的「開發」vs「建置」

### 開發階段（Development）

**命令**：`npm run dev`

**Vite 做什麼**：
1. 啟動開發伺服器
2. 即時編譯 TypeScript
3. 處理 npm 套件（ESM 預編譯）
4. 提供熱更新（HMR）
5. 顯示錯誤訊息

**特點**：
- 快速啟動
- 即時更新
- 不打包（按需載入）

### 建置階段（Build）

**命令**：`npm run build`

**Vite 做什麼**：
1. 編譯 TypeScript
2. 打包所有檔案
3. 優化程式碼（壓縮、Tree Shaking）
4. 處理資源（圖片、CSS）
5. 輸出到 `dist/` 資料夾

**特點**：
- 完整打包
- 最佳化
- 準備部署

---

## 📁 最小 Vite 專案結構

### 範例 D：TypeScript + Vite

> 💡 **實際範例**：完整的範例專案請參考 [範例 D：TypeScript + Vite](../examples/D_ts-vite/README.md)

**📂 完整範例專案：** [examples/D_ts-vite](../examples/D_ts-vite/)

```
ts-vite/
├── index.html           # 入口 HTML
├── src/
│   └── main.ts         # TypeScript 原始碼
├── vite.config.ts      # Vite 配置
├── tsconfig.json       # TypeScript 配置
└── package.json
```

### 檔案內容

#### `index.html`

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vite + TypeScript</title>
</head>
<body>
    <div id="app"></div>
    <!-- 注意：直接引用 src/main.ts -->
    <script type="module" src="/src/main.ts"></script>
</body>
</html>
```

#### `src/main.ts`

```typescript
const msg: string = "Hello Vite!";
const app = document.querySelector('#app');

if (app) {
    app.textContent = msg;
    console.log('✅ Vite + TypeScript 運作正常！');
}
```

#### `vite.config.ts`

```typescript
import { defineConfig } from 'vite';

export default defineConfig({
    // 預設配置就很好用了
    // 可以根據需求添加自訂配置
});
```

#### `package.json`

```json
{
  "name": "ts-vite",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "devDependencies": {
    "typescript": "^5.0.0",
    "vite": "^5.0.0"
  }
}
```

### 使用流程

```bash
# 1. 安裝依賴
npm install

# 2. 啟動開發伺服器
npm run dev

# 3. 瀏覽器自動開啟 http://localhost:5173
# 修改程式碼會自動重新載入！

# 4. 建置專案
npm run build

# 5. 預覽建置結果
npm run preview
```

---

## 💡 Vite 的優勢

### 1. 快速啟動

**傳統工具（Webpack）**：
- 啟動時間：10-30 秒
- 需要先打包所有檔案

**Vite**：
- 啟動時間：< 1 秒
- 按需編譯，只編譯需要的檔案

### 2. 熱更新（HMR）

**傳統工具**：
- 修改檔案 → 重新打包 → 重新載入整個頁面

**Vite**：
- 修改檔案 → 只更新修改的部分
- 保持應用狀態（例如表單輸入不會消失）

### 3. 預設配置

**傳統工具**：
- 需要大量配置
- 新手容易卡關

**Vite**：
- 預設配置就能用
- 幾乎零設定

### 4. 工具整合

**傳統工具**：
- TypeScript：需要配置
- npm 套件：需要配置
- 開發伺服器：需要配置

**Vite**：
- 一個工具整合所有功能
- 統一的配置檔案

---

## 🔍 深入理解：Vite 如何工作

### 開發階段

```
瀏覽器請求 → Vite Dev Server → 即時編譯 → 返回給瀏覽器
```

**特點**：
- 不預先打包
- 按需編譯
- 使用 ES Module（瀏覽器原生）

### 建置階段

```
原始碼 → TypeScript 編譯 → 打包 → 優化 → dist/
```

**特點**：
- 完整打包
- 最佳化
- 準備部署

---

## 🎓 關鍵理解

### Vite 不是框架

> **Vite 是工具，不是框架**

- React、Vue 是框架（解決 UI 問題）
- Vite 是工具（解決開發流程問題）

### Vite 不是 React 專屬

> **Vite 可以用在任何前端專案**

- React + Vite
- Vue + Vite
- 純 TypeScript + Vite
- 甚至純 JavaScript + Vite

### Vite 的價值

> **不在於它做了多少事，而在於它讓開發者不用每天重複做一樣的事**

- 自動處理 TypeScript
- 自動處理 npm 套件
- 自動提供開發伺服器
- 自動處理熱更新

---

## ⚠️ 學生常見迷思

### ❌ 迷思 1：「Vite 就是新的 React」

**事實**：Vite 是工具，React 是框架，兩者不同。

**為什麼**：Vite 解決開發流程問題，React 解決 UI 問題。

### ❌ 迷思 2：「用了 Vite，JavaScript 就不重要了」

**事實**：Vite 只是工具，最終還是執行 JavaScript。

**為什麼**：Vite 只是幫你處理開發流程，不改變 JavaScript 的本質。

### ❌ 迷思 3：「Vite 只是拿來跑起來比較快」

**事實**：Vite 提供完整的開發和建置工具鏈。

**為什麼**：Vite 不只是開發伺服器，還包含打包、優化等功能。

### ❌ 迷思 4：「不用 Vite 就不能寫現代前端」

**事實**：Vite 只是工具之一，還有 Webpack、Rollup 等選擇。

**為什麼**：工具是手段，不是目的，選擇適合專案的工具即可。

---

## 🎓 本章重點回顧

1. **Vite 是工具鏈整合器**
   - 整合 TypeScript、npm、開發伺服器
   - 不是框架

2. **開發 vs 建置**
   - 開發：快速啟動、熱更新
   - 建置：完整打包、最佳化

3. **Vite 的優勢**
   - 快速啟動
   - 熱更新
   - 預設配置
   - 工具整合

4. **Vite 的價值**
   - 讓開發者不用重複做一樣的事
   - 提供統一的開發流程

---

## 🚀 下一章預告

在下一章，我們將學習 **React 出現的理由**。

你會學到：
- 為什麼不用原生 DOM 操作
- UI = State 的概念
- Component 思維

👉 [前往第 5 章：React 出現的理由](./05_React出現的理由.md)

---

## 💪 練習建議

1. **實作題**：建立一個 Vite + TypeScript 專案
   - 體驗快速啟動
   - 體驗熱更新
   - 體驗建置流程
   - **推薦**：參考 [範例 D：TypeScript + Vite](../examples/D_ts-vite/README.md)

2. **對照題**：比較「沒有 Vite」和「有 Vite」的開發體驗差異

3. **研究題**：查看 Vite 官方文件，了解更多配置選項

**📂 完整範例專案：** [examples/D_ts-vite](../examples/D_ts-vite/)
