"""VIDEO 1 · v3: 萤火虫光点卡片 + 玻璃卡片 + 全蓝物业图 + 大字居中粗宋体 + 每秒弹簧放大放小."""
import math
import reel
from reel import Fn, spring_zoom, spring, clamp, ease_out, ease_io
import gfx
from gfx import *
F_BLACK = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc"
GOLDB = (212, 179, 110); GREEN = (76, 122, 100); ORANGE = (201, 111, 69); NAVY = (18, 28, 50)

def T(text, size, color=WHITE, f=F_BLACK): return text_layer(text, size, color, f)
_cache = {}
def big_title(text, size=150):
    k = ("bt", text, size)
    if k not in _cache: _cache[k] = glow(soft_shadow(T(text, size), 14, 0.5), int(size * 0.14), 0.9, BLUE)
    return _cache[k]
def cached(key, fn):
    if key not in _cache: _cache[key] = fn()
    return _cache[key]

def glass(c, box, tint=(20, 60, 150), a=120, r=44):
    x0, y0, x1, y1 = [int(v) for v in box]; w, h = x1 - x0, y1 - y0
    if w < 20 or h < 20: return
    bg = c.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(26))
    bg.alpha_composite(Image.new("RGBA", (w, h), tint + (a,)))
    sheen = Image.new("RGBA", (w, h), (0, 0, 0, 0)); sd = ImageDraw.Draw(sheen)
    for i in range(0, h // 3, 2): sd.line((0, i, w, i), fill=(255, 255, 255, int(38 * (1 - i / (h / 3)))), width=2)
    bg.alpha_composite(sheen)
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), min(r, h // 2), fill=255)
    c.paste(bg, (x0, y0), m)
    ImageDraw.Draw(c).rounded_rectangle((x0, y0, x1, y1), min(r, h // 2), outline=(190, 225, 255, 170), width=3)

def mini_card(c, box, no, title, lines, bar):
    x0, y0, x1, y1 = box
    L = Image.new("RGBA", (x1 - x0 + 4, y1 - y0 + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((0, 0, x1 - x0, y1 - y0), 26, fill=(255, 255, 255, 34), outline=(255, 255, 255, 110), width=2)
    d.rounded_rectangle((0, 0, x1 - x0, 14), 7, fill=bar + (255,)); c.alpha_composite(L, (x0, y0))
    c.alpha_composite(cached(("no", no), lambda: T(no, 46, GOLDB, F_SERIF)), (x0 + 4, y0 + 8))
    tt = cached(("mt", title), lambda: T(title, 50)); c.alpha_composite(tt, (x0 + (x1 - x0 - tt.width) // 2, y0 + 70))
    for k, ln in enumerate(lines):
        lt = cached(("ml", ln), lambda: T(ln, 34, (225, 235, 250), F_SERIF)); c.alpha_composite(lt, (x0 + (x1 - x0 - lt.width) // 2, y0 + 150 + k * 52))

def fade(c, a, fn):
    """draw fn on a copy and blend with alpha a."""
    if a <= 0.01: return
    if a >= 0.99: fn(c); return
    c2 = c.copy(); fn(c2); c.paste(Image.blend(c, c2, a))

# ---------- content blocks ----------
def panel_types(c):
    place(c, cached("pt_t", lambda: T("拍卖房产，不是全部一样", 52)), W / 2, 1100)
    for k, (no, tt, ls, bar) in enumerate([("01", "法院拍卖", ["已有地契", "法院程序"], GREEN), ("02", "LACA", ["地契未完成", "银行委托"], GOLDB),
                                           ("03", "Tender", ["密封式招标", "最高价得标"], ORANGE)]):
        xx = 80 + k * 310; mini_card(c, (xx, 1180, xx + 290, 1520), no, tt, ls, bar)
QS = ["自住、出租，还是转售？", "这间拍卖屋值不值得买？", "有欠费或冻结令，还能参与？", "竞标到什么价格该停？", "得标后，谁协助完成流程？"]
def panel_steps(c, tl):
    for k, q in enumerate(QS):
        a = clamp((tl - k * 0.18) / 0.2)
        if a <= 0: continue
        y = 1010 + k * 122; dx = 40 * (1 - ease_out(a))
        def draw(cc, y=y, k=k, q=q, dx=dx):
            ImageDraw.Draw(cc).ellipse((110 + dx, y, 190 + dx, y + 80), fill=GOLDB + (255,))
            n = cached(("qn", k), lambda: T(str(k + 1), 44, NAVY, F_SERIF)); cc.alpha_composite(n, (int(150 + dx - n.width // 2), y + 40 - n.height // 2))
            qt = cached(("q", q), lambda: T(q, 50)); cc.alpha_composite(qt, (int(215 + dx), y + 40 - qt.height // 2))
        fade(c, a, draw)

def expand(c, tl, start_xy, box, dur=0.32):
    q = clamp(tl / dur); q = 1 - (1 - q) ** 3
    sx, sy = start_xy; x0, y0, x1, y1 = box
    glass(c, (sx - 150 + (x0 - sx + 150) * q, sy - 180 + (y0 - sy + 180) * q, sx + 150 + (x1 - sx - 150) * q, sy + 180 + (y1 - sy - 180) * q))
    return q

def card_pop(c, img, xy, tl, ang, a=1.0):
    s = spring(tl, 0.2, 18, 6); place(c, img, xy[0], xy[1], max(0.05, s), min(1, tl / 0.08) * a, ang)

def title_el(t0, t1, text, size, y, out=0.15):
    spr = big_title(text, size)
    def f(c, tl, t): place(c, spr, W / 2, y, max(0.05, spring(tl, 0.4, 18, 7)), clamp(tl / 0.08) * clamp((t1 - t) / out))
    return Fn(t0, t1, f, z=8)

# ---------- elements ----------
def v3_elements(book1, book2):
    E = []
    C1 = cached("c1", lambda: card(book1, "第一本", 280, 330)); C2 = cached("c2", lambda: card(book2, "第二本", 280, 330))
    CA = cached("ca", lambda: card(book1, "拍卖经验", 300, 360)); CB = cached("cb", lambda: card(book2, "成功步骤", 300, 360))
    CC = cached("cc", lambda: card(book1, "留言 BOOK", 300, 360))
    # 0–2.85 两本书
    def books(c, tl, t, end=2.85):
        p = tl / 0.55; a = clamp((end - t) / 0.15)
        if p < 1:
            firefly(c, (1060, 1750), (860, 560), p); firefly(c, (20, 1750), (220, 560), p)
        else:
            bob = 6 * math.sin(tl * 3)
            card_pop(c, C1, (225, 560 + bob), tl - 0.55, 5, a); card_pop(c, C2, (860, 560 - bob), tl - 0.55, -5, a)
    E.append(Fn(0.0, 2.85, books, z=5))
    E.append(title_el(0.0, 2.85, "这2本书", 140, 960))
    E.append(title_el(1.04, 2.85, "里面有很多的", 80, 1110))
    # 2.92–4.95 拍卖经验：光点 → 小卡 → 玻璃卡（三种拍卖）
    def exp_a(c, tl, t, end=4.95):
        a = clamp((end - t) / 0.18)
        if tl < 0.33: firefly(c, (1060, 1750), (860, 620), tl / 0.33)
        elif tl < 0.55: card_pop(c, CA, (860, 620), tl - 0.33, -4)
        else:
            def d(cc):
                q = expand(cc, tl - 0.55, (860, 620), (50, 1020, 1030, 1560))
                if q > 0.9: panel_types(cc)
            fade(c, a, d)
    E.append(Fn(2.92, 4.95, exp_a, z=5))
    E.append(title_el(2.92, 4.95, "拍卖经验", 150, 900))
    # 4.95–7.40 成功步骤：5 个问题
    def exp_b(c, tl, t, end=7.40):
        a = clamp((end - t) / 0.18)
        if tl < 0.33: firefly(c, (20, 1750), (220, 620), tl / 0.33)
        elif tl < 0.5: card_pop(c, CB, (220, 620), tl - 0.33, 4)
        else:
            def d(cc):
                q = expand(cc, tl - 0.5, (220, 620), (60, 940, 1020, 1640))
                if q > 0.9: panel_steps(cc, tl - 0.8)
            fade(c, a, d)
    E.append(Fn(4.95, 7.40, exp_b, z=5))
    E.append(title_el(4.95, 7.40, "成功步骤", 150, 820))
    # 7.46–9.62
    E.append(title_el(7.46, 9.62, "怎样透过", 80, 820))
    E.append(title_el(7.60, 9.62, "拍卖房地产", 150, 960))
    # 9.70–14.35 全蓝物业图
    BOARD = cached("board", blue_board)
    steps = [(9.88, 1), (10.48, 2), (12.04, 4), (12.78, 6), (13.48, 10)]
    def prop(c, tl, t, t1=14.35):
        a = clamp(tl / 0.18) * clamp((t1 - t) / 0.18)
        def d(cc):
            cc.alpha_composite(BOARD)
            place(cc, cached("pt", lambda: soft_shadow(T("从一间 变 十间", 76))), W / 2, 300)
            cur = [s for s in steps if s[0] <= t]; n, t0 = (cur[-1][1], cur[-1][0]) if cur else (0, t)
            prev = cur[-2][1] if len(cur) > 1 else 0
            if n:
                sp = cached(("pn", n), lambda: glow(text_layer(str(n), 380, WHITE, num_path=F_NUM), 30, 1.3, (120, 200, 255)))
                nx = W / 2 - 120 if n < 10 else W / 2 - 170
                place(cc, sp, nx, 620, max(0.05, spring(t - t0, 0.5, 18, 6)))
                place(cc, cached("jw", lambda: T("间物业", 96)), nx + sp.width / 2 + 90, 690)
            cols = 5 if n > 4 else max(n, 1); s = 150 if n > 4 else 190; gx = W / 2 - (cols - 1) * (s + 20) / 2
            for k in range(n):
                r, q = divmod(k, cols); x = gx + q * (s + 20); y = 1000 + r * (s + 40)
                new = k >= prev
                ic = cached(("h", s, new), lambda: glow(house_icon(s, CYAN), 16, 1.4, BLUE) if new else house_icon(s, WHITE))
                place(cc, ic, x, y, max(0.05, spring(t - t0 - 0.05 * (k - prev), 0.2, 18, 6)) if new else 1)
            sx = W / 2 - 2 * 170; dd = ImageDraw.Draw(cc)
            for i, (_, v) in enumerate(steps):
                on = v <= n; x = sx + i * 170; y = 1520
                if i: dd.line((x - 130, y, x - 40, y), fill=(255, 255, 255, 220 if on else 60), width=6)
                dd.ellipse((x - 40, y - 40, x + 40, y + 40), fill=(255, 255, 255, 255) if on else (255, 255, 255, 50))
                place(cc, cached(("sd", v, on), lambda: text_layer(str(v), 40, BLUE_D if on else WHITE, num_path=F_NUM)), x, y + 2)
        fade(c, a, d)
    E.append(Fn(9.70, 14.35, prop, z=9))
    # 14.40–16.60 方程式 玻璃卡
    def formula(c, tl, t, end=16.60):
        a = clamp(tl / 0.2) * clamp((end - t) / 0.18)
        def d(cc):
            glass(cc, (60, 990, 1020, 1600), tint=(14, 26, 60), a=170)
            place(cc, cached("f_m", lambda: T("市价", 50, (200, 210, 230))), 290, 1080); place(cc, cached("f_q", lambda: T("起拍", 50, (200, 210, 230))), 790, 1080)
            place(cc, cached("f_5", lambda: glow(text_layer("RM500K", 84, WHITE, num_path=F_NUM), 8, 0.4)), 290, 1190)
            if tl > 0.45:
                q = clamp((tl - 0.45) / 0.25); ImageDraw.Draw(cc).line((150, 1195, 150 + 280 * q, 1195 - 8 * q), fill=ORANGE + (255,), width=10)
            if tl > 0.75: place(cc, cached("f_3", lambda: glow(text_layer("RM300K", 84, GOLDB, num_path=F_NUM), 18, 0.9, (240, 200, 120))), 790, 1190, max(0.05, spring(tl - 0.75, 0.3)))
            ImageDraw.Draw(cc).line((120, 1300, 960, 1300), fill=(255, 255, 255, 60), width=2)
            if tl > 1.1:
                place(cc, cached("f_d", lambda: T("表面差价", 60, GOLDB)), W / 2, 1385, 1, clamp((tl - 1.1) / 0.15))
                place(cc, cached("f_2", lambda: glow(text_layer("RM200,000", 120, GOLDB, num_path=F_NUM), 20, 1.0, (240, 200, 120))), W / 2, 1505,
                      1 + 0.8 * math.exp(-7 * (tl - 1.1)) * math.cos(18 * (tl - 1.1)), clamp((tl - 1.1) / 0.06))
        fade(c, a, d)
    E.append(Fn(14.40, 16.60, formula, z=5))
    E.append(title_el(14.40, 15.48, "整套的", 110, 870))
    E.append(title_el(15.50, 16.60, "方程式", 160, 870))
    # 16.64–18.70 书本特写 + 两张书卡回来
    def books2(c, tl, t):
        if tl < 0.4: firefly(c, (1060, 1750), (860, 420), tl / 0.4); firefly(c, (20, 1750), (220, 420), tl / 0.4)
        else:
            card_pop(c, C1, (225, 420), tl - 0.4, 5, clamp((18.70 - t) / 0.15)); card_pop(c, C2, (860, 420), tl - 0.4, -5, clamp((18.70 - t) / 0.15))
    E.append(Fn(16.64, 18.70, books2, z=5))
    E.append(title_el(16.64, 18.70, "所有经验", 150, 820))
    E.append(title_el(17.30, 18.70, "都记载在这两本书", 72, 960))
    E.append(title_el(18.72, 20.25, "所有的经验", 140, 960))
    E.append(title_el(20.32, 22.55, "如果你想学", 90, 820))
    E.append(title_el(20.50, 22.55, "拍卖房地产", 150, 960))
    # 22.68– CTA
    def cta(c, tl, t):
        if tl < 0.33: firefly(c, (1060, 1750), (860, 620), tl / 0.33); return
        if tl < 0.5: card_pop(c, CC, (860, 620), tl - 0.33, -4); return
        q = expand(c, tl - 0.5, (860, 620), (110, 990, 970, 1520))
        if q > 0.9:
            sp = cached("bk", lambda: glow(text_layer("BOOK", 230, WHITE, num_path=F_NUM), 30, 1.2, BLUE))
            place(c, sp, W / 2, 1180, max(0.05, 1 + 0.8 * math.exp(-7 * (tl - 0.8)) * math.cos(18 * (tl - 0.8))) if tl > 0.8 else 0.3, clamp((tl - 0.8) / 0.08))
            if t > 24.14: place(c, cached("rnd", lambda: T("我将会随机送给你", 64, GOLDB)), W / 2, 1400, max(0.05, spring(t - 24.14, 0.4)), clamp((t - 24.14) / 0.1))
    E.append(Fn(22.68, 26.7, cta, z=5))
    E.append(title_el(22.68, 26.7, "下方留言", 130, 880, 0.01))
    return E

_C = (610, 720)
ZOOM = spring_zoom([(0.0, 1.0, *_C), (1.04, 1.06, *_C), (2.0, 1.0, *_C), (2.92, 1.08, *_C), (3.9, 1.03, *_C), (4.95, 1.08, *_C),
                    (5.94, 1.02, *_C), (6.90, 1.07, *_C), (7.46, 1.0, *_C), (8.5, 1.08, *_C), (9.70, 1.0, *_C), (14.40, 1.06, *_C),
                    (15.50, 1.16, 600, 700), (16.64, 1.5, 560, 1500), (17.74, 1.38, 560, 1450), (18.72, 1.06, *_C), (19.50, 1.0, *_C),
                    (20.32, 1.1, *_C), (21.30, 1.02, *_C), (22.68, 1.0, *_C), (23.40, 1.05, *_C), (24.14, 1.0, *_C), (25.00, 1.06, *_C), (25.90, 1.0, *_C)])
SFX = [(0.0, "riser", -10), (0.45, "pop", -4), (0.5, "chime", -8), (1.04, "whoosh", -16), (2.92, "whoosh", -8), (3.25, "pop", -4),
       (3.47, "whoosh", -6), (3.8, "ding", -10), (4.95, "whoosh", -8), (5.28, "pop", -4), (5.45, "whoosh", -6)] + \
      [(5.75 + k * 0.18, "click", -8) for k in range(5)] + \
      [(7.46, "pop", -6), (8.5, "whoosh", -16), (9.70, "whoosh", -4), (9.88, "ding", -4), (10.48, "ding", -4), (12.04, "ding", -3),
       (12.78, "ding", -3), (13.48, "ding", -2), (14.30, "whoosh", -6), (14.85, "click", -4), (15.15, "pop", -4), (14.0, "riser", -8),
       (15.50, "impact", 0), (16.64, "whoosh", -6), (17.04, "pop", -6), (18.72, "pop", -8), (20.32, "pop", -8), (22.68, "whoosh", -6),
       (23.01, "pop", -4), (23.2, "whoosh", -6), (23.5, "impact", -6), (24.14, "chime", -4)]
