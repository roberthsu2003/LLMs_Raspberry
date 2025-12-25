// 等待 DOM 載入完成
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 TypeScript 網頁應用已啟動！');
    initFeatureCards();
    initButtons();
    initAnimations();
    initConnectionLines();
});
// 初始化功能卡片互動
function initFeatureCards() {
    const cards = document.querySelectorAll('.feature-card');
    cards.forEach((card) => {
        // 滑鼠懸停效果
        card.addEventListener('mouseenter', () => {
            card.classList.add('active');
            const category = card.getAttribute('data-category');
            console.log(`🎯 查看功能: ${category?.toUpperCase()}`);
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('active');
        });
        // 點擊效果
        card.addEventListener('click', () => {
            const category = card.getAttribute('data-category');
            showFeatureInfo(category || 'unknown');
        });
    });
}
// 顯示功能資訊
function showFeatureInfo(category) {
    const messages = {
        calls: '📞 通話功能：與銷售團隊即時對話，獲取客戶洞察',
        tickets: '🎫 工單系統：自動匯總支援工單，追蹤問題趨勢',
        reviews: '⭐ 評論管理：集中管理所有平台的客戶評論',
        surveys: '📊 問卷調查：設計調查問卷，自動生成分析報告'
    };
    const message = messages[category] || '功能說明';
    // 創建提示訊息
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.cssText = `
    position: fixed;
    top: 100px;
    right: 40px;
    background: rgba(59, 130, 246, 0.95);
    color: white;
    padding: 16px 24px;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 600;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    z-index: 10000;
    animation: slideInRight 0.3s ease;
  `;
    document.body.appendChild(toast);
    // 3 秒後移除
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
// 初始化按鈕互動
function initButtons() {
    const contactBtn = document.getElementById('contactBtn');
    const tryFreeBtn = document.getElementById('tryFreeBtn');
    if (contactBtn) {
        contactBtn.addEventListener('click', () => {
            console.log('📧 聯絡銷售團隊');
            showModal('聯絡銷售', '感謝您的興趣！我們的銷售團隊將盡快與您聯繫。');
        });
    }
    if (tryFreeBtn) {
        tryFreeBtn.addEventListener('click', () => {
            console.log('🎉 免費試用');
            showModal('免費試用', '歡迎體驗 Dovetail！請填寫註冊資訊開始您的試用之旅。');
        });
    }
    // Badge 點擊
    const badge = document.querySelector('.badge');
    if (badge) {
        badge.addEventListener('click', () => {
            console.log('📺 觀看 Keynote');
            showModal('2025 秋季發表會', '即將播放完整發表會影片...');
        });
    }
}
// 顯示模態對話框
function showModal(title, message) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
    <div class="modal-overlay"></div>
    <div class="modal-content">
      <h2>${title}</h2>
      <p>${message}</p>
      <button class="btn-primary" onclick="this.closest('.modal').remove()">確定</button>
    </div>
  `;
    modal.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 20000;
  `;
    const overlay = modal.querySelector('.modal-overlay');
    if (overlay) {
        overlay.style.cssText = `
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(5px);
    `;
    }
    const content = modal.querySelector('.modal-content');
    if (content) {
        content.style.cssText = `
      position: relative;
      background: #1a1a1a;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 40px;
      max-width: 500px;
      text-align: center;
      animation: scaleIn 0.3s ease;
    `;
        const h2 = content.querySelector('h2');
        if (h2) {
            h2.style.cssText = 'font-size: 28px; margin-bottom: 16px;';
        }
        const p = content.querySelector('p');
        if (p) {
            p.style.cssText = 'color: #a0a0a0; margin-bottom: 24px; line-height: 1.6;';
        }
    }
    document.body.appendChild(modal);
    // 點擊背景關閉
    overlay?.addEventListener('click', () => modal.remove());
}
// 初始化動畫
function initAnimations() {
    // 添加 CSS 動畫樣式
    const style = document.createElement('style');
    style.textContent = `
    @keyframes slideInRight {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
    
    @keyframes scaleIn {
      from {
        transform: scale(0.9);
        opacity: 0;
      }
      to {
        transform: scale(1);
        opacity: 1;
      }
    }
  `;
    document.head.appendChild(style);
}
// 初始化連接線動畫
function initConnectionLines() {
    const svg = document.querySelector('.connection-lines');
    if (!svg)
        return;
    const cards = document.querySelectorAll('.feature-card');
    const lines = [];
    // 創建連接線
    function createLines() {
        // 清除現有線條
        lines.forEach(line => line.remove());
        lines.length = 0;
        const cardsArray = Array.from(cards);
        for (let i = 0; i < cardsArray.length - 1; i++) {
            const card1 = cardsArray[i];
            const card2 = cardsArray[i + 1];
            if (!card1 || !card2)
                continue;
            const rect1 = card1.getBoundingClientRect();
            const rect2 = card2.getBoundingClientRect();
            const svgRect = svg.getBoundingClientRect();
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', String(rect1.left - svgRect.left + rect1.width / 2));
            line.setAttribute('y1', String(rect1.top - svgRect.top + rect1.height / 2));
            line.setAttribute('x2', String(rect2.left - svgRect.left + rect2.width / 2));
            line.setAttribute('y2', String(rect2.top - svgRect.top + rect2.height / 2));
            line.setAttribute('stroke', 'url(#lineGradient)');
            line.setAttribute('stroke-width', '2');
            line.setAttribute('opacity', '0.3');
            svg.appendChild(line);
            lines.push(line);
        }
    }
    // 初始創建
    setTimeout(createLines, 100);
    // 視窗大小改變時重新創建
    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = window.setTimeout(createLines, 250);
    });
    // 滑鼠移動時的視差效果
    document.addEventListener('mousemove', (e) => {
        const { clientX, clientY } = e;
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        const moveX = (clientX - centerX) / 50;
        const moveY = (clientY - centerY) / 50;
        cards.forEach((card, index) => {
            const element = card;
            const delay = index * 0.1;
            element.style.transform = `translate(${moveX * delay}px, ${moveY * delay}px)`;
        });
    });
}
// 統計資訊
console.log(`
╔══════════════════════════════════════╗
║   🎨 Customer Feedback Platform      ║
║   📦 TypeScript Demo Application     ║
║   🚀 Version 1.0.0                   ║
║   🍓 Ready for Raspberry Pi          ║
╚══════════════════════════════════════╝
`);
export {};
//# sourceMappingURL=index.js.map