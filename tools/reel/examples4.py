"""Sample frames for video 3 (车上口播): glass band hides burned-in subs; B-roll replaced by graphic boards."""
import sys, subprocess, math
sys.path.insert(0, sys.argv[1]); out = sys.argv[2]
from gfx import *
import specs3
from reel import pill
from specs3 import T, big_title, glass, mini_card, cached, GOLDB, GREEN, ORANGE, NAVY, F_BLACK
G = "eq=contrast=1.05:saturation=1.08,colorbalance=bs=0.03,vignette=PI/5"
def frame(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", "src3/src.mp4", "-map", "0:v:0", "-frames:v", "1",
                          "-vf", f"scale={W}:{H},{G}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.frombuffer("RGB", (W, H), raw).convert("RGBA")
def board(frames, path):
    fr = [f.convert("RGB").resize((360, 640), Image.LANCZOS) for f in frames]
    s = Image.new("RGB", (372 * len(fr) - 12, 640), (20, 20, 20))
    for i, f in enumerate(fr): s.paste(f, (i * 372, 0))
    s.save(path, quality=92)
def sub_band(c, text):
    """frosted band over the old burned-in subtitles + new big serif subtitle (no outline)."""
    glass(c, (30, 1250, 1050, 1510), tint=(10, 30, 80), a=150, r=40)
    import re
    parts = [(m, i % 2 == 1) for i, m in enumerate(re.split(r"\[|\]", text)) if m]
    imgs = [glow(T(p, 76, (130, 200, 255)), 10, 0.8, BLUE) if hl else T(p, 76) for p, hl in parts]
    w = sum(i.width for i in imgs) - 50 * (len(imgs) - 1); x = W / 2 - w / 2
    for i in imgs: c.alpha_composite(i, (int(x), int(1380 - i.height / 2))); x += i.width - 50
def gboard(title):
    c = blue_board().copy(); place(c, soft_shadow(T(title, 80)), W / 2, 330); return c

# 1 车上开场：钩子大字 + 字幕条盖住旧字幕
f1 = frame(2.0); place(f1, big_title("拍卖屋子不好？", 130), W / 2, 1080); sub_band(f1, "人家讲买[拍卖屋子]不好啊")

# 2 B-roll → graphic：一年比一年更好（上升图表）
f2 = gboard("一年比一年更好")
d = ImageDraw.Draw(f2); xs = [180, 340, 500, 660, 820]; hs = [180, 260, 360, 480, 640]
for k, (x, h) in enumerate(zip(xs, hs)):
    bar = Image.new("RGBA", (110, h), (0, 0, 0, 0)); ImageDraw.Draw(bar).rounded_rectangle((0, 0, 109, h - 1), 18, fill=(255, 255, 255, 70 + k * 40))
    if k == 4: bar = glow(Image.new("RGBA", (110, h), CYAN + (255,)), 24, 1.2, BLUE)
    f2.alpha_composite(bar, (x - 55, 1300 - h))
pts = [(x, 1300 - h - 60) for x, h in zip(xs, hs)]
d.line(pts, fill=(255, 255, 255, 255), width=8)
for p in pts: d.ellipse((p[0] - 16, p[1] - 16, p[0] + 16, p[1] + 16), fill=(255, 255, 255, 255))
place(f2, glow(text_layer("↗", 220, WHITE, num_path=F_NUM), 20, 1, BLUE), 900, 520)
place(f2, T("更加的突破 · 更加的进步", 60, (200, 225, 255)), W / 2, 1420)

# 3 B-roll → graphic：不是屋子好不好，是你本身好不好
f3 = gboard("关键是什么？")
glass(f3, (90, 560, 990, 900), tint=(255, 255, 255), a=30); place(f3, T("屋子好不好", 90, (190, 200, 220)), W / 2, 700)
ImageDraw.Draw(f3).line((260, 705, 820, 705), fill=ORANGE + (255,), width=10); place(f3, T("× 不是重点", 50, ORANGE, F_SANS), W / 2, 820)
glass(f3, (90, 960, 990, 1360), tint=(40, 120, 255), a=90)
place(f3, glow(T("你本身好不好", 110), 18, 1.0, BLUE), W / 2, 1110); place(f3, T("✓ 才是关键", 56, GOLDB, F_SANS), W / 2, 1260)

# 4 B-roll → graphic：疫情期间看 listing（拍卖 listing 卡）
f4 = gboard("疫情期间 · 看 Listing")
glass(f4, (120, 520, 960, 1500), tint=(255, 255, 255), a=36)
L = Image.new("RGBA", (760, 560), (225, 235, 250, 255)); dl = ImageDraw.Draw(L)
for i in range(560): dl.line((0, i, 760, i), fill=(90 + i // 8, 150 + i // 10, 235, 255))
hi = house_icon(360, WHITE); L.alpha_composite(hi, (200, 140))
dl.rectangle((0, 470, 760, 560), fill=(20, 40, 90, 255))
m = Image.new("L", L.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 759, 559), 28, fill=255); f4.paste(L, (160, 560), m)
f4.alpha_composite(text_layer("RM505,000", 60, WHITE, num_path=F_NUM), (190, 1035))
place(f4, pill("NEW · 拍卖", 46), 300, 620)
place(f4, T("前屋主没住过 · 一手单位", 50), W / 2, 1300); place(f4, T("区域找了很久 · 没有二手卖", 44, (190, 210, 240)), W / 2, 1400)

# 5 车上：价格对比 → RM505K（放在脸和字幕条之间，不挡脸）
f5 = frame(39.5); place(f5, big_title("拍卖只要", 96), W / 2, 300)
glass(f5, (60, 930, 1020, 1235), tint=(14, 26, 60), a=170)
place(f5, T("发展商", 38, (200, 210, 230)), 150, 1000); place(f5, T("二手", 38, (200, 210, 230)), 150, 1130)
place(f5, text_layer("RM700K", 50, WHITE, num_path=F_NUM), 330, 1000); place(f5, text_layer("RM800K", 50, WHITE, num_path=F_NUM), 330, 1130)
d5 = ImageDraw.Draw(f5); d5.line((240, 1003, 420, 997), fill=ORANGE + (255,), width=7); d5.line((240, 1133, 420, 1127), fill=ORANGE + (255,), width=7)
ImageDraw.Draw(f5).line((480, 960, 480, 1205), fill=(255, 255, 255, 70), width=2)
place(f5, T("拍卖", 42, GOLDB), 750, 985); place(f5, glow(text_layer("RM505K", 96, GOLDB, num_path=F_NUM), 18, 1.1, (240, 200, 120)), 750, 1110)
sub_band(f5, "我买这个[拍卖屋子]才[505千]")

# 6 车上：结论清单（横排，不挡脸）
f6 = frame(49.0); place(f6, big_title("买拍卖屋子", 100), W / 2, 300)
glass(f6, (60, 960, 1020, 1220), tint=(20, 60, 150), a=130)
for k, t_ in enumerate(["自己住", "赚到钱", "好地点"]):
    x = 210 + k * 330; ImageDraw.Draw(f6).ellipse((x - 120, 1020, x - 60, 1080), fill=GOLDB + (255,))
    place(f6, T("✓", 40, NAVY, F_SANS), x - 90, 1050); f6.alpha_composite(T(t_, 64), (x - 50, 1050 - 50))
    place(f6, T("可以" if k == 0 else ("又能" if k == 1 else "是我要的"), 34, (200, 220, 250)), x + 30, 1160)
sub_band(f6, "又可以[自己住] 又[赚到钱]")
board([f1, f2, f3, f4, f5, f6], out + "/ex_V3_sample.jpg"); print("ok")
