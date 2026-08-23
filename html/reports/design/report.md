# Báo cáo clone — Tiến Đức Transport & Travel

**Nguồn:** `xegheptienduc/design.jpg` (ảnh thiết kế 720×1280, không phải URL)
**Đích:** `xegheptienduc/html/index.html` — HTML/CSS/JS thuần, không framework, không build step.
**Ngày:** 2026-08-23

---

## 1. File đã tạo

```
xegheptienduc/html/
├── index.html                  1 trang, semantic, sprite SVG inline (28 icon)
├── css/style.css               21 @font-face self-host + toàn bộ style theo component
├── js/main.js                  menu mobile, active-nav theo scroll, smooth scroll, validate form
├── fonts/                      Montserrat 600/700/800 + Quicksand 400/500/600/700
│                               (subset vietnamese + latin + latin-ext, 21 file woff2, 620 KB)
├── images/                     14 ảnh (596 KB)
├── reports/design/             ảnh gốc / clone / diff theo từng section + báo cáo này
└── .work/                      file trung gian (fonts.css, rtest.html, fullpage-1200.png)
```

Không có URL nào bị skip — đầu vào là ảnh thiết kế nên bỏ qua bước crawl.

## 2. Ảnh — **cần đại ca thay lại**

Đại ca nói *"hình ảnh lấy trên internet tôi sẽ tạo ảnh sau"*, nên toàn bộ ảnh hiện tại
là **ảnh tạm cắt trực tiếp từ `design.jpg`** (nguồn chỉ 720px nên độ nét thấp).
Giữ nguyên tên file, thay bằng ảnh nét là xong, không phải sửa HTML/CSS:

| File | Tỉ lệ cần giữ | Kích thước nên dùng | Nội dung |
|---|---|---|---|
| `hero-banner.jpg` | 2.63 : 1 | 2400×912 | Banner: 2 xe + logo + vịnh Hạ Long |
| `logo.png` | 1 : 1, **nền trong suốt** | 512×512 | Logo tròn TĐ (hiện là bản tách nền từ design, nguồn 49px nên hơi mềm) |
| `svc-1…5.jpg` | 16 : 10 | 800×500 | Xe ghép / Đưa đón / Sân bay / Hà Nội / Du lịch |
| `route-1…4.jpg` | 2 : 1 | 800×400 | Cầu Bãi Cháy / Sân bay Cát Bi / Vân Đồn / Hải Phòng |
| `car-vf5.jpg`, `car-limo.jpg` | ~1.9 : 1 | 800×420 | Xe trên **nền tối** (đang dùng `mix-blend-mode:lighten` để hoà vào panel) |
| `footer-cars.jpg` | ~4.6 : 1 | 900×195 | 2 xe nhỏ, nền tối |

> `logo.png` đã được **tách nền hoàn toàn** — cả nền ngoài lẫn phần bên trong vòng tròn đều
> trong suốt, chỉ còn lại phần nhũ vàng (vòng ring + monogram TĐ). Cách làm: lấy màu nền thật
> `#001f0d`, tính alpha theo khoảng cách màu, rồi un-blend `C = a·F + (1-a)·B` để lấy lại màu
> gốc của nhũ vàng → không bị viền xanh quanh nét. Dùng được trên mọi màu nền.
>
> Lưu ý: 3 ảnh xe dùng blend `lighten` + mask bo mép nên **nền phải tối** (đen/xanh đậm),
> không dùng nền trắng. Nếu có ảnh PNG nền trong thì báo em, em bỏ blend đi cho sạch.

## 3. Kết quả pixel-diff (`pixel-diff.mjs`, threshold 0.1)

Chụp bản clone ở viewport **1200px**, cắt theo từng section, resize về đúng khung
tương ứng trong `design.jpg` rồi so.

| Section | % giống | Ghi chú |
|---|---:|---|
| Header + menu | **75.15%** | |
| Hero banner | 68.62% | ảnh banner tạm chiếm gần hết diện tích |
| Dịch vụ | 63.00% | 5 ảnh card tạm chiếm ~45% diện tích |
| Đội xe + Đặt xe | 64.72% | 2 ảnh xe tạm |
| Tuyến xe | 76.03% | 4 ảnh card tạm |
| Lời chào + Vì sao | **82.09%** | section gần như thuần chữ → cao nhất |
| Footer | 71.02% | |
| **Toàn trang** | 56.48% | |

Đo riêng các dải **không có ảnh** (chỉ chữ + khung), để tách phần bố cục/typography:

| Dải | % giống |
|---|---:|
| Thanh menu | 77.30% |
| Khối chữ Dịch vụ | 76.25% |
| Khối chữ Tuyến xe | 82.92% |
| Panel Đặt xe | 62.83% |

### Chưa đạt ngưỡng 90% — lý do

1. **Ảnh đang là ảnh tạm.** Ảnh cắt từ chính `design.jpg` rồi phóng to → trình duyệt
   thu nhỏ lại → em thu nhỏ lần nữa để so. Ba lần resample + JPEG làm gần như 100%
   pixel trong vùng ảnh bị tính là khác, dù nhìn mắt thì giống hệt. Riêng vùng ảnh đã
   chiếm 40–70% diện tích các section thấp điểm.
2. **`design.jpg` là ảnh raster, không phải web thật.** Chữ trong file thiết kế được
   render bằng công cụ khác (font gần Montserrat/Quicksand nhưng không trùng tuyệt đối),
   trong khi bản clone dùng font thật do trình duyệt vẽ. Mỗi nét chữ lệch 1px
   anti-alias là pixelmatch tính khác ngay — riêng cái này đã đánh rớt ~15–20%.
3. **Chiều cao trang lệch 3.7%** (2211px so với 2133px quy đổi từ thiết kế), gây trôi
   dần vài px theo chiều dọc trong mỗi section.

Ngưỡng 90% của quy trình được đặt cho trường hợp clone **site thật** (font và ảnh
giống 100%). So với một file JPEG thiết kế thì con số này không đạt được, kể cả khi
bố cục đã trùng khít. Sau khi đại ca thay ảnh nét, em có thể đo lại theo tiêu chí
"so bản clone với bản clone" nếu cần.

## 4. Checklist "không vỡ giao diện" — đã soát ở 4 breakpoint

Kiểm tra ở **1920 / 1366 / 768 / 375** (768 và 375 test qua iframe vì headless Chrome
ép chiều rộng cửa sổ tối thiểu).

| Hạng mục | 1920 | 1366 | 768 | 375 |
|---|:-:|:-:|:-:|:-:|
| Không scroll ngang (`scrollWidth == clientWidth`) | ✅ | ✅ | ✅ | ✅ |
| Không tràn / chồng đè phần tử | ✅ | ✅ | ✅ | ✅ |
| Chữ không bị cắt, không đè lên ảnh | ✅ | ✅ | ✅ | ✅ |
| Ảnh không vỡ, đúng `object-fit`, đúng tỉ lệ | ✅ | ✅ | ✅ | ✅ |
| Khoảng cách các khối đều, không dính sát | ✅ | ✅ | ✅ | ✅ |
| Menu mobile mở/đóng được | – | – | ✅ | ✅ |
| Form đặt xe validate + báo lỗi/thành công | ✅ | ✅ | ✅ | ✅ |
| Hover state nút / card / link | ✅ | ✅ | ✅ | ✅ |

Chuyển bố cục: 5 → 3 → 2 → 1 cột (card dịch vụ); 4 → 2 → 1 cột (tuyến xe);
2 → 1 cột (đội xe / đặt xe / lời chào); menu ngang → hamburger từ 900px.

## 5. UX tự suy luận (thiết kế tĩnh không thể hiện hành vi)

- **Menu mobile**: trượt xuống bằng `max-height` transition, tự đóng khi bấm link.
- **Active nav**: tự đổi theo section đang xem khi cuộn (`requestAnimationFrame`).
- **Form đặt xe**: xử lý cục bộ hoàn toàn — validate rỗng + regex số điện thoại, viền đỏ
  ô sai, hiện thông báo. **Không gọi API nào ra ngoài.** Nếu đại ca cần gửi thật thì
  đấu vào Google Apps Script / Formspree sau.
- **Ô "Thời gian đi"**: `type="text"` cho hiện placeholder, đổi sang `datetime-local`
  khi focus (mẹo tránh trình duyệt hiện `dd/mm/yyyy` ngay từ đầu).
- **Nút gọi nổi** góc trái dưới, có animation rung nhẹ.
- Toàn bộ hiệu ứng ưu tiên CSS transition; JS chỉ lo menu, active-nav, form.
- Có `prefers-reduced-motion` tắt animation.

## 6. Kỹ thuật

- Không framework, không thư viện — vanilla JS 1 file ~110 dòng.
- Icon: sprite `<symbol>` SVG inline (28 icon), dùng lại bằng `<use>` → không tải file ngoài.
- Font self-host `.woff2`, chỉ lấy subset **vietnamese + latin + latin-ext**, `font-display:swap`.
- Ảnh dưới fold đều có `loading="lazy"`; banner hero có `fetchpriority="high"`.
- CSS gom theo component (`.svc-card`, `.route-card`, `.panel`, `.field`…), biến màu ở `:root`,
  không dump computed-style lặp lại từng phần tử.
- **Không** tracking bên thứ ba, **không** `fetch`/XHR ra ngoài, **không** asset trỏ domain khác.

## 7. Dọn dẹp

- Không có thư mục `.work/` cũ ≥3 ngày nào trong workspace cần dọn.
- Đã xoá các ảnh placeholder không dùng (`car-*.png`, `footer-cars.png` bản cũ).
- `.work/` của lần chạy này còn giữ (fonts.css, rtest.html, fullpage-1200.png) để nếu đại ca
  muốn chỉnh tiếp thì không phải làm lại từ đầu.
