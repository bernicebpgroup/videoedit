"""Graphic kit v2: no-stroke translucent blue glow text, display numerals, blue property board, firefly orb -> card."""
import math, os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
W, H = 1080, 1920
_D = os.path.dirname(os.path.abspath(__file__)) + "/../fonts"
F_NUM = _D + "/pkg_fontsource-montserrat/files/montserrat-latin-900-normal.woff"
F_ANTON = _D + "/pkg_fontsource-anton/files/anton-latin-400-normal.woff"
F_SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
F_SANS = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
BLUE = (64, 150, 255); BLUE_D = (12, 64, 190); CYAN = (130, 210, 255); WHITE = (255, 255, 255)
_fc = {}
def font(path, size):
    k = (path, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(path, size, index=2 if path.endswith(".ttc") else 0)
    return _fc[k]
def is_num(ch): return ch.isascii()

def text_layer(text, size, color, fpath=None, num_path=F_NUM, alpha=255, track=0):
    """Mixed text: ASCII (numbers/latin) uses display font, CJK uses serif. Returns RGBA tight image."""
    runs = []
    for ch in text:
        fp = num_path if is_num(ch) and ch != " " else (fpath or F_SERIF)
        f = font(fp, int(size * (1.12 if fp == num_path else 1)))
        runs.append((ch, f))
    asc = max(f.getmetrics()[0] for _, f in runs); dsc = max(f.getmetrics()[1] for _, f in runs)
    widths = [f.getlength(c) + track for c, f in runs]
    pad = int(size * 0.35)
    img = Image.new("RGBA", (int(sum(widths)) + 2 * pad, asc + dsc + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(img); x = pad
    for (c, f), w in zip(runs, widths):
        d.text((x, pad + asc - f.getmetrics()[0]), c, font=f, fill=color + (alpha,)); x += w
    return img

def glow(img, radius=18, strength=1.6, color=None):
    """Add soft outer glow (no black stroke)."""
    a = img.split()[3]
    g = a.filter(ImageFilter.GaussianBlur(radius)).point(lambda v: min(255, int(v * strength)))
    col = Image.new("RGBA", img.size, (color or BLUE) + (0,)); col.putalpha(g)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.alpha_composite(col); out.alpha_composite(img); return out

def soft_shadow(img, radius=10, op=0.45, dy=4):
    a = img.split()[3].filter(ImageFilter.GaussianBlur(radius)).point(lambda v: int(v * op))
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sh.putalpha(a)
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.alpha_composite(sh, (0, dy)); out.alpha_composite(img); return out

def glass_text(text, size, alpha=215, fpath=None):
    """Semi-transparent blue text with light inner gradient + glow. No outline."""
    base = text_layer(text, size, BLUE, fpath, alpha=255)
    w, h = base.size; grad = Image.new("RGBA", (w, h))
    gp = np.zeros((h, w, 4), np.uint8); t = np.linspace(0, 1, h)[:, None]
    gp[..., 0] = (150 * (1 - t) + 40 * t); gp[..., 1] = (215 * (1 - t) + 120 * t); gp[..., 2] = 255
    gp[..., 3] = (np.array(base.split()[3]).astype(np.float32) * alpha / 255).astype(np.uint8)
    grad = Image.fromarray(gp, "RGBA")
    return glow(grad, int(size * 0.12), 1.2, BLUE)

def sub_text(text, size=66):
    """Subtitle: white, no outline, soft shadow; [..] keywords in translucent glowing blue."""
    import re
    parts = [(m, i % 2 == 1) for i, m in enumerate(re.split(r"\[|\]", text)) if m]
    imgs = [glass_text(p, size, 235) if hl else soft_shadow(text_layer(p, size, WHITE)) for p, hl in parts]
    h = max(i.height for i in imgs); pad = int(size * 0.35)
    out = Image.new("RGBA", (sum(i.width - 2 * pad for i in imgs) + 2 * pad, h), (0, 0, 0, 0)); x = 0
    for i in imgs: out.alpha_composite(i, (x, (h - i.height) // 2)); x += i.width - 2 * pad
    return out

# ---------- icons ----------
def house_icon(s=160, color=WHITE, fill_alpha=255):
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(img); c = color + (fill_alpha,)
    m = s * 0.08; roof = [(s / 2, m), (s - m, s * 0.45), (m, s * 0.45)]
    d.polygon(roof, fill=c); d.rounded_rectangle((s * 0.18, s * 0.42, s * 0.82, s - m), int(s * 0.05), fill=c)
    hole = (0, 0, 0, 0)
    d.rounded_rectangle((s * 0.43, s * 0.62, s * 0.57, s - m), int(s * 0.03), fill=hole)
    for x0 in (0.26, 0.62):
        d.rectangle((s * x0, s * 0.52, s * (x0 + 0.12), s * 0.62), fill=hole)
    return img

def building_icon(s=160, color=WHITE):
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(img); c = color + (255,)
    d.rounded_rectangle((s * 0.22, s * 0.1, s * 0.78, s * 0.92), int(s * 0.04), fill=c)
    for r in range(5):
        for k in range(3):
            x = s * (0.3 + k * 0.16); y = s * (0.18 + r * 0.13)
            d.rectangle((x, y, x + s * 0.09, y + s * 0.07), fill=(0, 0, 0, 0))
    return img

# ---------- backgrounds ----------
def blue_board():
    y = np.linspace(0, 1, H)[:, None]; x = np.linspace(0, 1, W)[None, :]
    r = np.sqrt((x - 0.5) ** 2 + ((y - 0.38) * 0.6) ** 2)
    base = np.stack([np.full((H, W), 8.), np.full((H, W), 40.), np.full((H, W), 140.)], -1)
    hi = np.array([40, 130, 255.]); k = np.clip(1 - r * 1.6, 0, 1)[..., None] ** 1.5
    img = base * (1 - k) + hi * k
    arr = np.dstack([img.astype(np.uint8), np.full((H, W), 255, np.uint8)])
    bg = Image.fromarray(arr, "RGBA"); d = ImageDraw.Draw(bg)
    for gx in range(0, W, 90): d.line((gx, 0, gx, H), fill=(255, 255, 255, 14), width=1)
    for gy in range(0, H, 90): d.line((0, gy, W, gy), fill=(255, 255, 255, 14), width=1)
    return bg

# ---------- firefly ----------
def orb(r=46, color=CYAN):
    s = r * 6; img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    yy, xx = np.mgrid[0:s, 0:s]; d = np.sqrt((xx - s / 2) ** 2 + (yy - s / 2) ** 2) / r
    a = np.clip(np.exp(-d ** 2 * 0.9) * 255 + np.exp(-d * 0.9) * 120, 0, 255)
    core = np.clip((1 - d) * 3, 0, 1)
    rgb = np.stack([color[0] + (255 - color[0]) * core, color[1] + (255 - color[1]) * core, np.full_like(core, 255.)], -1)
    return Image.fromarray(np.dstack([rgb, a]).astype(np.uint8), "RGBA")

def firefly(c, p0, p1, prog, trail=14, size=40):
    """Draw orb moving along a curved path from p0 to p1 with fading trail + sparkles. prog 0..1."""
    def pt(u):
        u = max(0, min(1, u)); cx = (p0[0] + p1[0]) / 2 + 160; cy = min(p0[1], p1[1]) - 220
        x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * cx + u * u * p1[0]; y = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * cy + u * u * p1[1]; return x, y
    rng = np.random.default_rng(3)
    for k in range(trail, 0, -1):
        u = prog - k * 0.035
        if u < 0: continue
        x, y = pt(u); o = orb(max(6, int(size * (1 - k / trail) * 0.7)))
        a = o.split()[3].point(lambda v: int(v * (1 - k / trail) * 0.6)); o.putalpha(a)
        c.alpha_composite(o, (int(x - o.width / 2), int(y - o.height / 2)))
        for _ in range(2):
            sx, sy = x + rng.normal(0, 25), y + rng.normal(0, 25); rr = rng.uniform(2, 5)
            ImageDraw.Draw(c).ellipse((sx - rr, sy - rr, sx + rr, sy + rr), fill=(200, 235, 255, int(200 * (1 - k / trail))))
    x, y = pt(prog); o = orb(size); c.alpha_composite(o, (int(x - o.width / 2), int(y - o.height / 2)))
    return x, y

def card(photo, label, w=360, h=420):
    """Rounded photo card with blue glow edge + label."""
    ph = photo.copy(); ph = ph.resize((w, int(w * ph.height / ph.width)))
    top = (ph.height - h) // 2 if ph.height > h else 0; ph = ph.crop((0, top, w, top + h))
    cd = Image.new("RGBA", (w, h), (0, 0, 0, 0)); m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), 34, fill=255); cd.paste(ph.convert("RGBA"), (0, 0), m)
    grad = Image.new("RGBA", (w, h), (0, 0, 0, 0)); gd = ImageDraw.Draw(grad)
    for i in range(160): gd.line((0, h - i, w, h - i), fill=(6, 30, 90, int(220 * (1 - i / 160))))
    cd.alpha_composite(Image.composite(grad, Image.new("RGBA", (w, h), (0, 0, 0, 0)), m))
    lt = text_layer(label, 46, WHITE, F_SANS); cd.alpha_composite(lt, ((w - lt.width) // 2, h - lt.height + 4))
    ImageDraw.Draw(cd).rounded_rectangle((1, 1, w - 2, h - 2), 34, outline=CYAN + (230,), width=4)
    out = Image.new("RGBA", (w + 120, h + 120), (0, 0, 0, 0)); ga = Image.new("L", out.size, 0)
    ImageDraw.Draw(ga).rounded_rectangle((60, 60, 60 + w, 60 + h), 34, fill=200); ga = ga.filter(ImageFilter.GaussianBlur(26))
    gl = Image.new("RGBA", out.size, BLUE + (0,)); gl.putalpha(ga); out.alpha_composite(gl); out.alpha_composite(cd, (60, 60)); return out

def place(c, spr, cx, cy, scale=1.0, alpha=1.0, angle=0):
    if scale != 1: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BICUBIC)
    if angle: spr = spr.rotate(angle, Image.BICUBIC, expand=True)
    if alpha < 1: spr = spr.copy(); spr.putalpha(spr.split()[3].point(lambda v: int(v * alpha)))
    c.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))
