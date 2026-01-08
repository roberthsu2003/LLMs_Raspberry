const msg: string = "Hello Vite!";
const app = document.querySelector('#app');

if (app) {
    app.innerHTML = `
        <h1>${msg}</h1>
        <p>✅ Vite + TypeScript 運作正常！</p>
        <p>修改這個檔案，觀察自動重新載入（HMR）</p>
    `;
    console.log('🚀 Vite + TypeScript 已啟動！');
}
