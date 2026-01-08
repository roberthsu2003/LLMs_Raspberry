# 第 5 章：React 出現的理由（只談思想）

## 🎯 教學目標

完成本章後，你應該能夠：

- 理解 React 解決的是「UI 複雜度」問題
- 建立 Component 與 State 的核心觀念
- 知道 React 是一種 UI 思維，不只是工具
- 理解為什麼不用原生 DOM 操作
- 知道 React 跟 Vite、TypeScript 是不同層次的問題

---

## 📖 核心觀念

### 這一章專談「思想」

> **這章專談「思想」，不要馬上講建置**

在學習 React 的環境配置之前，我們先理解：
- React 為什麼存在？
- React 解決了什麼問題？
- React 的核心思想是什麼？

---

## 🤔 為什麼不用原生 DOM 操作？

### 傳統方式：直接操作 DOM

假設你要建立一個計數器：

```html
<!DOCTYPE html>
<html>
<body>
    <div>
        <span id="count">0</span>
        <button id="increment">+</button>
        <button id="decrement">-</button>
    </div>

    <script>
        let count = 0;
        const countElement = document.getElementById('count');
        const incrementBtn = document.getElementById('increment');
        const decrementBtn = document.getElementById('decrement');

        function updateUI() {
            countElement.textContent = count;
        }

        incrementBtn.addEventListener('click', () => {
            count++;
            updateUI();
        });

        decrementBtn.addEventListener('click', () => {
            count--;
            updateUI();
        });
    </script>
</body>
</html>
```

### 問題 1：狀態和 UI 不同步

**問題**：
- 狀態（`count`）存在變數中
- UI（`<span>`）存在 DOM 中
- 需要手動同步兩者

**容易出錯**：
- 忘記更新 UI
- 更新了錯誤的元素
- 狀態和 UI 不一致

### 問題 2：複雜的 UI 難以維護

假設你要建立一個待辦事項列表：

```javascript
// 傳統方式：直接操作 DOM
function addTodo(text) {
    const li = document.createElement('li');
    li.textContent = text;
    document.getElementById('todo-list').appendChild(li);
}

function removeTodo(id) {
    const element = document.getElementById(`todo-${id}`);
    element.remove();
}

function toggleTodo(id) {
    const element = document.getElementById(`todo-${id}`);
    element.classList.toggle('completed');
}

// ... 更多函數
```

**問題**：
- 程式碼分散
- 難以追蹤狀態
- 容易產生 bug

---

## 💡 React 的核心思想

### UI = State 的函數

> **UI 應該是 State 的函數，而不是手動操作 DOM**

```
State（狀態） → UI（使用者介面）
```

### React 的方式

```jsx
// React 方式：UI = f(State)
function Counter() {
    const [count, setCount] = useState(0);

    return (
        <div>
            <span>{count}</span>
            <button onClick={() => setCount(count + 1)}>+</button>
            <button onClick={() => setCount(count - 1)}>-</button>
        </div>
    );
}
```

**優勢**：
- 狀態改變 → UI 自動更新
- 不需要手動操作 DOM
- 狀態和 UI 永遠同步

---

## 🧩 Component 思維

### 什麼是 Component？

> **Component = 可重複使用的 UI 單元**

### 生活化比喻

想像你在組裝樂高：
- **Component** = 樂高積木
- **組合 Component** = 組裝樂高
- **重複使用** = 同樣的積木可以用在很多地方

### React Component 範例

```jsx
// Button Component（可重複使用）
function Button({ text, onClick }) {
    return <button onClick={onClick}>{text}</button>;
}

// 使用 Button Component
function App() {
    return (
        <div>
            <Button text="確定" onClick={() => alert('確定')} />
            <Button text="取消" onClick={() => alert('取消')} />
        </div>
    );
}
```

### Component 的優勢

1. **可重複使用**
   - 寫一次，用很多次
   - 減少重複程式碼

2. **易於維護**
   - 每個 Component 獨立
   - 修改一個不影響其他

3. **易於測試**
   - 可以單獨測試每個 Component
   - 測試範圍明確

4. **易於理解**
   - Component 名稱就是功能
   - 程式碼結構清晰

---

## 🎯 React 解決的問題

### 問題 1：UI 複雜度

**傳統方式**：
- 手動操作 DOM
- 狀態和 UI 不同步
- 難以維護

**React 方式**：
- 宣告式 UI（描述「應該是什麼樣子」）
- 狀態改變自動更新 UI
- 易於維護

### 問題 2：程式碼組織

**傳統方式**：
- 程式碼分散
- 難以追蹤

**React 方式**：
- Component 組織
- 結構清晰

### 問題 3：狀態管理

**傳統方式**：
- 狀態存在變數中
- 需要手動同步 UI

**React 方式**：
- 狀態和 UI 綁定
- 自動同步

---

## 🔄 React 的渲染流程

### 傳統方式

```
狀態改變 → 手動找到 DOM 元素 → 手動更新 → UI 改變
```

### React 方式

```
狀態改變 → React 重新計算 UI → 比較差異 → 只更新改變的部分
```

**優勢**：
- 不需要手動操作 DOM
- React 自動處理更新
- 效能優化（只更新改變的部分）

---

## 💡 React 與其他工具的關係

### React vs TypeScript

- **React**：解決 UI 問題
- **TypeScript**：解決型別問題
- **關係**：可以一起使用（React + TypeScript）

### React vs Vite

- **React**：UI 框架
- **Vite**：開發工具
- **關係**：Vite 可以幫你開發 React 專案

### 不同層次的問題

```
框架層：React（解決 UI 問題）
    ↓
工具層：Vite（解決開發流程問題）
    ↓
語言層：TypeScript（解決型別問題）
    ↓
執行層：JavaScript（瀏覽器執行）
```

---

## 🎓 關鍵理解

### React 解決的是「UI 複雜度」

> **React 不是為了讓程式跑得更快，而是為了讓 UI 開發更容易**

- 傳統方式：命令式（告訴瀏覽器「怎麼做」）
- React 方式：宣告式（告訴 React「應該是什麼樣子」）

### React 是一種 UI 思維

> **React 不只是工具，更是一種思考 UI 的方式**

- Component 思維
- 狀態管理思維
- 單向資料流思維

### React 跟其他工具是不同層次

> **React 解決 UI 問題，Vite/TypeScript 解決其他問題**

- React：UI 框架
- Vite：開發工具
- TypeScript：型別系統

---

## ⚠️ 學生常見迷思

### ❌ 迷思 1：「React 是 JavaScript 的進階版」

**事實**：React 是 UI 框架，不是語言。

**為什麼**：React 是用 JavaScript 寫的框架，用來建立 UI。

### ❌ 迷思 2：「學會 React 就不用學 JavaScript」

**事實**：React 建立在 JavaScript 之上，需要 JavaScript 基礎。

**為什麼**：React 只是工具，JavaScript 是基礎。

### ❌ 迷思 3：「React 就是在寫 HTML」

**事實**：React 使用 JSX，看起來像 HTML 但不是。

**為什麼**：JSX 是語法糖，最終會轉換成 JavaScript。

### ❌ 迷思 4：「React = SPA（單頁應用）」

**事實**：React 可以用在任何地方，不一定是 SPA。

**為什麼**：React 只是 UI 框架，可以用在各種場景。

---

## 🎓 本章重點回顧

1. **React 解決 UI 複雜度問題**
   - 傳統方式：手動操作 DOM
   - React 方式：宣告式 UI

2. **UI = State 的函數**
   - 狀態改變 → UI 自動更新
   - 不需要手動同步

3. **Component 思維**
   - 可重複使用的 UI 單元
   - 易於維護和測試

4. **React 是 UI 框架**
   - 跟 Vite、TypeScript 是不同層次
   - 解決的是 UI 問題

---

## 🚀 下一章預告

在下一章，我們將學習 **React 與 JavaScript**。

你會學到：
- 為什麼 JSX 需要編譯
- 沒有工具時寫 React 的痛點
- React 為什麼幾乎一定需要工具

👉 [前往第 6 章：React 與 JavaScript](./06_React與JavaScript.md)

---

## 💪 練習建議

1. **思考題**：比較「傳統 DOM 操作」和「React 方式」的差異

2. **設計題**：設計一個簡單的 UI（例如待辦事項），思考如何用 Component 組織

3. **研究題**：搜尋「React 核心概念」，了解 Virtual DOM、單向資料流等概念
