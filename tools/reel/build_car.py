import sys, time, importlib
sys.path.insert(0, sys.argv[1])
from reel import render
import audio_real
SP = importlib.import_module(sys.argv[2]); base, vocals, out, music = sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
G = "null"
t0 = time.time()
n = render(base, out + ".video.mp4", 0.0, SP.DUR, SP.ZOOM, SP.elements(), G, SP.SHAKES)
print("frames", n, round(time.time() - t0), "s", flush=True)
audio_real.build(vocals, SP.DUR, SP.SFX, sys.argv[1] + "/../libs/sfx-kit", music, out + ".audio.wav", music_db=-21, duck_db=-7, lowcut=SP.LOWCUT)
import subprocess
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", out + ".video.mp4", "-i", out + ".audio.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
print("done", out, round(time.time() - t0), "s")
