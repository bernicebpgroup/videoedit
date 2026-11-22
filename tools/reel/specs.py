"""Edit specs for video 1 (2本书) and video 2 (拍卖得标 RM280千)."""
from reel import *

# ================= VIDEO 1 =================
def v1_elements():
    E = []; SY = 1330
    # header hook
    E.append(El(0.0, 5.9, rich_text("这[2本书]", 130, serif=True), W / 2, 1110, "slam", 0.2))
    E.append(El(2.92, 5.9, pill("拍卖经验", 48), W / 2 - 170, 1250, "pop"))
    E.append(El(4.20, 5.9, pill("成功步骤", 48), W / 2 + 170, 1250, "pop"))
    for t0, t1, s in [(1.04, 2.88, "里面有很多的"), (5.94, 7.40, "如果你想要学"), (7.46, 9.62, "怎样透过[拍卖房地产]"),
                      (16.64, 18.70, "这[两本书]记载着"), (18.72, 20.20, "[所有的经验]"),
                      (20.32, 22.50, "如果你想学[拍卖房地产]")]:
        E.append(sub(t0, t1, s, SY))
    # counter 1 -> 10 间
    steps = [(9.88, "1"), (10.48, "2"), (12.04, "4"), (12.78, "6"), (13.48, "10")]
    pnl = panel(820, 380)
    def counter(c, tl, t):
        place(c, pnl, W / 2, 1300, 0.9 + 0.1 * back_out(tl / 0.25), clamp(tl / 0.12) * clamp((14.35 - t) / 0.15))
        cur = [s for s in steps if s[0] <= t]
        if cur:
            t0, num = cur[-1]; sp = rich_text(f"[{num}] 间", 150, serif=True, hl_scale=1.3)
            place(c, sp, W / 2, 1255, 0.7 + 0.3 * back_out((t - t0) / 0.2), clamp((14.35 - t) / 0.15))
        row = "  →  ".join(n for _, n in steps if _ <= t)
        if row: place(c, rich_text(row, 44, color=GREY, stroke=3, shadow=False), W / 2, 1420, 1, clamp((14.35 - t) / 0.15))
    E.append(Fn(9.70, 14.35, counter))
    E.append(El(9.70, 14.35, rich_text("从一间变十间", 54), W / 2, 1040, "up"))
    # formula
    E.append(El(14.40, 16.55, rich_text("整套的", 60), W / 2, 1180, "up"))
    E.append(El(15.50, 16.55, rich_text("[方程式]", 170, serif=True), W / 2, 1330, "slam"))
    # header again
    E.append(El(16.64, 18.70, rich_text("[所有经验] 都在这里", 66), W / 2, 760, "pop"))
    # CTA
    E.append(El(22.68, 26.7, panel(860, 520), W / 2, 1290, "pop", 0))
    E.append(El(22.68, 26.7, rich_text("下方留言", 72), W / 2, 1130, "up", 0))
    E.append(typewriter(22.94, 26.7, "BOOK", W / 2, 1280, 120, 0.45))
    E.append(El(24.14, 26.7, rich_text("我将会[随机送给你]", 60), W / 2, 1450, "up", 0))
    return E

V1 = dict(src="src/src.mp4", t_start=0.0, dur=26.6,
          grade="eq=contrast=1.06:saturation=1.05:brightness=0.0,colorbalance=bs=0.04:bh=-0.02,vignette=PI/4.5",
          zoom=[(0.0, 1.0, 540, 760, 0, 0.02), (2.9, 1.14, 540, 700, 0.25), (5.94, 1.0, 540, 760, 0.3, 0.015),
                (9.70, 1.0, 540, 760, 0), (14.40, 1.16, 540, 720, 0.25), (16.64, 1.5, 540, 1500, 0.35),
                (18.72, 1.05, 540, 760, 0.35), (20.32, 1.12, 540, 720, 0.25), (22.68, 1.0, 540, 760, 0.3)],
          shakes=[(15.50, 14)])
V1_SFX = [(0.0, "impact", -8), (2.9, "whoosh", -6), (2.92, "pop", -6), (4.20, "pop", -6),
          (9.88, "ding", -4), (10.48, "ding", -4), (12.04, "ding", -3), (12.78, "ding", -3), (13.48, "ding", -2),
          (14.0, "riser", -6), (15.50, "impact", 0), (16.55, "whoosh", -6), (20.25, "whoosh", -8),
          (22.6, "whoosh", -6)] + [(22.94 + k * 0.11, "click", -4) for k in range(4)] + [(24.14, "chime", -4)]

# ================= VIDEO 2 =================
OFF2 = 1.0   # trim first second (silence)
from fx import text2, stack2, Impact, Neon, bubble, vs_card, price_drop
from reel import glass_label, Glass
from fx import ffont
def _gl(*a, **k):
    size = a[5] if len(a) > 5 else 48
    return glass_label(*a, fnt=ffont("sans_medium", size), **k)

# fonts: key words = 黑体特粗 (sans_black) with neon, small lines = 黑体中粗; all with deep shadow, no outlines.
BIG, SMALL = "sans_black", "sans_medium"
NEON_B = (120, 195, 255); ORANGE = (255, 150, 60)
SAFE_Y = (270, 1500)          # IG safe zone (vertical)
T_CR = 25.72                  # price crash moment

def cap(t0, t1, small, big, cy=1120, neon=True, hl=NEON_B, bsize=170):
    return stack2(t0, t1, [(text2(small, 66, SMALL), False), (text2(f"[{big}]" if neon else big, bsize, BIG, hl=hl, neon=neon), neon)], cy)

def thin(t0, t1, text, cy=1180):
    ch = [c for c in text.split("/") if c]; d = (t1 - t0) / len(ch)
    return [El(t0 + k * d, t0 + (k + 1) * d if k < len(ch) - 1 else t1, text2(c, 64, SMALL), W / 2, cy, "pop", 0.06, alpha=0.92) for k, c in enumerate(ch)]

def v2_elements():
    """premium/impact style: no outlines (deep shadow), one key phrase per sentence in the centre, neon key words,
    impact slams, glass bubbles, VS card, price-drop board. All text inside the IG safe zone (y 270-1500, x < 950)."""
    E = []
    # hook: 得标 huge, behind the speaker
    E.append(El(1.0, 3.5, text2("刚刚", 72, SMALL), W / 2 - 330, 320, "pop", 0.2))
    E.append(El(1.0, 3.5, text2("[得标]！", 300, BIG, hl=NEON_B, neon=True), W / 2 + 30, 445, "slam", 0.2, behind=True))
    E.append(_gl(2.60, 3.5, "新鲜出炉", W / 2, 760, 46, ic="gavel"))
    # location
    E += cap(3.62, 5.75, "这一个在", "KL", bsize=200)
    E.append(_gl(3.62, 5.75, "Kuala Lumpur", W / 2, 340, 44, ic="pin"))
    # VS card covers "这一个 Arte Plus / 在 Jalan Ampang"
    E.append(vs_card(5.84, 9.0))
    # new-launch price
    E += cap(9.00, 10.98, "人家买新的", "六七百千", neon=False)
    E.append(_gl(9.42, 12.9, "新房 RM600–700千", W / 2, 340, 46, ic="house", ic_color=WHITE))
    E += thin(11.06, 11.58, "你自己看")
    E += cap(11.60, 12.80, "我们刚标到", "多少钱？")
    # TAP -> screenshot pops out and zooms up (price)
    shot = Image.open("frames/shot.png").convert("RGBA")
    card = Image.new("RGBA", (shot.width + 36, shot.height + 36), (255, 255, 255, 255)); card.paste(shot, (18, 18))
    m = Image.new("L", card.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, card.width - 1, card.height - 1), 34, fill=255); card.putalpha(m)
    sh = Image.new("RGBA", (card.width + 80, card.height + 80), (0, 0, 0, 0)); sa = Image.new("L", sh.size, 0)
    ImageDraw.Draw(sa).rounded_rectangle((40, 50, 40 + card.width, 50 + card.height), 34, fill=150); sh.putalpha(sa.filter(ImageFilter.GaussianBlur(22)))
    sh.alpha_composite(card, (40, 40)); CARD = sh
    HB = (40 + 18 + 315, 40 + 18 + 625, 40 + 18 + 850, 40 + 18 + 785)   # price box inside CARD
    TAP = (390, 830); T_TAP, T_POP, T_OUT, T_END = 13.40, 13.62, 15.70, 16.05
    def tap(c, tl, t):
        for k in range(2):
            p = (tl - 0.12 * k) / 0.45
            if 0 <= p <= 1:
                r = 30 + 110 * ease_out(p); o = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
                ImageDraw.Draw(o).ellipse((150 - r, 150 - r, 150 + r, 150 + r), outline=GOLD + (int(255 * (1 - p)),), width=10)
                c.alpha_composite(o, (TAP[0] - 150, TAP[1] - 150))
        if tl < 0.3:
            d = Image.new("RGBA", (100, 100), (0, 0, 0, 0)); ImageDraw.Draw(d).ellipse((20, 20, 80, 80), fill=(255, 255, 255, 200)); c.alpha_composite(d, (TAP[0] - 50, TAP[1] - 50))
    E.append(Fn(T_TAP, T_TAP + 0.6, tap, z=5))
    def flash(c, tl, t):
        a = int(230 * (1 - ease_out(tl / 0.28))); c.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, a)))
    E.append(Fn(T_POP - 0.04, T_POP + 0.28, flash, z=9))
    def shotfx(c, tl, t):
        if t < T_OUT:
            p = back_out(tl / 0.38, 1.2); cx = TAP[0] + (W / 2 - TAP[0]) * ease_out(tl / 0.3); cy = TAP[1] + (900 - TAP[1]) * ease_out(tl / 0.3)
            s = 0.12 + (1.0 - 0.12) * p; s *= 1 + 0.015 * math.sin(max(0, tl - 0.4) * 2.2); ang = -6 * (1 - ease_out(tl / 0.4)) + 1.5
            img = CARD.copy()
            if tl > 0.55:   # blue highlight box draws in
                q = ease_out((tl - 0.55) / 0.3); x0, y0, x1, y1 = HB; dd = ImageDraw.Draw(img)
                dd.rounded_rectangle((x0, y0, x0 + (x1 - x0) * q, y1), 22, outline=BLUEBG + (255,), width=9)
            place(c, img, cx, cy, s, clamp(tl / 0.08), ang)
        else:
            q = ease_io((t - T_OUT) / (T_END - T_OUT)); place(c, CARD, W / 2 + q * 200, 900 - q * 300, 1 - 0.75 * q, 1 - q, 1.5 + 8 * q)
    E.append(Fn(T_POP, T_END, shotfx, z=6))
    E.append(El(13.95, 15.75, text2("拍卖得标价", 50, SMALL), W / 2, 420, "pop", 0.15))
    E.append(Impact(14.06, 15.75, text2("RM[280千]", 130, BIG, hl=NEON_B, neon=True), W / 2, 1430, z=7, flash=False))
    # impact: 便宜一倍
    E.append(El(15.86, 17.4, text2("比别人", 66, SMALL), W / 2, 610, "pop", 0.12))
    E.append(Impact(15.92, 17.4, text2("[便宜一倍]", 190, BIG, hl=NEON_B, neon=True), W / 2, 760))
    E += cap(17.96, 19.50, "买新的", "600多千", neon=False)
    E += thin(19.94, 21.80, "这是一个/中国人的名字/买到的")
    E += thin(22.06, 22.85, "那么我们讲")
    # price drop: 600 -> 500 (现在市场500多千) -> crash 280 (才标280千)
    E.append(price_drop(22.9, 23.55, T_CR, 27.75))
    # bubbles replace the bar chart: 你会选哪一个？
    E += thin(27.76, 28.55, "所以我问你")
    E += cap(28.6, 34.8, "你会选", "哪一个？", cy=1150)
    E.append(bubble(28.82, 34.8, 300, 420, "新房", "RM600多千", "市场价", WHITE, "house"))
    E.append(bubble(30.30, 34.8, 740, 400, "二手", "RM500千", "现在市场", ORANGE, None, glow=True))
    E.append(bubble(32.18, 34.8, 520, 650, "拍卖", "RM280多千", "得标价", NEON_B, "check", glow=True, w=470))
    E += thin(34.92, 35.90, "有一句话")
    # 经营者 vs 消费者 (glass panel)
    E.append(Glass(35.9, 44.6, 900, 330, W / 2, 1120, out=0.2))
    def split(c, tl, t):
        fo = clamp((44.6 - t) / 0.2)
        if t >= 36.04:
            pulse = 1 + (0.08 * abs(math.sin((t - 40.66) * 5)) if 40.66 <= t < 42.5 else 0)
            place(c, SPL1, W / 2, 1055, pulse * (0.7 + 0.3 * spring(t - 36.04)), clamp((t - 36.04) / 0.1) * fo)
        if t >= 38.52:
            place(c, SPL2, W / 2, 1185, 0.7 + 0.3 * spring(t - 38.52), clamp((t - 38.52) / 0.1) * fo)
    SPL1 = text2("先知先觉 → [经营者]", 64, BIG, hl=NEON_B, neon=True); SPL2 = text2("后知后觉 → 消费者", 60, SMALL, color=GREY)
    E.append(Fn(35.9, 44.6, split, z=1))
    E.append(El(40.66, 44.6, text2("经营者", 400, BIG, shadow=None), W / 2, 600, "slam", 0.25, behind=True, alpha=0.3))   # ghost
    E += thin(40.66, 42.45, "你要成为/像我们这样的/经营者", 1390)
    E += thin(43.08, 44.50, "还是消费者？", 1390)
    E += thin(45.10, 46.50, "如果你想要/买到这样的property")
    # BMV 50%
    E.append(El(46.56, 48.2, text2("Below Market Value", 60, SMALL), W / 2, 400, "up"))
    E.append(El(47.22, 48.2, text2("[50%]", 380, BIG, hl=NEON_B, neon=True), W / 2, 690, "slam", 0.1, behind=True))
    # CTA (glass)
    E.append(Glass(48.24, 51.8, 860, 440, W / 2, 1200, out=0))
    E.append(El(48.24, 51.8, text2("下方留言", 64, SMALL), W / 2, 1060, "up", 0))
    E.append(typewriter(48.70, 51.8, "AUCTION", W / 2, 1200, 110, 0.6, fnt=ffont("sans_black", 110)))
    E.append(El(49.68, 51.8, text2("我们教你也一样[买得到]", 54, SMALL, hl=NEON_B, hl_fam=BIG, neon=True), W / 2, 1345, "pop", 0))
    return E

V2 = dict(src="src2/src.mp4", t_start=OFF2, dur=50.78,
          grade="eq=contrast=1.07:saturation=1.06,colorbalance=bs=0.03,vignette=PI/5",
          zoom=[(1.0, 1.0, 540, 900, 0), (13.40, 1.12, 400, 840, 0.25), (16.05, 1.0, 540, 900, 0.35),
                (22.06, 1.1, 540, 800, 0.25), (22.9, 1.0, 540, 900, 0.3), (34.92, 1.12, 540, 760, 0.25),
                (40.66, 1.0, 540, 900, 0.3), (45.10, 1.12, 540, 760, 0.25), (48.24, 1.0, 540, 900, 0.3)],
          shakes=[(2.14, 12), (14.2, 12), (16.06, 16), (6.64, 10), (T_CR + 0.55, 18), (32.18, 8), (47.22, 12)])
V2_SFX = [(2.14, "impact", 0), (2.60, "pop", -6), (3.62, "whoosh", -6), (3.70, "pop", -5),
          (5.84, "whoosh", -4), (6.06, "pop", -4), (6.29, "pop", -4), (6.64, "impact", -2), (9.0, "whoosh", -6), (9.42, "pop", -6),
          (11.60, "pop", -5), (12.6, "riser", -7), (13.40, "click", -2), (13.58, "shutter", -2), (13.62, "whoosh", -5),
          (14.2, "impact", 0), (14.70, "ding", -5), (15.70, "whoosh", -6), (15.80, "whoosh", -6), (16.06, "impact", 0),
          (17.96, "pop", -5), (22.9, "whoosh", -6), (23.55, "ding", -6), (T_CR - 0.9, "riser", -6), (T_CR, "whoosh", -2),
          (T_CR + 0.55, "impact", 0), (T_CR + 0.75, "pop", -3), (T_CR + 0.8, "chime", -6), (27.76, "whoosh", -7),
          (28.82, "pop", -4), (30.30, "pop", -4), (32.18, "ding", -3), (32.25, "impact", -4), (35.9, "whoosh", -6),
          (36.04, "pop", -4), (38.52, "pop", -6), (40.66, "impact", -6), (46.56, "whoosh", -6),
          (47.22, "impact", -1), (48.24, "whoosh", -6)] + [(48.70 + k * 0.085, "click", -4) for k in range(7)] + [(49.68, "chime", -5)]
