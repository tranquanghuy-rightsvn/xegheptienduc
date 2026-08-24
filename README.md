# xegheptienduc — Nhà xe Tiến Đức

Site tĩnh (HTML/CSS/JS thuần) + CMS quản lý qua Google Apps Script, theo playbook
`free-cms-static-site-pipeline` (GAS + GitHub Contents API + GitHub Actions build).

## Cấu trúc

```
html/               site tĩnh thật (deploy trực tiếp thư mục này)
  index.html         trang chủ
  lien-he/           trang liên hệ (có form gửi CMS)
  tin-tuc/           trang tin tức — index.html + <slug>.html do scripts/build.py sinh ra
data/                nguồn dữ liệu tin tức — CMS ghi khi Lưu/Xoá qua GitHub Contents API
  posts.json          index nhẹ mọi bài
  tin-tuc/<slug>.json nội dung đầy đủ 1 bài
templates/           khung HTML tin tức (sửa TAY khi cần đổi design, build.py không tự sinh)
scripts/build.py     đọc data/ + templates/ -> ghi html/tin-tuc/**.html + vá sitemap.xml
.github/workflows/   build.yml — chạy build.py khi data/posts.json đổi
gas/                 CMS backend (KHÔNG track git — xem gas/README.md để deploy)
```

## Quy tắc — đừng sửa nhầm chỗ

| Ai ghi | Ai đọc | Sửa tay được không |
|---|---|---|
| `data/posts.json`, `data/tin-tuc/*.json` | `scripts/build.py` | **Không** — build lại sẽ mất, đây là nơi CMS ghi |
| `data/site-config.json` | `scripts/build.py` | **Không** — CMS ghi qua tab "Cài đặt quảng cáo" |
| `html/tin-tuc/*.html` | trình duyệt khách | **Không** — `build.py` ghi đè mỗi lần chạy |
| `html/index.html` — vùng `GOOGLE_ADS_CONFIG_START...END` | trình duyệt khách | **Không** — `build.py` vá lại vùng này mỗi lần chạy |
| `html/index.html` — phần còn lại, `html/lien-he/index.html` | trình duyệt khách | **Có** — không qua build script |
| `templates/*.html` | `build.py` đọc để render | **Có** — đây là chỗ sửa design trang tin tức |

## Vận hành hằng ngày

- **Thêm/sửa/xoá tin tức**: qua CMS (`gas/README.md` có URL sau khi deploy) — không sửa tay
  `html/tin-tuc/*.html`, sẽ bị build tiếp theo ghi đè.
- **Sửa trang chủ / trang liên hệ / thiết kế chung**: sửa trực tiếp trong `html/`, commit +
  push bình thường.
- **Đổi design trang tin tức**: sửa `templates/post.html` hoặc `templates/tin-tuc-index.html`
  rồi chạy `python3 scripts/build.py` (không cần internet/dependency ngoài) để build lại toàn
  bộ, review diff trước khi commit.

## Test build script cục bộ

```bash
python3 scripts/build.py
git diff html/tin-tuc html/sitemap.xml   # xem có đổi gì ngoài ý muốn không trước khi commit
```

Idempotent — chạy 2 lần liên tiếp không tự sinh thêm diff.

## Form công khai (Đặt xe / Liên hệ)

`html/index.html` (form `#booking-form`) và `html/lien-he/index.html` (form `#contact-form`)
gửi trực tiếp lên GAS `doPost()` qua `fetch()` (xem `html/js/main.js`, biến `GAS_EXEC_URL`).
Đặt xe → lưu Sheet `Bookings` + gửi email tới `Tienductransport@gmail.com`. Liên hệ → chỉ lưu
Sheet `Contacts` (không gửi mail, giữ quota Gmail 100 mail/ngày cho OTP đăng nhập CMS). Xem
chi tiết deploy ở `gas/README.md`.

## Google Ads (Tag + conversion tracking)

Chỉ gắn ở **trang chủ** (`html/index.html`) — chiến dịch Ads chỉ chạy cho trang chủ, các trang
Tin tức/Liên hệ không có đoạn này. **Cấu hình qua CMS**, tab "Cài đặt quảng cáo" (không sửa
code tay) — nguồn chân lý là `data/site-config.json`, giống Tin tức: Lưu trong CMS → GAS ghi
thẳng lên GitHub → GitHub Actions tự chạy `scripts/build.py` (hàm `patch_homepage_ads_config`)
→ vá lại đúng vùng `<!-- GOOGLE_ADS_CONFIG_START -->...END` trong `html/index.html` (kỹ thuật
"vá tại chỗ" bằng mốc neo, không dùng template cho toàn trang chủ) → push → deploy.

4 ô cần điền trong tab "Cài đặt quảng cáo" sau khi có tài khoản Google Ads:

1. **Tag ID** (`AW-XXXXXXXXX`) — Google Ads → Tools → Conversions → nhấn vào tag.
2. **3 conversion label** (`AW-XXXXXXXXX/AbCdEfGhIjKlMnOp`, khác Tag ID) — mỗi hành động tạo
   1 "Conversion action" riêng trong Google Ads: gửi form Đặt xe thành công, bấm số điện
   thoại, bấm Zalo (đều ở trang chủ: header, hero, nút nổi góc trái, footer).

Để trống bất kỳ ô nào = hành động đó chưa được track, không lỗi gì (đã tự test: không tải
gtag.js khi Tag ID rỗng, không dispatch conversion giả ở demo mode chưa deploy CMS, chống được
injection nếu ai đó lỡ dán `</script>` vào 1 ô).
