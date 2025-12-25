/**
 * 下一世代程式碼審查平台 - JavaScript 主程式
 * Next Gen Code Review Platform - Main JavaScript
 */

// 等待 DOM 載入完成
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Next Gen Code Review Platform 已啟動！');
  
  initButtons();
  initNavigation();
  initAnimations();
  logWelcomeMessage();
});

/**
 * 初始化按鈕互動
 */
function initButtons() {
  // 主要 CTA 按鈕
  const primaryButtons = document.querySelectorAll('.btn-primary');
  primaryButtons.forEach((btn) => {
    btn.addEventListener('click', handlePrimaryAction);
  });
  
  // 次要按鈕
  const secondaryButtons = document.querySelectorAll('.btn:not(.btn-primary)');
  secondaryButtons.forEach((btn) => {
    if (btn.textContent.includes('Log in')) {
      btn.addEventListener('click', handleLogin);
    } else if (btn.textContent.includes('Demo')) {
      btn.addEventListener('click', handleDemo);
    }
  });
  
  // Logo 點擊返回首頁
  const logo = document.querySelector('.logo');
  if (logo) {
    logo.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      showToast('🏠 返回首頁');
    });
  }
}

/**
 * 處理主要 CTA 動作
 */
function handlePrimaryAction(e) {
  const btnText = e.target.textContent.trim();
  
  if (btnText.includes('免費開始') || btnText.includes('Sign up')) {
    showModal(
      '🎉 歡迎加入！',
      '感謝您選擇我們的服務！請填寫註冊資訊開始您的免費試用之旅。',
      [
        { text: '立即註冊', class: 'btn-primary', action: () => console.log('開始註冊流程') },
        { text: '稍後再說', class: 'btn', action: closeModal }
      ]
    );
  }
}

/**
 * 處理登入
 */
function handleLogin() {
  showModal(
    '🔐 登入帳號',
    '請輸入您的帳號資訊以繼續使用我們的服務。',
    [
      { text: '登入', class: 'btn-primary', action: () => console.log('登入') },
      { text: '取消', class: 'btn', action: closeModal }
    ]
  );
}

/**
 * 處理申請 Demo
 */
function handleDemo() {
  showModal(
    '📺 申請產品展示',
    '我們的專業團隊將為您安排一對一的產品展示，讓您深入了解如何提升團隊的程式碼審查效率。',
    [
      { text: '立即預約', class: 'btn-primary', action: () => showToast('✅ 預約成功！我們將盡快與您聯繫') },
      { text: '取消', class: 'btn', action: closeModal }
    ]
  );
}

/**
 * 初始化導航互動
 */
function initNavigation() {
  const navLinks = document.querySelectorAll('nav a');
  
  navLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const section = link.textContent.trim();
      showToast(`📍 導航至：${section}`);
      console.log(`導航至：${section}`);
    });
  });
  
  // 品牌標誌互動
  const brandItems = document.querySelectorAll('.brand-item');
  brandItems.forEach((item) => {
    item.addEventListener('click', () => {
      const brandName = item.textContent.trim();
      showToast(`🏢 查看 ${brandName} 的使用案例`);
    });
  });
}

/**
 * 初始化動畫效果
 */
function initAnimations() {
  // Intersection Observer 用於滾動動畫
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'fadeInUp 0.8s ease';
      }
    });
  }, observerOptions);
  
  // 觀察所有需要動畫的元素
  const animatedElements = document.querySelectorAll('.brands, footer');
  animatedElements.forEach((el) => observer.observe(el));
}

/**
 * 顯示模態對話框
 */
function showModal(title, message, buttons = []) {
  // 移除現有的 modal
  const existingModal = document.querySelector('.modal');
  if (existingModal) {
    existingModal.remove();
  }
  
  // 創建新的 modal
  const modal = document.createElement('div');
  modal.className = 'modal active';
  
  // 創建按鈕 HTML
  const buttonsHTML = buttons.length > 0 
    ? buttons.map(btn => `
        <button class="btn ${btn.class}" data-action="${btn.text}">
          ${btn.text}
        </button>
      `).join('')
    : '<button class="btn btn-primary modal-close">確定</button>';
  
  modal.innerHTML = `
    <div class="modal-overlay"></div>
    <div class="modal-content">
      <h2>${title}</h2>
      <p>${message}</p>
      <div style="display: flex; gap: 12px; justify-content: center;">
        ${buttonsHTML}
      </div>
    </div>
  `;
  
  document.body.appendChild(modal);
  
  // 綁定按鈕事件
  if (buttons.length > 0) {
    buttons.forEach((btn, index) => {
      const btnElement = modal.querySelectorAll('.btn')[index];
      if (btnElement) {
        btnElement.addEventListener('click', () => {
          btn.action();
          if (btn.class.includes('primary')) {
            closeModal();
          }
        });
      }
    });
  } else {
    modal.querySelector('.modal-close').addEventListener('click', closeModal);
  }
  
  // 點擊背景關閉
  modal.querySelector('.modal-overlay').addEventListener('click', closeModal);
  
  // ESC 鍵關閉
  document.addEventListener('keydown', handleEscKey);
}

/**
 * 關閉模態對話框
 */
function closeModal() {
  const modal = document.querySelector('.modal');
  if (modal) {
    modal.classList.remove('active');
    setTimeout(() => modal.remove(), 300);
  }
  document.removeEventListener('keydown', handleEscKey);
}

/**
 * 處理 ESC 鍵
 */
function handleEscKey(e) {
  if (e.key === 'Escape') {
    closeModal();
  }
}

/**
 * 顯示 Toast 提示
 */
function showToast(message, duration = 3000) {
  // 移除現有的 toast
  const existingToast = document.querySelector('.toast');
  if (existingToast) {
    existingToast.remove();
  }
  
  // 創建新的 toast
  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.textContent = message;
  
  document.body.appendChild(toast);
  
  // 自動移除
  setTimeout(() => {
    toast.style.animation = 'slideOutRight 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

/**
 * 輸出歡迎訊息
 */
function logWelcomeMessage() {
  console.log(`
╔══════════════════════════════════════╗
║   🎨 Next Gen Code Review Platform   ║
║   📦 Pure JavaScript Application     ║
║   🚀 Version 1.0.0                   ║
║   🍓 Ready for Raspberry Pi          ║
╚══════════════════════════════════════╝
  `);
  
  console.log('📌 可用功能：');
  console.log('  - 免費開始試用');
  console.log('  - 申請產品展示');
  console.log('  - 帳號登入');
  console.log('  - 互動式導航');
}

/**
 * 視差滾動效果
 */
window.addEventListener('scroll', () => {
  const scrolled = window.pageYOffset;
  const glowWrap = document.querySelector('.glow-wrap');
  
  if (glowWrap && scrolled < 800) {
    const parallax = scrolled * 0.5;
    glowWrap.style.transform = `translateY(${parallax}px)`;
  }
});

/**
 * 滑鼠移動視差效果
 */
document.addEventListener('mousemove', (e) => {
  const glowWrap = document.querySelector('.glow-wrap');
  if (!glowWrap) return;
  
  const { clientX, clientY } = e;
  const { innerWidth, innerHeight } = window;
  
  const xPercent = (clientX / innerWidth - 0.5) * 20;
  const yPercent = (clientY / innerHeight - 0.5) * 20;
  
  glowWrap.style.transform = `translate(${xPercent}px, ${yPercent}px)`;
});

