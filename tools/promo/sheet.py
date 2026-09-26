# usage: python3 sheet.py <take> <start> <end> <step> <out.jpg> [cols] [thumb_w]
import sys, os
from PIL import Image, ImageDraw
take, a, b, st, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 4
tw = int(sys.argv[7]) if len(sys.argv) > 7 else 480
d = f"/var/tmp/promo/{take}"
fr = [i for i in range(a, b + 1, st) if os.path.exists(f"{d}/f{i:05d}.jpg")]
im0 = Image.open(f"{d}/f{fr[0]:05d}.jpg"); th = int(tw * im0.size[1] / im0.size[0])
rows = (len(fr) + cols - 1) // cols
S = Image.new("RGB", (cols * tw, rows * th), (0, 0, 0)); D = ImageDraw.Draw(S)
for k, i in enumerate(fr):
    im = Image.open(f"{d}/f{i:05d}.jpg").resize((tw, th)); x, y = (k % cols) * tw, (k // cols) * th
    S.paste(im, (x, y)); D.rectangle([x, y, x + 58, y + 16], fill=(0, 0, 0)); D.text((x + 3, y + 3), str(i), fill=(255, 255, 0))
S.save(out, quality=82); print(out, len(fr), S.size)
