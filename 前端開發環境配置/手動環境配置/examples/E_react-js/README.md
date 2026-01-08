# 範例 E：React + JavaScript（最小可理解版）

## 教學重點

這個範例展示：
- JSX 為什麼需要編譯
- React 為什麼需要工具
- JSX → JavaScript 的轉換過程

## 檔案結構

```
E_react-js/
├── index.html          # 入口 HTML
├── src/
│   └── main.jsx        # JSX 檔案
├── vite.config.js      # Vite 配置（包含 React 插件）
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
- 自動開啟瀏覽器
- 自動轉換 JSX 成 JavaScript
- 提供熱更新

### 步驟 3：觀察 JSX 轉換

1. 打開瀏覽器開發者工具（F12）
2. 切換到「Sources」標籤
3. 查看 `src/main.jsx`
4. 觀察 JSX 如何被轉換

## 關鍵點

### 1. JSX 需要轉換

**JSX 寫法**：
```jsx
function App() {
    return <h1>Hello React</h1>;
}
```

**轉換後的 JavaScript**（Vite 自動處理）：
```javascript
function App() {
    return React.createElement('h1', null, 'Hello React');
}
```

### 2. Vite React 插件

在 `vite.config.js` 中：

```javascript
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],  // 這個插件會處理 JSX
});
```

這個插件會：
- 轉換 JSX 成 JavaScript
- 處理 React 的特殊語法
- 提供熱更新

### 3. 直接引用 JSX

在 `index.html` 中：

```html
<script type="module" src="/src/main.jsx"></script>
```

**注意**：直接引用 `.jsx` 檔案，Vite 會自動處理！

## 對照：沒有工具 vs 有工具

### 沒有工具

```javascript
// 需要手動寫 React.createElement
function App() {
    return React.createElement('h1', null, 'Hello React');
}
```

### 有工具（Vite）

```jsx
// 可以用 JSX，工具自動轉換
function App() {
    return <h1>Hello React</h1>;
}
```

## 學習目標

完成這個範例後，你應該能夠：
- ✅ 理解 JSX 需要編譯
- ✅ 知道 React 為什麼需要工具
- ✅ 體驗 JSX 轉換過程

## 延伸練習

1. 嘗試寫更複雜的 JSX，觀察轉換結果
2. 查看瀏覽器開發者工具的 Sources，看看轉換後的程式碼
3. 思考：如果沒有 Vite，要如何處理 JSX？

## 對應章節

👉 [第 6 章：React 與 JavaScript](../../chapters/06_React與JavaScript.md)
