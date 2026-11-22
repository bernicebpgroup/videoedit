"""Render still preview frames at chosen times (with zoom + grade + overlays) and tile them."""
import sys, subprocess, math
sys.path.insert(0, sys.argv[1])
from reel import *
import specs

def frame_at(spec, els, t):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", spec["src"], "-map", "0:v:0", "-frames:v", "1",
                          "-vf", f"scale={W}:{H},{spec['grade']}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    im = Image.frombuffer("RGB", (W, H), raw)
    zk = spec["zoom"]; k = max([z for z in zk if z[0] <= t], key=lambda z: z[0], default=zk[0])
    prev = max([z for z in zk if z[0] < k[0]], key=lambda z: z[0], default=k)
    e = ease_io((t - k[0]) / k[4]) if k[4] > 0 else 1
    s = prev[1] + (k[1] - prev[1]) * e + (k[5] * (t - k[0]) if len(k) > 5 else 0)
    cx = prev[2] + (k[2] - prev[2]) * e; cy = prev[3] + (k[3] - prev[3]) * e
    if s > 1.001:
        cw, ch = W / s, H / s; x0 = clamp(cx - cw / 2, 0, W - cw); y0 = clamp(cy - ch / 2, 0, H - ch)
        im = im.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch))
    c = im.convert("RGBA")
    for el in sorted(els, key=lambda x: x.z): el.draw(c, t)
    return c.convert("RGB")

out, which = sys.argv[2], sys.argv[3]
times = [float(x) for x in sys.argv[4].split(",")]
spec, els = (specs.V1, specs.v1_elements()) if which == "1" else (specs.V2, specs.v2_elements())
fr = [frame_at(spec, els, t).resize((432, 768), Image.LANCZOS) for t in times]
sheet = Image.new("RGB", (432 * len(fr) + 12 * (len(fr) - 1), 768), (20, 20, 20))
for i, f in enumerate(fr): sheet.paste(f, (i * 444, 0))
sheet.save(out, quality=92)
