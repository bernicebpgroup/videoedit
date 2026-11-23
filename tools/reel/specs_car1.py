"""Car video 1 (拍卖屋子可以自住): glass subtitle band, B-roll -> graphic boards, price cards, CTA 留言「拍卖」."""
import math, re
from reel import Fn, spring_zoom, spring, clamp, ease_out, pill
from gfx import *
from specs3 import T, big_title, glass, mini_card, cached, fade, firefly, card_pop, expand, title_el, GOLDB, GREEN, ORANGE, NAVY, F_BLACK

DUR = 56.6; END = 53.9
BROLL = [(13.6, 15.8), (15.8, 18.6), (20.3, 23.1), (24.3, 29.3)]
SUBS = [(0.00, 2.40, "人家讲买[拍卖屋子]不好啊"), (2.50, 3.55, "说不好啊"), (3.62, 5.20, "省了[200多300千]"),
        (5.28, 6.60, "我用这个省到的钱"), (6.60, 7.95, "去把屋子[装修美美]"), (7.96, 9.95, "[拍卖房地产]可不可以[自住]啊？"),
        (10.16, 12.30, "我的屋子就是[买拍卖屋子]来住的"), (12.44, 13.60, "[一年比一年]更好嘛"),
        (18.60, 20.25, "是[你本身]好不好"), (23.10, 24.28, "[没有二手卖]"),
        (29.30, 29.95, "那个前屋主买了"), (30.60, 32.30, "到被拍卖那天 都[没住过]"), (32.54, 34.90, "发展商早期要卖[700千]"),
        (35.24, 37.05, "二手要卖[七八百千]"), (37.14, 38.60, "因为在[疫情期间]"), (38.70, 39.42, "一个机会"),
        (39.46, 41.80, "我买这个拍卖屋子才[505千]"), (41.98, 42.70, "这么便宜"), (42.78, 44.20, "省了[200多300千]"),
        (44.38, 45.95, "我用这个省到的钱"), (46.00, 47.32, "去把屋子[装修美美]"), (47.38, 49.40, "买来 我又可以[自己住]"),
        (49.64, 50.50, "又[赚到钱]"), (50.70, 51.75, "是我要的[地点]"), (51.80, 53.10, "买拍卖屋子 可以[自己住]"), (53.24, 53.90, "[没问题]的")]

def sub_img(text):
    def mk():
        parts = [(m, i % 2 == 1) for i, m in enumerate(re.split(r"\[|\]", text)) if m]
        size = 74 if len(re.sub(r"\[|\]", "", text)) <= 12 else 62
        imgs = [glow(T(p, size, (130, 200, 255)), 10, 0.8, BLUE) if hl else T(p, size) for p, hl in parts]
        pad = int(size * 0.35); w = sum(i.width - 2 * pad for i in imgs) + 2 * pad; h = max(i.height for i in imgs)
        out = Image.new("RGBA", (w, h), (0, 0, 0, 0)); x = 0
        for i in imgs: out.alpha_composite(i, (x, (h - i.height) // 2)); x += i.width - 2 * pad
        return out
    return cached(("sub", text), mk)

def in_broll(t): return any(a <= t < b for a, b in BROLL)

def band(c, tl, t):
    if in_broll(t) or t >= END: return
    glass(c, (30, 1250, 1050, 1645), tint=(10, 30, 80), a=150, r=40)
    for a, b, s in SUBS:
        if a <= t < b:
            place(c, sub_img(s), W / 2, 1440, max(0.05, spring(t - a, 0.6, 18, 8)), clamp((t - a) / 0.06)); break

def mid_card(t0, t1, draw):
    """glass card between face and subtitle band (y 930–1235) — covers old burned-in captions too."""
    def f(c, tl, t):
        def d(cc): glass(cc, (60, 930, 1020, 1235), tint=(14, 26, 60), a=170); draw(cc, tl, t)
        fade(c, clamp(tl / 0.15) * clamp((t1 - t) / 0.15), d)
    return Fn(t0, t1, f, z=6)

def num(text, size, color=WHITE, g=None):
    return cached(("num", text, size, color), lambda: glow(text_layer(text, size, color, num_path=F_NUM), int(size * 0.18), 1.0, g or BLUE) if g is not False else text_layer(text, size, color, num_path=F_NUM))

def countup(c, t, t0, dur, lo, hi, fmt, size, y, color=GOLDB):
    v = lo + (hi - lo) * ease_out((t - t0) / dur); place(c, num(fmt(int(v)), size, color, (240, 200, 120)), W / 2, y)

def board_bg(title):
    def mk():
        b = blue_board().copy(); b.alpha_composite(soft_shadow(T(title, 84)), (0, 0)); return b
    bg = cached(("bb", title), blue_board)
    return bg

def board(t0, t1, title, draw):
    def f(c, tl, t):
        def d(cc):
            cc.alpha_composite(cached("board", blue_board))
            place(cc, cached(("bt", title), lambda: soft_shadow(T(title, 84))), W / 2, 330, max(0.05, spring(tl, 0.6, 16, 7)))
            draw(cc, tl, t)
        fade(c, clamp(tl / 0.12) * clamp((t1 - t) / 0.12) if t1 - t0 > 0.3 else 1, d)
    return Fn(t0, t1, f, z=9)

def house_card(label):
    def mk():
        L = Image.new("RGBA", (420, 480), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
        for i in range(480): d.line((0, i, 420, i), fill=(70 + i // 10, 140 + i // 8, 250, 255))
        L.alpha_composite(glow(house_icon(240, WHITE), 20, 1.0, CYAN), (90, 90))
        for k in range(9):
            x, y = 40 + (k * 97) % 360, 50 + (k * 61) % 260; d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 255, 200))
        return card(L, label, 300, 360)
    return cached(("hc", label), mk)

def elements():
    E = [Fn(0, END, band, z=7)]
    # 0–2.4 hook
    E.append(title_el(0.0, 2.45, "拍卖屋子不好？", 120, 300))
    # 3.62–5.9 省了 RM200–300K（盖住旧字幕 "省了200-300k"）
    def save1(c, tl, t):
        place(c, cached("sv", lambda: T("省了", 56, (200, 215, 240))), W / 2, 990)
        countup(c, t, 3.62, 0.9, 0, 300, lambda v: f"RM{min(v, 200)}-{v}K" if v > 200 else f"RM{v}K", 110, 1120)
    E.append(mid_card(3.62, 5.90, save1))
    # 5.28–7.95 光点 → 「装修美美」卡（左边）
    HC = house_card("装修美美")
    def reno(c, tl, t, end=7.95):
        if tl < 0.33: firefly(c, (20, 1750), (230, 760), tl / 0.33)
        else: card_pop(c, HC, (230, 760), tl - 0.33, 4, clamp((end - t) / 0.15))
    E.append(Fn(5.28, 7.95, reno, z=5)); E.append(title_el(5.28, 7.95, "省下的钱 → 装修", 84, 300))
    # 7.96–12.4 自住？（盖住 Dr Alwyn 名牌）
    E.append(mid_card(7.96, 12.40, lambda c, tl, t: (
        place(c, big_title("可以自住吗？", 104), W / 2, 1080) if t < 10.1 else
        (place(c, big_title("买拍卖屋子", 100), W / 2, 1040), place(c, cached("zz", lambda: glow(T("自己住", 70, GOLDB), 12, 0.9, (240, 200, 120))), W / 2, 1160)))))
    E.append(title_el(12.44, 13.60, "一年比一年更好", 96, 300))
    # ---- B1 13.6–15.8 一年比一年更好：柱状图
    def b1(c, tl, t):
        xs = [180, 340, 500, 660, 820]; hs = [180, 260, 360, 480, 640]; d = ImageDraw.Draw(c); pts = []
        for k, (x, h) in enumerate(zip(xs, hs)):
            p = ease_out(clamp((tl - 0.1 - k * 0.15) / 0.4)); hh = max(2, int(h * p))
            bar = Image.new("RGBA", (110, hh), (0, 0, 0, 0)); ImageDraw.Draw(bar).rounded_rectangle((0, 0, 109, hh - 1), 18, fill=(255, 255, 255, 70 + k * 40) if k < 4 else CYAN + (255,))
            c.alpha_composite(bar, (x - 55, 1300 - hh)); pts.append((x, 1300 - hh - 60))
        if tl > 0.9:
            q = clamp((tl - 0.9) / 0.4); n = 1 + int(q * 4); d.line(pts[:n + 1], fill=(255, 255, 255, 255), width=8)
            for p in pts[:n + 1]: d.ellipse((p[0] - 16, p[1] - 16, p[0] + 16, p[1] + 16), fill=(255, 255, 255, 255))
        if t > 14.66: place(c, cached("tp", lambda: glow(T("更加的突破", 66), 10, 0.8, BLUE)), W / 2, 1420, max(0.05, spring(t - 14.66, 0.5)))
        if t > 15.36: place(c, cached("jb", lambda: glow(T("更加的进步", 66, (130, 200, 255)), 12, 0.9, BLUE)), W / 2, 1530, max(0.05, spring(t - 15.36, 0.5)))
    E.append(board(13.6, 15.8, "一年比一年更好", b1))
    # ---- B2 15.8–18.6 屋子好不好 vs 你本身
    def b2(c, tl, t):
        glass(c, (90, 560, 990, 900), tint=(255, 255, 255), a=30); place(c, cached("wz", lambda: T("屋子好不好", 96, (200, 210, 230))), W / 2, 700)
        if t > 18.0:
            q = clamp((t - 18.0) / 0.25); ImageDraw.Draw(c).line((250, 708, 250 + 580 * q, 702), fill=ORANGE + (255,), width=12)
            place(c, cached("bz", lambda: T("× 不是重点", 50, ORANGE, F_SANS)), W / 2, 830, 1, q)
        if t > 18.3:
            def d(cc): glass(cc, (90, 960, 990, 1360), tint=(40, 120, 255), a=90); place(cc, cached("nb", lambda: glow(T("你本身好不好", 110), 18, 1.0, BLUE)), W / 2, 1110)
            fade(c, clamp((t - 18.3) / 0.15), d)
    E.append(board(15.8, 18.6, "关键是什么？", b2))
    E.append(mid_card(18.6, 20.25, lambda c, tl, t: (place(c, big_title("你本身好不好", 104), W / 2, 1050),
                                                     place(c, cached("gj", lambda: T("✓ 才是关键", 52, GOLDB, F_SANS)), W / 2, 1170))))
    # ---- B3 20.3–23.1 找区域：搜索框
    def b3(c, tl, t):
        glass(c, (90, 600, 990, 760), tint=(255, 255, 255), a=40, r=80)
        q = "我要的区域 · 二手单位"; n = int(clamp((tl - 0.2) / 1.2) * len(q))
        place(c, cached(("sq", n), lambda: T("🔍" if False else "搜索：" + q[:n] + ("|" if n < len(q) else ""), 56, WHITE, F_SANS)), W / 2, 680)
        if t > 22.4:
            for k in range(3):
                y = 860 + k * 130; a = clamp((t - 22.4 - k * 0.12) / 0.2)
                def d(cc, y=y): glass(cc, (130, y - 50, 950, y + 50), tint=(255, 255, 255), a=22, r=30)
                fade(c, a, d)
            if t > 22.9: place(c, cached("zero", lambda: glow(T("二手单位：0 间", 78, (255, 150, 120)), 14, 0.9, ORANGE)), W / 2, 1300, max(0.05, spring(t - 22.9, 0.5)))
        place(c, cached("zh", lambda: T("找了很久 · 没有二手卖", 52, (200, 220, 250))), W / 2, 1460)
    E.append(board(20.3, 23.1, "我要的区域", b3))
    # ---- B4 24.3–29.3 疫情期间 → 看 listing
    LC = cached("lc", lambda: house_card("拍卖 Listing"))
    def b4(c, tl, t):
        if t < 27.22: place(c, cached("mxd", lambda: glow(T("没想到", 150), 24, 1.0, BLUE)), W / 2, 760, max(0.05, spring(tl, 0.4)))
        if t > 25.66: place(c, cached("yq", lambda: glow(T("疫情期间", 130, (150, 210, 255)), 24, 1.1, BLUE)), W / 2, 560 if t >= 27.22 else 1000, max(0.05, spring(t - 25.66, 0.4)))
        if 27.22 <= t < 27.6: firefly(c, (1060, 1800), (W / 2, 1060), (t - 27.22) / 0.38)
        elif t >= 27.6:
            card_pop(c, cached("lcb", lambda: LC.resize((int(LC.width * 1.4), int(LC.height * 1.4)), Image.BICUBIC)), (W / 2, 1060), t - 27.6, -3)
            place(c, pill("NEW · 拍卖", 46), W / 2 - 150, 860, max(0.05, spring(t - 27.9, 0.3)))
        if t > 28.9: place(c, cached("qz", lambda: glow(T("前屋主 · 没住过", 64), 10, 0.8, BLUE)), W / 2, 1520, max(0.05, spring(t - 28.9, 0.5)))
    E.append(board(24.3, 29.3, "没想到……", b4))
    E.append(mid_card(29.30, 32.30, lambda c, tl, t: (place(c, big_title("一手单位", 110), W / 2, 1040),
                                                      place(c, cached("mz", lambda: T("被拍卖那天都没住过", 50, GOLDB)), W / 2, 1170))))
    # ---- 32.54–41.9 价格卡
    def price(c, tl, t):
        L = (200, 210, 230)
        if t > 32.54: place(c, cached("fz", lambda: T("发展商", 38, L)), 150, 1000)
        if t > 34.22: place(c, num("RM700K", 50, WHITE, False), 330, 1000, max(0.05, spring(t - 34.22, 0.4)))
        if t > 35.24: place(c, cached("es", lambda: T("二手", 38, L)), 150, 1130)
        if t > 36.12: place(c, num("RM700-800K", 44, WHITE, False), 345, 1130, max(0.05, spring(t - 36.12, 0.4)))
        if t > 39.46:
            q = clamp((t - 39.46) / 0.3); d = ImageDraw.Draw(c)
            d.line((240, 1003, 240 + 180 * q, 997), fill=ORANGE + (255,), width=7); d.line((220, 1133, 220 + 260 * q, 1127), fill=ORANGE + (255,), width=7)
        ImageDraw.Draw(c).line((500, 960, 500, 1205), fill=(255, 255, 255, 70), width=2)
        if t > 39.7: place(c, cached("pm", lambda: T("拍卖", 42, GOLDB)), 760, 985)
        if t > 40.64: place(c, num("RM505K", 96, GOLDB, (240, 200, 120)), 760, 1110, 1 + 0.8 * math.exp(-7 * (t - 40.64)) * math.cos(18 * (t - 40.64)))
    E.append(mid_card(32.54, 41.90, price))
    E.append(title_el(37.14, 41.90, "疫情期间 · 一个机会", 84, 300))
    # 41.98–44.3 省了
    def save2(c, tl, t):
        place(c, cached("sv2", lambda: T("这么便宜 · 省了", 50, (200, 215, 240))), W / 2, 990)
        if t > 42.78: countup(c, t, 42.78, 0.9, 0, 300, lambda v: f"RM{min(v, 200)}-{v}K" if v > 200 else f"RM{v}K", 110, 1120)
    E.append(mid_card(41.98, 44.30, save2))
    # 44.38–47.3 装修美美（右边卡）
    def reno2(c, tl, t, end=47.32):
        if tl < 0.33: firefly(c, (1060, 1750), (850, 760), tl / 0.33)
        else: card_pop(c, HC, (850, 760), tl - 0.33, -4, clamp((end - t) / 0.15))
    E.append(Fn(44.38, 47.32, reno2, z=5)); E.append(title_el(44.38, 47.32, "省下的钱 → 装修", 84, 300))
    # 47.38–51.75 清单
    def check(c, tl, t):
        for k, (tt, s, sm) in enumerate([(48.66, "自己住", "可以"), (49.80, "赚到钱", "又能"), (51.34, "好地点", "是我要的")]):
            if t < tt: continue
            x = 210 + k * 330; sc = max(0.05, spring(t - tt, 0.3))
            ImageDraw.Draw(c).ellipse((x - 120, 1020, x - 60, 1080), fill=GOLDB + (255,)); place(c, cached("ck", lambda: T("✓", 40, NAVY, F_SANS)), x - 90, 1050)
            place(c, cached(("cs", s), lambda: T(s, 64)), x + 45, 1050, sc); place(c, cached(("cm", sm), lambda: T(sm, 34, (200, 220, 250))), x + 30, 1160)
    E.append(mid_card(47.38, 51.78, check)); E.append(title_el(47.38, 51.78, "买拍卖屋子", 100, 300))
    E.append(mid_card(51.80, END, lambda c, tl, t: (place(c, big_title("可以自己住", 104), W / 2, 1040),
                                                   place(c, cached("mw", lambda: T("✓ 没问题", 56, GOLDB, F_SANS)), W / 2, 1170, max(0.05, spring(t - 53.24, 0.4)) if t > 53.24 else 0.05))))
    # ---- CTA 53.9–56.6
    def cta(c, tl, t):
        c.paste(c.filter(ImageFilter.GaussianBlur(min(18, tl * 60))))
        def d(cc):
            q = expand(cc, tl, (W / 2, 1050), (110, 760, 970, 1340))
            if q > 0.9:
                place(cc, cached("xf", lambda: T("下方留言", 80)), W / 2, 880)
                place(cc, cached("pmb", lambda: glow(T("「拍卖」", 190), 30, 1.2, BLUE)), W / 2, 1060, max(0.05, 1 + 0.8 * math.exp(-7 * (tl - 0.35)) * math.cos(18 * (tl - 0.35))))
                if tl > 0.9: place(cc, cached("jn", lambda: T("教你怎么买拍卖屋子", 54, GOLDB)), W / 2, 1240, max(0.05, spring(tl - 0.9, 0.4)))
        d(c)
    E.append(Fn(END, DUR, cta, z=10))
    return E

_C = (620, 660)
_keys = [(0.0, 1.0, *_C)]; t = 0.9; k = 0
while t < END:
    if not in_broll(t): _keys.append((t, 1.06 if k % 2 == 0 else 1.0, *_C)); k += 1
    t += 1.0
_keys += [(40.64, 1.12, 620, 640), (41.5, 1.0, *_C), (END, 1.0, *_C)]
ZOOM = spring_zoom(_keys)
SHAKES = [(40.64, 12), (3.62, 6)]
FLY = [5.28, 27.22, 44.38]
SFX = ([(0.0, "riser-1s-soft", -6), (0.02, "boom-hit-soft", -4), (3.62, "data-countup-medium", -2), (4.5, "data-number-land", 0)] +
       [(t, "shimmer-short-sparkle", -2) for t in FLY] + [(t + 0.33, "pop-large-in", 0) for t in FLY] +
       [(7.96, "whoosh-medium-soft", -4), (10.16, "pop-medium-in", -4), (12.44, "pop-medium-in", -4)] +
       [(13.6, "whoosh-medium-medium", 0)] + [(13.7 + k * 0.15, "data-bar-grow", -3) for k in range(5)] + [(14.66, "pop-small-in", -2), (15.36, "pop-small-in", -2)] +
       [(15.8, "whoosh-fast-medium", -2), (18.0, "data-decrease-short", -2), (18.3, "pop-large-in", 0), (18.6, "whoosh-fast-soft", -4)] +
       [(20.3, "whoosh-medium-medium", -2)] + [(20.5 + k * 0.09, "click-tap-soft", -6) for k in range(12)] + [(22.4, "click-mouse-soft", -2), (22.9, "data-number-land", 0)] +
       [(24.3, "whoosh-medium-medium", -2), (25.66, "pop-medium-in", -2), (28.9, "shimmer-short-soft", -4), (29.3, "whoosh-fast-soft", -4)] +
       [(34.22, "pop-small-in", -2), (36.12, "pop-small-in", -2), (37.14, "whoosh-fast-soft", -6), (39.46, "data-decrease-short", 0),
        (40.64, "riser-1s-soft", -4), (40.64, "boom-hit-medium", 0), (40.66, "shimmer-short-bright", -6)] +
       [(42.78, "data-countup-medium", -2), (43.7, "data-number-land", 0)] +
       [(48.66, "tone-step-1", -2), (49.80, "tone-step-3", -2), (51.34, "tone-step-5", -2), (51.80, "pop-medium-in", -4), (53.24, "tone-ding-high", -4)] +
       [(END, "whoosh-medium-medium", -2), (END + 0.35, "boom-hit-soft", -2), (END + 0.9, "sting-bright-short", -4)] +
       [(t, "whoosh-fast-soft", -14) for t, *_ in _keys[1:] if not in_broll(t)])
LOWCUT = [(a - 0.05, a + 0.25) for a, _ in BROLL] + [(END - 0.05, END + 0.3)]
