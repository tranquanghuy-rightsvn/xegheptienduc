/* =====================================================================
   TIẾN ĐỨC — gợi ý địa điểm (Điểm đón / Điểm trả)
   Dùng "Vietnam Provinces API" (provinces.open-api.vn) — API hành chính
   Việt Nam miễn phí, không cần key. Toàn bộ danh sách Tỉnh/Thành và
   Phường/Xã (~3.300 đơn vị, ~340KB) được tải một lần rồi tìm kiếm ngay
   trên trình duyệt (không gọi lại API mỗi lần gõ phím).
   ===================================================================== */
(function () {
  'use strict';

  var MIN_CHARS = 2;
  var MAX_RESULTS = 8;
  var API_BASE = 'https://provinces.open-api.vn/api/v2/';

  var inputs = Array.prototype.slice.call(document.querySelectorAll('.js-place-autocomplete'));
  if (!inputs.length) return;

  function normalize(str) {
    return str
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .replace(/đ/g, 'd')
      .replace(/Đ/g, 'D')
      .toLowerCase()
      .trim();
  }

  /* ---------- Tải dữ liệu Tỉnh/Thành + Phường/Xã một lần, dùng chung cho mọi ô ---------- */
  var placesReady = Promise.all([
    fetch(API_BASE + 'p/').then(function (r) { return r.json(); }),
    fetch(API_BASE + 'w/').then(function (r) { return r.json(); }),
  ]).then(function (res) {
    var provinces = res[0];
    var wards = res[1];

    var provinceByCode = {};
    provinces.forEach(function (p) { provinceByCode[p.code] = p.name; });

    var places = provinces.map(function (p) {
      return { label: p.name, norm: normalize(p.name) };
    });

    wards.forEach(function (w) {
      var provinceName = provinceByCode[w.province_code];
      var label = provinceName ? w.name + ', ' + provinceName : w.name;
      places.push({ label: label, norm: normalize(label) });
    });

    return places;
  });

  function search(places, query) {
    var q = normalize(query);
    var matches = [];
    for (var i = 0; i < places.length; i++) {
      var idx = places[i].norm.indexOf(q);
      if (idx !== -1) matches.push({ label: places[i].label, rank: idx });
    }
    matches.sort(function (a, b) {
      return a.rank - b.rank || a.label.length - b.label.length;
    });
    return matches.slice(0, MAX_RESULTS).map(function (m) { return m.label; });
  }

  inputs.forEach(function (input) {
    var wrap = input.closest('.field__autocomplete');
    var list = wrap ? wrap.querySelector('.autocomplete-list') : null;
    if (!list) return;

    var items = [];
    var activeIndex = -1;

    function closeList() {
      list.hidden = true;
      list.innerHTML = '';
      items = [];
      activeIndex = -1;
      input.setAttribute('aria-expanded', 'false');
    }

    function renderMessage(text) {
      list.innerHTML = '<li class="autocomplete-msg">' + text + '</li>';
      list.hidden = false;
    }

    function renderItems(labels) {
      items = labels;
      activeIndex = -1;
      if (!labels.length) {
        renderMessage('Không tìm thấy địa danh phù hợp');
        return;
      }
      list.innerHTML = labels
        .map(function (label, i) {
          return '<li class="autocomplete-item" role="option" data-index="' + i + '">' + label + '</li>';
        })
        .join('');
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

    function selectItem(index) {
      if (!items[index]) return;
      input.value = items[index];
      closeList();
    }

    input.addEventListener('input', function () {
      var value = input.value.trim();
      if (value.length < MIN_CHARS) {
        closeList();
        return;
      }

      renderMessage('Đang tải dữ liệu địa danh...');

      placesReady
        .then(function (places) {
          if (input.value.trim() !== value) return; // đã gõ tiếp, bỏ kết quả cũ
          renderItems(search(places, value));
        })
        .catch(function () {
          renderMessage('Không thể tải dữ liệu địa danh, vui lòng thử lại');
        });
    });

    input.addEventListener('keydown', function (e) {
      if (list.hidden) return;
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        highlight(Math.min(activeIndex + 1, items.length - 1));
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        highlight(Math.max(activeIndex - 1, 0));
      } else if (e.key === 'Enter') {
        if (activeIndex >= 0) {
          e.preventDefault();
          selectItem(activeIndex);
        }
      } else if (e.key === 'Escape') {
        closeList();
      }
    });

    list.addEventListener('mousedown', function (e) {
      var item = e.target.closest('.autocomplete-item');
      if (!item) return;
      e.preventDefault();
      selectItem(Number(item.dataset.index));
    });

    document.addEventListener('click', function (e) {
      if (e.target !== input && !list.contains(e.target)) closeList();
    });
  });
})();
