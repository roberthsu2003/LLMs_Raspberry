# 範例 D：TypeScript + Vite

## 教學重點

這個範例展示：
- Vite 的便利性
- 開發伺服器
- 熱更新（HMR）
- 自動編譯 TypeScript

## 檔案結構

```
D_ts-vite/
├── index.html          # 入口 HTML
├── src/
│   └── main.ts         # TypeScript 原始碼
├── vite.config.ts      # Vite 配置
├── tsconfig.json       # TypeScript 配置
├── package.json
└── README.md
```

## 如何執行

### 步驟 1：安裝依賴

```bash
npm install
```

### 步驟 2：啟動開發伺服器

```bash
npm run dev
```

這會：
- 啟動 Vite 開發伺服器
- 自動開啟瀏覽器（`http://localhost:5173`）
- 自動編譯 TypeScript
- 提供熱更新（修改檔案後自動重新載入）

### 步驟 3：體驗熱更新

1. 修改 `src/main.ts` 的內容
2. 儲存檔案
3. 觀察瀏覽器自動更新（不需要手動重新整理！）

### 步驟 4：建置專案

```bash
npm run build
```

這會：
- 編譯 TypeScript
- 打包所有檔案
- 輸出到 `dist/` 資料夾

### 步驟 5：預覽建置結果

```bash
npm run preview
```

這會啟動一個本地伺服器，預覽建置後的結果。

## 關鍵點

### 1. 直接引用 TypeScript

在 `index.html` 中：

```html
<script type="module" src="/src/main.ts"></script>
```

**注意**：直接引用 `.ts` 檔案，Vite 會自動處理！

### 2. 自動編譯

- 開發時：Vite 自動編譯 TypeScript
- 不需要手動執行 `tsc`
- 即時看到結果

### 3. 熱更新（HMR）

- 修改檔案後自動重新載入
- 保持應用狀態（某些情況下）
- 快速看到變更

## 對照：沒有 Vite vs 有 Vite

### 沒有 Vite

1. 寫 TypeScript
2. 手動執行 `tsc` 編譯
3. 手動重新整理瀏覽器
4. 重複步驟 2-3

### 有 Vite

1. 寫 TypeScript
2. 自動編譯、自動重新載入
3. 完成！

## 學習目標

完成這個範例後，你應該能夠：
- ✅ 體驗 Vite 的便利性
- ✅ 理解開發伺服器的作用
- ✅ 體驗熱更新
- ✅ 理解 Vite 如何整合工具

## 延伸練習

1. 嘗試修改 `vite.config.ts`，觀察變化
2. 新增更多 TypeScript 檔案，觀察 Vite 如何處理
3. 比較「有 Vite」和「沒有 Vite」的開發體驗

## 對應章節

👉 [第 4 章：為什麼需要 Vite](../../chapters/04_為什麼需要Vite.md)
