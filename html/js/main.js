/* =====================================================================
   TIẾN ĐỨC — main.js  |  Vanilla JS, không thư viện ngoài
   ===================================================================== */
(function () {
  'use strict';

  /* ---------- 1. Mobile menu ---------- */
  var toggle = document.querySelector('.nav-toggle');
  var navlist = document.getElementById('navlist');

  if (toggle && navlist) {
    toggle.addEventListener('click', function () {
      var open = navlist.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    navlist.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        navlist.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---------- 2. Đánh dấu menu đang xem ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.navlist a[href^="#"]'));
  var targets = links
    .map(function (a) {
      return { link: a, el: document.querySelector(a.getAttribute('href')) };
    })
    .filter(function (t) { return t.el; });

  function markActive() {
    var y = window.scrollY + 140;
    var current = targets[0];
    for (var i = 0; i < targets.length; i++) {
      if (targets[i].el.offsetTop <= y) current = targets[i];
    }
    links.forEach(function (a) { a.classList.remove('is-active'); });
    if (current) current.link.classList.add('is-active');
  }

  var ticking = false;
  window.addEventListener('scroll', function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      markActive();
      ticking = false;
    });
  }, { passive: true });
  markActive();

  /* ---------- 3. Cuộn mượt tới section ---------- */
  document.addEventListener('click', function (e) {
    var a = e.target.closest('a[href^="#"]');
    if (!a) return;
    var id = a.getAttribute('href');
    if (id === '#' || id.length < 2) return;
    var el = document.querySelector(id);
    if (!el) return;
    e.preventDefault();
    var top = el.getBoundingClientRect().top + window.scrollY - 10;
    window.scrollTo({ top: top < 0 ? 0 : top, behavior: 'smooth' });
  });

  /* ---------- 4. Form đặt xe / liên hệ (xử lý cục bộ, không gọi API) ---------- */
  var forms = Array.prototype.slice.call(document.querySelectorAll('form[novalidate]'));

  forms.forEach(function (form) {
    var msg = form.querySelector('[role="status"]');
    if (!msg) return;

    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var fields = Array.prototype.slice.call(form.querySelectorAll('.field__input'));
      var invalid = null;

      fields.forEach(function (f) {
        var value = f.value.trim();
        var bad = f.required && !value;
        if (value && f.type === 'tel') {
          bad = bad || !/^[0-9+\s.\-()]{9,15}$/.test(value);
        }
        if (value && f.type === 'email') {
          bad = bad || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
        }
        f.classList.toggle('is-error', bad);
        if (bad && !invalid) invalid = f;
      });

      if (invalid) {
        msg.textContent = (invalid.type === 'tel' || invalid.type === 'email') && invalid.value.trim()
          ? 'Thông tin chưa đúng định dạng, Quý khách kiểm tra lại giúp em nhé.'
          : 'Quý khách vui lòng điền đầy đủ thông tin giúp em nhé.';
        msg.classList.add('is-error');
        invalid.focus();
        return;
      }

      msg.classList.remove('is-error');
      msg.textContent = form.dataset.successMsg || 'Đã ghi nhận yêu cầu! Tiến Đức sẽ liên hệ lại với Quý khách trong ít phút.';
      form.reset();
      fields.forEach(function (f) {
        if (f.type === 'datetime-local') f.type = 'text';
      });
    });

    form.addEventListener('input', function (e) {
      if (e.target.classList.contains('field__input')) {
        e.target.classList.remove('is-error');
      }
    });
  });
})();
