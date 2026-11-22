"""Demo: impact caption + price-drop board (with SFX), and an IG safe-zone check frame."""
import sys, subprocess
sys.path.insert(0, sys.argv[1])
from reel import *
from fx import *
import specs
out = sys.argv[2]; sp = specs.V2
NEON_B = (120, 195, 255)

def impact_cap(t0, t1, small, big, cy, hl=NEON_B):
    return [El(t0, t1, text2(small, 66, "sans_medium"), W / 2, cy - 150, "pop", 0.12, z=5),
            Impact(t0 + 0.06, t1, text2(f"[{big}]", 190, "sans_black", hl=hl, neon=True), W / 2, cy, z=6)]

T_CR = 25.72
clips = [("a", 15.4, 2.2, impact_cap(15.86, 17.4, "比别人", "便宜一倍", 760), [(16.0, 16)],
          [(15.80, "whoosh", -6), (16.0, "impact", 0)]),
         ("b", 22.7, 5.1, [price_drop(22.9, 23.55, T_CR, 27.75)], [(T_CR + 0.55, 18)],
          [(22.9, "whoosh", -6), (23.55, "ding", -6), (T_CR - 0.9, "riser", -6), (T_CR, "whoosh", -2),
           (T_CR + 0.55, "impact", 0), (T_CR + 0.75, "pop", -3), (T_CR + 0.8, "chime", -6)])]
for nm, t0, dur, els, shakes, fxs in clips:
    render(sp["src"], f"{out}/drop_{nm}.v.mp4", t0, dur, [(0, 1.0, 540, 900, 0)], els, sp["grade"], shakes)
    voice = load_audio(sp["src"], t0, dur, VOICE_FILTER)
    mix(voice, dur, [(t - t0, n, g) for t, n, g in fxs], f"{out}/drop_{nm}.wav", 81, 0, -17, None)
    mux(f"{out}/drop_{nm}.v.mp4", f"{out}/drop_{nm}.wav", f"{out}/drop_{nm}.mp4")
# safe-zone check frame
import fx as _fx
c = Image.new("RGBA", (W, H)); raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(T_CR + 1.2), "-i", sp["src"], "-map", "0:v:0", "-frames:v", "1", "-vf", f"scale={W}:{H},{sp['grade']}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
c = Image.frombuffer("RGB", (W, H), raw).convert("RGBA"); clips[1][3][0].draw(c, T_CR + 1.2); safe_overlay(c); c.convert("RGB").save(f"{out}/safe_check.jpg", quality=90)
open(f"{out}/l.txt", "w").write("file 'drop_a.mp4'\nfile 'drop_b.mp4'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{out}/l.txt", "-c", "copy", f"{out}/drop_demo.mp4"], check=True)
