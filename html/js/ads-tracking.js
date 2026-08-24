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

  /** Gửi 1 sự kiện conversion. redirectUrl (nếu có, vd "tel:08...") sẽ được điều hướng tới
     NGAY SAU KHI gtag xác nhận đã gửi xong (hoặc timeout 2s nếu mạng chậm/bị chặn) — theo
     đúng pattern Google Ads khuyến nghị cho click-to-call, tránh mất conversion vì trình
     duyệt rời trang (gọi điện) trước khi request kịp gửi đi. */
  function sendConversion(sendTo, redirectUrl) {
    if (!sendTo || typeof gtag !== 'function') {
      if (redirectUrl) window.location = redirectUrl;
      return;
    }
    var navigated = false;
    var go = function () {
      if (navigated) return;
      navigated = true;
      if (redirectUrl) window.location = redirectUrl;
    };
    gtag('event', 'conversion', {
      send_to: sendTo,
      event_callback: go,
      event_timeout: 2000,
    });
    if (redirectUrl) setTimeout(go, 2000);
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
    if (!label) return; // chưa cấu hình label này - giữ hành vi mặc định (gọi/mở Zalo ngay)
    e.preventDefault();
    sendConversion(label, link.href);
  });
})();
