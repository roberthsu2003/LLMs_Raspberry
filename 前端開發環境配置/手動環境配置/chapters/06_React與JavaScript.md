# 第 6 章：React + JavaScript（最小 React 環境）

## 🎯 教學目標

完成本章後，你應該能夠：

- 讓學生實際感受「沒有工具時寫 React 的痛點」
- 理解 JSX 為什麼需要編譯
- 建立「框架 ≠ 能直接丟進瀏覽器」的概念
- 知道 React 為什麼幾乎一定需要工具
- 理解 JSX 轉換成 JavaScript 的過程

---

## 📖 核心觀念

### 讓學生「痛一次」

> **目的：讓學生實際感受「沒有工具時寫 React 的痛點」**

這很重要，因為：
- 親身體驗比聽講更深刻
- 理解為什麼需要工具
- 知道工具的價值在哪裡

---

## ❌ 為什麼不能直接用 React？

### 嘗試 1：直接引入 React

假設你寫了這樣的程式碼：

```html
<!DOCTYPE html>
<html>
<body>
    <div id="app"></div>
    
    <!-- 直接引入 React -->
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    
    <script>
        // 嘗試寫 React 程式碼
        function App() {
            return <h1>Hello React</h1>;
        }
        
        ReactDOM.render(<App />, document.getElementById('app'));
    </script>
</body>
</html>
```

### 瀏覽器報錯

打開瀏覽器 Console，你會看到：

```
Uncaught SyntaxError: Unexpected token '<'
```

**為什麼？**

因為瀏覽器不認識 `<h1>Hello React</h1>` 這種語法！

---

## 🔍 JSX 是什麼？

### JSX 不是 JavaScript

```jsx
// 這是 JSX（不是標準 JavaScript）
function App() {
    return <h1>Hello React</h1>;
}
```

**問題**：瀏覽器只能執行 JavaScript，不認識 JSX。

### JSX 需要轉換

JSX 必須轉換成 JavaScript：

```jsx
// JSX（瀏覽器不認識）
function App() {
    return <h1>Hello React</h1>;
}
```

↓ 轉換 ↓

```javascript
// JavaScript（瀏覽器認識）
function App() {
    return React.createElement('h1', null, 'Hello React');
}
```

---

## 🛠️ 手動轉換 JSX（理解過程）

### 使用 React.createElement

**JSX 寫法**：
```jsx
function App() {
    return (
        <div>
            <h1>Hello</h1>
            <p>World</p>
        </div>
    );
}
```

**手動轉換成 JavaScript**：
```javascript
function App() {
    return React.createElement(
        'div',
        null,
        React.createElement('h1', null, 'Hello'),
        React.createElement('p', null, 'World')
    );
}
```

### 使用 React.createElement 的完整範例

```html
<!DOCTYPE html>
<html>
<head>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
</head>
<body>
    <div id="app"></div>
    
    <script>
        // 不使用 JSX，使用 React.createElement
        function App() {
            return React.createElement(
                'div',
                null,
                React.createElement('h1', null, 'Hello React'),
                React.createElement('p', null, '這是用 React.createElement 寫的')
            );
        }
        
        const root = ReactDOM.createRoot(document.getElementById('app'));
        root.render(React.createElement(App));
    </script>
</body>
</html>
```

**這可以運作！** 但寫起來很痛苦。

---

## 💡 為什麼需要工具？

### 問題 1：JSX 需要轉換

- 手動寫 `React.createElement` 太麻煩
- 需要工具自動轉換 JSX

### 問題 2：模組系統

- 需要 `import React from 'react'`
- 瀏覽器不認識 npm 套件

### 問題 3：開發體驗

- 沒有自動重新載入
- 沒有錯誤提示
- 沒有熱更新

---

## 📁 最小 React 環境（使用 Vite）

### 範例 E：React + JavaScript（最小可理解版）

```
react-js/
├── index.html
├── src/
│   └── main.jsx          # JSX 檔案
├── vite.config.js
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
    <title>React + JavaScript</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>
```

#### `src/main.jsx`

```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
    return (
        <div>
            <h1>Hello React</h1>
            <p>這是用 JSX 寫的 React 元件</p>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
```

#### `vite.config.js`

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
    plugins: [react()],  // 這個插件會處理 JSX
});
```

#### `package.json`

```json
{
  "name": "react-js",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.0",
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

# 3. Vite 會自動：
#    - 轉換 JSX 成 JavaScript
#    - 處理 React 套件
#    - 提供熱更新
```

---

## 🔄 JSX 轉換過程

### 轉換前（JSX）

```jsx
function App() {
    const name = 'World';
    return (
        <div className="container">
            <h1>Hello {name}</h1>
            <button onClick={() => alert('Clicked!')}>
                Click me
            </button>
        </div>
    );
}
```

### 轉換後（JavaScript）

```javascript
function App() {
    const name = 'World';
    return React.createElement(
        'div',
        { className: 'container' },
        React.createElement('h1', null, 'Hello ', name),
        React.createElement(
            'button',
            { onClick: () => alert('Clicked!') },
            'Click me'
        )
    );
}
```

**觀察**：
- `<div>` → `React.createElement('div', ...)`
- `className` → 屬性物件
- `{name}` → JavaScript 表達式
- `onClick` → 事件處理函數

---

## 🎓 關鍵理解

### JSX 不是瀏覽器語法

> **JSX 是語法糖，需要轉換成 JavaScript**

- 瀏覽器不認識 JSX
- 需要工具轉換
- React.createElement 是實際執行的程式碼

### React 幾乎離不開工具

> **React 幾乎一定需要工具來處理 JSX**

- 手動寫 React.createElement 太麻煩
- 需要工具自動轉換
- 需要工具處理模組系統

### 框架 ≠ 能直接丟進瀏覽器

> **框架需要工具來處理**

- React 需要轉換 JSX
- Vue 需要轉換 template
- 都需要工具鏈支援

---

## ⚠️ 學生常見迷思

### ❌ 迷思 1：「React 檔案可以直接用 <script> 引入」

**事實**：可以引入 React 函式庫，但不能直接寫 JSX。

**為什麼**：JSX 需要轉換，瀏覽器不認識。

### ❌ 迷思 2：「JSX 是瀏覽器語法」

**事實**：JSX 是語法糖，需要轉換成 JavaScript。

**為什麼**：瀏覽器只能執行 JavaScript，不認識 JSX。

### ❌ 迷思 3：「只要會 React，就不用管建置」

**事實**：React 幾乎一定需要工具來處理 JSX。

**為什麼**：手動寫 React.createElement 太麻煩，不實用。

---

## 🎓 本章重點回顧

1. **JSX 需要轉換**
   - 瀏覽器不認識 JSX
   - 需要轉換成 React.createElement

2. **React 幾乎離不開工具**
   - 手動寫太麻煩
   - 需要工具自動轉換

3. **框架 ≠ 能直接丟進瀏覽器**
   - 需要工具鏈支援
   - 需要轉換過程

4. **體驗「痛點」的價值**
   - 理解為什麼需要工具
   - 知道工具的價值

---

## 🚀 下一章預告

在下一章，我們將學習 **React 與 TypeScript**。

你會學到：
- 型別如何幫助元件設計
- Props、State 為什麼需要型別
- React + TypeScript 的優勢

👉 [前往第 7 章：React 與 TypeScript](./07_React與TypeScript.md)

---

## 💪 練習建議

1. **實作題**：嘗試手動寫 React.createElement，感受一下沒有 JSX 的痛苦

2. **對照題**：比較「JSX 寫法」和「React.createElement 寫法」的差異

3. **研究題**：查看 Vite 如何轉換 JSX，了解轉換過程
