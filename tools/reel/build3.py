import sys, time, subprocess
sys.path.insert(0, sys.argv[1])
from reel import *
import specs3
from PIL import Image
out = sys.argv[2]; mode = sys.argv[3] if len(sys.argv) > 3 else "full"
G = "eq=contrast=1.06:saturation=1.05,colorbalance=bs=0.04:bh=-0.02,vignette=PI/4.5"
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", "0.5", "-i", "src/src.mp4", "-map", "0:v:0", "-frames:v", "1", "-vf", f"scale={W}:{H},{G}",
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
base = Image.frombuffer("RGB", (W, H), raw).convert("RGBA")
b1 = base.crop((110, 1470, 560, 1880)).rotate(180); b2 = base.crop((470, 1500, 900, 1900)).rotate(180)
els = specs3.v3_elements(b1, b2)
if mode == "preview":
    times = [float(x) for x in sys.argv[4].split(",")]
    import preview as P
    sys.exit(0)
t0 = time.time()
n = render("src/src.mp4", f"{out}.video.mp4", 0.0, 26.6, specs3.ZOOM, els, G, [(15.50, 14)])
print("frames", n, round(time.time() - t0), "s", flush=True)
voice = load_audio("src/src.mp4", 0.0, 26.6, VOICE_FILTER)
mix(voice, 26.6, specs3.SFX, f"{out}.audio.wav", 81, 0.0, -17, 20.3)
mux(f"{out}.video.mp4", f"{out}.audio.wav", out)
print("done", out, round(time.time() - t0), "s")
