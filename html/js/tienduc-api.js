/*
 * Client gọi API gợi ý địa chỉ, dùng lại đúng backend/API đang chạy cho dự
 * án xevip (api.xevipsanbay.com — Goong Maps autocomplete). Backend đó giới
 * hạn CORS theo origin, nên request ở đây CHỈ thành công khi domain đang
 * chạy trang đã được phía backend cho phép — chạy ở localhost/domain khác
 * sẽ bị trình duyệt tự chặn (browser chặn preflight, không phải lỗi code).
 * Trước khi lên production cho domain thật của Tiến Đức, cần xác nhận lại
 * với bên vận hành backend xem dùng chung endpoint này hay endpoint riêng.
 */
(function () {
  "use strict";

  var API_BASE = "https://api.xevipsanbay.com";

  function buildQuery(params) {
    return Object.keys(params)
      .filter(function (k) {
        return params[k] !== undefined && params[k] !== null && params[k] !== "";
      })
      .map(function (k) {
        return encodeURIComponent(k) + "=" + encodeURIComponent(params[k]);
      })
      .join("&");
  }

  // GET /v1/goong-map/autocomplete — trả nguyên mảng predictions (object đầy
  // đủ, không chỉ description) để có thể dùng thẳng làm địa chỉ khi cần gửi
  // đi sau này, đúng cách xevip đang làm.
  async function fetchAddressSuggestions(input) {
    if (!input || !input.trim()) return [];
    try {
      var qs = buildQuery({ input: input, has_deprecated_administrative_unit: true });
      var res = await fetch(API_BASE + "/v1/goong-map/autocomplete?" + qs);
      var json = await res.json();
      if (!json.success) {
        console.error("[tienduc-api] Lỗi tìm địa chỉ:", json);
        return [];
      }
      return (json.data && json.data.predictions) || [];
    } catch (err) {
      console.error("[tienduc-api] Không gọi được goong-map/autocomplete:", err);
      return [];
    }
  }

  window.TienDucApi = {
    fetchAddressSuggestions: fetchAddressSuggestions,
  };
})();
