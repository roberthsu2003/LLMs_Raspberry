import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
    return (
        <div>
            <h1>Hello React</h1>
            <p>這是用 JSX 寫的 React 元件</p>
            <p>修改這個檔案，觀察 JSX 如何被轉換</p>
        </div>
    );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
