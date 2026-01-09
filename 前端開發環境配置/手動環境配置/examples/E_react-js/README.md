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

---

## 🛠️ 建立新專案

### 方式一：使用 `npm create` 快速建立（推薦）

最快速的方式是使用 Vite 官方提供的腳手架工具：

```bash
# 建立新專案
npm create vite@latest my-react-project

# 在建立過程中選擇：
# ✓ Select a framework: › React
# ✓ Select a variant: › JavaScript
```

**完整步驟：**

1. **執行建立命令：**
   ```bash
   npm create vite@latest my-react-project
   ```

2. **選擇專案模板：**
   - 選擇 `React` 框架
   - 選擇 `JavaScript` 變體（不是 TypeScript）

3. **進入專案目錄並安裝依賴：**
   ```bash
   cd my-react-project
   npm install
   ```

4. **啟動開發伺服器：**
   ```bash
   npm run dev
   ```

**✅ 優點：**
- 快速建立，幾秒鐘完成
- 自動配置好所有必要的檔案（`vite.config.js`、`package.json` 等）
- 自動安裝 React 和 Vite React 插件（`@vitejs/plugin-react`）
- 使用官方推薦的配置
- 適合快速開始新專案

**💡 模板選擇說明：**
- `react`：React + JavaScript（就是這個範例使用的）
- `react-ts`：React + TypeScript（進階版本）

### 方式二：手動建立專案（學習用）

如果你想深入了解每個檔案的用途和配置，可以參考這個範例的檔案結構手動建立：

1. 建立專案目錄和基本檔案
2. 初始化 `package.json`
3. 安裝依賴套件（`react`、`react-dom`、`vite`、`@vitejs/plugin-react`）
4. 建立配置檔案（`vite.config.js`）
5. 建立原始碼檔案（`src/main.jsx`、`index.html`）

這種方式適合想要深入理解 React + Vite 配置的學習者。

---

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
