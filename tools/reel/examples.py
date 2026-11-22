import sys, subprocess, numpy as np
sys.path.insert(0, sys.argv[1]); out = sys.argv[2]
from gfx import *
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

# ---- A: 字样式（无黑边、半透明蓝、数字用 Montserrat） ----
a1 = frame(0.5)
place(a1, glass_text("2", 540), 215, 480)
place(a1, soft_shadow(text_layer("这", 96, WHITE)), 140, 250 + 60)
place(a1, glass_text("本书", 150), 905, 430)
place(a1, sub_text("这[两本书]里面有"), W / 2, 1330)
a2 = frame(10.6)
place(a2, glass_text("1 → 10", 230), W / 2, 330)
place(a2, sub_text("从[一间]变[十间]", 70), W / 2, 1330)
a3 = frame(15.9)
place(a3, soft_shadow(text_layer("整套的", 70, WHITE)), W / 2, 1120)
place(a3, glass_text("方程式", 200), W / 2, 1260)
a4 = frame(24.6)
pnl = Image.new("RGBA", (820, 430), (0, 0, 0, 0)); d = ImageDraw.Draw(pnl)
d.rounded_rectangle((0, 0, 819, 429), 40, fill=(20, 80, 200, 110), outline=CYAN + (200,), width=3)
place(a4, glow(pnl, 20, 0.8), W / 2, 1270)
place(a4, soft_shadow(text_layer("下方留言", 72, WHITE)), W / 2, 1140)
place(a4, glass_text("BOOK", 170), W / 2, 1270)
place(a4, sub_text("我将会[随机送给你]", 58), W / 2, 1410)
board([a1, a2, a3, a4], out + "/ex_A_text.jpg")

# ---- B: 全蓝色 物业 graphic（1间 → 2间 → 4间 → 10间） ----
def prop_board(n, prev):
    c = blue_board()
    place(c, soft_shadow(text_layer("从一间 变 十间", 70, WHITE)), W / 2, 300)
    place(c, glow(text_layer(str(n), 380, WHITE), 30, 1.3, (120, 200, 255)), W / 2 - 90, 620); place(c, text_layer("间物业", 96, WHITE), W / 2 + 230, 690)
    cols = 5 if n > 4 else n; rows = (n + cols - 1) // cols; s = 150 if n > 4 else 190
    gx = W / 2 - (cols - 1) * (s + 20) / 2
    for k in range(n):
        r, q = divmod(k, cols); x = gx + q * (s + 20); y = 1000 + r * (s + 40)
        ic = house_icon(s, WHITE if k < prev else CYAN)
        if k >= prev: ic = glow(ic, 16, 1.4, BLUE)
        place(c, ic, x, y)
    steps = [1, 2, 4, 6, 10]; sx = W / 2 - 2 * 170
    for i, v in enumerate(steps):
        on = v <= n; d = ImageDraw.Draw(c); x = sx + i * 170; y = 1520
        if i: d.line((x - 170 + 40, y, x - 40, y), fill=(255, 255, 255, 200 if on else 60), width=6)
        d.ellipse((x - 40, y - 40, x + 40, y + 40), fill=(255, 255, 255, 255) if on else (255, 255, 255, 40))
        t = text_layer(str(v), 40, BLUE_D if on else WHITE, num_path=F_NUM); place(c, t, x, y + 2)
    return c
board([prop_board(1, 0), prop_board(2, 1), prop_board(4, 2), prop_board(10, 6)], out + "/ex_B_property.jpg")

# ---- C: 萤火虫光点飞进来 → 变成卡片 ----
books = frame(0.5).crop((90, 1480, 860, 1900))
def ff(t, prog, show_card=0.0, label="拍卖经验", second=False):
    c = frame(t)
    if prog < 1: firefly(c, (1060, 1750), (860, 640), prog)
    else:
        if show_card < 0.25:
            o = orb(60); place(c, o, 860, 640, 1 + show_card * 6, 1 - show_card * 3)
        cd = card(books, label, 300, 360); sc = 0.3 + 0.7 * min(1, show_card / 0.3) * (1 + 0.08 * math.sin(show_card * 20) * math.exp(-show_card * 5))
        place(c, cd, 860, 640, sc, min(1, show_card * 4), -4)
        if second:
            cd2 = card(frame(0.5).crop((300, 1480, 1000, 1900)), "成功步骤", 300, 360); place(c, cd2, 230, 760, 1, 1, 5)
    place(c, sub_text("拍卖[经验]" if not second else "拍卖[成功步骤]", 70), W / 2, 1330)
    return c
board([ff(2.95, 0.35), ff(3.05, 0.85), ff(3.2, 1.0, 0.12), ff(4.6, 1.0, 1.0, second=True)], out + "/ex_C_firefly.jpg")
print("ok")
