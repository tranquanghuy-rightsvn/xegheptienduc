I Đối với tính năng đăng nhập:
  1. sử dụng luồng gửi OTP -> xác nhận -> Vào trang admin. 
  2. Chỉ email được đăng ký mới được gửi OTP
  3. Acount chủ của GAS luôn hợp lệ, không cần lưu vào Database (Excel), Không quản lý account này trên trang quản trị
  4. Tham khảo dự án mẫu(trithucworld)
  5. Phân quyền tối thiểu 2 cấp: root (chính là account chủ GAS ở mục 3) và editor (tài khoản
     do root "đăng ký" thêm qua 1 tab riêng trong trang Admin — chỉ cần nhập email, người đó
     tự đăng nhập bằng OTP gửi tới email đó, không cần cấp mật khẩu). Chỉ thêm quyền mới ngoài
     2 cấp này nếu có hành vi PHÂN BIỆT rõ ràng trong nghiệp vụ thật — không thêm "phòng khi
     sau này cần".
  6. Mã OTP sống 10 phút, cooldown 60 giây giữa 2 lần xin mã liên tiếp cùng 1 email, tối đa 5
     lần nhập sai rồi phải xin mã mới (chặn dò mã 6 số). Mã xác thực xong đổi thành 1 token
     phiên đăng nhập sống 30 ngày, lưu ở trình duyệt (localStorage) để lần sau vào không phải
     xin OTP lại.
  7. Server luôn tự kiểm tra quyền ở MỌI hành động (lưu bài, xoá bài, đổi cài đặt...) — không
     tin việc ẩn nút/menu trên giao diện là đủ để bảo mật, vì ai gọi thẳng được hàm xử lý vẫn
     làm được nếu server không tự chặn.
  8. Bẫy dễ gặp nhất — xem chi tiết + cách né ở mục IX, bug "Đăng nhập GAS nhưng không vào
     trang Admin".

II Đối với tính năng viết bài
  1. Các field mặc định (CÓ ô nhập riêng trên giao diện — không tự ý thêm field mới hoặc bỏ
     đi field mặc định nếu không được phép):
  - Tiêu đề 
  - Slug (tự sinh theo quy tắc bỏ dấu, dấu cách thay bằng gạch ngang; bất biến sau khi đã
    Lưu lần đầu — xem mục III)
  - Danh mục: chữ tự do (không phải 1 bảng danh mục quản lý riêng), gợi ý lại các danh mục
    đã dùng qua để chọn nhanh cho nhất quán, không bắt buộc đúng y hệt tên cũ.
  - Description: Chính là description ở meta đồng thời sử dụng để hiện thị ở UI nếu cần —
    CHỈ 1 field duy nhất phục vụ CẢ 2 mục đích (hiện ở thẻ bài viết ngoài danh sách VÀ làm
    nội dung thẻ meta description cho SEO), KHÔNG tách thành 2 field riêng (Tóm tắt / Mô tả
    SEO) — tách ra là dư thừa vì gần như lúc nào cũng gõ giống nhau.
  - Cover: Ảnh được lưu trực tiếp trên github sau khi upload, sử dụng file ảnh tạm thời của ảnh để hiển thị trên bài viết.
    RIÊNG cho từng bài — KHÔNG có cơ chế "chọn lại ảnh đã dùng ở bài khác". Tên file trên
    GitHub đặt CỨNG theo slug (`<slug>-cover.jpg`), không theo tên gốc client gửi lên: tải
    ảnh mới cho cùng 1 bài sẽ tự GHI ĐÈ đúng ảnh cũ (không tạo file rác); xoá bài sẽ xoá
    đúng ảnh của bài đó (an toàn vì chắc chắn không bài/trang nào khác dùng chung đường dẫn
    này — xem mục IV). Phải điền xong URL bài viết TRƯỚC khi tải ảnh (ảnh cần biết slug để
    đặt tên) — sau khi tải ảnh xong, URL tự khoá lại luôn (không đợi tới lúc bấm Lưu), tránh
    đổi slug sau đó làm ảnh vừa tải bị lạc khỏi bài.
  - Nội dung: Sử dụng tinyMCE, cần có: Link, kiểu chữ (h1 -> h6), style chữ (nghiêng, đậm, gạch chân), chèn bảng, chèn ảnh. Trong đó:
      + Chèn ảnh: Chèn xong upload lên github ngay lập tức 
      + Hiển thị ảnh tạm tên giao diện
      + Khi thêm xong thì có caption, caption có style riêng (text caption: Sửa caption ...).
      + Khi thêm xong thì con trỏ ở "Sửa caption ..." sẵn sảng để sửa
  - Tham khảo dự án mẫu (trithucworld) 

  2. Các field KHÔNG có ô nhập trên giao diện — server tự suy ra lúc Lưu, không hỏi người
     viết (giữ form gọn, tránh bắt điền lặp lại thứ có thể tự đoán được):
     - Tiêu đề SEO (thẻ <title>): tự lấy = Tiêu đề.
     - Tiêu đề breadcrumb (hiện ở đầu trang bài viết, nếu layout có): tự lấy = Tiêu đề.
     - Mô tả ảnh bìa (cover alt — cho SEO/accessibility): tự lấy = Tiêu đề.
     - Ngày đăng: KHÔNG cho chọn tay. Bài MỚI tự lấy đúng ngày bấm Lưu lần đầu tiên (theo
       múi giờ Việt Nam); bài ĐÃ CÓ mà sửa lại thì GIỮ NGUYÊN ngày đăng gốc ban đầu, không
       tính lại theo lần sửa gần nhất (lần sửa chỉ cập nhật "cập nhật lúc" ở hậu trường,
       không đổi "ngày đăng" hiển thị công khai trên bài).

  3. List danh sách bài viết: trang Admin gọi GAS đọc trực tiếp từ GitHub (Contents API) mỗi
     lần vào danh sách — luôn đúng dữ liệu mới nhất kể cả khi site tĩnh CHƯA build/deploy
     xong, đổi lại tốn 1 lượt gọi GitHub API mỗi lần tải (chấp nhận được ở quy mô nhỏ). KHÔNG
     fetch từ file JSON công khai trên site đã deploy.

  4. Ảnh (áp dụng cho cả ảnh bìa lẫn ảnh chèn trong nội dung):
     - Nén/resize phía trình duyệt (canvas) TRƯỚC khi upload — cạnh dài tối đa 1600px, xuất
       JPEG chất lượng 0.85 (luôn ép về JPEG, không giữ nguyên PNG/khác — vì ảnh bìa đặt tên
       cứng đuôi `.jpg`, xem mục II.1). Ảnh chụp từ điện thoại vài MB giảm còn vài trăm KB,
       giảm hẳn thời gian chờ khi Lưu.
     - Không chặn thao tác khi đang upload: chọn ảnh xong hiển thị NGAY bằng ảnh tạm (xem
       được liền dù chưa upload xong), việc upload thật chạy ngầm; chỉ khi bấm Lưu bài mới
       cần đợi các ảnh upload xong hết.
     - Ảnh chèn trong nội dung cần có caption + alt: alt lấy đúng nội dung caption nếu người
       viết đã nhập; nếu còn để trống/còn là chữ placeholder ("Sửa caption...") thì alt tự
       lấy tạm theo Tiêu đề bài viết — không để trống hẳn, xấu cho SEO.
     - Ngay trước khi Lưu: dọn caption còn nguyên chữ placeholder (xoá hẳn dòng caption đó,
       giữ nguyên khung ảnh) — tuyệt đối không để chữ "Sửa caption..." lọt lên bài viết thật.

III. Đối với sửa bài viết: 
   - Giống viết bài
   - Slug không được phép sửa
   - Ảnh hiển thị lấy từ url raw của github (cả cover lẫn ảnh trong bài viết)
   - Tham khảo dự án mẫu (trithucworld)
   - Slug bất biến phải chặn ở CẢ 2 lớp, thiếu 1 lớp là chưa đủ: khoá cứng ô nhập slug trên
     giao diện (không cho gõ) VÀ server tự so sánh, từ chối lưu nếu phát hiện slug gửi lên
     khác slug cũ của đúng bài đang sửa — chỉ khoá ở giao diện thì ai gọi thẳng hàm lưu vẫn
     đổi được slug.
   - Đường dẫn ảnh raw dùng đúng dạng
     `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<đường-dẫn-file>` — KHÔNG
     dùng domain thật của site để xem trước ảnh trong lúc sửa bài, vì domain thật có thể
     đang ở bản CŨ (site tĩnh build/deploy có độ trễ) nên ảnh mới có thể 404 dù đã có sẵn
     trên GitHub từ trước.
   - Mở form "Bài viết mới" ngay sau khi vừa sửa xong 1 bài khác (nếu giao diện dùng lại
     cùng 1 form, không tạo form mới mỗi lần) phải nhớ MỞ LẠI ô slug (bỏ khoá) — nếu quên,
     tạo bài mới sẽ vô tình bị khoá cứng slug theo trạng thái còn sót của lần sửa trước.

IV. Đối với xoá bài 
   - Chỉ đơn giản là xoá bài viết 
   - Xoá đủ CẢ 2 nơi trong 1 thao tác: file nội dung chi tiết của riêng bài đó, VÀ gỡ đúng
     dòng của bài đó khỏi file danh sách tổng — thiếu 1 trong 2 sẽ để lại rác (file chi tiết
     mồ côi không ai trỏ tới) hoặc lỗi (danh sách còn nhắc tên 1 bài đã không còn file chi
     tiết).
   - Xoá kèm ảnh bìa của bài — xoá đúng file `<slug>-cover.jpg` của bài đang xoá (an toàn vì
     ảnh bìa RIÊNG cho từng bài, không có cơ chế dùng chung/chọn lại ảnh cũ, xem mục II.1
     "Cover" — không đụng ảnh bài khác/trang chủ). Không xoá được nếu ảnh không tồn tại (bài
     tạo trước khi có quy ước này) — bỏ qua êm, không báo lỗi.
   - Bắt buộc có bước xác nhận (popup Huỷ/Xoá — xem mục VII) trước khi xoá thật, vì thao tác
     không thể hoàn tác (Contents API không có "thùng rác").

V. Đối với liên hệ: 
   - Được submit từ UI thông qua trang chính
   - Có thể đánh dấu là đã xem
   - Có thể xoá
   - Có "honeypot": 1 ô ẩn tên `_hp` bằng CSS mà người dùng thật không bao giờ thấy/điền —
     bot tự động điền form thường điền cả ô ẩn, điền là biết ngay là bot, âm thầm không lưu
     (vẫn báo "thành công" cho bot để không lộ ra là đã bị phát hiện, tránh bot đổi cách né).
   - Giới hạn tần suất gửi: 20 giây / lần, tính theo số điện thoại người gửi, để chặn spam
     gửi dồn dập.
   - Vì form nằm trên trang chính (site tĩnh, khác domain/nguồn gốc với chính GAS) nên phải
     gọi bằng cách gửi yêu cầu ngầm (không phải điều hướng cả trang) và cố tình gửi
     `Content-Type: text/plain;charset=utf-8` (không phải `application/json`) để trình duyệt
     không tự ý gửi OPTIONS preflight trước (GAS không xử lý được OPTIONS, sẽ báo lỗi nếu
     trình duyệt tự gửi).
   - Liên hệ báo qua Email, dùng CHUNG 1 địa chỉ nhận với mục VI (Đặt xe) — Script Property
     `NOTIFY_EMAIL` (xem mục X). Dùng chung tài khoản Gmail với OTP đăng nhập (giới hạn 100
     mail/ngày/tài khoản) — quy mô Liên hệ + Đặt xe thực tế còn thấp nên chưa đáng lo; nếu sau
     này lưu lượng tăng cao, cân nhắc tách hẳn 1 tài khoản Gmail khác riêng cho OTP.

VI. Đối với mua hàng 
   - Được mua từ ngoài trang chính
   - Đơn hàng có thể xem chi tiết, đổi status, hoặc xoá.
   - Áp dụng chung honeypot + giới hạn tần suất như mục V (Liên hệ).
   - Gửi qua email cùng với liên hệ — dùng CHUNG 1 Script Property `NOTIFY_EMAIL` (xem mục V
     + mục X), không tách riêng biến cho từng loại form.
   - Khi ghi nhận đơn mới, cần khoá tạm (tránh 2 yêu cầu ghi cùng lúc bị ghi đè lẫn nhau) —
     đặc biệt quan trọng nếu nhiều khách đặt cùng lúc trong khung giờ cao điểm.
   - Giới hạn thực tế không nằm ở "tổng số đơn/ngày" mà ở việc dồn cục nhiều đơn cùng 1 thời
     điểm (vd giờ cao điểm, sự kiện) — nếu thường xuyên gặp tình trạng dồn cục mạnh hoặc vượt
     ngưỡng vài trăm đơn/ngày đều, cần cân nhắc tách phần nhận đơn sang hạ tầng backend khác,
     không cố gồng tiếp trên nền tảng này.


VII. Một số lưu ý: 
   - Tất cả action làm thay đổi trang chính đều có pop-up (không phải alert trình duyệt), xác nhận thay đổi website và thông báo: "Website sẽ được cập nhật sau 2 phút". Người dùng xác nhận thì mới đóng. Pop-up đẹp xuất hiện ở giữa. 
   - Có loading ở button khi website thay đổi. 
   - Có 2 loại pop-up RIÊNG BIỆT, không dùng chung 1 khung cho cả 2 mục đích:
     1) Pop-up XÁC NHẬN (dùng trước hành động không thể hoàn tác, vd Xoá) — 2 nút Huỷ/Xoá,
        hỏi TRƯỚC khi bắt đầu xử lý (chưa loading), người dùng chọn xong mới quyết định có
        chạy hành động hay không.
     2) Pop-up THÔNG BÁO kết quả (Thành công/Lỗi) — 1 nút Đóng duy nhất, hiện SAU khi xử lý
        xong, không tự động biến mất (khác kiểu thông báo "thoáng qua rồi ẩn" ở góc màn
        hình) — bắt người dùng chủ động xác nhận đã đọc, nhất là thông báo quan trọng như
        "cần chờ ít phút để cập nhật".
   - Mọi nút gọi hành động chờ mạng (Lưu, Xoá, Đổi trạng thái...) đều phải tự disable + hiện
     icon xoay trong lúc chờ, tự phục hồi khi xong (kể cả khi lỗi) — tránh người dùng tưởng
     chưa bấm trúng nên bấm lại nhiều lần, gây gửi trùng dữ liệu.
   - Sau khi Lưu/Xoá thành công, danh sách đang hiển thị trong Admin phải TỰ cập nhật ngay
     lập tức từ đúng kết quả vừa trả về — không đợi người dùng tự bấm tải lại hay F5 mới thấy
     đúng, và F5 ngay sau đó cũng không được hiện lại dữ liệu cũ dù chỉ trong chốc lát.
   - Chuyển giữa các tab trong Admin (Bài viết / Liên hệ / Đặt xe / Người dùng...) chỉ là
     hiệu ứng giao diện (ẩn/hiện đúng phần tương ứng) — KHÔNG tải lại toàn trang, KHÔNG gọi
     lại toàn bộ dữ liệu từ đầu mỗi lần bấm tab (xem bug cụ thể ở mục IX).
   - Đăng nhập lần đầu chỉ cần OTP + 1 lượt tải dữ liệu duy nhất là vào thẳng được Admin đầy
     đủ — không thiết kế theo kiểu tải xong 1 phần mới tải tiếp phần khác (nhiều lượt gọi nối
     tiếp làm Admin cảm giác chậm dù bản thân từng lượt gọi không hề chậm).
   - Lần vào Admin SAU (đã từng đăng nhập trước đó, F5 lại hoặc mở lại sau vài ngày) nên hiện
     giao diện gần như ngay lập tức từ dữ liệu đã nhớ sẵn ở trình duyệt, rồi mới âm thầm kiểm
     tra/làm mới lại dữ liệu phía sau — tránh cảm giác phải "tải lại từ đầu" mỗi lần mở, và
     tránh nhấp nháy hiện màn Đăng nhập trước rồi mới nhảy vào Admin dù thật ra vẫn còn đăng
     nhập hợp lệ.
   - ⚠️ ĐI KÈM ĐIỀU TRÊN — BẮT BUỘC: mọi key `localStorage` (trừ token đăng nhập) phải mang
     hậu tố hằng số phiên bản client `CLIENT_BUILD` (khai ở đầu `js.html`), và **PHẢI BUMP
     `CLIENT_BUILD` mỗi lần sửa `app.html` hoặc `js.html`**. Không làm việc này thì cache cũ
     trên máy người dùng sẽ giữ mãi giao diện cũ sau khi deploy, và cách duy nhất để thoát là
     bắt khách tự xoá localStorage — điều KHÔNG được phép xảy ra. Xem bug ⭐ ở mục IX để hiểu
     đầy đủ (đã gặp thật + đã fix).

VIII. Kiến trúc lưu trữ (nơi gì nằm ở đâu, ai đọc/ghi):
   - 1 bảng tính (Google Sheet "Tiến Đức CMS Data", tự tạo lần đầu khi cần, không bắt phải
     tạo tay trước) — TÊN SHEET/CỘT dưới đây cố định, không tự ý đổi:
       + `Users` — cột: email, role. Danh sách tài khoản được phép đăng nhập.
       + `Bookings` — cột: id, created_at, pickup, drop, time, people, phone, status.
         Giá trị `status` hợp lệ: "Mới" / "Đã liên hệ" / "Đã hoàn tất" / "Đã hủy".
       + `Contacts` — cột: id, created_at, name, phone, email, message, status.
         Giá trị `status` hợp lệ: "Mới" / "Đã xử lý".
     Cả 3 sheet chỉ chứa dữ liệu CHỈ Admin cần xem, không hiển thị công khai trên site.
   - GitHub (qua API, KHÔNG phải qua git clone/push tay của người phát triển): nơi chứa nội
     dung sẽ HIỂN THỊ CÔNG KHAI trên site — mỗi lần Lưu/Xoá trong Admin là 1-vài commit ghi
     THẲNG lên nhánh chính, độc lập hoàn toàn với việc người phát triển code đang sửa gì cục
     bộ trên máy (có thể phát sinh lệch nhánh, xem mục IX). ĐƯỜNG DẪN dưới đây cố định — đổi
     tên phải sửa luôn `scripts/build.py`/CI, không đổi tuỳ tiện phía GAS:
       + `data/posts.json` — index tổng mọi bài viết (commit CHỐT, trigger CI build).
       + `data/tin-tuc/<slug>.json` — nội dung chi tiết từng bài.
       + `data/site-config.json` — cấu hình quảng cáo (commit CHỐT, trigger CI build).
       + `html/images/<slug>-cover.jpg` — ảnh bìa RIÊNG của từng bài, tên đặt cứng theo slug
         (xem mục II.1 "Cover" + mục IV) — không phải thư viện ảnh dùng chung.
   - Ảnh publish THẲNG lên GitHub ngay lúc chọn trong lúc soạn bài — không lưu tạm ở nơi
     khác rồi mới chuyển thật lúc bấm Lưu; ảnh đã nằm đúng vị trí site cần ngay từ đầu.
   - Trong 1 thao tác Lưu/Xoá có nhiều file cần ghi (ảnh, nội dung chi tiết, danh sách tổng):
     file "danh sách tổng" LUÔN ghi SAU CÙNG — vì đây là file duy nhất kích hoạt site tự
     build/deploy lại; ghi trước các file khác đảm bảo khi site build lại thì mọi thứ đã sẵn
     sàng đầy đủ, không build nhầm lúc dữ liệu đang dở dang.
   - Site tĩnh tự build + deploy lại mỗi khi file "danh sách tổng" đổi — có độ trễ thực tế
     (thường khoảng 1 phút, tuỳ hạ tầng) mới thấy thay đổi trên site thật, không phải tức
     thì ngay sau khi bấm Lưu — đây là lý do bắt buộc phải có pop-up nhắc ở mục VII.

IX. Check list bug thường gặp
   - Đăng nhập GAS nhưng không vào trang Admin — thường do 1 trong các nguyên nhân sau, cần
     loại trừ từng cái:
       + Bước "xin mã OTP" chỉ kiểm tra email có nằm trong danh sách tài khoản đã đăng ký,
         QUÊN cho phép ngoại lệ với chính account chủ GAS → chủ script tự khoá mình ra khỏi
         hệ thống ngay từ bước xin mã, không bao giờ tới được bước có quyền cao nhất ngầm
         định (dù phần code xử lý quyền phía sau có viết đúng cũng vô ích, vì không bao giờ
         chạy tới đó được). Cách né: kiểm tra "có phải chính account chủ không" SONG SONG với
         kiểm tra danh sách đăng ký, không chỉ dựa vào danh sách.
       + Xác thực OTP thành công, có token, nhưng bước đọc lại quyền từ token trả về rỗng do
         so sánh email sai lệch (chưa đưa về cùng chữ thường, còn khoảng trắng thừa).
       + Token bị lưu sai chỗ hoặc bị xoá nhầm bởi 1 đoạn code khác ngay sau khi vừa lưu.
   - GAS tải trang mỗi khi chuyển tab — do phần chuyển tab đang điều hướng/tải lại cả trang
     (hoặc gọi lại toàn bộ dữ liệu từ đầu) thay vì chỉ ẩn/hiện đúng phần nội dung bằng giao
     diện. Cách né: toàn bộ dữ liệu cần cho Admin chỉ tải 1 lần lúc đăng nhập (hoặc tải riêng
     đúng phần cần khi vào 1 tab lần đầu, rồi giữ nguyên khi quay lại tab đó lần sau), chuyển
     tab chỉ đơn thuần là hiệu ứng giao diện, không kèm theo việc tải lại gì cả.

   - Ảnh hiển thị đúng lúc đang soạn bài nhưng bị mất sau vài giây — do đang hiện tạm bằng
     ảnh local (blob/base64) trong lúc chờ upload thật lên GitHub chạy xong, nhưng code lại
     không đợi upload thành công trước khi cho phép rời form/đóng preview. Cách né: giữ ảnh
     tạm hiển thị liên tục cho tới khi có phản hồi upload thành công thật sự từ server, không
     tự tắt/thay preview sớm.
   - Vừa xoá xong 1 mục, tải lại trang ngay sau đó (trong vài giây) vẫn thấy mục đó còn —
     do màn hình đang hiển thị từ dữ liệu ghi nhớ tạm ở trình duyệt chưa kịp cập nhật lại
     đúng lúc, không phải do việc xoá thật sự thất bại. Cách né: mọi thao tác Xoá phải tự cập
     nhật lại đúng phần cache liên quan NGAY sau khi server xác nhận thành công, không chỉ
     dựa vào lần tải lại kế tiếp.
   - ⭐ **[ĐÃ GẶP VÀ ĐÃ FIX THÀNH CÔNG — 2026-08-26] Sửa code, deploy New version đúng cách,
     F5 Admin nhiều lần nhưng giao diện vẫn y hệt bản CŨ** (thiếu/thừa field so với code hiện
     tại; ở dự án này là form bài viết vẫn hiện 5 field đã bị bỏ).

     **Triệu chứng dễ chẩn đoán sai:** ai cũng nghĩ là "cache trình duyệt" hoặc "deploy sai
     version". KHÔNG PHẢI. Thủ phạm là cache `localStorage` của CHÍNH APP: cơ chế "hiện ngay
     từ cache lúc mở trang" (mục VII) lưu nguyên HTML của `app.html` (biến `appHtml`, trả về
     từ `boot()`) vào `localStorage` với key CỐ ĐỊNH không mang phiên bản (`tienduc_cms_boot_cache`).
     Mỗi lần F5, app đọc đúng key đó ra vẽ TRƯỚC → bản HTML cũ tự lặp lại vô hạn.

     **Vì sao xoá localStorage bằng tay KHÔNG phải cách chữa (đã thử, không hết):** xoá xong,
     vừa mở lại là app ghi đè lại đúng key cũ đó → chỉ sạch được đúng 1 lần load, lần F5 sau
     lại y như trước. Và quan trọng hơn: KHÔNG THỂ yêu cầu khách hàng tự mở DevTools xoá cache.
     ⛔ **TUYỆT ĐỐI KHÔNG "chữa" bug này bằng cách hướng dẫn người dùng xoá localStorage** —
     đó là đẩy lỗi thiết kế của mình sang cho khách, không phải fix.

     **CÁCH FIX ĐÚNG (đã kiểm chứng chạy thật, làm ĐỦ cả 2 lớp):**
       + **Lớp 1 — ĐÓNG DẤU PHIÊN BẢN VÀO KEY CACHE (đây là fix gốc rễ, tự phục hồi 100%):**
         khai 1 hằng số phiên bản client ở đầu `js.html`:
         `const CLIENT_BUILD = "<ngày>-<chữ>";` (dự án này đang dùng `"2026-08-25-a"`), ghép
         vào MỌI key `localStorage` của CMS (`..._boot_cache_<CLIENT_BUILD>`,
         `..._bookings_<CLIENT_BUILD>`...), CỘNG VỚI 1 hàm tự chạy lúc tải script quét sạch mọi
         key cùng tiền tố nhưng khác phiên bản hiện tại (`purgeStaleCaches_`). Nhờ vậy chính
         CODE tự dọn cache cũ trên máy mọi khách, không cần ai can thiệp.
         → **BẮT BUỘC BUMP `CLIENT_BUILD` mỗi lần sửa `app.html` hoặc `js.html`.** Quên bump =
         dính lại đúng bug này.
         → RIÊNG key token đăng nhập KHÔNG mang phiên bản — không được bắt người dùng đăng nhập
         lại chỉ vì ta sửa giao diện.
         → Nên `console.log(CLIENT_BUILD)` lúc khởi động: mở Console thấy đúng phiên bản mới là
         biết chắc đang chạy bản mới, khỏi phải đoán "đã deploy chưa".
       + **Lớp 2 — revalidate ngầm tự vẽ lại giao diện (phòng thủ khi quên bump lớp 1):** so
         `appHtml` mới nhận với bản đang dùng; khác thì vẽ lại DOM (`innerHTML`) + khởi tạo lại
         mọi thứ phụ thuộc DOM cũ (TinyMCE: reset biến trạng thái init vì ô nhập cũ đã bị thay)
         + giữ nguyên đúng tab đang xem; KHÔNG vẽ đè khi người dùng đang mở form soạn/sửa (có
         thể đang gõ dở).

     **CÁCH TEST BẮT BUỘC trước khi báo xong:** F5 Admin trong lúc localStorage vẫn còn cache
     CŨ (KHÔNG xoá tay gì cả) → giao diện phải tự đúng ngay lần F5 đầu tiên. Nếu phải xoá tay
     mới đúng thì CHƯA fix xong.

     **Mẹo debug:** localStorage của web app GAS nằm ở origin `*.googleusercontent.com` (dạng
     `https://n-xxxxx-script.googleusercontent.com`), KHÔNG phải `script.google.com` — trong
     DevTools → Application → Local Storage phải chọn đúng origin đó, chọn sai sẽ thấy trống
     trơn rồi kết luận nhầm "không phải do cache" và mò sai hướng cả buổi.

   - Hàm chạy ngầm nuốt lỗi hoàn toàn (`.catch(() => {})`) → khi nó throw giữa chừng (vd truy
     cập 1 element không tồn tại trong `appHtml` cũ), giao diện kẹt ở trạng thái sai mà Console
     SẠCH TRƠN, không còn dấu vết nào để lần ra nguyên nhân. Chính điều này khiến bug ⭐ ở trên
     mất hàng giờ thay vì 5 phút. Cách né: không hiện lỗi lên UI (đúng, vì chạy ngầm, không nên
     làm phiền người đang dùng) NHƯNG luôn `console.warn`/`console.error` lại.
   - TinyMCE "không chạy" (mở tab soạn bài mà ô nội dung trống trơn/không nhập được, hoặc cao
     0px) dù không có lỗi gì trong Console — do khởi tạo TinyMCE (`tinymce.init`) NGAY LÚC
     `boot()` xong, trong khi tab chứa ô soạn bài vẫn đang `display:none` (chỉ tab danh sách
     đang hiện). TinyMCE đo kích thước vùng chứa NGAY LÚC init; init trên phần tử đang ẩn thì
     editor bị tính cao 0px và KHÔNG tự đo lại dù sau đó tab có hiện ra thật (`display:block`)
     — nhìn giống hệt "không chạy" dù không hề báo lỗi. Cách né: chỉ gọi `tinymce.init` SAU
     KHI tab chứa nó đã thật sự hiện ra (`display:block`) trong DOM, không gọi lúc boot lúc
     tab đó còn ẩn — vd gọi ngay trong hàm mở form soạn bài, ngay sau dòng set hiện tab (nhớ
     tự nhớ đã init rồi để không init lặp lại mỗi lần mở form).

X. Script Properties (biến cấu hình lưu trong Project Settings > Script Properties của GAS) —
   TÊN BIẾN dưới đây CỐ ĐỊNH, không tự ý đổi tên/thêm/bớt nếu không được yêu cầu rõ ràng. GIÁ
   TRỊ do người deploy tự điền riêng theo từng dự án, không hard-code trong code:
   - `GITHUB_TOKEN`, `GITHUB_OWNER`, `GITHUB_REPO`, `GITHUB_BRANCH` — bắt buộc.
   - `NOTIFY_EMAIL` — tuỳ chọn, để trống thì mặc định `Tienductransport@gmail.com`. Dùng
     CHUNG 1 địa chỉ cho CẢ Đặt xe lẫn Liên hệ (xem mục V/VI), không tách riêng biến theo
     từng loại form.
   - `SPREADSHEET_ID` — KHÔNG cần tự điền, code tự tạo Sheet lần đầu chạy và tự lưu lại.