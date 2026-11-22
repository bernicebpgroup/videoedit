"""Extra looks: heavy fonts, deep shadow, neon glow captions, glass bubbles, VS graphic card."""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from reel import W, H, WHITE, GOLD, BLUEBG, GREY, clamp, spring, place, icon, El, Fn

FONT_DIR = os.environ.get("FONT_DIR", "fonts")
NOTO = "/usr/share/fonts/opentype/noto/"
FAMS = {   # name -> (path, ttc index, variation name)
    "serif_black": (f"{FONT_DIR}/NotoSerifSC-Black.ttf", 0, None),
    "serif_bold": (NOTO + "NotoSerifCJK-Bold.ttc", 2, None),
    "serif_light": (NOTO + "NotoSerifCJK-Regular.ttc", 2, None),
    "sans_black": (f"{FONT_DIR}/NotoSansSC-Black.ttf", 0, None),
    "sans_medium": (f"{FONT_DIR}/NotoSansSC-Medium.ttf", 0, None),
    "qingke": (f"{FONT_DIR}/ZCOOLQingKeHuangYou-Regular.ttf", 0, None),
    "brush": (f"{FONT_DIR}/MaShanZheng-Regular.ttf", 0, None),
}
_fc = {}
def ffont(fam, size):
    k = (fam, size)
    if k not in _fc:
        p, idx, var = FAMS[fam]; f = ImageFont.truetype(p, size, index=idx)
        if var: f.set_variation_by_name(var)
        _fc[k] = f
    return _fc[k]

def _glow(alpha, color, radius, strength):
    g = Image.new("RGBA", alpha.size, color + (0,)); g.putalpha(alpha.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: min(255, int(v * strength))))
    return g

def text2(text, size, fam="serif_black", color=WHITE, hl=GOLD, hl_scale=1.0, hl_fam=None,
          shadow="deep", neon=False, tracking=0):
    """'[..]' = highlight. shadow: 'deep' (dark, readable, no hard outline) | 'soft' | None.
    neon=True: highlighted parts get a bright core + coloured glow (fluorescent)."""
    import re
    parts = [(m, i % 2 == 1) for i, m in enumerate(re.split(r"\[|\]", text)) if m]
    fonts = [ffont(hl_fam or fam if h else fam, int(size * (hl_scale if h else 1))) for _, h in parts]
    asc = max(f.getmetrics()[0] for f in fonts); desc = max(f.getmetrics()[1] for f in fonts)
    widths = [f.getbbox(p)[2] - f.getbbox(p)[0] + tracking * len(p) for (p, _), f in zip(parts, fonts)]
    P = 60; Wd, Hd = sum(widths) + 2 * P, asc + desc + 2 * P
    base = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); hlm = Image.new("L", (Wd, Hd), 0)
    d = ImageDraw.Draw(base); dm = ImageDraw.Draw(hlm); x = P
    for (p, h), f, w in zip(parts, fonts, widths):
        y = P + asc - f.getmetrics()[0]; xx = x - f.getbbox(p)[0]
        for ch in p:
            fill = hl if h else color
            if h and neon: fill = tuple(int(c + (255 - c) * 0.55) for c in hl)   # neon core: near-white tint
            d.text((xx, y), ch, font=f, fill=fill)
            if h: dm.text((xx, y), ch, font=f, fill=255)
            xx += f.getlength(ch) + tracking
        x += w
    a = base.split()[3]; out = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0))
    if shadow == "deep":
        out.alpha_composite(_glow(a, (4, 8, 16), 22, 0.55), (0, 8))
        out.alpha_composite(_glow(a, (4, 8, 16), 7, 0.85), (0, 5))
    elif shadow == "soft":
        out.alpha_composite(_glow(a, (8, 12, 22), 16, 0.45), (0, 4))
    if neon:
        out.alpha_composite(_glow(hlm, hl, 30, 1.1)); out.alpha_composite(_glow(hlm, hl, 12, 1.6)); out.alpha_composite(_glow(hlm, hl, 4, 1.3))
    out.alpha_composite(base)
    return out

class Neon(El):
    """neon caption: spring pop + 'tube turning on' flicker in the first 0.3s."""
    def __init__(self, t0, t1, spr, cx, cy, out=0.12, z=3, alpha=1.0, behind=False):
        super().__init__(t0, t1, spr, cx, cy, "pop", out, 0, z, behind, alpha)
    def draw(self, c, t):
        if not (self.t0 <= t < self.t1): return
        a = t - self.t0; o = clamp((self.t1 - t) / self.out) * self.alpha
        fl = 1.0
        if a < 0.32: fl = [0.2, 1, 0.35, 1, 0.6, 1, 1, 1][min(7, int(a / 0.04))]
        p = spring(a, 0.4, 3.4); s = 0.5 + 0.5 * p
        place(c, self.spr, self.cx, self.cy + 40 * (1 - p), s, o * fl * clamp(a / 0.04))

def stack2(t0, t1, lines, cy, gap=-20, stagger=0.09, out=0.15, z=3):
    """lines: list of (sprite, neon?)."""
    E = []; hs = [sp.height - 120 for sp, _ in lines]; tot = sum(hs) + gap * (len(hs) - 1); y = cy - tot / 2
    for k, ((sp, ne), h) in enumerate(zip(lines, hs)):
        cls = Neon if ne else None
        e = Neon(t0 + k * stagger, t1, sp, W / 2, y + h / 2, out, z) if ne else El(t0 + k * stagger, t1, sp, W / 2, y + h / 2, "pop", out, z=z)
        E.append(e); y += h + gap
    return E

# ---------------- glass bubble ----------------
def bubble(t0, t1, cx, cy, top, big, sub=None, accent=WHITE, ic=None, glow=False, w=None, z=4, tilt=0):
    """floating frosted bubble: [icon] big value / small sub-label, optional coloured outline glow."""
    fb = ffont("sans_black", 60); fs = ffont("sans_medium", 30); ft = ffont("sans_medium", 28)
    bw = fb.getbbox(big)[2] - fb.getbbox(big)[0]; isz = 64 if ic else 0
    w = w or max(bw + isz + (24 if ic else 0) + 80, 300); h = 170 if sub else 130
    spr = Image.new("RGBA", (w + 80, h + 80), (0, 0, 0, 0)); d = ImageDraw.Draw(spr); ox, oy = 40, 40
    if glow:
        m = Image.new("L", spr.size, 0); ImageDraw.Draw(m).rounded_rectangle((ox, oy, ox + w, oy + h), 30, outline=255, width=6)
        spr.alpha_composite(_glow(m, accent, 16, 1.4))
    x = ox + 40
    if top: d.text((x, oy + 14), top, font=ft, fill=WHITE + (200,))
    yb = oy + (48 if top else 30)
    if ic: spr.alpha_composite(icon(ic, isz, accent), (x, yb + 6)); x += isz + 24
    d.text((x - fb.getbbox(big)[0], yb - 6), big, font=fb, fill=accent if glow else WHITE)
    if sub:
        sw = fs.getbbox(sub)[2] + 30
        d.rounded_rectangle((ox + w / 2 - sw / 2, oy + h - 48, ox + w / 2 + sw / 2, oy + h - 12), 16, fill=(255, 255, 255, 40))
        d.text((ox + w / 2 - sw / 2 + 15, oy + h - 48), sub, font=fs, fill=WHITE + (230,))
    border = accent if glow else (255, 255, 255)
    d.rounded_rectangle((ox, oy, ox + w, oy + h), 30, outline=border + (200 if glow else 120,), width=3 if glow else 2)
    return Bubble(t0, t1, w, h, cx, cy, spr, z, tilt)

class Bubble:
    def __init__(self, t0, t1, w, h, cx, cy, spr, z, tilt):
        self.t0, self.t1, self.w, self.h, self.cx, self.cy, self.spr, self.z, self.tilt = t0, t1, w, h, cx, cy, spr, z, tilt; self.behind = False
    def draw(self, c, t):
        if not (self.t0 <= t < self.t1): return
        a = t - self.t0; o = clamp((self.t1 - t) / 0.15) * clamp(a / 0.06)
        p = spring(a, 0.42, 3.2); s = 0.4 + 0.6 * p
        fy = 8 * math.sin(a * 2.4 + self.cx * 0.01)          # gentle float
        cy = self.cy + 60 * (1 - p) + fy
        w, h = int(self.w * s), int(self.h * s); x0, y0 = int(self.cx - w / 2), int(cy - h / 2)
        if w < 8 or x0 < 0 or y0 < 0 or x0 + w > W or y0 + h > H: place(c, self.spr, self.cx, cy, s, o, self.tilt); return
        reg = c.crop((x0, y0, x0 + w, y0 + h)).filter(ImageFilter.GaussianBlur(20))
        reg.alpha_composite(Image.new("RGBA", reg.size, (255, 255, 255, 34))); reg.alpha_composite(Image.new("RGBA", reg.size, (10, 20, 36, 70)))
        m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), int(30 * s), fill=int(255 * o))
        c.paste(reg, (x0, y0), m)
        place(c, self.spr, self.cx, cy, s, o, self.tilt)

# ---------------- VS graphic card ----------------
def placeholder_building(w, h):
    """stand-in until the real Arte Plus photo is supplied (frames/building.jpg)."""
    im = Image.new("RGB", (w, h)); d = ImageDraw.Draw(im)
    for y in range(h):
        k = y / h; d.line([(0, y), (w, y)], fill=(int(120 + 90 * k), int(160 + 60 * k), int(205 + 30 * k)))
    for bx, bw2, top in [(0.18, 0.28, 0.12), (0.52, 0.30, 0.18), (0.02, 0.12, 0.45), (0.86, 0.12, 0.5)]:
        x0, x1, y0 = int(w * bx), int(w * (bx + bw2)), int(h * top); d.rectangle((x0, y0, x1, h), fill=(34, 40, 52))
        for yy in range(y0 + 14, h, 22): d.line([(x0 + 6, yy), (x1 - 6, yy)], fill=(180, 70, 90) if bw2 > 0.2 else (70, 80, 96), width=4)
    return im

def load_photo(path, w, h):
    if os.path.exists(path):
        im = Image.open(path).convert("RGB"); r = max(w / im.width, h / im.height)
        im = im.resize((int(im.width * r + 1), int(im.height * r + 1)), Image.LANCZOS)
        x0, y0 = (im.width - w) // 2, (im.height - h) // 2; return im.crop((x0, y0, x0 + w, y0 + h)), True
    return placeholder_building(w, h), False

def vs_card(t0, t1, photo="frames/building.jpg", z=6):
    """full-screen graphic: building photo top, neon title, VS badge, two price slips (新房 vs 拍卖)."""
    ph, real = load_photo(photo, W, 1150)
    def draw(c, tl, t):
        o = clamp(tl / 0.12) * clamp((t1 - t) / 0.2)
        if o <= 0: return
        g = Image.new("RGBA", (W, H), (10, 16, 28, 255))
        zoom = 1.0 + 0.04 * tl; pw, phh = int(W * zoom), int(1150 * zoom)
        g.paste(ph.resize((pw, phh)).crop(((pw - W) // 2, 0, (pw - W) // 2 + W, 1150)), (0, 0))
        fade = Image.new("L", (1, 1150)); [fade.putpixel((0, y), int(255 * clamp((y - 700) / 450))) for y in range(1150)]
        g.paste(Image.new("RGBA", (W, 1150), (10, 16, 28, 255)), (0, 0), fade.resize((W, 1150)))
        c.alpha_composite(Image.blend(c, g, 1.0) if o >= 1 else Image.blend(c.copy(), g, o))
        # title
        p = spring(tl - 0.1, 0.45, 3.2)
        place(c, TITLE1, W / 2, 330 + 30 * (1 - p), 0.6 + 0.4 * p, clamp((tl - 0.1) / 0.05) * o)
        p2 = spring(tl - 0.22, 0.4, 3.4); fl = [0.2, 1, 0.4, 1, 1][min(4, int(max(0, tl - 0.22) / 0.05))]
        place(c, TITLE2, W / 2, 470 + 30 * (1 - p2), 0.5 + 0.5 * p2, clamp((tl - 0.22) / 0.04) * fl * o)
        # slips
        for k, (sp, cx, ang, td) in enumerate([(SLIP_L, 280, -5, 0.45), (SLIP_R, 800, 5, 0.6)]):
            q = spring(tl - td, 0.5, 2.8)
            place(c, sp, cx, 1500 + 400 * (1 - q), 1, clamp((tl - td) / 0.05) * o, ang)
        q = spring(tl - 0.8, 0.35, 3.6)
        place(c, VS, W / 2, 1230, 0.2 + 0.8 * q, clamp((tl - 0.8) / 0.04) * o, -10 * (1 - q))
        if not real: place(c, NOTE, W / 2, 1880, 1, 0.6 * o)
    TITLE1 = text2("这一个 Arte Plus", 70, "sans_black", shadow="deep")
    TITLE2 = text2("[新房 VS 拍卖]", 150, "sans_black", hl=(150, 205, 255), shadow="deep", neon=True)
    def slip(title, price, accent, mark):
        s = Image.new("RGBA", (440, 330), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
        sh = Image.new("L", s.size, 0); ImageDraw.Draw(sh).rounded_rectangle((14, 20, 426, 320), 24, fill=150)
        s.alpha_composite(_glow(sh, (0, 0, 0), 14, 1.0))
        d.rounded_rectangle((10, 10, 420, 310), 24, fill=(248, 248, 246, 255))
        d.rounded_rectangle((10, 10, 420, 80), 24, fill=accent + (255,)); d.rectangle((10, 50, 420, 80), fill=accent + (255,))
        d.text((36, 18), title, font=ffont("sans_black", 40), fill=WHITE)
        d.text((36, 110), "价格", font=ffont("sans_medium", 30), fill=(90, 96, 110))
        d.text((36, 150), price, font=ffont("sans_black", 66), fill=(20, 26, 40))
        d.text((36, 250), mark, font=ffont("sans_medium", 30), fill=accent)
        return s
    SLIP_L = slip("新房", "RM600多千", (120, 130, 150), "市场价")
    SLIP_R = slip("拍卖", "RM280千", BLUEBG, "✓ 得标价")
    VS = Image.new("RGBA", (230, 230), (0, 0, 0, 0)); dv = ImageDraw.Draw(VS)
    m = Image.new("L", VS.size, 0); ImageDraw.Draw(m).ellipse((25, 25, 205, 205), fill=255); VS.alpha_composite(_glow(m, (0, 0, 0), 12, 0.9))
    dv.ellipse((25, 25, 205, 205), fill=WHITE, outline=(20, 26, 40), width=6)
    fv = ffont("sans_black", 90); b = fv.getbbox("VS"); dv.text((115 - (b[2] - b[0]) / 2 - b[0], 115 - (b[3] - b[1]) / 2 - b[1]), "VS", font=fv, fill=(20, 26, 40))
    NOTE = text2("（占位图：请提供 Arte Plus 大楼照片）", 30, "sans_medium", shadow="soft")
    return Fn(t0, t1, draw, z=z)

# ---------------- Instagram safe zone ----------------
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT, SAFE_LEFT = 270, 1500, 950, 60   # keep text inside (IG header / caption+buttons / action rail)

def safe_overlay(c):
    """debug overlay: shade the IG UI zones."""
    o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(o)
    for box in [(0, 0, W, SAFE_TOP), (0, SAFE_BOTTOM, W, H), (SAFE_RIGHT, SAFE_TOP, W, SAFE_BOTTOM)]:
        d.rectangle(box, fill=(255, 40, 40, 70))
    d.rectangle((SAFE_LEFT, SAFE_TOP, SAFE_RIGHT, SAFE_BOTTOM), outline=(80, 255, 120, 220), width=4)
    c.alpha_composite(o)

# ---------------- impact caption (震撼) ----------------
def _tint(spr, col):
    t = Image.new("RGBA", spr.size, col + (0,)); t.putalpha(spr.split()[3]); return t

class Impact:
    """slam caption: drops in from 3x with motion-trail ghosts, RGB split + shockwave ring + white flash on landing,
    then a light sweep across the letters. Pair with an impact SFX + screen shake at t0 + LAND."""
    LAND = 0.14
    def __init__(self, t0, t1, spr, cx, cy, z=5, flash=True, ring=GOLD, out=0.15):
        self.t0, self.t1, self.spr, self.cx, self.cy, self.z, self.flash, self.ring, self.out = t0, t1, spr, cx, cy, z, flash, ring, out
        self.behind = False; self.r = _tint(spr, (255, 40, 80)); self.b = _tint(spr, (40, 220, 255))
        m = spr.split()[3]; self.mask = m
    def draw(self, c, t):
        if not (self.t0 <= t < self.t1): return
        a = t - self.t0; o = clamp((self.t1 - t) / self.out); L = self.LAND
        if a < L:                                    # falling: 3x -> 1x with ghost trail
            k = a / L; s = 3.0 - 2.0 * k ** 2
            for g in range(4, 0, -1):
                sg = 3.0 - 2.0 * max(0, k - g * 0.06) ** 2
                place(c, self.spr, self.cx, self.cy, sg, 0.12 * clamp(k * 3) * o)
            place(c, self.spr, self.cx, self.cy, s, clamp(k * 4) * o); return
        b = a - L
        if b < 0.5:                                  # shockwave ring
            r = 80 + 900 * (1 - (1 - b / 0.5) ** 3); w = max(2, int(26 * (1 - b / 0.5)))
            ring = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse((self.cx - r, self.cy - r * 0.55, self.cx + r, self.cy + r * 0.55), outline=self.ring + (int(200 * (1 - b / 0.5)),), width=w)
            c.alpha_composite(ring.filter(ImageFilter.GaussianBlur(2)))
        if self.flash and b < 0.12:                  # white flash
            c.alpha_composite(Image.new("RGBA", (W, H), (255, 255, 255, int(150 * (1 - b / 0.12)))))
        s = 1 + 0.12 * math.exp(-b * 9) * math.cos(b * 30)     # settle wobble
        sp = max(0.0, 1 - b / 0.35); off = int(18 * sp)          # RGB split decays
        if off: place(c, self.r, self.cx - off, self.cy, s, 0.7 * o); place(c, self.b, self.cx + off, self.cy, s, 0.7 * o)
        place(c, self.spr, self.cx, self.cy, s, o)
        if 0.15 < b < 0.75:                          # light sweep
            q = (b - 0.15) / 0.6; sw = Image.new("L", self.spr.size, 0); x = int(-200 + (self.spr.width + 400) * q)
            ImageDraw.Draw(sw).polygon([(x, 0), (x + 90, 0), (x - 30, self.spr.height), (x - 120, self.spr.height)], fill=210)
            sw = Image.composite(sw.filter(ImageFilter.GaussianBlur(14)), Image.new("L", sw.size, 0), self.mask)
            hi = Image.new("RGBA", self.spr.size, (255, 255, 255, 0)); hi.putalpha(sw)
            place(c, hi, self.cx, self.cy, s, o)

# ---------------- price drop (跳楼价) ----------------
def price_drop(t0, t_mid, t_crash, t1, start=600, mid=500, end=280, cy=1060, label="Arte Plus 价格", unit=1000):
    """glass board: price line chart that holds at `start`, steps to `mid`, then plunges off a cliff to `end`;
    big counter rolls down with it; 'jumped-off-a-building' crash = shake/RGB split; savings stamp lands after."""
    PW, PH = 840, 720; x0, y0 = W / 2 - PW / 2, cy - PH / 2
    fN = ffont("sans_black", 120); fL = ffont("sans_medium", 44); fS = ffont("sans_black", 46)
    def val(t):
        if t < t_mid: return start
        if t < t_mid + 0.5: return start + (mid - start) * spring(t - t_mid, 0.9, 2.0)
        if t < t_crash: return mid
        k = clamp((t - t_crash) / 0.55); return mid + (end - mid) * (1 - (1 - k) ** 3)
    stamp = text2(f"[便宜 RM{(start - end) * unit:,}]", 80, "sans_black", hl=(255, 214, 80), neon=True, shadow="deep")
    gx0, gx1, gy_top, gy_bot = x0 + 70, x0 + PW - 70, y0 + 300, y0 + PH - 60
    ymap = lambda v: gy_top + (start - v) / (start - end) * (gy_bot - gy_top)
    def draw(c, tl, t):
        o = clamp(tl / 0.1) * clamp((t1 - t) / 0.2)
        if o <= 0: return
        # glass board
        p = spring(tl, 0.5, 3.0); bx = (int(x0), int(y0 + 40 * (1 - p)), int(x0 + PW), int(y0 + PH + 40 * (1 - p)))
        reg = c.crop(bx).filter(ImageFilter.GaussianBlur(22)); reg.alpha_composite(Image.new("RGBA", reg.size, (12, 20, 36, 150)))
        m = Image.new("L", reg.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, reg.width - 1, reg.height - 1), 36, fill=int(255 * o)); c.paste(reg, bx[:2], m)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov); dy = bx[1] - y0
        d.rounded_rectangle(bx, 36, outline=(255, 255, 255, int(110 * o)), width=2)
        d.text((x0 + 60, y0 + 40 + dy), label, font=fL, fill=(200, 210, 225, int(255 * o)))
        v = val(t); crashing = t >= t_crash and t < t_crash + 0.55; landed = t >= t_crash + 0.55
        col = (255, 70, 80) if crashing else ((120, 195, 255) if landed else WHITE)
        num = f"RM{int(round(v)) * unit:,}"
        # chart: polyline up to now
        pts = []; T0 = t0 + 0.2
        def tx(tt):   # x position: hold+step take 55% of width, the crash the last 45% (steep cliff)
            if tt < t_crash: return gx0 + (gx1 - gx0) * 0.55 * (tt - T0) / (t_crash - T0)
            return gx0 + (gx1 - gx0) * (0.55 + 0.45 * clamp((tt - t_crash) / 0.55) ** 2.5)
        for i in range(0, 141):
            tt = T0 + (t_crash + 0.55 - T0) * i / 140
            if tt > t: break
            pts.append((tx(tt), ymap(val(tt)) + dy))
        if len(pts) > 1:
            gl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(gl).line(pts, fill=col + (255,), width=14, joint="curve")
            ov.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10))); d.line(pts, fill=col + (int(255 * o),), width=7, joint="curve")
            ex, ey = pts[-1]; d.ellipse((ex - 12, ey - 12, ex + 12, ey + 12), fill=WHITE + (int(255 * o),))
            if crashing:    # falling arrow head
                d.polygon([(ex - 26, ey - 10), (ex + 26, ey - 10), (ex, ey + 34)], fill=col + (int(255 * o),))
        # dashed reference at start price
        for xx in range(int(gx0), int(gx1), 28): d.line([(xx, ymap(start) + dy), (xx + 14, ymap(start) + dy)], fill=(255, 255, 255, int(70 * o)), width=2)
        c.alpha_composite(ov)
        # big counter (shakes + RGB split while crashing)
        sx = int(14 * math.sin(t * 90)) if crashing else 0
        spr = text2(num, 120, "sans_black", color=col, shadow="deep")
        if crashing:
            place(c, _tint(spr, (255, 40, 80)), W / 2 - 14 + sx, y0 + 175 + dy, 1, 0.6 * o); place(c, _tint(spr, (40, 220, 255)), W / 2 + 14 + sx, y0 + 175 + dy, 1, 0.6 * o)
        if landed:
            q = t - (t_crash + 0.55); s2 = 1 + 0.18 * math.exp(-q * 8) * math.cos(q * 28)
            place(c, text2(f"[{num}]", 120, "sans_black", hl=(120, 195, 255), neon=True), W / 2, y0 + 175 + dy, s2, o)
        else:
            place(c, spr, W / 2 + sx, y0 + 175 + dy, 1, o)
        # savings stamp
        ts = t_crash + 0.75
        if t >= ts:
            q = t - ts; s3 = 2.6 - 1.6 * spring(q, 0.4, 3.4)
            place(c, stamp, W / 2 + 40, y0 - 30 + dy, s3, clamp(q / 0.05) * o, -6)
    return Fn(t0, t1, draw, z=6)
