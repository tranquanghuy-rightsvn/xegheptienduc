/*
 * Gợi ý địa chỉ cho các ô "Điểm đón"/"Điểm trả" dạng nhập tự do, dùng
 * TienDucApi.fetchAddressSuggestions (GET /v1/goong-map/autocomplete) —
 * copy nguyên cơ chế đang chạy ở dự án xevip (js/xevip-address-autocomplete.js)
 * theo yêu cầu dùng chung API giữa 2 dự án.
 *
 * Module lưu lại toàn bộ object gợi ý đã chọn (không chỉ set input.value)
 * qua getSelectedAddress(input), phòng khi sau này cần gửi nguyên object đó
 * đi thay vì chỉ gửi chuỗi text.
 */
(function () {
  "use strict";

  var selectedAddressByInput = new WeakMap();

  function getSelectedAddress(input) {
    return (input && selectedAddressByInput.get(input)) || null;
  }

  function clearSelectedAddress(input) {
    if (input) selectedAddressByInput.delete(input);
  }

  function setSelectedAddress(input, address) {
    if (!input) return;
    if (address) selectedAddressByInput.set(input, address);
    else selectedAddressByInput.delete(input);
  }

  function attachAddressAutocomplete(input, list) {
    if (!input || !list) return;

    var activeIndex = -1;
    var currentItems = [];
    var debounceTimer = null;
    var requestSeq = 0;

    function closeList() {
      list.hidden = true;
      list.innerHTML = "";
      activeIndex = -1;
      currentItems = [];
    }

    function renderList(items) {
      currentItems = items;
      activeIndex = -1;
      if (!items.length) {
        closeList();
        return;
      }
      list.innerHTML = items
        .map(function (item, i) {
          var fmt = item.structured_formatting || {};
          var main = fmt.main_text || item.description || "";
          var rest = fmt.secondary_text || "";
          return (
            '<li class="address-suggestion-item" data-index="' +
            i +
            '"><strong>' +
            main +
            "</strong>" +
            (rest ? ", " + rest : "") +
            "</li>"
          );
        })
        .join("");
      list.hidden = false;
      clampListToViewport();
    }

    // Backstop cho trường hợp gợi ý dài đẩy dropdown tràn khỏi màn hình trên
    // mobile (đặc biệt Android khi bàn phím ảo đang mở) — CSS lo phần chính,
    // đây chỉ là lớp bảo hiểm nếu CSS chưa chặn hết.
    function clampListToViewport() {
      requestAnimationFrame(function () {
        if (list.hidden) return;
        var rect = list.getBoundingClientRect();
        var viewportWidth = document.documentElement.clientWidth;
        var overflowRight = rect.right - viewportWidth;
        if (overflowRight > 0) {
          list.style.maxWidth = Math.max(0, rect.width - overflowRight - 4) + "px";
        }
        if (document.documentElement.scrollWidth > viewportWidth) {
          closeList();
        }
      });
    }

    function selectItem(item) {
      input.value = item.description || "";
      try {
        input.setSelectionRange(0, 0);
      } catch (err) {
        /* setSelectionRange không áp dụng cho vài loại input — bỏ qua */
      }
      input.scrollLeft = 0;
      selectedAddressByInput.set(input, item);
      closeList();
    }

    function setActive(index) {
      var children = list.querySelectorAll(".address-suggestion-item");
      children.forEach(function (el) {
        el.classList.remove("active");
      });
      if (index >= 0 && children[index]) {
        children[index].classList.add("active");
        children[index].scrollIntoView({ block: "nearest" });
      }
      activeIndex = index;
    }

    input.addEventListener("input", function () {
      clearSelectedAddress(input);
      var query = input.value;
      var seq = ++requestSeq;
      clearTimeout(debounceTimer);
      if (!query.trim()) {
        closeList();
        return;
      }
      debounceTimer = setTimeout(function () {
        TienDucApi.fetchAddressSuggestions(query).then(function (items) {
          if (seq === requestSeq) renderList(items);
        });
      }, 250);
    });

    input.addEventListener("keydown", function (e) {
      if (list.hidden || !currentItems.length) return;
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setActive((activeIndex + 1) % currentItems.length);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setActive((activeIndex - 1 + currentItems.length) % currentItems.length);
      } else if (e.key === "Enter") {
        if (activeIndex >= 0) {
          e.preventDefault();
          selectItem(currentItems[activeIndex]);
        }
      } else if (e.key === "Escape") {
        closeList();
      }
    });

    list.addEventListener("mousedown", function (e) {
      var item = e.target.closest(".address-suggestion-item");
      if (!item) return;
      e.preventDefault();
      var idx = Number(item.dataset.index);
      if (currentItems[idx]) selectItem(currentItems[idx]);
    });

    document.addEventListener("click", function (e) {
      if (e.target !== input && !list.contains(e.target)) closeList();
    });
  }

  function initAddressAutocomplete() {
    document.querySelectorAll(".place-autocomplete-input").forEach(function (input) {
      var list = input.parentElement.querySelector(".address-suggestions");
      attachAddressAutocomplete(input, list);
    });
  }

  window.TienDucAddressAutocomplete = {
    getSelectedAddress: getSelectedAddress,
    clearSelectedAddress: clearSelectedAddress,
    setSelectedAddress: setSelectedAddress,
    init: initAddressAutocomplete,
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAddressAutocomplete);
  } else {
    initAddressAutocomplete();
  }
})();
