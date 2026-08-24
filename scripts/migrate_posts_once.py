#!/usr/bin/env python3
"""
Script scaffold CHẠY MỘT LẦN: đưa 4 bài tin tức viết tay hiện có vào data/ để CMS quản lý
từ đây về sau. Không chạy lại (sẽ ghi đè data/ nếu chạy lại — dữ liệu sau này chỉnh qua CMS
mới là nguồn chân lý, không phải file HTML gốc nữa).
"""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")
POSTS_DIR = os.path.join(DATA_DIR, "tin-tuc")

POSTS = [
    {
        "slug": "cam-nang-du-lich-ha-long-cat-ba",
        "title": "Cẩm Nang Du Lịch Hạ Long – Cát Bà Cho Người Mới Đi Lần Đầu",
        "seo_title": "Cẩm Nang Du Lịch Hạ Long – Cát Bà | Tiến Đức",
        "description": "Cách di chuyển giữa Hạ Long và Cát Bà, những điểm đến không thể bỏ lỡ và gợi ý lịch trình cho người mới đi lần đầu. Tổng hợp bởi Tiến Đức.",
        "excerpt": "Từ cách di chuyển giữa hai điểm đến, đến những nơi không thể bỏ lỡ – tổng hợp kinh nghiệm giúp chuyến đi Hạ Long – Cát Bà của bạn trọn vẹn hơn.",
        "category": "Du lịch",
        "date": "2026-08-08",
        "cover": "svc-5-du-lich.jpg",
        "cover_alt": "Du lịch Hạ Long - Cát Bà",
        "breadcrumb": "Cẩm nang du lịch Hạ Long – Cát Bà",
        "cta_title": "Lên kế hoạch cho chuyến đi Hạ Long – Cát Bà?",
        "cta_desc": "Liên hệ Tiến Đức để được tư vấn lịch trình và đặt xe đưa đón phù hợp.",
        "content_html": """<p>Hạ Long và Cát Bà là hai điểm đến nằm không xa nhau nhưng lại mang hai màu sắc rất khác biệt: một bên là thành phố du lịch sầm uất với vịnh di sản nổi tiếng thế giới, một bên là đảo ngọc hoang sơ với bãi biển và rừng quốc gia. Với nhiều du khách lần đầu đến khu vực này, việc kết hợp cả hai điểm trong một chuyến đi là lựa chọn lý tưởng. Dưới đây là những kinh nghiệm giúp hành trình của bạn thuận lợi hơn.</p>

        <h2>Di chuyển giữa Hạ Long và Cát Bà</h2>
        <p>Từ trung tâm Hạ Long, du khách có thể di chuyển đến Cát Bà bằng cách kết hợp xe và phà/cao tốc qua Cái Viềng hoặc Gia Luận, tổng thời gian khoảng 1,5–2 giờ tùy thời điểm. Nếu đi theo nhóm hoặc gia đình có hành lý cồng kềnh, đặt xe riêng hoặc xe ghép đưa đón tận nơi sẽ tiện hơn nhiều so với việc tự di chuyển qua nhiều chặng.</p>

        <h2>Những điểm đến không thể bỏ lỡ</h2>
        <ul>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Vịnh Hạ Long:</strong> tham quan bằng du thuyền, ngắm hệ thống hang động và đảo đá vôi được UNESCO công nhận là di sản thiên nhiên thế giới.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Bãi Cháy:</strong> khu vực trung tâm với nhiều nhà hàng, khách sạn và các hoạt động về đêm sôi động.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Vườn quốc gia Cát Bà:</strong> phù hợp cho du khách yêu thích trekking, khám phá thiên nhiên hoang sơ.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Vịnh Lan Hạ:</strong> ít đông đúc hơn vịnh Hạ Long, nước trong xanh, thích hợp chèo kayak hoặc tắm biển.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Thị trấn Cát Bà:</strong> nhiều hải sản tươi ngon với giá hợp lý, thích hợp nghỉ ngơi buổi tối.</span></li>
        </ul>

        <h2>Gợi ý lịch trình 2 ngày 1 đêm</h2>
        <p>Ngày đầu tiên nên dành trọn cho vịnh Hạ Long: tham quan bằng du thuyền, khám phá hang động và nghỉ đêm tại Bãi Cháy hoặc trên tàu. Sáng hôm sau di chuyển sang Cát Bà, dành buổi chiều khám phá vườn quốc gia hoặc vịnh Lan Hạ trước khi quay về. Với lịch trình dày như vậy, việc chủ động được xe đưa đón đúng giờ giữa các điểm là yếu tố quan trọng để không bỏ lỡ hoạt động nào.</p>

        <p>Nếu Quý khách cần xe đưa đón giữa Hạ Long, Cát Bà, sân bay Cát Bi hoặc các điểm tham quan, Tiến Đức luôn sẵn sàng hỗ trợ với đội xe điện đời mới, tài xế thông thạo địa bàn và có thể linh hoạt theo lịch trình riêng của từng đoàn khách.</p>""",
    },
    {
        "slug": "kinh-nghiem-di-xe-ghep-ha-long-hai-phong",
        "title": "Kinh Nghiệm Chọn Xe Ghép Hạ Long – Hải Phòng Tiết Kiệm Và An Toàn",
        "seo_title": "Kinh Nghiệm Chọn Xe Ghép Hạ Long – Hải Phòng | Tiến Đức",
        "description": "Xe ghép là lựa chọn tiết kiệm cho hành trình Hạ Long - Hải Phòng, nhưng chọn đúng nhà xe mới đảm bảo an toàn, đúng giờ. Tiến Đức chia sẻ kinh nghiệm chọn xe ghép uy tín.",
        "excerpt": "Xe ghép là lựa chọn tiết kiệm cho hành trình Hạ Long – Hải Phòng, nhưng chọn đúng nhà xe mới đảm bảo an toàn, đúng giờ. Cùng Tiến Đức điểm qua những tiêu chí quan trọng nhất.",
        "category": "Kinh nghiệm di chuyển",
        "date": "2026-08-20",
        "cover": "svc-1-xe-ghep-tien-chuyen.jpg",
        "cover_alt": "Xe ghép Hạ Long - Hải Phòng của Tiến Đức",
        "breadcrumb": "Kinh nghiệm chọn xe ghép Hạ Long – Hải Phòng",
        "cta_title": "Cần đặt xe ghép Hạ Long – Hải Phòng?",
        "cta_desc": "Gọi ngay hotline hoặc nhắn Zalo, Tiến Đức hỗ trợ tư vấn và giữ chỗ trong vài phút.",
        "content_html": """<p>Tuyến Hạ Long – Hải Phòng mỗi ngày đón hàng trăm lượt khách đi công tác, thăm thân, du lịch hoặc ra sân bay Cát Bi. Với những ai đi một mình hoặc nhóm nhỏ, xe ghép luôn là lựa chọn được cân nhắc đầu tiên vì chi phí hợp lý mà vẫn được đón trả tận nơi thay vì phải ra bến xe. Tuy nhiên, không phải nhà xe ghép nào cũng đảm bảo chất lượng như quảng cáo. Dưới đây là những kinh nghiệm Tiến Đức đúc kết được sau nhiều năm phục vụ tuyến này.</p>

        <h2>Vì sao nên chọn xe ghép thay vì xe khách thường?</h2>
        <p>So với xe khách chạy tuyến cố định, xe ghép linh hoạt hơn hẳn về điểm đón – điểm trả: tài xế có thể đón tận nhà, khách sạn hoặc bất kỳ địa điểm nào thuận tiện trên cung đường. Thời gian di chuyển cũng thường ngắn hơn vì xe ghép ưu tiên đi thẳng, ít dừng đỗ dọc đường như xe khách tuyến. Với quãng đường Hạ Long – Hải Phòng, hành trình bằng xe ghép chỉ mất khoảng hơn 1 giờ nếu không kẹt xe.</p>

        <h2>Những tiêu chí chọn nhà xe ghép uy tín</h2>
        <p>Không phải cứ giá rẻ là nên đặt. Trước khi quyết định, Quý khách nên kiểm tra một vài yếu tố sau để tránh gặp phải xe không đảm bảo hoặc bị "nhồi khách":</p>
        <ul>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Xe đời mới, có bảo dưỡng định kỳ:</strong> hạn chế rủi ro hỏng hóc giữa đường, đặc biệt vào mùa cao điểm.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Giá cước công khai, không phát sinh:</strong> nên hỏi rõ giá trước khi lên xe, tránh tình trạng báo giá một đằng thu tiền một nẻo.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Tài xế có kinh nghiệm, lịch sự:</strong> quen đường, xử lý tình huống tốt và tôn trọng giờ hẹn của khách.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Hỗ trợ đặt xe qua nhiều kênh:</strong> hotline, Zalo hoặc website giúp Quý khách chủ động thời gian, dễ dàng đổi lịch khi cần.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Có phản hồi, đánh giá thực tế từ khách cũ:</strong> đây là căn cứ đáng tin cậy hơn nhiều so với quảng cáo.</span></li>
        </ul>

        <h2>Nên đặt xe trước bao lâu?</h2>
        <p>Với ngày thường, Quý khách nên đặt trước ít nhất 1–2 giờ để nhà xe sắp xếp hành trình phù hợp. Vào dịp lễ, Tết hoặc cuối tuần đông khách, nên đặt trước từ 1 ngày để chắc chắn có xe và giữ được khung giờ đẹp, tránh phải chờ ghép thêm khách hoặc đổi giờ đón.</p>

        <p>Tiến Đức hiện khai thác tuyến Hạ Long – Hải Phòng bằng đội xe điện VinFast đời mới, đón trả tận nơi và hỗ trợ đặt xe 24/7 qua hotline hoặc Zalo. Nếu Quý khách đang cần tìm một nhà xe ghép uy tín cho hành trình sắp tới, đừng ngần ngại liên hệ để được tư vấn giờ đón phù hợp nhất.</p>""",
    },
    {
        "slug": "luu-y-dat-xe-san-bay-cat-bi",
        "title": "5 Lưu Ý Khi Đặt Xe Đưa Đón Sân Bay Cát Bi",
        "seo_title": "5 Lưu Ý Khi Đặt Xe Đưa Đón Sân Bay Cát Bi | Tiến Đức",
        "description": "Đặt xe trước bao lâu, chọn giờ đón thế nào để không lỡ chuyến bay? Tiến Đức chia sẻ 5 lưu ý giúp hành trình ra/vào sân bay Cát Bi suôn sẻ.",
        "excerpt": "Đặt xe trước bao lâu, chọn giờ đón thế nào để không lỡ chuyến bay? Tiến Đức chia sẻ 5 lưu ý giúp hành trình ra/vào sân bay Cát Bi suôn sẻ.",
        "category": "Đưa đón sân bay",
        "date": "2026-08-01",
        "cover": "svc-3-dua-don-san-bay.jpg",
        "cover_alt": "Xe đưa đón sân bay Cát Bi của Tiến Đức",
        "breadcrumb": "5 lưu ý khi đặt xe đưa đón sân bay Cát Bi",
        "cta_title": "Cần đưa đón sân bay Cát Bi?",
        "cta_desc": "Đặt xe trước để giữ khung giờ đẹp, Tiến Đức hỗ trợ theo dõi giờ bay 24/7.",
        "content_html": """<p>Đưa đón sân bay là một trong những dịch vụ được khách hàng sử dụng nhiều nhất tại Tiến Đức, đặc biệt với khách từ Hạ Long, Cẩm Phả cần ra sân bay Cát Bi (Hải Phòng) để bay các chặng nội địa hoặc quốc tế. Để chuyến đi không bị động, dưới đây là 5 lưu ý quan trọng khi đặt xe.</p>

        <h2>1. Đặt xe trước ít nhất 3–4 giờ bay</h2>
        <p>Với chặng Hạ Long – sân bay Cát Bi, thời gian di chuyển trung bình khoảng 1–1,5 giờ tùy điểm đón. Quý khách nên đặt xe sao cho có mặt tại sân bay trước giờ bay ít nhất 2 giờ với chuyến nội địa, cộng thêm thời gian di chuyển và dự phòng kẹt xe. Vào giờ cao điểm hoặc mùa du lịch, nên đặt xe trước 1 ngày để chắc chắn có xe đúng khung giờ mong muốn.</p>

        <h2>2. Cung cấp đúng thông tin chuyến bay</h2>
        <p>Khi đặt xe, Quý khách nên cung cấp giờ bay, mã chuyến (nếu có) và số lượng hành lý để nhà xe sắp xếp loại xe và thời gian đón phù hợp. Điều này đặc biệt quan trọng nếu đi đông người hoặc mang theo hành lý cồng kềnh, cần xe 7 chỗ hoặc lớn hơn.</p>

        <h2>3. Xác nhận lại điểm đón trước giờ khởi hành</h2>
        <p>Nên nhắn tin hoặc gọi lại xác nhận với nhà xe trước 30–60 phút để đảm bảo tài xế đến đúng nơi, đúng giờ, tránh trường hợp thay đổi lịch trình đột xuất mà không kịp thông báo.</p>

        <h2>4. Ưu tiên xe có theo dõi chuyến bay hoặc hỗ trợ đổi giờ</h2>
        <p>Với chuyến bay đến, nếu máy bay delay hoặc đến sớm hơn dự kiến, nên chọn nhà xe có thể linh hoạt điều chỉnh giờ đón thay vì cố định cứng nhắc, giúp Quý khách không phải chờ đợi lâu tại sân bay.</p>

        <h2>5. Kiểm tra giá cước trọn gói trước khi đặt</h2>
        <p>Giá đưa đón sân bay nên được báo rõ ràng theo tuyến, tránh tình trạng phát sinh phụ phí giờ đêm, chờ đợi hoặc hành lý mà không thông báo trước. Quý khách có thể tham khảo bảng giá công khai trên website hoặc hỏi trực tiếp qua hotline trước khi xác nhận đặt xe.</p>

        <ul>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Đặt trước:</strong> tối thiểu 3–4 giờ trước giờ bay, sớm hơn vào cao điểm.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Cung cấp thông tin chuyến bay:</strong> giờ bay, số lượng khách và hành lý.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Xác nhận lại điểm đón:</strong> trước giờ khởi hành 30–60 phút.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Chọn nhà xe linh hoạt:</strong> hỗ trợ đổi giờ khi chuyến bay delay.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Hỏi rõ giá trọn gói:</strong> tránh phát sinh phụ phí không thông báo trước.</span></li>
        </ul>

        <p>Tiến Đức nhận đưa đón sân bay Cát Bi 24/7, hỗ trợ theo dõi giờ bay và linh hoạt điều chỉnh lịch đón trả theo tình hình thực tế, giúp Quý khách yên tâm cho mỗi chuyến đi.</p>""",
    },
    {
        "slug": "xe-dien-vinfast-va-xe-xang-khac-nhau-the-nao",
        "title": "Xe Điện VinFast Có Gì Khác So Với Xe Xăng Truyền Thống?",
        "seo_title": "Xe Điện VinFast Có Gì Khác So Với Xe Xăng? | Tiến Đức",
        "description": "Không mùi xăng dầu, vận hành êm ái và chi phí thấp hơn - vì sao Tiến Đức chuyển đổi đội xe sang VinFast. Tìm hiểu sự khác biệt giữa xe điện và xe xăng truyền thống.",
        "excerpt": "Không mùi xăng dầu, vận hành êm ái và chi phí vận hành thấp hơn – đây là những lý do Tiến Đức chuyển đổi đội xe sang VinFast. Cùng tìm hiểu chi tiết.",
        "category": "Xe điện & Công nghệ",
        "date": "2026-08-15",
        "cover": "hero-banner.jpg",
        "cover_alt": "Xe điện VinFast khác gì xe xăng truyền thống",
        "breadcrumb": "Xe điện VinFast khác gì xe xăng?",
        "cta_title": "Trải nghiệm xe điện VinFast cùng Tiến Đức",
        "cta_desc": "Đặt xe ngay để trải nghiệm hành trình êm ái, hiện đại với đội xe VinFast của Tiến Đức.",
        "content_html": """<p>Vài năm trở lại đây, xe điện dần trở thành lựa chọn quen thuộc trong vận tải hành khách, và Tiến Đức cũng không nằm ngoài xu hướng đó khi đưa VinFast VF 5 và Limo Green vào khai thác tuyến Hạ Long – Hải Phòng. Nhiều khách hàng thắc mắc xe điện thực sự khác gì so với xe xăng truyền thống, và liệu có đáng để trải nghiệm không. Bài viết này sẽ giải đáp những khác biệt rõ rệt nhất.</p>

        <h2>Vận hành êm ái, không mùi xăng dầu</h2>
        <p>Khác với động cơ đốt trong luôn có độ rung và tiếng ồn nhất định, xe điện vận hành gần như im lặng, không có mùi xăng dầu phả vào cabin. Đây là điểm cộng lớn với hành khách dễ say xe hoặc nhạy cảm với mùi, đặc biệt trên những chặng đường dài như Hạ Long – Hải Phòng.</p>

        <h2>Tăng tốc mượt, phù hợp di chuyển trong đô thị lẫn đường dài</h2>
        <p>Động cơ điện cho phản ứng ga tức thời, xe tăng tốc mượt mà ngay từ vòng tua đầu tiên mà không bị giật cục như hộp số xe xăng. Nhờ vậy, hành trình cảm giác êm hơn dù đi qua đoạn đường đông xe hay cao tốc.</p>

        <h2>Chi phí vận hành và bảo dưỡng khác biệt</h2>
        <p>Xe điện không cần thay dầu nhớt, lọc gió, bugi định kỳ như xe xăng, giúp giảm đáng kể chi phí bảo dưỡng về lâu dài. Chi phí "nhiên liệu" (sạc điện) cũng thấp hơn nhiều so với đổ xăng cho quãng đường tương đương – đây là lý do các hãng xe dịch vụ, trong đó có Tiến Đức, dần chuyển đổi đội xe.</p>

        <p>Một vài lợi ích khác của việc lựa chọn xe điện cho hành trình của Quý khách:</p>
        <ul>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Thân thiện với môi trường:</strong> không phát thải khí trực tiếp, phù hợp xu hướng du lịch xanh tại Hạ Long.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Nội thất hiện đại:</strong> các dòng VinFast được trang bị màn hình, cổng sạc, điều hòa tự động mang lại trải nghiệm cao cấp hơn.</span></li>
          <li><svg class="ic"><use href="#i-check"/></svg><span><strong>Độ ồn thấp:</strong> phù hợp cho khách cần nghỉ ngơi, làm việc trong lúc di chuyển.</span></li>
        </ul>

        <p>Với đội xe VinFast VF 5 và Limo Green, Tiến Đức mong muốn mang đến trải nghiệm di chuyển hiện đại, êm ái và an toàn hơn cho mọi hành trình Hạ Long – Hải Phòng và các tuyến lân cận.</p>""",
    },
]

os.makedirs(POSTS_DIR, exist_ok=True)

index = []
for i, p in enumerate(POSTS):
    record = dict(p)
    record["id"] = p["slug"]
    record["updated_at"] = p["date"] + "T00:00:00Z"
    with open(os.path.join(POSTS_DIR, p["slug"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        f.write("\n")
    index.append({
        "id": record["id"],
        "slug": p["slug"],
        "title": p["title"],
        "excerpt": p["excerpt"],
        "category": p["category"],
        "date": p["date"],
        "cover": p["cover"],
        "cover_alt": p["cover_alt"],
        "updated_at": record["updated_at"],
    })

# posts.json sắp theo ngày mới nhất trước (giống thứ tự hiện có trên site)
index.sort(key=lambda r: r["date"], reverse=True)

with open(os.path.join(DATA_DIR, "posts.json"), "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
    f.write("\n")

print("Da tao", len(POSTS), "bai trong data/tin-tuc/ + data/posts.json")
