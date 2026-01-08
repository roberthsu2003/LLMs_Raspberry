# 範例 F：React + TypeScript + Vite（完整現代環境）

## 教學重點

這個範例展示：
- 整合所有概念（React + TypeScript + Vite）
- 每一層技術在做什麼
- 現代前端專案的標準組成

## 檔案結構

```
F_react-ts-vite/
├── index.html              # 入口 HTML
├── src/
│   ├── App.tsx            # 主應用元件
│   ├── main.tsx           # 入口檔案
│   └── components/        # 元件資料夾
│       └── Button.tsx     # Button 元件（有型別）
├── vite.config.ts         # Vite 配置
├── tsconfig.json          # TypeScript 配置
├── tsconfig.node.json     # Node 環境 TypeScript 配置
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
- 自動開啟瀏覽器（`http://localhost:3000`）
- 自動編譯 TypeScript 和 JSX
- 提供熱更新

### 步驟 3：體驗完整環境

1. 修改 `src/App.tsx`，觀察自動更新
2. 嘗試寫型別錯誤，觀察 TypeScript 提示
3. 新增更多元件，體驗元件化開發

### 步驟 4：建置專案

```bash
npm run build
```

這會：
- 編譯 TypeScript
- 轉換 JSX
- 打包所有檔案
- 優化程式碼
- 輸出到 `dist/` 資料夾

### 步驟 5：預覽建置結果

```bash
npm run preview
```

## 各層技術的作用

### 1. React（框架層）

**作用**：解決 UI 問題
- 元件化開發
- 狀態管理
- 虛擬 DOM

**檔案**：`src/App.tsx`、`src/components/Button.tsx`

### 2. TypeScript（語言層）

**作用**：型別安全
- Props 型別檢查
- State 型別檢查
- 開發時錯誤提示

**檔案**：所有 `.tsx`、`.ts` 檔案

### 3. Vite（工具層）

**作用**：工具整合
- 開發伺服器
- JSX 轉換
- TypeScript 編譯
- 打包和優化

**檔案**：`vite.config.ts`

## 關鍵點

### 1. 型別安全的 Props

```tsx
interface ButtonProps {
    text: string;
    onClick: () => void;
}

function Button({ text, onClick }: ButtonProps) {
    // TypeScript 確保傳入的資料正確
}
```

### 2. 型別安全的 State

```tsx
const [count, setCount] = useState<number>(0);
// TypeScript 確保 count 永遠是 number
```

### 3. 完整的工具鏈

- **開發時**：Vite Dev Server + 熱更新
- **建置時**：TypeScript 編譯 + 打包 + 優化
- **執行時**：瀏覽器執行 JavaScript

## 學習目標

完成這個範例後，你應該能夠：
- ✅ 理解完整環境的組成
- ✅ 知道每一層的作用
- ✅ 能夠手動配置完整專案
- ✅ 理解各層技術之間的關係

## 延伸練習

1. 新增更多元件，體驗元件化開發
2. 嘗試寫型別錯誤，觀察 TypeScript 如何提示
3. 修改 Vite 配置，觀察變化
4. 建立一個實際的專案（例如待辦事項）

## 對應章節

👉 [第 8 章：完整現代環境](../../chapters/08_完整現代環境.md)

---

**恭喜！你已經完成了完整的前端環境配置學習！** 🎉
