"""Reel style engine: neon ribbon, keyword pops, film-strip cards, UI cards, circle-crop mode, audio bars."""
import math, subprocess, sys, json
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
NEON = (212, 242, 58)        # yellow-green accent
NEON_D = (150, 178, 30)
NEON_L = (240, 255, 170)
INK = (24, 26, 22)
PAPER = (238, 240, 230)

F_LAT = '/usr/share/fonts/truetype/google-fonts/ofl/crimsontext/CrimsonText-BoldItalic.ttf'
F_CJK = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc'
F_UI = '/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
F_UIB = '/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf'
F_CJK_SANS = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
F_CJK_SANS_M = '/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc'

_fc = {}
def font(path, size, index=None):
    k = (path, size, index)
    if k not in _fc:
        if index is None and path.endswith('.ttc'): index = 2  # SC
        _fc[k] = ImageFont.truetype(path, size, index=index or 0)
    return _fc[k]

def is_cjk(s): return any('　' <= c <= '鿿' or '＀' <= c <= '￯' for c in s)

# ---------- easing ----------
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x): x = clamp(x); return 3 * x * x - 2 * x * x * x
def back_out(x, s=1.9):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def pop(t, t0, t1, dur=0.28, out=0.22):
    """scale/alpha envelope for an element visible in [t0,t1]"""
    if t < t0 or t > t1: return 0., 0.
    a = clamp((t - t0) / 0.12) * clamp((t1 - t) / out)
    s = back_out((t - t0) / dur) * (0.85 + 0.15 * clamp((t1 - t) / out))
    return s, a

# ---------- sprite helpers ----------
def shadowed(img, blur=18, off=(0, 14), alpha=0.28, pad=40):
    """add soft drop shadow to RGBA sprite"""
    w, h = img.size
    out = Image.new('RGBA', (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh = Image.new('RGBA', out.size, (0, 0, 0, 0))
    a = img.split()[3].point(lambda v: int(v * alpha))
    blk = Image.new('RGBA', img.size, (0, 0, 0, 255)); blk.putalpha(a)
    sh.paste(blk, (pad + off[0], pad + off[1]), blk)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out = Image.alpha_composite(sh, out)
    out.alpha_composite(img, (pad, pad))
    return out

def text_sprite(txt, size, color=NEON, italic=True, stroke=0, stroke_col=INK, font_path=None, shear=0.22):
    fp = font_path or (F_CJK if is_cjk(txt) else F_LAT)
    f = font(fp, size)
    bb = f.getbbox(txt, stroke_width=stroke)
    w, h = bb[2] - bb[0] + 20, bb[3] - bb[1] + 20
    pad = int(h * shear) + 10 if (italic and is_cjk(txt)) else 10
    im = Image.new('RGBA', (w + pad * 2, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.text((pad + 10 - bb[0], 10 - bb[1]), txt, font=f, fill=color + (255,), stroke_width=stroke, stroke_fill=stroke_col + (255,))
    if italic and is_cjk(txt):  # synthetic italic for CJK
        im = im.transform(im.size, Image.AFFINE, (1, shear, -shear * h * 0.5, 0, 1, 0), Image.BICUBIC)
    return im.crop(im.getbbox())

def rounded(w, h, r, fill, outline=None, width=0):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), r, fill=fill, outline=outline, width=width)
    return im

def pill(txt, size=34, bg=(255, 255, 255), fg=INK, dot=NEON, pad=26):
    f = font(F_CJK_SANS_M if is_cjk(txt) else F_UI, size)
    bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    hh = th + pad * 2 - 6; dotr = hh // 4
    w = tw + pad * 2 + (dotr * 2 + 16 if dot else 0)
    im = rounded(w, hh, hh // 2, bg + (255,))
    d = ImageDraw.Draw(im); x = pad
    if dot:
        d.ellipse((x, hh // 2 - dotr, x + dotr * 2, hh // 2 + dotr), fill=dot + (255,)); x += dotr * 2 + 16
    d.text((x - bb[0], (hh - th) // 2 - bb[1]), txt, font=f, fill=fg + (255,))
    return shadowed(im, 14, (0, 8), 0.25, 30)

# ---------- icons ----------
def icon(kind, s=120, col=INK):
    S = s * 4
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lw = S // 14; c = col + (255,)
    if kind == 'pin':
        d.ellipse((S*.22, S*.08, S*.78, S*.64), outline=c, width=lw)
        d.polygon([(S*.27, S*.5), (S*.73, S*.5), (S*.5, S*.92)], fill=c)
        d.ellipse((S*.22+lw, S*.08+lw, S*.78-lw, S*.64-lw), fill=(0, 0, 0, 0))
        d.ellipse((S*.40, S*.26, S*.60, S*.46), fill=c)
    elif kind == 'house':
        d.polygon([(S*.5, S*.12), (S*.9, S*.48), (S*.1, S*.48)], fill=c)
        d.rectangle((S*.2, S*.46, S*.8, S*.88), fill=c)
        d.rectangle((S*.42, S*.62, S*.58, S*.88), fill=(0, 0, 0, 0))
    elif kind == 'search':
        d.ellipse((S*.12, S*.12, S*.66, S*.66), outline=c, width=lw)
        d.line((S*.58, S*.58, S*.88, S*.88), fill=c, width=int(lw * 1.4))
    elif kind == 'gavel':
        d.rounded_rectangle((S*.18, S*.18, S*.62, S*.40), 12, fill=c)
        d.line((S*.40, S*.30, S*.82, S*.78), fill=c, width=lw)
        d.rectangle((S*.12, S*.82, S*.62, S*.9), fill=c)
    elif kind == 'doc':
        d.rounded_rectangle((S*.22, S*.1, S*.78, S*.9), 20, outline=c, width=lw)
        for y in (.32, .5, .68): d.line((S*.34, S*y, S*.66, S*y), fill=c, width=lw // 2)
    elif kind == 'money':
        d.ellipse((S*.12, S*.12, S*.88, S*.88), outline=c, width=lw)
        f = font(F_UIB, int(S * .5)); d.text((S * .5, S * .52), '$', font=f, fill=c, anchor='mm')
    elif kind == 'web':
        d.ellipse((S*.12, S*.12, S*.88, S*.88), outline=c, width=lw)
        d.ellipse((S*.34, S*.12, S*.66, S*.88), outline=c, width=lw // 2)
        d.line((S*.12, S*.5, S*.88, S*.5), fill=c, width=lw // 2)
    elif kind == 'check':
        d.line([(S*.18, S*.52), (S*.42, S*.76), (S*.84, S*.26)], fill=c, width=lw, joint='curve')
    elif kind == 'people':
        d.ellipse((S*.36, S*.12, S*.64, S*.4), fill=c)
        d.pieslice((S*.2, S*.46, S*.8, S*1.1), 180, 360, fill=c)
    return im.resize((s, s), Image.LANCZOS)

def card(kind, label, w=230, h=270):
    im = rounded(w, h, 34, (255, 255, 255, 250))
    d = ImageDraw.Draw(im)
    cr = 66; cx = w // 2; cy = 100
    d.ellipse((cx - cr, cy - cr, cx + cr, cy + cr), fill=NEON + (255,))
    ic = icon(kind, 78); im.alpha_composite(ic, (cx - 39, cy - 39))
    f = font(F_CJK_SANS_M if is_cjk(label) else F_UIB, 30)
    d.text((cx, 214), label, font=f, fill=INK + (255,), anchor='mm')
    return shadowed(im, 20, (0, 14), 0.3, 40)

def filmstrip(w, h, inner=None):
    im = rounded(w, h, 18, (22, 24, 20, 240))
    d = ImageDraw.Draw(im)
    hole_w, hole_h, gap = 22, 14, 18
    for x in range(14, w - 14, hole_w + gap):
        for y in (10, h - 10 - hole_h):
            d.rounded_rectangle((x, y, x + hole_w, y + hole_h), 3, fill=(235, 235, 225, 255))
    if inner is not None:
        iw, ih = w - 24, h - 2 * (hole_h + 22)
        inn = inner.resize((iw, ih)).convert('RGBA')
        m = Image.new('L', (iw, ih), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, iw - 1, ih - 1), 8, fill=255)
        im.paste(inn, (12, hole_h + 22), m)
    return shadowed(im, 22, (0, 16), 0.35, 44)

# ---------- compositing ----------
def to_np(sprite): return np.asarray(sprite, dtype=np.uint8)

def blit(dst, spr, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    """alpha-composite RGBA numpy sprite centred at (cx,cy) onto dst (float32 HxWx3)"""
    if alpha <= 0.003 or scale <= 0.01: return
    h, w = spr.shape[:2]
    if abs(scale - 1) > 1e-3 or abs(rot) > 1e-3:
        M = cv2.getRotationMatrix2D((w / 2, h / 2), rot, scale)
        nw, nh = int(w * scale * 1.0 + abs(math.sin(math.radians(rot))) * h * scale) + 4, int(h * scale + abs(math.sin(math.radians(rot))) * w * scale) + 4
        M[0, 2] += nw / 2 - w / 2; M[1, 2] += nh / 2 - h / 2
        spr = cv2.warpAffine(spr, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        h, w = nh, nw
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    sx0, sy0 = max(0, -x0), max(0, -y0)
    dx0, dy0 = max(0, x0), max(0, y0)
    dx1, dy1 = min(dst.shape[1], x0 + w), min(dst.shape[0], y0 + h)
    if dx1 <= dx0 or dy1 <= dy0: return
    s = spr[sy0:sy0 + dy1 - dy0, sx0:sx0 + dx1 - dx0].astype(np.float32)
    a = s[..., 3:4] / 255. * alpha
    roi = dst[dy0:dy1, dx0:dx1]
    roi *= (1 - a); roi += s[..., :3] * a

def layer_over(dst, rgba):
    a = rgba[..., 3:4].astype(np.float32) / 255.
    dst *= (1 - a); dst += rgba[..., :3].astype(np.float32) * a

# ---------- ribbon ----------
def ribbon_layers(t, cx, cy, prog=1.0, R=430, top=-200, length=2300, turns=1.35, width=96, phase=0.0, tail=0.0):
    """returns (back, front) RGBA layers at half res, upscaled later"""
    sc = 0.5
    back = np.zeros((H // 2, W // 2, 4), np.uint8); front = back.copy()
    N = 220
    us = np.linspace(tail, prog, N)
    if prog - tail < 0.01: return back, front
    phi = phase + us * turns * 2 * math.pi + t * 0.55
    x = cx + R * np.cos(phi) * (0.85 + 0.15 * np.sin(us * 3))
    y = top + us * length + 120 * np.sin(phi)
    z = np.sin(phi)
    pts = np.stack([x, y], 1)
    tan = np.gradient(pts, axis=0); tan /= np.linalg.norm(tan, axis=1, keepdims=True) + 1e-6
    nrm = np.stack([-tan[:, 1], tan[:, 0]], 1)
    tw = us * 9 + t * 1.3 + phase
    k = np.cos(tw)
    ww = width * (0.28 + 0.72 * np.abs(k)) * (1 + 0.18 * z)
    # taper ends
    ends = np.clip((us - tail) / 0.06, 0, 1) * np.clip((prog - us) / 0.06, 0, 1)
    ww *= 0.25 + 0.75 * ends
    L = pts + nrm * ww[:, None] / 2; Rr = pts - nrm * ww[:, None] / 2
    for i in range(N - 1):
        light = 0.5 + 0.5 * k[i]
        face = k[i] >= 0
        base = np.array(NEON if face else (226, 246, 140), np.float32)
        shade = np.array(NEON_D if face else (176, 200, 70), np.float32)
        hi = np.array(NEON_L if face else (250, 255, 215), np.float32)
        c = shade + (base - shade) * min(1, light * 1.4)
        c = c + (hi - c) * max(0, light - 0.75) * 3
        poly = np.array([L[i], L[i + 1] + (L[i + 1] - L[i]) * 0.3, Rr[i + 1] + (Rr[i + 1] - Rr[i]) * 0.3, Rr[i]]) * sc
        tgt = front if z[i] > 0 else back
        cv2.fillPoly(tgt, [poly.astype(np.int32)], (int(c[0]), int(c[1]), int(c[2]), 255), lineType=cv2.LINE_AA)
    return back, front

def up(layer):
    return cv2.resize(layer, (W, H), interpolation=cv2.INTER_LINEAR)

def drop_shadow(layer, off=18, blur=31, strength=0.35):
    a = layer[..., 3].astype(np.float32) / 255.
    a = cv2.GaussianBlur(a, (0, 0), blur)
    M = np.float32([[1, 0, 0], [0, 1, off]]); a = cv2.warpAffine(a, M, (a.shape[1], a.shape[0]))
    return a * strength
