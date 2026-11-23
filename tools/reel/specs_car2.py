"""Car video 2 (现在的拍卖屋是新屋): same system as car1."""
import math, re, subprocess
from reel import Fn, spring_zoom, spring, clamp, ease_out, pill
from gfx import *
from specs3 import T, big_title, glass, cached, fade, firefly, card_pop, expand, title_el, GOLDB, ORANGE, NAVY
import specs_car1 as C1
from specs_car1 import sub_img, mid_card, num, house_card

DUR = 42.6; END = 39.8
BROLL = [(9.5, 14.2), (15.5, 20.0), (20.6, 24.1), (25.0, 29.9)]
SUBS = [(0.00, 1.25, "发展商卖[600千]"), (1.30, 2.90, "我买拍卖才[350千]"), (2.96, 3.60, "又是[新屋]"), (3.70, 4.50, "好还是不好？"),
        (4.58, 6.40, "最近看到很多[年轻一代]"), (6.42, 7.30, "一些投资者"), (7.38, 9.30, "不是买拍卖屋来[投资]"), (9.34, 9.50, "买来[自己住]"),
        (14.20, 15.50, "以前的拍卖屋"), (20.00, 20.60, "[没人住过]"), (24.10, 25.00, "开门进去 发展商送[冷气]"),
        (29.90, 31.20, "[新屋] 没人住过"), (31.34, 32.80, "你讲买拍卖屋[好不好]？"), (33.00, 34.10, "发展商卖[600千]"),
        (34.18, 35.75, "我买拍卖才[350千]"), (35.84, 36.55, "又是[新屋]"), (36.64, 37.40, "你讲好还是不好？"),
        (37.78, 38.90, "买拍卖屋[自己住]"), (39.00, 39.80, "[没问题]")]
def in_broll(t): return any(a <= t < b for a, b in BROLL)
def band(c, tl, t):
    if in_broll(t) or t >= END: return
    glass(c, (30, 1200, 1050, 1645), tint=(10, 30, 80), a=150, r=40)
    for a, b, s in SUBS:
        if a <= t < b: place(c, sub_img(s), W / 2, 1420, max(0.05, spring(t - a, 0.6, 18, 8)), clamp((t - a) / 0.06)); break
def board(t0, t1, title, draw):
    def f(c, tl, t):
        def d(cc):
            cc.alpha_composite(cached("board", blue_board))
            place(cc, cached(("bt", title), lambda: soft_shadow(T(title, 84))), W / 2, 330, max(0.05, spring(tl, 0.6, 16, 7)))
            draw(cc, tl, t)
        fade(c, clamp(tl / 0.12) * clamp((t1 - t) / 0.12), d)
    return Fn(t0, t1, f, z=9)
def photo(t, box):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", "src4/src.mp4", "-map", "0:v:0", "-frames:v", "1", "-vf", "scale=1080:1920",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return Image.frombuffer("RGB", (1080, 1920), raw).crop(box).convert("RGBA")
def price_block(c, t, ts):
    """ts: (t_dev, t_auc, t_new)"""
    L = (200, 210, 230)
    if t > ts[0]: place(c, cached("fz2", lambda: T("发展商", 40, L)), 250, 985); place(c, num("RM600K", 70, WHITE, False), 250, 1100, max(0.05, spring(t - ts[0], 0.4)))
    if t > ts[1]:
        q = clamp((t - ts[1]) / 0.3); ImageDraw.Draw(c).line((120, 1105, 120 + 260 * q, 1097), fill=ORANGE + (255,), width=8)
        place(c, cached("pm2", lambda: T("拍卖", 40, GOLDB)), 760, 985)
        place(c, num("RM350K", 100, GOLDB, (240, 200, 120)), 760, 1105, 1 + 0.8 * math.exp(-7 * (t - ts[1])) * math.cos(18 * (t - ts[1])))
    ImageDraw.Draw(c).line((500, 960, 500, 1205), fill=(255, 255, 255, 70), width=2)
    if t > ts[2]: place(c, pill("✓ 新屋", 40), 760, 1195, max(0.05, spring(t - ts[2], 0.3)))

def elements():
    E = [Fn(0, END, band, z=7)]
    E.append(mid_card(0.0, 4.50, lambda c, tl, t: price_block(c, t, (0.60, 2.22, 3.20))))
    E.append(title_el(3.70, 4.50, "好还是不好？", 110, 300))
    E.append(title_el(4.58, 9.50, "年轻一代", 110, 300))
    def young(c, tl, t):
        place(c, cached("tz", lambda: T("投资", 70, (200, 210, 230))), 300, 1040)
        if t > 7.38: q = clamp((t - 7.9) / 0.25); ImageDraw.Draw(c).line((220, 1045, 220 + 160 * q, 1040), fill=ORANGE + (255,), width=8)
        if t > 9.0: place(c, cached("zzz", lambda: glow(T("自己住 ✓", 80), 14, 1, BLUE)), 740, 1060, max(0.05, spring(t - 9.0, 0.4)))
        place(c, cached("vs", lambda: T("→", 70, (180, 200, 230), F_SANS)), 510, 1050)
    E.append(mid_card(6.42, 9.50, young))
    # B1 9.5–14.2 年轻一代：自己住 / 以前不一样
    def b1(c, tl, t):
        for k in range(10):
            r, q = divmod(k, 5); x = 220 + q * 160; y = 700 + r * 200; a = clamp((tl - 0.1 - k * 0.06) / 0.2)
            col = CYAN if k < 7 else WHITE
            ic = cached(("person", col), lambda: person_icon(150, col)); place(c, ic, x, y, max(0.05, spring(tl - 0.1 - k * 0.06, 0.3)), a)
        place(c, cached("b1a", lambda: glow(T("买来自己住的很多", 72), 12, 0.9, BLUE)), W / 2, 1170, 1, clamp((tl - 0.6) / 0.2))
        if t > 11.52: place(c, cached("b1b", lambda: T("现在的拍卖屋 ≠ 以前", 64, GOLDB)), W / 2, 1420, max(0.05, spring(t - 11.52, 0.5)))
    E.append(board(9.5, 14.2, "年轻一代的选择", b1))
    # B2 15.5–20.0 以前：烂烂的（用旧屋子照片做卡）
    OLD = cached("old", lambda: photo(16.5, (0, 150, 1080, 1180)).convert("L").convert("RGBA"))
    def b2(c, tl, t):
        def d(cc):
            ph = OLD.resize((800, 762)); m = Image.new("L", ph.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 799, 761), 34, fill=255)
            cc.paste(ph, (140, 480), m); ImageDraw.Draw(cc).rounded_rectangle((140, 480, 940, 1242), 34, outline=(255, 255, 255, 150), width=4)
        d(c)
        for k, (tt, s) in enumerate([(16.52, "烂烂的"), (17.38, "没屋顶"), (18.00, "没有床"), (18.82, "旧的")]):
            if t > tt: place(c, pill("× " + s, 52, fg=WHITE, bg=(200, 80, 50)), [300, 780, 300, 780][k], [620, 820, 1060, 1260][k], max(0.05, spring(t - tt, 0.3)), 1, [-6, 5, 4, -5][k])
    E.append(board(15.5, 20.0, "以前的拍卖屋", b2))
    # B3 20.6–24.1 现在：没人住过 / 最近买了几间
    def b3(c, tl, t):
        hc = house_card("现在 · 新屋"); place(c, hc, W / 2, 820, max(0.05, spring(tl, 0.3)))
        place(c, cached("mr", lambda: glow(T("很多没人住过 ✓", 70), 12, 0.9, BLUE)), W / 2, 1180, 1, clamp((tl - 0.3) / 0.2))
        if t > 22.56:
            for k in range(3):
                if t > 23.62 + k * 0.15: place(c, cached("hi", lambda: glow(house_icon(150, CYAN), 14, 1.2, BLUE)), 330 + k * 210, 1400, max(0.05, spring(t - 23.62 - k * 0.15, 0.2)))
    E.append(board(20.6, 24.1, "现在的拍卖屋", b3))
    E.append(mid_card(24.1, 25.0, lambda c, tl, t: (place(c, big_title("开门进去", 96), W / 2, 1020),
                                                   place(c, pill("✓ 冷气", 50), W / 2, 1165, max(0.05, spring(t - 25.62, 0.3)) if t > 25.62 else 0.05))))
    # B4 26.2–29.9 保持原状 清单
    def b4(c, tl, t):
        glass(c, (110, 520, 970, 1260), tint=(255, 255, 255), a=28)
        for k, (tt, s) in enumerate([(24.1, "发展商送的冷气"), (26.36, "壁橱"), (28.54, "整间保持原状"), (29.84, "新屋 · 没人住过")]):
            y = 620 + k * 160
            if t > max(tt, 25.1):
                sc = max(0.05, spring(t - max(tt, 25.1), 0.4))
                ImageDraw.Draw(c).ellipse((170, y - 40, 250, y + 40), fill=GOLDB + (255,)); place(c, cached("ck2", lambda: T("✓", 44, NAVY, F_SANS)), 210, y)
                place(c, cached(("l4", s), lambda: T(s, 64)), 300 + cached(("l4", s), lambda: T(s, 64)).width / 2 - 20, y, sc)
        place(c, cached("b4s", lambda: glow(T("跟新屋一样", 80, (130, 200, 255)), 14, 1, BLUE)), W / 2, 1440, 1, clamp((t - 28.6) / 0.2))
    E.append(board(25.0, 29.9, "开门进去……", b4))
    E.append(mid_card(29.9, 31.30, lambda c, tl, t: place(c, big_title("没人住过的新屋", 96), W / 2, 1080)))
    E.append(title_el(31.34, 33.0, "你讲好不好？", 110, 300))
    E.append(mid_card(33.0, 37.50, lambda c, tl, t: price_block(c, t, (33.30, 35.08, 35.94))))
    E.append(title_el(36.64, 37.50, "好还是不好？", 110, 300))
    E.append(mid_card(37.78, END, lambda c, tl, t: (place(c, big_title("自己住", 110), W / 2, 1040),
                                                   place(c, cached("mw2", lambda: T("✓ 没问题", 56, GOLDB, F_SANS)), W / 2, 1170, max(0.05, spring(t - 39.12, 0.4)) if t > 39.12 else 0.05))))
    def cta(c, tl, t):
        c.paste(c.filter(ImageFilter.GaussianBlur(min(18, tl * 60))))
        q = expand(c, tl, (W / 2, 1050), (110, 760, 970, 1340))
        if q > 0.9:
            place(c, cached("xf", lambda: T("下方留言", 80)), W / 2, 880)
            place(c, cached("pmb", lambda: glow(T("「拍卖」", 190), 30, 1.2, BLUE)), W / 2, 1060, max(0.05, 1 + 0.8 * math.exp(-7 * (tl - 0.35)) * math.cos(18 * (tl - 0.35))))
            if tl > 0.9: place(c, cached("jn", lambda: T("教你怎么买拍卖屋子", 54, GOLDB)), W / 2, 1240, max(0.05, spring(tl - 0.9, 0.4)))
    E.append(Fn(END, DUR, cta, z=10))
    return E

def person_icon(s, color):
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(img); c = color + (255,)
    d.ellipse((s * 0.32, s * 0.08, s * 0.68, s * 0.44), fill=c); d.rounded_rectangle((s * 0.18, s * 0.5, s * 0.82, s * 0.95), int(s * 0.2), fill=c)
    return glow(img, 10, 0.8, BLUE) if color == CYAN else img

_C = (600, 660)
_keys = [(0.0, 1.0, *_C)]; t = 0.9; k = 0
while t < END:
    if not in_broll(t): _keys.append((t, 1.06 if k % 2 == 0 else 1.0, *_C)); k += 1
    t += 1.0
_keys += [(2.22, 1.1, 600, 650), (3.0, 1.0, *_C), (35.08, 1.1, 600, 650), (35.9, 1.0, *_C), (END, 1.0, *_C)]
ZOOM = spring_zoom(_keys)
SHAKES = [(2.22, 10), (35.08, 10)]
SFX = ([(0.0, "riser-1s-soft", -6), (0.6, "pop-small-in", -2), (2.22, "data-decrease-short", -2), (2.22, "boom-hit-soft", -3), (3.2, "pop-medium-in", -2),
        (3.70, "whoosh-fast-soft", -6), (4.58, "pop-medium-in", -4), (7.9, "data-decrease-short", -4), (9.0, "tone-ding-mid", -4)] +
       [(9.5, "whoosh-medium-medium", 0)] + [(9.6 + k * 0.06, "pop-small-in", -8) for k in range(10)] + [(11.52, "pop-medium-in", -2)] +
       [(15.5, "whoosh-medium-medium", -2)] + [(tt, "click-snap-soft", -2) for tt in (16.52, 17.38, 18.0, 18.82)] +
       [(20.0, "whoosh-fast-soft", -4), (20.6, "whoosh-medium-medium", -2), (20.7, "shimmer-short-sparkle", -2)] + [(23.62 + k * 0.15, "pop-small-in", -2) for k in range(3)] +
       [(24.1, "whoosh-fast-soft", -4), (25.62, "tone-step-1", -2), (25.0, "whoosh-medium-medium", -2), (26.36, "tone-step-2", -2), (28.54, "tone-step-3", -2),
        (29.84, "tone-step-4", -2), (28.6, "shimmer-medium-soft", -4)] +
       [(29.9, "whoosh-fast-soft", -4), (31.34, "pop-medium-in", -4), (33.3, "pop-small-in", -2), (35.08, "data-decrease-short", -2), (35.08, "boom-hit-medium", 0),
        (35.94, "pop-medium-in", -2), (36.64, "pop-medium-in", -4), (37.78, "pop-medium-in", -4), (39.12, "tone-ding-high", -4)] +
       [(END, "whoosh-medium-medium", -2), (END + 0.35, "boom-hit-soft", -2), (END + 0.9, "sting-bright-short", -4)] +
       [(t, "whoosh-fast-soft", -14) for t, *_ in _keys[1:] if not in_broll(t)])
LOWCUT = [(a - 0.05, a + 0.25) for a, _ in BROLL] + [(END - 0.05, END + 0.3)]
