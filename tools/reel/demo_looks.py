"""Look-development stills + short clip: font/neon options, glass bubbles, VS graphic card."""
import sys, subprocess
sys.path.insert(0, sys.argv[1])
from reel import *
from fx import *
import specs
out = sys.argv[2]

def base(t):
    sp = specs.V2
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", sp["src"], "-map", "0:v:0", "-frames:v", "1",
                          "-vf", f"scale={W}:{H},{sp['grade']}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.frombuffer("RGB", (W, H), raw).copy()

def shot(t, els, tt=None):
    im = base(t); c = composite(im, tt or t, sorted(els, key=lambda e: e.z), Seg()); return c.convert("RGB")

def label(im, txt):
    d = ImageDraw.Draw(im); f = ffont("sans_black", 54); d.rounded_rectangle((30, 1780, 60 + f.getlength(txt), 1870), 20, fill=(0, 0, 0)); d.text((45, 1785), txt, font=f, fill=WHITE); return im

# 1) font + neon options on the same sentence (才标 / 280千)
T = 26.6; opts = [
    ("① 宋体特粗", "serif_light", "serif_black"),
    ("② 黑体特粗", "sans_medium", "sans_black"),
    ("③ 站酷庆科（潮）", "sans_medium", "qingke"),
    ("④ 书法（马善政）", "sans_medium", "brush")]
ims = []
for name, small, bigf in opts:
    els = stack2(T - 2, T + 5, [(text2("才标", 70, small), False), (text2("[280千]", 230, bigf, hl=(110, 190, 255), neon=True), True)], 1180)
    ims.append(label(shot(T, els), name))
sheet = Image.new("RGB", (W * 2 + 10, 1300 + 10), (16, 16, 16))   # 2x2, caption area at full resolution
for i, im in enumerate(ims):
    cr = im.crop((0, 820, W, 1470)); d = ImageDraw.Draw(cr); f = ffont("sans_black", 50)
    d.rounded_rectangle((20, 20, 40 + f.getlength(opts[i][0]), 95), 18, fill=(0, 0, 0)); d.text((30, 22), opts[i][0], font=f, fill=WHITE)
    sheet.paste(cr, ((i % 2) * (W + 10), (i // 2) * 660))
sheet.save(f"{out}/look_fonts.jpg", quality=92)

# 2) bubbles above head + 3) VS card
BUB = lambda t0: [
    bubble(t0, t0 + 6, 290, 420, "新房", "RM600多千", "市场价", WHITE, "house"),
    bubble(t0 + 0.35, t0 + 6, 790, 390, "二手", "RM500千", "现在市场", (255, 150, 60), None, glow=True),
    bubble(t0 + 0.8, t0 + 6, 540, 640, "拍卖得标", "RM280千", "便宜一倍", (110, 190, 255), "check", glow=True, w=470)]
b = shot(25.9, BUB(23.4) + stack2(25.68, 27.5, [(text2("才标", 70, "sans_medium"), False), (text2("[280千]", 230, "sans_black", hl=(110, 190, 255), neon=True), True)], 1180))
v = shot(7.0, [vs_card(5.84, 9.0)])
s2 = Image.new("RGB", (W + 10, H // 2), (16, 16, 16)); s2.paste(b.resize((W // 2, H // 2)), (0, 0)); s2.paste(v.resize((W // 2, H // 2)), (W // 2 + 10, 0))
s2.save(f"{out}/look_bubbles_vs.jpg", quality=92)

# short animated clip: VS card (5.84-9.0) then bubbles + neon caption (22.0-27.6)
if len(sys.argv) > 3:
    sp = specs.V2
    for nm, t0, dur, els in [("a", 5.6, 3.4, [vs_card(5.84, 9.0)]),
                             ("b", 22.6, 5.0, BUB(23.4) + stack2(25.68, 27.5, [(text2("才标", 70, "sans_medium"), False), (text2("[280千]", 230, "sans_black", hl=(110, 190, 255), neon=True), True)], 1180))]:
        render(sp["src"], f"{out}/clip_{nm}.v.mp4", t0, dur, [(0, 1.0, 540, 900, 0)], els, sp["grade"])
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{out}/clip_{nm}.v.mp4", "-ss", str(t0), "-t", str(dur), "-i", sp["src"], "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-af", "loudnorm=I=-14", f"{out}/clip_{nm}.mp4"], check=True)
    open(f"{out}/list.txt", "w").write(f"file 'clip_a.mp4'\nfile 'clip_b.mp4'\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out}/list.txt", "-c", "copy", f"{out}/looks_demo.mp4"], check=True)
