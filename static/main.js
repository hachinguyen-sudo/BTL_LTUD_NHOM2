/* =============================================
   CLEANSPACE – main.js
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ── Navbar scroll shadow ────────────────── */
  const navbar = document.getElementById('csNavbar');
  if (navbar) {
    window.addEventListener('scroll', () => {
      navbar.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
  }

  /* ── Back to top ─────────────────────────── */
  const backTop = document.getElementById('cs-back-top');
  if (backTop) {
    window.addEventListener('scroll', () => {
      backTop.classList.toggle('visible', window.scrollY > 400);
    }, { passive: true });
    backTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ── Auto-dismiss alerts sau 5s ─────────── */
  document.querySelectorAll('.alert-dismissible').forEach((el, i) => {
    setTimeout(() => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(el);
      bsAlert?.close();
    }, 5000 + i * 400);
  });

  /* ── Scroll-reveal ───────────────────────── */
  const revealEls = document.querySelectorAll('[data-reveal]');
  if (revealEls.length && 'IntersectionObserver' in window) {
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-fadeup');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    revealEls.forEach(el => obs.observe(el));
  }

});

/* ── Toast helper (dùng toàn site) ──────────
   Cách dùng: csToast('Đặt lịch thành công!', 'success')
   type: 'success' | 'danger' | 'warning' | 'info'
─────────────────────────────────────────────── */
function csToast(message, type = 'success', duration = 4000) {
  let container = document.getElementById('cs-toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'cs-toast-container';
    container.style.cssText = 'position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;display:flex;flex-direction:column;gap:.5rem;';
    document.body.appendChild(container);
  }

  const colors = {
    success: '#2E8B63',
    danger:  '#D94040',
    warning: '#F5C842',
    info:    '#1A6B4A'
  };
  const icons = {
    success: 'bi-check-circle-fill',
    danger:  'bi-exclamation-circle-fill',
    warning: 'bi-exclamation-triangle-fill',
    info:    'bi-info-circle-fill'
  };

  const toast = document.createElement('div');
  toast.style.cssText = `
    background:#fff;
    border-left:3px solid ${colors[type]};
    border-radius:10px;
    padding:.75rem 1rem;
    box-shadow:0 4px 16px rgba(0,0,0,.1);
    display:flex;align-items:center;gap:.65rem;
    font-family:'DM Sans',sans-serif;font-size:.9rem;
    min-width:240px;max-width:340px;
    cursor:pointer;
    animation:fadeUp .3s ease both;
  `;
  toast.innerHTML = `<i class="bi ${icons[type]}" style="color:${colors[type]};font-size:1rem;"></i><span>${message}</span>`;
  toast.addEventListener('click', () => toast.remove());
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity .3s';
    setTimeout(() => toast.remove(), 320);
  }, duration);
}
