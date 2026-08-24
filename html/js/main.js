/* =====================================================================
   TIẾN ĐỨC — main.js  |  Vanilla JS, không thư viện ngoài
   ===================================================================== */
(function () {
  'use strict';

  /* Dán URL /exec của Web App Google Apps Script vào đây sau khi deploy CMS (xem
     gas/README.md). Rỗng = form vẫn validate/hiện thông báo cục bộ như trước nhưng
     KHÔNG gửi đi đâu — chỉ để tránh vỡ trang khi chưa deploy xong CMS. */
  var GAS_EXEC_URL = '';

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

  /* ---------- 4. Form đặt xe / liên hệ ----------
     Validate cục bộ như cũ, sau đó gửi thật lên GAS doPost() qua fetch(). Content-Type
     text/plain (không phải application/json) để request ở lại dạng "simple request" —
     trình duyệt không gửi OPTIONS preflight trước, vì GAS không xử lý được OPTIONS (xem
     skill free-cms-static-site-pipeline, gas-backend-patterns.md mục 6). */
  var forms = Array.prototype.slice.call(document.querySelectorAll('form[novalidate]'));

  function withLoading(button, run) {
    if (!button) return run();
    var originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = 'Đang gửi...';
    return run().finally(function () {
      button.disabled = false;
      button.innerHTML = originalText;
    });
  }

  forms.forEach(function (form) {
    var msg = form.querySelector('[role="status"]');
    if (!msg) return;

    var submitBtn = form.querySelector('button[type="submit"]');
    var apiAction = form.dataset.apiAction || '';

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

      // Honeypot: field ẩn bằng CSS (.hp-field), người dùng thật không bao giờ điền.
      // Bot form-filler tự động điền vào mọi input kể cả ẩn — có giá trị là biết ngay bot.
      // Âm thầm báo "thành công" (không gửi gì) để không "dạy" bot biết nó bị phát hiện.
      var hp = form.querySelector('input[name="_hp"]');
      var isBot = hp && hp.value.trim();

      function showSuccess() {
        msg.classList.remove('is-error');
        msg.textContent = form.dataset.successMsg || 'Đã ghi nhận yêu cầu! Tiến Đức sẽ liên hệ lại với Quý khách trong ít phút.';
        form.reset();
        fields.forEach(function (f) {
          if (f.type === 'datetime-local') f.type = 'text';
        });
      }

      if (isBot) {
        showSuccess();
        return;
      }

      if (!GAS_EXEC_URL || !apiAction) {
        // Chưa deploy CMS / chưa dán URL — vẫn hiện thông báo để không vỡ trải nghiệm
        // demo, nhưng KHÔNG gửi đi đâu cả.
        showSuccess();
        return;
      }

      var payload = { formType: apiAction, _hp: '' };
      fields.forEach(function (f) {
        if (f.name) payload[f.name] = f.value.trim();
      });

      withLoading(submitBtn, function () {
        return fetch(GAS_EXEC_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          body: JSON.stringify(payload),
        })
          .then(function (res) { return res.json(); })
          .then(function (json) {
            if (json && json.ok) {
              showSuccess();
              // Báo cho ads-tracking.js (nếu có, chỉ tồn tại ở trang chủ) rằng vừa có 1
              // chuyển đổi thật (không phải bot, không phải demo mode) - main.js cố tình
              // không biết gì về Google Ads, chỉ phát 1 sự kiện DOM chung.
              document.dispatchEvent(new CustomEvent('tienduc:conversion', { detail: { type: apiAction } }));
            } else {
              msg.classList.add('is-error');
              msg.textContent = 'Có lỗi xảy ra, Quý khách vui lòng gọi trực tiếp hotline 0862 933 233 giúp em nhé.';
            }
          })
          .catch(function () {
            msg.classList.add('is-error');
            msg.textContent = 'Không gửi được yêu cầu (lỗi mạng), Quý khách vui lòng gọi trực tiếp hotline 0862 933 233 giúp em nhé.';
          });
      });
    });

    form.addEventListener('input', function (e) {
      if (e.target.classList.contains('field__input')) {
        e.target.classList.remove('is-error');
      }
    });
  });
})();
