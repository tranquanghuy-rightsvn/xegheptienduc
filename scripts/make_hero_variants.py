"""Cắt 1 ảnh gốc thành các biến thể banner cho trang dịch vụ (srcset).

Dùng:  python3 scripts/make_hero_variants.py <ảnh-gốc> <tên> [cx cy] [mcx mcy]
  vd:  python3 scripts/make_hero_variants.py ~/Desktop/hai-phong.jpg xe-ghep-hai-phong

  cx cy   : tâm vùng cắt desktop (0..1), mặc định 0.5 0.5
  mcx mcy : tâm vùng cắt mobile  (0..1), mặc định bằng desktop

Sinh vào html/images/:
  <tên>-{960,1280,1752}.webp         banner desktop, tỉ lệ 1752x598
  <tên>-m-{480,640,860}.webp         banner mobile,  tỉ lệ 860x506
  <tên>-og.jpg                       1200x630 cho Facebook/Zalo (giữ JPG: Zalo không đọc webp)
"""
import os, sys
from PIL import Image, ImageOps

IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "html", "images")
DESKTOP = (1752 / 598, [960, 1280, 1752])
MOBILE = (860 / 506, [480, 640, 860])


def crop(im, ratio, cx, cy):
    W, H = im.size
    w, h = (int(H * ratio), H) if W / H > ratio else (W, int(W / ratio))
    x = int(min(max(cx * W - w / 2, 0), W - w))
    y = int(min(max(cy * H - h / 2, 0), H - h))
    return im.crop((x, y, x + w, y + h))


def save(im, path_noext):
    im.save(path_noext + ".webp", quality=72, method=6)


def main():
    src, name = sys.argv[1], sys.argv[2]
    nums = [float(v) for v in sys.argv[3:]]
    cx, cy = nums[0:2] if len(nums) >= 2 else (0.5, 0.5)
    mcx, mcy = nums[2:4] if len(nums) >= 4 else (cx, cy)

    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    print("nguồn:", im.size)

    ratio, widths = DESKTOP
    d = crop(im, ratio, cx, cy)
    for w in widths:
        save(d.resize((w, round(w / ratio)), Image.LANCZOS), os.path.join(IMG_DIR, f"{name}-{w}"))

    ratio, widths = MOBILE
    m = crop(im, ratio, mcx, mcy)
    for w in widths:
        save(m.resize((w, round(w / ratio)), Image.LANCZOS), os.path.join(IMG_DIR, f"{name}-m-{w}"))

    og = crop(im, 1200 / 630, cx, cy).resize((1200, 630), Image.LANCZOS)
    og.save(os.path.join(IMG_DIR, f"{name}-og.jpg"), quality=82, optimize=True, progressive=True)

    if d.width < widths[-1] * 2 and d.width < 1752:
        print(f"⚠ ảnh gốc hơi nhỏ: vùng desktop chỉ rộng {d.width}px (< 1752)")
    for f in sorted(os.listdir(IMG_DIR)):
        if f.startswith(name + "-"):
            print(f"  {f:40s} {os.path.getsize(os.path.join(IMG_DIR, f)) // 1024} KB")


if __name__ == "__main__":
    main()
