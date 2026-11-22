import sys, subprocess, numpy as np
sys.path.insert(0, sys.argv[1]); out = sys.argv[2]
import gfx
from gfx import *
F_BLACK = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc"
GOLDB = (212, 179, 110); GREEN = (76, 122, 100); ORANGE = (201, 111, 69); CREAM = (243, 239, 231); NAVY = (18, 28, 50)
GRADE = "eq=contrast=1.06:saturation=1.05,colorbalance=bs=0.04:bh=-0.02,vignette=PI/4.5"
def frame(t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", "src/src.mp4", "-map", "0:v:0", "-frames:v", "1",
                          "-vf", f"scale={W}:{H},{GRADE}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.frombuffer("RGB", (W, H), raw).convert("RGBA")
def board(frames, path):
    fr = [f.convert("RGB").resize((432, 768), Image.LANCZOS) for f in frames]
    s = Image.new("RGB", (444 * len(fr) - 12, 768), (20, 20, 20))
    for i, f in enumerate(fr): s.paste(f, (i * 444, 0))
    s.save(path, quality=92)
def T(text, size, color=WHITE, f=F_BLACK): return text_layer(text, size, color, f)
def big_title(text, size=150):   # 大、居中、粗宋体、无黑边：白字 + 蓝光
    return glow(soft_shadow(T(text, size), 14, 0.5), int(size * 0.14), 0.9, BLUE)
def glass(c, box, tint=(20, 60, 150), a=120, r=44):
    """Frosted glass panel: blur what's behind + tint + light border + top sheen."""
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0
    bg = c.crop(box).filter(ImageFilter.GaussianBlur(28))
    tint_l = Image.new("RGBA", (w, h), tint + (a,)); bg.alpha_composite(tint_l)
    sheen = Image.new("RGBA", (w, h), (0, 0, 0, 0)); sd = ImageDraw.Draw(sheen)
    for i in range(h // 3): sd.line((0, i, w, i), fill=(255, 255, 255, int(38 * (1 - i / (h / 3)))))
    bg.alpha_composite(sheen)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=255)
    sh = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); sa = Image.new("L", sh.size, 0)
    ImageDraw.Draw(sa).rounded_rectangle((40, 52, 40 + w, 52 + h), r, fill=120); sh.putalpha(sa.filter(ImageFilter.GaussianBlur(24)))
    c.alpha_composite(sh, (x0 - 40, y0 - 40)); c.paste(bg, (x0, y0), m)
    ImageDraw.Draw(c).rounded_rectangle(box, r, outline=(190, 225, 255, 170), width=3)
def mini_card(c, box, no, title, lines, bar):
    x0, y0, x1, y1 = box
    L = Image.new("RGBA", c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle(box, 26, fill=(255, 255, 255, 34), outline=(255, 255, 255, 110), width=2)
    d.rounded_rectangle((x0, y0, x1, y0 + 14), 7, fill=bar + (255,)); c.alpha_composite(L)
    c.alpha_composite(T(no, 46, GOLDB, F_SERIF), (x0 + 4, y0 + 8))
    tt = T(title, 50); c.alpha_composite(tt, (x0 + (x1 - x0 - tt.width) // 2, y0 + 70))
    for k, ln in enumerate(lines):
        lt = T(ln, 34, (225, 235, 250), F_SERIF); c.alpha_composite(lt, (x0 + (x1 - x0 - lt.width) // 2, y0 + 150 + k * 52))

# E1 拍卖经验：三种拍卖类型
e1 = frame(3.4)
place(e1, big_title("拍卖经验", 150), W / 2, 900)
glass(e1, (50, 1020, 1030, 1560))
place(e1, T("拍卖房产，不是全部一样", 52), W / 2, 1100)
for k, (no, tt, ls, bar) in enumerate([("01", "法院拍卖", ["已有地契", "法院程序"], GREEN),
                                       ("02", "LACA", ["地契未完成", "银行委托"], GOLDB),
                                       ("03", "Tender", ["密封式招标", "最高价得标"], ORANGE)]):
    x0 = 80 + k * 310; mini_card(e1, (x0, 1180, x0 + 290, 1520), no, tt, ls, bar)

# E2 成功步骤：5 个问题
e2 = frame(4.7)
place(e2, big_title("成功步骤", 150), W / 2, 820)
glass(e2, (60, 940, 1020, 1640), tint=(14, 30, 70), a=150)
for k, q in enumerate(["自住、出租，还是转售？", "这间拍卖屋值不值得买？", "有欠费或冻结令，还能参与？", "竞标到什么价格该停？", "得标后，谁协助完成流程？"]):
    y = 1010 + k * 122; d = ImageDraw.Draw(e2)
    d.ellipse((110, y, 190, y + 80), fill=GOLDB + (255,)); n = T(str(k + 1), 44, NAVY, F_SERIF); e2.alpha_composite(n, (150 - n.width // 2, y + 40 - n.height // 2))
    qt = T(q, 50); e2.alpha_composite(qt, (215, y + 40 - qt.height // 2))

# E3 方程式：市价 vs 起拍
e3 = frame(15.9)
place(e3, big_title("整套方程式", 140), W / 2, 870)
glass(e3, (60, 990, 1020, 1600), tint=(14, 26, 60), a=170)
place(e3, T("市价", 50, (200, 210, 230)), 290, 1080); place(e3, T("起拍", 50, (200, 210, 230)), 790, 1080)
m1 = glow(text_layer("RM500K", 84, WHITE, num_path=F_NUM), 8, 0.4); place(e3, m1, 290, 1190)
ImageDraw.Draw(e3).line((150, 1195, 430, 1187), fill=ORANGE + (255,), width=10)
m2 = glow(text_layer("RM300K", 84, GOLDB, num_path=F_NUM), 18, 0.9, (240, 200, 120)); place(e3, m2, 790, 1190)
ImageDraw.Draw(e3).line((120, 1300, 960, 1300), fill=(255, 255, 255, 60), width=2)
place(e3, T("表面差价", 60, GOLDB), W / 2, 1385)
place(e3, glow(text_layer("RM200,000", 120, GOLDB, num_path=F_NUM), 20, 1.0, (240, 200, 120)), W / 2, 1505)

# E4 CTA
e4 = frame(24.6)
place(e4, big_title("下方留言", 130), W / 2, 880)
glass(e4, (110, 990, 970, 1520))
place(e4, glow(text_layer("BOOK", 230, WHITE, num_path=F_NUM), 30, 1.2, BLUE), W / 2, 1180)
place(e4, T("我将会随机送给你", 64, GOLDB), W / 2, 1400)
board([e1, e2, e3, e4], out + "/ex_D_glass.jpg")
print("ok")
