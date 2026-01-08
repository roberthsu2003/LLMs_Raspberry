import { useState } from 'react';
import Button from './components/Button';

function App() {
    const [count, setCount] = useState<number>(0);

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1>React + TypeScript + Vite</h1>
            <p>Count: {count}</p>
            <div style={{ display: 'flex', gap: '10px' }}>
                <Button 
                    text="增加" 
                    onClick={() => setCount(count + 1)} 
                />
                <Button 
                    text="減少" 
                    onClick={() => setCount(count - 1)} 
                />
            </div>
            <p style={{ marginTop: '20px', color: '#666' }}>
                這是完整的現代前端環境範例
            </p>
        </div>
    );
}

export default App;
