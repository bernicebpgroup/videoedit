"""Reel render engine: base video (zoom/grade) + animated overlays + synthesized music/SFX."""
import subprocess, math, re, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import scipy.signal as ss

W, H, FPS, SR = 1080, 1920, 30, 48000
FONT_SANS = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
FONT_SERIF = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
GOLD = (88, 178, 255); BLUEBG = (28, 118, 240); WHITE = (255, 255, 255); NAVY = (14, 26, 43); GREY = (160, 168, 180)
_fc = {}
def font(size, serif=False):
    k = (size, serif)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONT_SERIF if serif else FONT_SANS, size, index=2)
    return _fc[k]

# ---------- easing / anim helpers ----------
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_io(x): x = clamp(x); return x * x * (3 - 2 * x)
def back_out(x, s=1.7):
    x = clamp(x); x -= 1; return x * x * ((s + 1) * x + s) + 1
def spring(tsec, zeta=0.45, freq=3.5):
    """damped spring 0 -> 1 (overshoots ~20%, settles in ~0.4s). tsec = seconds since start."""
    if tsec <= 0: return 0.0
    w = 2 * math.pi * freq; wd = w * math.sqrt(1 - zeta * zeta)
    return 1 - math.exp(-zeta * w * tsec) * (math.cos(wd * tsec) + zeta * w / wd * math.sin(wd * tsec))

# ---------- sprite builders ----------
def rich_text(text, size, color=WHITE, hl=GOLD, serif=False, stroke=6, shadow=True, hl_scale=1.0):
    """'[...]' segments drawn in highlight colour (optionally bigger)."""
    parts = [(m, i % 2 == 1) for i, m in enumerate(re.split(r"\[|\]", text)) if m]
    fonts = [font(int(size * (hl_scale if h else 1)), serif) for _, h in parts]
    widths = [f.getbbox(p)[2] - f.getbbox(p)[0] for (p, _), f in zip(parts, fonts)]
    asc = max(f.getmetrics()[0] for f in fonts); desc = max(f.getmetrics()[1] for f in fonts)
    pad = stroke + 14
    img = Image.new("RGBA", (sum(widths) + 2 * pad, asc + desc + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img); x = pad
    for (p, h), f, w in zip(parts, fonts, widths):
        y = pad + asc - f.getmetrics()[0]
        d.text((x - f.getbbox(p)[0], y), p, font=f, fill=hl if h else color,
               stroke_width=stroke, stroke_fill=(10, 14, 24, 235))
        x += w
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); a = img.split()[3].filter(ImageFilter.GaussianBlur(10))
        sh.putalpha(a.point(lambda v: int(v * 0.55))); base = Image.new("RGBA", img.size, (0, 0, 0, 0))
        base.alpha_composite(sh, (0, 6)); base.alpha_composite(img); img = base
    return img

def panel(w, h, fill=(14, 26, 43, 215), radius=36, border=GOLD, bw=3):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius, fill=fill, outline=border + (255,) if border else None, width=bw if border else 0)
    return img

def pill(text, size, fg=WHITE, bg=BLUEBG, padx=34, pady=16, serif=False):
    f = font(size, serif); b = f.getbbox(text); tw, th = b[2] - b[0], f.getmetrics()[0] + f.getmetrics()[1]
    img = Image.new("RGBA", (tw + 2 * padx, th + 2 * pady), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, img.width - 1, img.height - 1), img.height // 2, fill=bg + (255,) if len(bg) == 3 else bg)
    d.text((padx - b[0], pady), text, font=f, fill=fg); return img

def place(canvas, spr, cx, cy, scale=1.0, alpha=1.0, angle=0):
    if alpha <= 0.01 or scale <= 0.01: return
    if abs(scale - 1) > 1e-3:
        spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.BICUBIC)
    if angle: spr = spr.rotate(angle, Image.BICUBIC, expand=True)
    if alpha < 0.999:
        a = spr.split()[3].point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    canvas.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))

# ---------- element: generic timed sprite with pop-in / fade-out ----------
class El:
    def __init__(self, t0, t1, spr, cx, cy, anim="pop", out=0.15, angle=0, z=0, behind=False):
        self.t0, self.t1, self.spr, self.cx, self.cy, self.anim, self.out, self.angle, self.z = t0, t1, spr, cx, cy, anim, out, angle, z
        self.behind = behind   # True = drawn between background and the (segmented) person
    def draw(self, c, t):
        if not (self.t0 <= t < self.t1): return
        a = (t - self.t0); o = clamp((self.t1 - t) / self.out) if self.out else 1
        if self.anim == "pop":      # spring jump: small + below -> overshoot -> settle
            p = spring(a); s = 0.55 + 0.45 * p; dy = 50 * (1 - p); al = clamp(a / 0.08) * o
            place(c, self.spr, self.cx, self.cy + dy, s, al, self.angle)
        elif self.anim == "slam":   # huge -> undershoot -> settle (spring)
            s = 2.4 - 1.4 * spring(a, 0.4, 3.2); al = clamp(a / 0.05) * o; place(c, self.spr, self.cx, self.cy, s, al, self.angle)
        elif self.anim == "up":     # spring rise
            dy = 70 * (1 - spring(a, 0.5, 3.0)); place(c, self.spr, self.cx, self.cy + dy, 1, clamp(a / 0.15) * o, self.angle)
        elif self.anim == "slide":  # from right, spring
            dx = 320 * (1 - spring(a, 0.55, 2.8)); place(c, self.spr, self.cx + dx, self.cy, 1, clamp(a / 0.12) * o, self.angle)
        else: place(c, self.spr, self.cx, self.cy, 1, o, self.angle)

class Fn:
    """custom element: f(canvas, t_local, t) ."""
    def __init__(self, t0, t1, f, z=0): self.t0, self.t1, self.f, self.z = t0, t1, f, z
    def draw(self, c, t):
        if self.t0 <= t < self.t1: self.f(c, t - self.t0, t)

def sub(t0, t1, text, y, size=68):
    return El(t0, t1, rich_text(text, size), W / 2, y, "pop", 0.08)

def typewriter(t0, t1, text, cx, cy, size, t_type, box=True, cursor=True):
    f = font(size); full = text
    def draw(c, tl, t):
        n = int(clamp(tl / t_type) * len(full) + 0.999) if tl < t_type else len(full)
        s = full[:n] + ("|" if cursor and (int(t * 2.5) % 2 == 0 or tl < t_type) else " ")
        b = f.getbbox(full + "|"); bw, bh = b[2] - b[0] + 90, f.getmetrics()[0] + f.getmetrics()[1] + 40
        if box:
            bx = panel(bw, bh, fill=BLUEBG + (255,), radius=24, border=None)
            ImageDraw.Draw(bx).text((45 - b[0], 20), s, font=f, fill=WHITE)
            sc = 0.8 + 0.2 * back_out(tl / 0.2); place(c, bx, cx, cy, sc, clamp(tl / 0.08))
    return Fn(t0, t1, draw)

# ---------- person segmentation (for text-behind-person) ----------
import os
SEG_MODEL = os.environ.get("SEG_MODEL", "models/selfie_multiclass_256x256.tflite")
class Seg:
    """per-frame person mask (MediaPipe selfie multiclass), feathered + temporally smoothed."""
    def __init__(self):
        self.m = None; self.prev = None; self.prev_i = -9
    def mask(self, rgb, i=None):
        if self.m is None:
            import mediapipe as mp
            from mediapipe.tasks.python import vision, BaseOptions
            self.mp = mp
            self.m = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
                base_options=BaseOptions(model_asset_path=SEG_MODEL), output_confidence_masks=True))
        a = np.ascontiguousarray(np.asarray(rgb.convert("RGB")))
        r = self.m.segment(self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=a))
        p = 1 - np.squeeze(r.confidence_masks[0].numpy_view())
        if self.prev is not None and i is not None and i == self.prev_i + 1: p = 0.6 * p + 0.4 * self.prev
        self.prev, self.prev_i = p, (i if i is not None else -9)
        m = Image.fromarray((np.clip((p - 0.5) * 4 + 0.5, 0, 1) * 255).astype(np.uint8)).resize(rgb.size, Image.BILINEAR)
        return m.filter(ImageFilter.GaussianBlur(3))

def composite(im, t, elements, seg=None, i=None):
    """im: graded+zoomed RGB frame. Elements with .behind=True go under the person."""
    c = im.convert("RGBA")
    beh = [e for e in elements if getattr(e, "behind", False) and e.t0 <= t < e.t1]
    if beh and seg is not None:
        pm = seg.mask(im, i)
        for el in beh: el.draw(c, t)
        c.paste(im.convert("RGBA"), (0, 0), pm)
    for el in elements:
        if not (getattr(el, "behind", False) and seg is not None): el.draw(c, t)
    return c

# ---------- render ----------
def render(src, out_noaudio, t_start, dur, zoom_keys, elements, grade, shakes=()):
    """zoom_keys: list of (t, scale, cx, cy, ease_time). shakes: list of (t, strength)."""
    elements = sorted(elements, key=lambda e: e.z)
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(t_start), "-t", str(dur), "-i", src, "-map", "0:v:0",
                            "-vf", f"fps={FPS},scale={W}:{H},{grade}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out_noaudio], stdin=subprocess.PIPE)
    fs = W * H * 3; i = 0
    seg = Seg() if any(getattr(e, "behind", False) for e in elements) else None
    while True:
        buf = dec.stdout.read(fs)
        if len(buf) < fs: break
        t = t_start + i / FPS
        im = Image.frombuffer("RGB", (W, H), buf)
        # zoom: find segment
        k = max([z for z in zoom_keys if z[0] <= t], key=lambda z: z[0], default=zoom_keys[0])
        prev = max([z for z in zoom_keys if z[0] < k[0]], key=lambda z: z[0], default=k)
        e = ease_io((t - k[0]) / k[4]) if k[4] > 0 else 1
        s = prev[1] + (k[1] - prev[1]) * e; cx = prev[2] + (k[2] - prev[2]) * e; cy = prev[3] + (k[3] - prev[3]) * e
        # slow drift inside a segment (push-in) if key has 6th element
        if len(k) > 5: s += k[5] * (t - k[0])
        sx = sy = 0
        for st, amp in shakes:
            if 0 <= t - st < 0.35:
                d = 1 - (t - st) / 0.35; sx += amp * d * math.sin((t - st) * 90); sy += amp * d * math.cos((t - st) * 70)
        if s > 1.001 or sx or sy:
            s = max(s, 1.0 + (0.03 if (sx or sy) else 0))
            cw, ch = W / s, H / s
            x0 = clamp(cx - cw / 2 + sx, 0, W - cw); y0 = clamp(cy - ch / 2 + sy, 0, H - ch)
            im = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
        c = composite(im, t, elements, seg, i)
        enc.stdin.write(c.convert("RGB").tobytes()); i += 1
    enc.stdin.close(); enc.wait(); dec.wait(); return i

# ---------- audio ----------
def load_audio(path, t_start, dur, filt):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t_start), "-t", str(dur), "-i", path, "-map", "0:a:0", "-af", filt,
                          "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()

rng = np.random.default_rng(7)
def _env(n, a, r):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr) ** 2; return e
def bp(x, lo, hi): b, a = ss.butter(2, [lo / (SR / 2), hi / (SR / 2)], "band"); return ss.lfilter(b, a, x)
def lp(x, f): b, a = ss.butter(2, f / (SR / 2)); return ss.lfilter(b, a, x)
def hp(x, f): b, a = ss.butter(2, f / (SR / 2), "high"); return ss.lfilter(b, a, x)

def sfx_whoosh(d=0.45):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); seg = 512
    for i in range(0, n, seg):
        fr = 400 + 5000 * math.sin(math.pi * i / n) ** 2; out[i:i + seg] = bp(x[i:i + seg + 0], fr * 0.6, min(fr * 1.6, 20000))[:len(out[i:i + seg])]
    env = np.sin(np.linspace(0, math.pi, n)) ** 2; return 0.5 * out * env / (np.abs(out).max() + 1e-9)
def sfx_impact(d=0.9):
    n = int(d * SR); t = np.arange(n) / SR; f = 38 + 70 * np.exp(-t * 18)
    body = np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-t * 4.5)
    nz = lp(rng.standard_normal(n), 900) * np.exp(-t * 25)
    x = body + 0.5 * nz / (np.abs(nz).max() + 1e-9); return 0.9 * x / np.abs(x).max()
def sfx_ding(f=1318.5, d=1.0):
    t = np.arange(int(d * SR)) / SR
    x = (np.sin(2 * math.pi * f * t) + 0.35 * np.sin(2 * math.pi * 2 * f * t) + 0.15 * np.sin(2 * math.pi * 3.01 * f * t)) * np.exp(-t * 5)
    x[:200] *= np.linspace(0, 1, 200); return 0.35 * x / np.abs(x).max()
def sfx_pop(d=0.08):
    t = np.arange(int(d * SR)) / SR; f = 500 + 900 * t / d
    return 0.4 * np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-t * 45)
def sfx_click(): x = hp(rng.standard_normal(int(0.02 * SR)), 2500) * np.exp(-np.arange(int(0.02 * SR)) / SR * 300); return 0.35 * x / np.abs(x).max()
def sfx_tick(): t = np.arange(int(0.04 * SR)) / SR; return 0.22 * np.sin(2 * math.pi * 2200 * t) * np.exp(-t * 120)
def sfx_riser(d=1.5):
    n = int(d * SR); t = np.arange(n) / SR; f = 180 * (12 ** (t / d))
    tone = np.sin(2 * math.pi * np.cumsum(f) / SR); nz = hp(rng.standard_normal(n), 3000)
    x = (0.5 * tone + 0.4 * nz / np.abs(nz).max()) * (t / d) ** 2.2; return 0.45 * x / np.abs(x).max()
def sfx_chime():
    out = np.zeros(int(1.4 * SR))
    for k, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0]):
        d = sfx_ding(f, 1.0) * 0.8; s = int(k * 0.07 * SR); out[s:s + len(d)] += d
    return out
def sfx_shutter():
    n = int(0.12 * SR); x = hp(rng.standard_normal(n), 1500) * np.exp(-np.arange(n) / SR * 60)
    y = np.zeros(int(0.2 * SR)); y[:n] += x; y[int(0.07 * SR):int(0.07 * SR) + n] += 0.7 * x; return 0.5 * y / np.abs(y).max()
SFX = dict(shutter=sfx_shutter, whoosh=sfx_whoosh, impact=sfx_impact, ding=sfx_ding, pop=sfx_pop, click=sfx_click, tick=sfx_tick, riser=sfx_riser, chime=sfx_chime)

def music(dur, bpm=81, start=0.0, swell_from=None):
    """Soft cinematic bed: detuned pad + sub bass + soft kick on 1&3 + light hat. Am-F-C-G."""
    n = int(dur * SR); out = np.zeros(n); beat = 60 / bpm; bar = 4 * beat
    chords = [(57, 60, 64), (53, 57, 60), (48, 52, 55, 60), (55, 59, 62)]
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    t_all = np.arange(n) / SR
    for bi in range(int(dur / bar) + 2):
        ch = chords[bi % 4]; s0 = int((start + bi * bar) * SR); s1 = min(n, int((start + (bi + 1) * bar) * SR) + int(0.3 * SR))
        if s0 >= n: break
        if s1 <= s0: continue
        t = np.arange(s1 - s0) / SR; seg = np.zeros(s1 - s0)
        for m in ch:
            for det in (-0.08, 0.08):
                seg += ss.sawtooth(2 * math.pi * hz(m + 12) * (1 + det / 100) * t) * 0.10
        seg = lp(seg, 1400) * _env(len(seg), 0.6, 0.5)
        seg += 0.35 * np.sin(2 * math.pi * hz(ch[0] - 12) * t) * _env(len(seg), 0.05, 0.4)
        out[s0:s1] += seg
    for k in range(int(dur / beat) + 1):
        tb = start + k * beat; s = int(tb * SR)
        if s >= n or tb < start: continue
        if k % 2 == 0:
            kk = sfx_impact(0.35) * 0.55; e = min(n, s + len(kk)); out[s:e] += kk[:e - s]
        h = hp(rng.standard_normal(int(0.03 * SR)), 7000) * np.exp(-np.arange(int(0.03 * SR)) / SR * 150) * 0.05
        s2 = int((tb + beat / 2) * SR); e2 = min(n, s2 + len(h))
        if s2 < n: out[s2:e2] += h[:e2 - s2]
    out[:int(start * SR)] = 0
    fade = np.ones(n)
    a = int(start * SR); fade[a:a + int(0.4 * SR)] = np.linspace(0, 1, len(fade[a:a + int(0.4 * SR)]))
    fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR))
    if swell_from is not None:
        fade *= np.where(t_all > swell_from, 1 + 0.6 * np.clip((t_all - swell_from) / 6, 0, 1), 1)
    return out / (np.abs(out).max() + 1e-9) * fade

def mix(voice, dur, sfx_events, out_wav, bpm=81, music_start=0.0, music_gain_db=-17, swell_from=None):
    n = int(dur * SR); v = np.zeros(n); v[:min(n, len(voice))] = voice[:n]
    m = music(dur, bpm, music_start, swell_from) * 10 ** (music_gain_db / 20)
    # ducking: voice envelope
    env = np.sqrt(np.convolve(v ** 2, np.ones(4800) / 4800, "same")); act = (env > 0.01).astype(float)
    act = np.convolve(act, np.ones(9600) / 9600, "same"); m *= 1 - 0.55 * np.clip(act, 0, 1)
    fx = np.zeros(n)
    for t, name, g in sfx_events:
        x = SFX[name]() * 10 ** (g / 20); s = int(t * SR)
        if s < 0: x = x[-s:]; s = 0
        e = min(n, s + len(x)); fx[s:e] += x[:e - s]
    y = v + m + fx
    pcm = (np.clip(y, -1, 1) * 32767).astype(np.int16)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2", out_wav], input=pcm.tobytes(), check=True)

def mux(video, audio, out):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)

VOICE_FILTER = "highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-2"
