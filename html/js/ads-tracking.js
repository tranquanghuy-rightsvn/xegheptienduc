/* =====================================================================
   TIẾN ĐỨC — ads-tracking.js
   Chỉ include ở trang chủ (index.html) — chiến dịch Google Ads chỉ chạy cho trang chủ,
   không cần gtag ở trang Tin tức/Liên hệ.

   Đọc cấu hình từ window.GOOGLE_ADS_TAG_ID / window.GOOGLE_ADS_LABELS — 2 biến này nằm ở
   <head> của index.html, trong vùng do scripts/build.py TỰ VÁ LẠI từ data/site-config.json
   mỗi khi Lưu tab "Cài đặt quảng cáo" trong CMS. KHÔNG cấu hình bằng cách sửa file JS này.
   Để trống bất kỳ giá trị nào = hành động đó chưa được track (không lỗi gì cả).
   ===================================================================== */
(function () {
  'use strict';

  if (!window.GOOGLE_ADS_TAG_ID) return; // chưa cấu hình Tag ID - không làm gì cả

  var labels = window.GOOGLE_ADS_LABELS || {};

  /** Gửi 1 sự kiện conversion. KHÔNG preventDefault/điều hướng lại bằng JS cho tel:/zalo.me —
     trình duyệt (Chrome/Safari) chặn thẳng tay các lượt "tự động gọi điện" khi việc điều
     hướng tel: xảy ra ngoài lượt click gốc (vd trong setTimeout hoặc event_callback của
     gtag), vì lúc đó không còn được tính là user-gesture nữa. Nên: cứ để thẻ
     <a href="tel:...">/"https://zalo.me/..."> tự điều hướng ngay trong lượt
     click gốc như bình thường, chỉ bắn ping conversion song song, không chờ, không chặn. */
  function sendConversion(sendTo) {
    if (!sendTo || typeof gtag !== 'function') return;
    gtag('event', 'conversion', { send_to: sendTo });
  }

  // Gửi form đặt xe thành công - main.js tự phát sự kiện này sau khi server xác nhận đã lưu
  // (không phát khi honeypot chặn bot, không phát khi demo mode chưa deploy GAS).
  document.addEventListener('tienduc:conversion', function (e) {
    if (e.detail && e.detail.type === 'booking') sendConversion(labels.booking);
  });

  // Bấm gọi điện / Zalo ở bất kỳ đâu trên trang chủ (header, hero, floating button, footer).
  document.addEventListener('click', function (e) {
    var telLink = e.target.closest('a[href^="tel:"]');
    var zaloLink = !telLink && e.target.closest('a[href*="zalo.me"]');
    var link = telLink || zaloLink;
    if (!link) return;
    var label = telLink ? labels.call : labels.zalo;
    if (!label) return; // chưa cấu hình label này - không track gì thêm
    sendConversion(label);
  });
})();
