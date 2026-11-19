import sys, json, math, subprocess
import numpy as np, cv2
from PIL import Image, ImageDraw
from engine import *

spec = json.load(open(sys.argv[1])); out = sys.argv[2]
T0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
T1 = float(sys.argv[4]) if len(sys.argv) > 4 else 99.0

masks = np.load('masks.npz')['m']
faces = np.load('faces.npy')
rms = np.load('rms.npy')
fx_all = np.nan_to_num(faces[:, 0], nan=np.nanmean(faces[:, 0])); fy_all = np.nan_to_num(faces[:, 1], nan=np.nanmean(faces[:, 1]))
def face_at(t):
    i = t * 2; i0 = int(clamp(math.floor(i), 0, len(faces) - 1)); i1 = min(i0 + 1, len(faces) - 1); f = i - i0
    # smooth: average neighbourhood
    lo, hi = max(0, i0 - 2), min(len(faces), i0 + 3)
    return float(fx_all[lo:hi].mean()), float(fy_all[lo:hi].mean())

# ---- prebuild sprites ----
def kw_sprites(k):
    big = to_np(shadowed(text_sprite(k['big'], k.get('size', 210), NEON, stroke=3, stroke_col=(60, 70, 20)), 16, (0, 10), 0.45, 30))
    smalls = []
    for s in k.get('small', []):
        smalls.append(to_np(shadowed(text_sprite(s, k.get('small_size', 58), (255, 255, 255), italic=False,
                                                  font_path=F_CJK_SANS_M if is_cjk(s) else F_UIB), 10, (0, 6), 0.55, 20)))
    return big, smalls

KW = [(k, *kw_sprites(k)) for k in spec.get('keywords', [])]
CARDS = [(c, [to_np(card(i, l)) for i, l in c['items']]) for c in spec.get('cards', [])]
PILLS = [(p, to_np(pill(p['text'], p.get('size', 36)))) for p in spec.get('pills', [])]
SUBS = []
for s in spec.get('subs', []):
    f = font(F_CJK_SANS if is_cjk(s['text']) else F_UIB, 54)
    im = text_sprite(s['text'], 54, (255, 255, 255), italic=False, stroke=7, stroke_col=(15, 15, 15), font_path=F_CJK_SANS if is_cjk(s['text']) else F_UIB)
    SUBS.append((s, to_np(im)))

def ring_text_sprite(txt, r, size=40):
    S = int(r * 2 + size * 3)
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    f = font(F_UIB if not is_cjk(txt) else F_CJK_SANS, size)
    c = S / 2; n = len(txt); ang = 0
    total = sum(f.getlength(ch) for ch in txt)
    circ = 2 * math.pi * r; spacing = circ / total
    for ch in txt:
        cw = f.getlength(ch) * spacing
        a = ang + cw / 2 / r
        g = Image.new('RGBA', (size * 2, size * 2), (0, 0, 0, 0))
        ImageDraw.Draw(g).text((size, size), ch, font=f, fill=NEON + (255,), anchor='mm')
        g = g.rotate(-math.degrees(a), resample=Image.BICUBIC)
        x = c + r * math.sin(a) - size; y = c - r * math.cos(a) - size
        im.alpha_composite(g, (int(x), int(y)))
        ang += cw / r
    return to_np(im)

CIRC = []
for c in spec.get('circle', []):
    CIRC.append((c, ring_text_sprite(c['ring'], 395, 42),
                 to_np(pill(c['pill'], 40)) if c.get('pill') else None,
                 [to_np(card(i, l, 210, 250)) for i, l in c.get('items', [])]))

FILM_INNER = {}

def zoom_at(t):
    zs = spec.get('zooms', [[0, 1.0]])
    z = zs[0][1]; prev = z
    for i, (t0, zz) in enumerate(zs):
        if t >= t0:
            prev = zs[i - 1][1] if i else zz
            z = prev + (zz - prev) * ease_out((t - t0) / 0.18)
    return z

# ---- io ----
nf_total = masks.shape[0]
f0 = int(T0 * FPS); f1 = min(nf_total, int(T1 * FPS))
reader = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', str(T0), '-i', 'src.mp4', '-vf', f'fps={FPS},scale={W}:{H}',
                           '-frames:v', str(f1 - f0), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
writer = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                           '-ss', str(T0), '-t', str((f1 - f0) / FPS), '-i', 'src.mp4', '-map', '0:v', '-map', '1:a',
                           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                           '-movflags', '+faststart', out], stdin=subprocess.PIPE)

paper = np.zeros((H, W, 3), np.float32)
yy, xx = np.mgrid[0:H, 0:W]
g = 1 - 0.10 * (((xx - W / 2) / W) ** 2 + ((yy - H * 0.4) / H) ** 2) * 2
paper[:] = np.array(PAPER, np.float32)[None, None] * g[..., None]

snap_idx = set(int(s * FPS) for s in spec.get('snaps', []))
for fi in range(f0, f1):
    buf = reader.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    t = fi / FPS
    fr = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    m = cv2.resize(masks[min(fi, nf_total - 1)], (W, H), interpolation=cv2.INTER_LINEAR)
    fx, fy = face_at(t)
    z = zoom_at(t)
    if abs(z - 1) > 1e-3:
        M = np.float32([[z, 0, fx * (1 - z)], [0, z, fy * (1 - z)]])
        fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        m = cv2.warpAffine(m, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        fx2, fy2 = fx, fy
    else:
        fx2, fy2 = fx, fy
    a = (m.astype(np.float32) / 255.)[..., None]
    img = fr.astype(np.float32)
    # background: soft focus + airy grade
    small = cv2.resize(fr, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    bg = cv2.resize(cv2.GaussianBlur(small, (0, 0), 6), (W, H)).astype(np.float32)
    bg = bg * 0.72 + np.array([250, 252, 238], np.float32) * 0.28
    person = img.copy()
    # gentle grade on person: lift + contrast
    person = np.clip((person - 128) * 1.06 + 134, 0, 255)

    # ribbon state
    rb_back = rb_front = None
    for r in spec.get('ribbon', []):
        if r[0] <= t <= r[1] + 0.6:
            prog = ease_out((t - r[0]) / r[2].get('in', 0.9))
            tail = ease_io((t - r[1]) / 0.6) if t > r[1] else 0
            p = r[2]
            rb_back, rb_front = ribbon_layers(t, fx2 + p.get('dx', 0), fy2, prog=prog, tail=tail * prog,
                                              R=p.get('R', 430), top=fy2 + p.get('top', -900), length=p.get('len', 2400),
                                              turns=p.get('turns', 1.35), width=p.get('w', 96), phase=p.get('phase', 0))
            rb_back, rb_front = up(rb_back), up(rb_front)
            break

    comp = bg
    if rb_back is not None:
        layer_over(comp, rb_back)
    sh = None
    if rb_front is not None:
        sh = drop_shadow(rb_front, 22, 18, 0.35)[..., None]
    comp = comp * (1 - a) + person * a
    if sh is not None:
        comp *= (1 - sh)
        layer_over(comp, rb_front)

    # ---- circle mode ----
    for c, ring, pl, cds in CIRC:
        if c['t0'] <= t <= c['t1']:
            ti = ease_io((t - c['t0']) / 0.45); to_ = ease_io((c['t1'] - t) / 0.4)
            k = min(ti, to_)
            ccx, ccy = 540, 720
            rmax = 1400; rmin = 330
            rad = rmax + (rmin - rmax) * k
            # move face to circle centre
            sx, sy = ccx - fx2 * 1.0, ccy - fy2 * 1.0
            Mv = np.float32([[1, 0, sx * k], [0, 1, sy * k]])
            moved = cv2.warpAffine(np.clip(comp, 0, 255).astype(np.uint8), Mv, (W, H), borderMode=cv2.BORDER_REFLECT).astype(np.float32)
            cm = np.zeros((H, W), np.float32)
            cv2.circle(cm, (ccx, ccy), int(rad), 1.0, -1, lineType=cv2.LINE_AA)
            cm = cv2.GaussianBlur(cm, (0, 0), 1.2)[..., None]
            frame2 = paper.copy()
            # neon ring + progress arc
            if k > 0.3:
                ka = clamp((k - 0.3) / 0.7)
                ov = np.zeros((H, W, 3), np.float32); oa = np.zeros((H, W), np.float32)
                cv2.circle(oa, (ccx, ccy), int(rad + 22), 1.0, 10, lineType=cv2.LINE_AA)
                prog = ease_out((t - c['t0'] - 0.3) / (c['t1'] - c['t0'] - 0.6))
                cv2.ellipse(oa, (ccx, ccy), (int(rad + 118), int(rad + 118)), -90, 0, 360 * prog, 1.0, 14, lineType=cv2.LINE_AA)
                cv2.circle(oa, (ccx, ccy), int(rad + 118), 0.25, 2, lineType=cv2.LINE_AA)
                oa = (oa * ka)[..., None]
                frame2 = frame2 * (1 - oa) + np.array(NEON_D, np.float32) * oa
                blit(frame2, ring, ccx, ccy, 1.0, ka, rot=-(t - c['t0']) * 22)
            comp = frame2 * (1 - cm) + moved * cm
            if pl is not None:
                s, al = pop(t, c['t0'] + 0.55, c['t1'] - 0.15)
                blit(comp, pl, ccx, 1280, s, al)
            for j, cd in enumerate(cds):
                s, al = pop(t, c['t0'] + 0.8 + j * 0.15, c['t1'] - 0.1)
                bob = 8 * math.sin(t * 3 + j)
                blit(comp, cd, 540 + (j - (len(cds) - 1) / 2) * 250, 1520 + bob, s, al)

    # ---- film strip keyword ----
    for k, big, smalls in KW:
        if k['t0'] <= t <= k['t1']:
            y = k.get('y', 1180)
            if k.get('film', True):
                s, al = pop(t, k['t0'], k['t1'], 0.3)
                key = id(k)
                if key not in FILM_INNER:
                    inner = Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8)).crop((0, 300, W, 900))
                    FILM_INNER[key] = to_np(filmstrip(min(1000, big.shape[1] + 160), 260, inner))
                blit(comp, FILM_INNER[key], 540, y, s, al * 0.97, rot=k.get('rot', -2))
            s, al = pop(t, k['t0'] + 0.08, k['t1'], 0.3)
            blit(comp, big, 540 + k.get('dx', 0), y + 4, s, al, rot=k.get('rot', -2))
            for j, sm in enumerate(smalls):
                pos = k.get('small_pos', [[-1, -1], [1, 1]])[j % 2]
                s2, al2 = pop(t, k['t0'] + 0.25 + 0.15 * j, k['t1'])
                fh = 260 if k.get('film', True) else big.shape[0]
                bx = 540 + pos[0] * (big.shape[1] / 2 - sm.shape[1] / 2 + 20)
                by = y + pos[1] * (fh / 2 + sm.shape[0] / 2 + 6)
                blit(comp, sm, bx, by, s2, al2)

    # ---- card rows ----
    for c, sp in CARDS:
        for j, cd in enumerate(sp):
            s, al = pop(t, c['t0'] + j * 0.14, c['t1'])
            n = len(sp); bob = 10 * math.sin(t * 2.6 + j * 1.3)
            x = 540 + (j - (n - 1) / 2) * 260
            y = c.get('y', 1450) + (abs(j - (n - 1) / 2) * 40 if c.get('arc', True) else 0) + bob
            blit(comp, cd, x, y, s, al, rot=(j - (n - 1) / 2) * -5)

    for p, sp in PILLS:
        s, al = pop(t, p['t0'], p['t1'])
        blit(comp, sp, p.get('x', 540), p.get('y', 380), s, al)

    # ---- audio bars ----
    for b in spec.get('bars', []):
        if b[0] <= t <= b[1]:
            s, al = pop(t, b[0], b[1])
            nb = 26; bw = 22; gap = 12; base_y = b[2] if len(b) > 2 else 1640
            x0 = 540 - (nb * (bw + gap)) / 2
            plate = np.zeros((H, W), np.float32)
            for j in range(nb):
                fi2 = min(len(rms) - 1, max(0, fi - abs(j - nb // 2)))
                hgt = (14 + 120 * rms[fi2] * (0.6 + 0.4 * math.sin(j * 1.7 + t * 9) ** 2)) * s
                x = int(x0 + j * (bw + gap))
                cv2.rectangle(plate, (x, int(base_y - hgt / 2)), (x + bw, int(base_y + hgt / 2)), 1.0, -1, lineType=cv2.LINE_AA)
            pa = (plate * al)[..., None]
            card_a = np.zeros((H, W), np.float32)
            x1c = int(x0 + nb * (bw + gap) + 18); x0c = int(x0 - 30)
            rr = 36
            cv2.rectangle(card_a, (x0c + rr, base_y - 95), (x1c - rr, base_y + 95), 1.0, -1)
            cv2.rectangle(card_a, (x0c, base_y - 95 + rr), (x1c, base_y + 95 - rr), 1.0, -1)
            for cx_, cy_ in ((x0c + rr, base_y - 95 + rr), (x1c - rr, base_y - 95 + rr), (x0c + rr, base_y + 95 - rr), (x1c - rr, base_y + 95 - rr)):
                cv2.circle(card_a, (cx_, cy_), rr, 1.0, -1, lineType=cv2.LINE_AA)
            card_a = cv2.GaussianBlur(card_a, (0, 0), 1.2)[..., None] * al * 0.85
            comp = comp * (1 - card_a) + np.array((22, 24, 20), np.float32) * card_a
            comp = comp * (1 - pa) + np.array(NEON, np.float32) * pa

    for s, sp in SUBS:
        if s['t0'] <= t <= s['t1']:
            al = clamp((t - s['t0']) / 0.08) * clamp((s['t1'] - t) / 0.08)
            blit(comp, sp, 540, s.get('y', 1700), 1.0, al)

    outf = np.clip(comp, 0, 255).astype(np.uint8)
    if fi in snap_idx:
        cv2.imwrite(f'snap_{fi:05d}.jpg', cv2.cvtColor(outf, cv2.COLOR_RGB2BGR))
    writer.stdin.write(outf.tobytes())
    if fi % 60 == 0: print('t', round(t, 1), flush=True)

writer.stdin.close(); writer.wait()
print('done')
