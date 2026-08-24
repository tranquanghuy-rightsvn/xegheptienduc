#!/usr/bin/env python3
"""
Build site tĩnh phần Tin tức từ data/ + templates/ — chạy bởi GitHub Actions mỗi khi
data/posts.json đổi (commit chốt của CMS, xem architecture.md mục "trigger CI").

Không dùng thư viện ngoài (chỉ stdlib) — chạy được cả trên máy dev lẫn CI runner.

  data/posts.json            -> index nhẹ mọi bài (CMS ghi khi Lưu/Xoá)
  data/tin-tuc/<slug>.json   -> nội dung đầy đủ 1 bài
  templates/post.html        -> khung 1 trang bài viết (KHÔNG generate lại, sửa tay ở đây)
  templates/tin-tuc-index.html -> khung trang danh sách

Ghi ra:
  html/tin-tuc/<slug>.html   -> ghi đè mỗi lần build
  html/tin-tuc/index.html    -> ghi đè mỗi lần build
  html/sitemap.xml           -> vá lại đúng danh sách URL /tin-tuc/*
Dọn:
  html/tin-tuc/*.html không còn trong data/posts.json (bài đã xoá qua CMS) -> xoá file
"""
import html
import json
import os
import re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")
POSTS_DATA_DIR = os.path.join(DATA_DIR, "tin-tuc")
TEMPLATES_DIR = os.path.join(BASE, "templates")
HTML_DIR = os.path.join(BASE, "html")
NEWS_HTML_DIR = os.path.join(HTML_DIR, "tin-tuc")
SITEMAP_PATH = os.path.join(HTML_DIR, "sitemap.xml")

SITE_URL = "https://tienductransport.vn"
MAX_RELATED = 3


def esc(s):
    return html.escape(str(s or ""), quote=True)


def json_ld(obj):
    """json.dumps an toàn để nhúng trong <script type="application/ld+json">: nếu chuỗi
    JSON chứa literal "</script" (vd tiêu đề bài viết có ai đó gõ "</script>"), trình duyệt
    (HTML parser, không phải JSON parser) sẽ đóng thẻ script bao ngoài SỚM tại đó, biến phần
    JSON còn lại thành HTML thô — chèn được script/markup tuỳ ý (XSS thật, đã test tái hiện
    được). Escape "/" trong "</script" thành "\\/" để phá literal đó, JSON vẫn hợp lệ (\\/ là
    escape hợp lệ cho "/") và trình duyệt không nhận ra thẻ đóng nữa."""
    return json.dumps(obj, ensure_ascii=False, indent=2).replace("</script", "<\\/script")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_template(name):
    with open(os.path.join(TEMPLATES_DIR, name), "r", encoding="utf-8") as f:
        return f.read()


def date_display(iso_date):
    # "2026-08-08" -> "08/08/2026"
    y, m, d = iso_date.split("-")
    return f"{d}/{m}/{y}"


def render_placeholders(tpl, mapping):
    # re.sub thay thế trong 1 lượt quét duy nhất trên chuỗi TEMPLATE GỐC, không quét lại
    # phần vừa được chèn vào - khác với gọi .replace() tuần tự từng key một (sẽ có bug thật:
    # nếu nội dung bài viết do editor nhập tự do vô tình chứa đúng literal "{{CTA_TITLE}}",
    # cách .replace() tuần tự sẽ thay nhầm nó ở bước xử lý CTA_TITLE sau đó, dù đó là text
    # bình thường trong content_html, không phải placeholder thật của template).
    pattern = re.compile(r"\{\{(\w+)\}\}")
    return pattern.sub(lambda m: mapping.get(m.group(1), m.group(0)), tpl)


def build_related_cards(all_posts, current_slug):
    others = [p for p in all_posts if p["slug"] != current_slug][:MAX_RELATED]
    cards = []
    for p in others:
        cards.append(f"""          <li class="news-card">
            <a href="{esc(p['slug'])}.html">
              <img class="news-card__img" src="../images/{esc(p['cover'])}" alt="{esc(p['cover_alt'])}" width="800" height="450" loading="lazy">
            </a>
            <div class="news-card__body">
              <span class="news-card__meta">{esc(p['category'])}</span>
              <h2 class="news-card__title"><a href="{esc(p['slug'])}.html">{esc(p['title'])}</a></h2>
              <a class="news-card__link" href="{esc(p['slug'])}.html">Đọc tiếp <svg class="ic"><use href="#i-arrow"/></svg></a>
            </div>
          </li>""")
    return "\n".join(cards)


def build_post_cards(all_posts):
    cards = []
    for p in all_posts:
        cards.append(f"""      <li class="news-card">
        <a href="{esc(p['slug'])}.html">
          <img class="news-card__img" src="../images/{esc(p['cover'])}" alt="{esc(p['cover_alt'])}" width="800" height="450" loading="lazy">
        </a>
        <div class="news-card__body">
          <span class="news-card__meta">{esc(p['category'])} · {date_display(p['date'])}</span>
          <h2 class="news-card__title"><a href="{esc(p['slug'])}.html">{esc(p['title'])}</a></h2>
          <p class="news-card__desc">{esc(p['excerpt'])}</p>
          <a class="news-card__link" href="{esc(p['slug'])}.html">Đọc tiếp <svg class="ic"><use href="#i-arrow"/></svg></a>
        </div>
      </li>""")
    return "\n\n".join(cards)


def render_post_page(tpl, post, all_posts):
    slug = post["slug"]
    canonical = f"{SITE_URL}/tin-tuc/{slug}.html"
    og_image = f"{SITE_URL}/images/{post['cover']}"

    jsonld_article = json_ld({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": post["title"],
        "description": post["description"],
        "image": og_image,
        "datePublished": post["date"],
        "dateModified": post.get("updated_date", post["date"]),
        "author": {"@type": "Organization", "name": "Tiến Đức", "url": f"{SITE_URL}/"},
        "publisher": {
            "@type": "Organization",
            "name": "Tiến Đức",
            "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/images/logo.png"},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
    })

    jsonld_breadcrumb = json_ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Tin tức", "item": f"{SITE_URL}/tin-tuc/"},
            {"@type": "ListItem", "position": 3, "name": post["breadcrumb"], "item": canonical},
        ],
    })

    mapping = {
        "SEO_TITLE": esc(post["seo_title"]),
        "DESCRIPTION": esc(post["description"]),
        "CANONICAL_URL": canonical,
        "OG_IMAGE": og_image,
        "JSONLD_ARTICLE": jsonld_article,
        "JSONLD_BREADCRUMB": jsonld_breadcrumb,
        "BREADCRUMB": esc(post["breadcrumb"]),
        "TITLE": esc(post["title"]),
        "CATEGORY": esc(post["category"]),
        "DATE_DISPLAY": date_display(post["date"]),
        "COVER": esc(post["cover"]),
        "COVER_ALT": esc(post["cover_alt"]),
        "CONTENT_HTML": post["content_html"],  # đã là HTML thật, không escape
        "CTA_TITLE": esc(post["cta_title"]),
        "CTA_DESC": esc(post["cta_desc"]),
        "RELATED_CARDS": build_related_cards(all_posts, slug),
    }
    return render_placeholders(tpl, mapping)


def render_index_page(tpl, all_posts):
    return render_placeholders(tpl, {"POST_CARDS": build_post_cards(all_posts)})


def update_sitemap(all_posts):
    if not os.path.exists(SITEMAP_PATH):
        print("  (sitemap.xml không tồn tại, bỏ qua bước vá)")
        return
    with open(SITEMAP_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Xoá mọi <url> trỏ tới tin-tuc/*.html hiện có (giữ nguyên / , /lien-he/ , /tin-tuc/)
    content = re.sub(
        r'[ \t]*<url>\s*<loc>[^<]*?/tin-tuc/[^/]+\.html</loc>.*?</url>\s*\n?',
        "",
        content,
        flags=re.S,
    )
    content = content.rstrip("\n") + "\n"

    entries = []
    for p in all_posts:
        entries.append(
            "  <url>\n"
            f"    <loc>{SITE_URL}/tin-tuc/{p['slug']}.html</loc>\n"
            f"    <lastmod>{p.get('updated_date', p['date'])}</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n"
            "    <priority>0.6</priority>\n"
            "  </url>\n"
        )
    content = content.replace("</urlset>\n", "").rstrip("\n") + "\n" + "".join(entries) + "</urlset>\n"
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(content)


def clean_orphan_html(valid_slugs):
    if not os.path.isdir(NEWS_HTML_DIR):
        return
    for name in os.listdir(NEWS_HTML_DIR):
        if not name.endswith(".html"):
            continue
        if name == "index.html":
            continue
        slug = name[:-5]
        if slug not in valid_slugs:
            path = os.path.join(NEWS_HTML_DIR, name)
            os.remove(path)
            print("  Đã xoá file mồ côi:", path)


def main():
    posts_index = load_json(os.path.join(DATA_DIR, "posts.json"))
    posts_index = sorted(posts_index, key=lambda r: r["date"], reverse=True)

    post_tpl = read_template("post.html")
    index_tpl = read_template("tin-tuc-index.html")

    os.makedirs(NEWS_HTML_DIR, exist_ok=True)

    valid_slugs = set()
    for p in posts_index:
        slug = p["slug"]
        valid_slugs.add(slug)
        full = load_json(os.path.join(POSTS_DATA_DIR, slug + ".json"))
        out_html = render_post_page(post_tpl, full, posts_index)
        out_path = os.path.join(NEWS_HTML_DIR, slug + ".html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out_html)
        print("  Đã build:", out_path)

    index_html = render_index_page(index_tpl, posts_index)
    with open(os.path.join(NEWS_HTML_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("  Đã build:", os.path.join(NEWS_HTML_DIR, "index.html"))

    clean_orphan_html(valid_slugs)
    update_sitemap(posts_index)
    print(f"Build xong: {len(posts_index)} bài tin tức.")


if __name__ == "__main__":
    main()
