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
def v2_elements():
    E = []; SY = 1450
    # hook
    # text-behind-person: huge 得标 sits between the wall and the speaker
    E.append(El(1.0, 3.5, rich_text("刚刚", 72), W / 2 - 330, 300, "pop", 0.2))
    E.append(El(1.0, 3.5, rich_text("[得标]！", 300, hl_scale=1.0), W / 2 + 30, 445, "slam", 0.2, behind=True))
    E.append(El(2.60, 3.5, pill("新鲜出炉", 50), W / 2, 750, "pop"))
    # location tag (UI chip)
    E.append(El(3.62, 9.0, pill("KL · Arte Plus", 50, fg=WHITE, bg=(14, 26, 43, 225)), W / 2, 330, "slide"))
    E.append(El(7.28, 9.0, pill("Jalan Ampang", 46), W / 2, 450, "pop"))
    subs = [(3.62, 5.55, "这一个在[KL]"), (5.84, 7.20, "这一个[Arte Plus]"), (7.28, 8.95, "在[Jalan Ampang]"),
            (9.00, 10.98, "人家买新的[六七百千]"), (11.06, 11.58, "你自己看"), (11.60, 12.80, "我们刚标到[多少钱]？"),
            (15.86, 17.40, "比别人[便宜一倍]"), (17.96, 19.50, "买新的[600多千]"), (19.94, 20.95, "这是一个中国人"),
            (20.95, 21.80, "的名字买到的"), (22.06, 23.30, "那么我们讲"), (23.40, 25.30, "现在市场[500多千]"),
            (25.68, 27.50, "才标[280千]"), (34.92, 35.90, "有一句话"),
            (40.66, 42.45, "你要成为像我们这样的[经营者]"), (43.08, 44.50, "还是[消费者]？"),
            (45.10, 46.50, "如果你想要买到这样的property"), (49.68, 51.70, "我们教你也一样[买得到]")]
    for t0, t1, s in subs: E.append(sub(t0, t1, s, SY, 64 if len(s) < 14 else 56))
    # new price card
    E.append(El(9.42, 12.9, pill("新房 RM600–700千", 54, fg=WHITE, bg=(14, 26, 43, 225)), W / 2, 330, "slide"))
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
    E.append(El(13.95, 15.75, pill("拍卖得标价", 50), W / 2, 420, "pop", 0.15))
    E.append(El(14.12, 15.75, rich_text("RM[280千]", 130, hl_scale=1.15), W / 2, 1400, "slam", 0.15))
    # comparison bars
    bars = [(28.82, "新房", 600, "600多千", GREY), (30.30, "二手", 500, "500千", GREY), (32.18, "拍卖", 280, "280多千", GOLD)]
    pnl = panel(900, 470)
    def chart(c, tl, t):
        fo = clamp((34.8 - t) / 0.2); place(c, pnl, W / 2, 1230, 0.92 + 0.08 * back_out(tl / 0.25), clamp(tl / 0.12) * fo)
        place(c, rich_text("你会选哪一个？", 48, stroke=3), W / 2, 1060, 1, clamp(tl / 0.2) * fo)
        for k, (tb, lab, val, txt, col) in enumerate(bars):
            if t < tb: continue
            p = ease_out((t - tb) / 0.5); y = 1160 + k * 110; bw = int(520 * val / 700 * p)
            bar = Image.new("RGBA", (max(bw, 1), 64), col + (255,))
            c.alpha_composite(bar, (300, y - 32))
            place(c, rich_text(lab, 46, stroke=3, shadow=False), 220, y, 1, clamp((t - tb) / 0.15) * fo)
            place(c, rich_text(txt, 40, color=col, stroke=3, shadow=False), 300 + bw + 95, y, 1, clamp((t - tb - 0.3) / 0.2) * fo)
    E.append(Fn(27.76, 34.8, chart))
    E.append(El(27.76, 28.55, rich_text("所以我问你", 64), W / 2, SY, "pop", 0.08))
    # 经营者 vs 消费者
    pnl2 = panel(900, 330)
    def split(c, tl, t):
        fo = clamp((44.6 - t) / 0.2); place(c, pnl2, W / 2, 1250, 0.92 + 0.08 * back_out(tl / 0.25), clamp(tl / 0.12) * fo)
        if t >= 36.04:
            pulse = 1 + (0.08 * abs(math.sin((t - 40.66) * 5)) if 40.66 <= t < 42.5 else 0)
            place(c, rich_text("先知先觉 → [经营者]", 62), W / 2, 1185, pulse, clamp((t - 36.04) / 0.15) * fo)
        if t >= 38.52:
            place(c, rich_text("后知后觉 → 消费者", 62, color=GREY), W / 2, 1315, 1, clamp((t - 38.52) / 0.15) * fo)
    E.append(Fn(35.9, 44.6, split))
    # BMV 50%
    E.append(El(46.56, 48.2, rich_text("Below Market Value", 64), W / 2, 330, "up"))
    E.append(El(47.22, 48.2, rich_text("[50%]", 400, serif=True), W / 2, 680, "slam", 0.1, behind=True))
    # CTA
    E.append(El(48.24, 51.8, panel(860, 400), W / 2, 1180, "pop", 0))
    E.append(El(48.24, 51.8, rich_text("下方留言", 72), W / 2, 1070, "up", 0))
    E.append(typewriter(48.70, 51.8, "AUCTION", W / 2, 1220, 110, 0.6))
    return E

V2 = dict(src="src2/src.mp4", t_start=OFF2, dur=50.78,
          grade="eq=contrast=1.07:saturation=1.06,colorbalance=bs=0.03,vignette=PI/5",
          zoom=[(1.0, 1.0, 540, 900, 0), (13.40, 1.12, 400, 840, 0.25), (16.05, 1.0, 540, 900, 0.35),
                (22.06, 1.1, 540, 800, 0.25), (27.76, 1.0, 540, 900, 0.3), (34.92, 1.12, 540, 760, 0.25),
                (40.66, 1.0, 540, 900, 0.3), (45.10, 1.12, 540, 760, 0.25), (48.24, 1.0, 540, 900, 0.3)],
          shakes=[(2.14, 12), (14.0, 10), (32.92, 10), (47.22, 12)])
V2_SFX = [(2.14, "impact", 0), (2.60, "pop", -6), (3.62, "whoosh", -6), (7.28, "pop", -6), (9.42, "whoosh", -6),
          (12.6, "riser", -7), (13.40, "click", -2), (13.58, "shutter", -2), (13.62, "whoosh", -5), (14.0, "impact", 0),
          (14.12, "pop", -5), (14.70, "ding", -5), (15.70, "whoosh", -9), (27.76, "whoosh", -6), (28.82, "ding", -6), (30.30, "ding", -6), (32.18, "ding", -3),
          (32.92, "impact", -3), (35.9, "whoosh", -6), (36.04, "pop", -4), (38.52, "pop", -6), (46.56, "whoosh", -6),
          (47.22, "impact", -1), (48.24, "whoosh", -6)] + [(48.70 + k * 0.085, "click", -4) for k in range(7)] + [(49.68, "chime", -5)]
