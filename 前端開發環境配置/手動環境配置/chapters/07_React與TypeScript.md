# 第 7 章：React + TypeScript（型別與元件）

## 🎯 教學目標

完成本章後，你應該能夠：

- 理解型別如何幫助元件設計
- 知道 Props、State 為什麼需要型別
- 建立「型別是輔助，而不是負擔」的觀念
- 理解 React + TypeScript 的優勢
- 知道如何為 React 元件加上型別

---

## 📖 核心觀念

### 為什麼 React + TypeScript？

在前面的章節，我們學到了：
- React：解決 UI 問題
- TypeScript：解決型別問題

**組合起來**：
- React + TypeScript = 型別安全的 UI 開發

---

## 🎯 Props 型別

### 沒有型別的 Props

```jsx
// JavaScript（沒有型別）
function Button(props) {
    return <button onClick={props.onClick}>{props.text}</button>;
}

// 使用時可能出錯
<Button text="確定" />  // 忘記傳 onClick，執行時才發現錯誤
<Button onClick={handleClick} />  // 忘記傳 text，執行時才發現錯誤
```

### 有型別的 Props

```tsx
// TypeScript（有型別）
interface ButtonProps {
    text: string;
    onClick: () => void;
}

function Button({ text, onClick }: ButtonProps) {
    return <button onClick={onClick}>{text}</button>;
}

// 使用時 IDE 會提示
<Button text="確定" onClick={handleClick} />  // ✅ 正確
<Button text="確定" />  // ❌ TypeScript 錯誤：缺少 onClick
<Button onClick={handleClick} />  // ❌ TypeScript 錯誤：缺少 text
```

**優勢**：
- 開發時就發現錯誤
- IDE 會自動提示
- 程式碼就是文件

---

## 📝 常見的 React + TypeScript 模式

### 1. 函數元件（Function Component）

```tsx
interface GreetingProps {
    name: string;
    age?: number;  // 可選屬性
}

function Greeting({ name, age }: GreetingProps) {
    return (
        <div>
            <h1>Hello, {name}!</h1>
            {age && <p>You are {age} years old.</p>}
        </div>
    );
}

// 使用
<Greeting name="John" />
<Greeting name="Jane" age={25} />
```

### 2. 狀態（State）型別

```tsx
import { useState } from 'react';

function Counter() {
    // TypeScript 會自動推斷 count 是 number
    const [count, setCount] = useState(0);
    
    // 也可以明確指定型別
    const [name, setName] = useState<string>('');
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>+</button>
        </div>
    );
}
```

### 3. 事件處理函數型別

```tsx
function Form() {
    const [value, setValue] = useState('');
    
    // 事件處理函數的型別
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setValue(e.target.value);
    };
    
    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log(value);
    };
    
    return (
        <form onSubmit={handleSubmit}>
            <input 
                type="text" 
                value={value} 
                onChange={handleChange} 
            />
            <button type="submit">Submit</button>
        </form>
    );
}
```

### 4. 子元件（Children）型別

```tsx
interface ContainerProps {
    children: React.ReactNode;  // 可以是任何 React 節點
    title: string;
}

function Container({ children, title }: ContainerProps) {
    return (
        <div>
            <h2>{title}</h2>
            {children}
        </div>
    );
}

// 使用
<Container title="標題">
    <p>這是內容</p>
    <button>按鈕</button>
</Container>
```

---

## 🎨 實際範例：待辦事項

### 完整的 TypeScript + React 範例

```tsx
import { useState } from 'react';

// 定義 Todo 的型別
interface Todo {
    id: number;
    text: string;
    completed: boolean;
}

// TodoItem 元件的 Props
interface TodoItemProps {
    todo: Todo;
    onToggle: (id: number) => void;
    onDelete: (id: number) => void;
}

// TodoItem 元件
function TodoItem({ todo, onToggle, onDelete }: TodoItemProps) {
    return (
        <div>
            <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => onToggle(todo.id)}
            />
            <span style={{ 
                textDecoration: todo.completed ? 'line-through' : 'none' 
            }}>
                {todo.text}
            </span>
            <button onClick={() => onDelete(todo.id)}>刪除</button>
        </div>
    );
}

// 主 App 元件
function App() {
    const [todos, setTodos] = useState<Todo[]>([]);
    const [input, setInput] = useState<string>('');

    const addTodo = () => {
        if (input.trim()) {
            setTodos([
                ...todos,
                {
                    id: Date.now(),
                    text: input,
                    completed: false,
                },
            ]);
            setInput('');
        }
    };

    const toggleTodo = (id: number) => {
        setTodos(
            todos.map(todo =>
                todo.id === id ? { ...todo, completed: !todo.completed } : todo
            )
        );
    };

    const deleteTodo = (id: number) => {
        setTodos(todos.filter(todo => todo.id !== id));
    };

    return (
        <div>
            <h1>待辦事項</h1>
            <div>
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addTodo()}
                />
                <button onClick={addTodo}>新增</button>
            </div>
            <div>
                {todos.map(todo => (
                    <TodoItem
                        key={todo.id}
                        todo={todo}
                        onToggle={toggleTodo}
                        onDelete={deleteTodo}
                    />
                ))}
            </div>
        </div>
    );
}

export default App;
```

---

## 💡 React + TypeScript 的優勢

### 1. 型別安全的 Props

```tsx
// ✅ 正確使用
<Button text="確定" onClick={handleClick} />

// ❌ TypeScript 會報錯
<Button text="確定" />  // 缺少 onClick
<Button onClick={handleClick} />  // 缺少 text
<Button text={123} onClick={handleClick} />  // text 應該是 string
```

### 2. 自動完成

```tsx
interface User {
    name: string;
    age: number;
    email: string;
}

function UserProfile({ user }: { user: User }) {
    // IDE 會自動提示 user.name, user.age, user.email
    return <div>{user.name}</div>;
}
```

### 3. 重構安全

```tsx
// 修改介面名稱
interface ButtonProps {
    text: string;  // 改成 label
    onClick: () => void;
}

// TypeScript 會告訴你所有需要修改的地方
```

### 4. 程式碼即文件

```tsx
// 型別就是文件
interface FormData {
    username: string;      // 使用者名稱
    password: string;       // 密碼
    rememberMe: boolean;    // 記住我
}
```

---

## 🎓 關鍵理解

### 型別是輔助，不是負擔

> **型別幫助你寫出更好的程式碼，而不是限制你**

- 開發時發現錯誤
- IDE 自動完成
- 程式碼更容易理解

### Props、State 為什麼需要型別

> **型別確保資料結構正確，避免執行時錯誤**

- Props：確保傳入的資料正確
- State：確保狀態的型別正確
- 事件：確保事件處理函數的參數正確

### React + TypeScript 是主流

> **現代 React 開發幾乎都使用 TypeScript**

- 更好的開發體驗
- 更少的錯誤
- 更容易維護

---

## ⚠️ 學生常見迷思

### ❌ 迷思 1：「React + TS 很難，一定要很會 TS」

**事實**：不需要，基本的型別就夠用了。

**為什麼**：React + TypeScript 有很好的型別推斷，很多時候不需要明確寫型別。

### ❌ 迷思 2：「型別寫越多越好」

**事實**：適度就好，過度型別化反而增加負擔。

**為什麼**：TypeScript 有型別推斷，很多時候可以省略。

### ❌ 迷思 3：「any 可以解決一切」

**事實**：使用 `any` 會失去 TypeScript 的優勢。

**為什麼**：`any` 會關閉型別檢查，應該避免使用。

### ❌ 迷思 4：「錯誤變多是因為 TypeScript 很嚴格」

**事實**：這些錯誤本來就存在，TypeScript 只是提前發現。

**為什麼**：TypeScript 在開發時發現錯誤，避免執行時才發現。

---

## 🎓 本章重點回顧

1. **Props 需要型別**
   - 確保傳入的資料正確
   - IDE 自動完成

2. **State 需要型別**
   - 確保狀態的型別正確
   - 避免型別錯誤

3. **型別是輔助**
   - 幫助寫出更好的程式碼
   - 不是負擔

4. **React + TypeScript 是主流**
   - 更好的開發體驗
   - 更少的錯誤

---

## 🚀 下一章預告

在下一章，我們將學習 **完整現代環境**。

你會學到：
- 整合所有概念（React + TypeScript + Vite）
- 每一層技術在做什麼
- 現代前端專案的標準組成

👉 [前往第 8 章：完整現代環境](./08_完整現代環境.md)

---

## 💪 練習建議

1. **實作題**：建立一個 React + TypeScript 專案，為所有元件加上型別

2. **對照題**：比較「有型別」和「沒有型別」的 React 元件，感受差異

3. **研究題**：查看 React TypeScript 官方文件，了解更多型別模式
