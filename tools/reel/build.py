import sys, time
sys.path.insert(0, sys.argv[1])
from reel import *
import specs

which = sys.argv[2]; out = sys.argv[3]
if which == "1":
    sp, els, fx, mstart, swell = specs.V1, specs.v1_elements(), specs.V1_SFX, 0.0, 20.3
else:
    sp, els, fx, mstart, swell = specs.V2, specs.v2_elements(), specs.V2_SFX, 2.14, 40.6
t0 = time.time(); T = sp["t_start"]; D = sp["dur"]
n = render(sp["src"], f"{out}.video.mp4", T, D, sp["zoom"], els, sp["grade"], sp["shakes"])
print("frames", n, "video", round(time.time() - t0), "s", flush=True)
voice = load_audio(sp["src"], T, D, VOICE_FILTER)
mix(voice, D, [(t - T, name, g) for t, name, g in fx], f"{out}.audio.wav", 81, mstart - T if mstart > T else mstart, -17, swell - T)
mux(f"{out}.video.mp4", f"{out}.audio.wav", out)
print("done", out, round(time.time() - t0), "s")
