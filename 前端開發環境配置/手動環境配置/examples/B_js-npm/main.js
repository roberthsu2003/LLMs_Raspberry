// ❌ 這樣不行！瀏覽器不認識 'lodash'
// 這會導致錯誤：Failed to resolve module specifier "lodash"
import _ from 'lodash';

console.log('嘗試使用 lodash...');

// 如果上面的 import 成功，這行才會執行
const result = _.add(1, 2);
console.log('1 + 2 =', result);

document.querySelector('#app').textContent = 
    '如果看到這行，表示 import 失敗了。請查看 Console 的錯誤訊息。';
