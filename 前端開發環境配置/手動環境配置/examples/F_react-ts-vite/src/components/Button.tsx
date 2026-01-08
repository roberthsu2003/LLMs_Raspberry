interface ButtonProps {
    text: string;
    onClick: () => void;
}

function Button({ text, onClick }: ButtonProps) {
    return (
        <button 
            onClick={onClick}
            style={{
                padding: '10px 20px',
                fontSize: '16px',
                cursor: 'pointer',
                backgroundColor: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
            }}
        >
            {text}
        </button>
    );
}

export default Button;
