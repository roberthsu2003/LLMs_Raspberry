// 可以 import 其他模組
import { msg } from './msg.js';
import { greet, add } from './utils.js';

// 使用 import 的內容
console.log(msg);
greet('World');

const result = add(1, 2);
console.log(`1 + 2 = ${result}`);

// DOM 操作
const app = document.querySelector('#app');
if (app) {
    app.textContent = `${msg} - 計算結果：${result}`;
}
