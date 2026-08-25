/* =====================================================================
   TIẾN ĐỨC — gợi ý địa điểm (Điểm đón / Điểm trả)
   Dùng đúng API backend của xevip (api.xevipsanbay.com — Goong Maps autocomplete),
   theo yêu cầu dùng chung API giữa 2 dự án. Backend giới hạn CORS theo origin đã đăng ký
   phía họ — cần domain của Tiến Đức được thêm vào whitelist mới gọi thành công khi deploy
   thật; không quan tâm việc đó ở đây theo yêu cầu, chỉ tập trung đúng cơ chế gọi.
   ===================================================================== */
(function () {
  'use strict';

  var API_BASE = 'https://api.xevipsanbay.com';
  var DEBOUNCE_MS = 250;

  var inputs = Array.prototype.slice.call(document.querySelectorAll('.js-place-autocomplete'));
  if (!inputs.length) return;

  function buildQuery(params) {
    return Object.keys(params)
      .filter(function (k) { return params[k] !== undefined && params[k] !== null && params[k] !== ''; })
      .map(function (k) { return encodeURIComponent(k) + '=' + encodeURIComponent(params[k]); })
      .join('&');
  }

  // GET /v1/goong-map/autocomplete — trả nguyên mảng predictions (object đầy đủ, không chỉ
  // description) để có thể dùng lại sau này nếu cần gửi kèm khi đặt xe.
  function fetchSuggestions(input) {
    if (!input || !input.trim()) return Promise.resolve([]);
    var qs = buildQuery({ input: input, has_deprecated_administrative_unit: true });
    return fetch(API_BASE + '/v1/goong-map/autocomplete?' + qs)
      .then(function (res) { return res.json(); })
      .then(function (json) {
        if (!json || !json.success) {
          console.error('[place-autocomplete] Lỗi tìm địa chỉ:', json);
          return [];
        }
        return (json.data && json.data.predictions) || [];
      })
      .catch(function (err) {
        console.error('[place-autocomplete] Không gọi được goong-map/autocomplete:', err);
        return [];
      });
  }

  var selectedAddressByInput = new WeakMap();

  function attach(input) {
    var wrap = input.closest('.field__autocomplete');
    var list = wrap ? wrap.querySelector('.autocomplete-list') : null;
    if (!list) return;

    var items = [];
    var activeIndex = -1;
    var debounceTimer = null;
    var requestSeq = 0;

    function closeList() {
      list.hidden = true;
      list.innerHTML = '';
      items = [];
      activeIndex = -1;
      input.setAttribute('aria-expanded', 'false');
    }

    function renderMessage(text) {
      list.innerHTML = '';
      var li = document.createElement('li');
      li.className = 'autocomplete-msg';
      li.textContent = text;
      list.appendChild(li);
      list.hidden = false;
    }

    function renderItems(predictions) {
      items = predictions;
      activeIndex = -1;
      if (!predictions.length) {
        renderMessage('Không tìm thấy địa điểm phù hợp');
        return;
      }
      list.innerHTML = '';
      predictions.forEach(function (item, i) {
        var fmt = item.structured_formatting || {};
        var main = fmt.main_text || item.description || '';
        var rest = fmt.secondary_text || '';
        var li = document.createElement('li');
        li.className = 'autocomplete-item';
        li.setAttribute('role', 'option');
        li.dataset.index = i;
        var strong = document.createElement('strong');
        strong.textContent = main;
        li.appendChild(strong);
        if (rest) li.appendChild(document.createTextNode(', ' + rest));
        list.appendChild(li);
      });
      list.hidden = false;
      input.setAttribute('aria-expanded', 'true');
    }

    function highlight(index) {
      var els = list.querySelectorAll('.autocomplete-item');
      els.forEach(function (el) { el.classList.remove('is-active'); });
      if (index >= 0 && els[index]) {
        els[index].classList.add('is-active');
        els[index].scrollIntoView({ block: 'nearest' });
      }
      activeIndex = index;
    }

    function selectItem(item) {
      input.value = item.description || '';
      selectedAddressByInput.set(input, item);
      closeList();
    }

    input.addEventListener('input', function () {
      selectedAddressByInput.delete(input);
      var value = input.value;
      var seq = ++requestSeq;
      clearTimeout(debounceTimer);
      if (!value.trim()) { closeList(); return; }

      renderMessage('Đang tìm...');
      debounceTimer = setTimeout(function () {
        fetchSuggestions(value).then(function (predictions) {
          if (seq === requestSeq) renderItems(predictions);
        });
      }, DEBOUNCE_MS);
    });

    input.addEventListener('keydown', function (e) {
      if (list.hidden || !items.length) return;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        highlight(Math.min(activeIndex + 1, items.length - 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        highlight(Math.max(activeIndex - 1, 0));
      } else if (e.key === 'Enter') {
        if (activeIndex >= 0) { e.preventDefault(); selectItem(items[activeIndex]); }
      } else if (e.key === 'Escape') {
        closeList();
      }
    });

    list.addEventListener('mousedown', function (e) {
      var li = e.target.closest('.autocomplete-item');
      if (!li) return;
      e.preventDefault();
      var idx = Number(li.dataset.index);
      if (items[idx]) selectItem(items[idx]);
    });

    document.addEventListener('click', function (e) {
      if (e.target !== input && !list.contains(e.target)) closeList();
    });
  }

  inputs.forEach(attach);

  window.PlaceAutocomplete = {
    getSelectedAddress: function (input) { return selectedAddressByInput.get(input) || null; },
  };
})();
