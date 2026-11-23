"""Real-sample mixer: sfx-kit (CC0) sound effects + alvana (CC0) music, ducked under voice, -14 LUFS."""
import sys, json, subprocess, numpy as np
SR = 48000
def load(path, t0=0.0, dur=None, filt=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t0)]
    if dur: cmd += ["-t", str(dur)]
    cmd += ["-i", path, "-map", "0:a:0"] + (["-af", filt] if filt else []) + ["-f", "f32le", "-ac", "1", "-ar", str(SR), "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.float32).copy()
def rms_db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)

class Kit:
    def __init__(self, root):
        self.root = root; self.s = {x["id"]: x for x in json.load(open(root + "/sounds.json"))["sounds"]}; self.cache = {}
    def get(self, sid):
        if sid not in self.cache: self.cache[sid] = load(self.root + "/" + self.s[sid]["file"])
        return self.cache[sid], (self.s[sid].get("sync") or {}).get("at") or 0.0, self.s[sid].get("under_voiceover_db") or 0

def music_segment(track_mp3, track_json, dur):
    meta = json.load(open(track_json)); e = (meta.get("energy") or {}).get("v") or []; step = (meta.get("energy") or {}).get("step", 0.5)
    start = 0.0
    for i, v in enumerate(e):              # start where the track has settled in (energy >= 60), on a beat
        if v >= 60: start = max(0.0, i * step - 1.0); break
    beats = meta.get("beats") or []
    if beats: start = min(beats, key=lambda b: abs(b - start))
    if start + dur > meta["dur"]: start = max(0.0, meta["dur"] - dur - 1)
    return load(track_mp3, start, dur + 0.5), start

def build(voice_src, dur, events, kit_root, music_mp3, out_wav, music_db=-23, duck_db=-9, sfx_gain_db=-6, lowcut=()):
    kit = Kit(kit_root); n = int(dur * SR)
    v = np.zeros(n); vv = load(voice_src, 0, dur, "highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=120,loudnorm=I=-16:TP=-2")
    v[:min(n, len(vv))] = vv[:n]
    env = np.sqrt(np.convolve(v ** 2, np.ones(4800) / 4800, "same")); act = np.convolve((env > 0.01).astype(float), np.ones(9600) / 9600, "same")
    m = np.zeros(n)
    if music_mp3:
        mm, st = music_segment(music_mp3, music_mp3[:-4] + ".json", dur); mm = mm[:n]
        mm = mm * 10 ** ((music_db - rms_db(mm)) / 20); m[:len(mm)] = mm
        fi = int(0.6 * SR); fo = int(1.5 * SR); m[:fi] *= np.linspace(0, 1, fi); m[n - fo:] *= np.linspace(1, 0, fo)
        m *= 10 ** (duck_db * np.clip(act, 0, 1) / 20)
        for a, b in lowcut:                 # 拿掉音乐（切场景时只留高频/空一下）
            s0, s1 = int(a * SR), int(b * SR); g = np.ones(s1 - s0); r = min(int(0.08 * SR), len(g) // 2)
            g[:r] = np.linspace(1, 0.15, r); g[r:-r] = 0.15; g[-r:] = np.linspace(0.15, 1, r); m[s0:s1] *= g
        print("music", music_mp3.split("/music/")[-1], "start", round(st, 2))
    fx = np.zeros(n)
    for t, sid, g in events:
        x, sync, vo = kit.get(sid)
        duck = vo if act[min(n - 1, max(0, int(t * SR)))] > 0.5 else 0
        x = x * 10 ** ((g + sfx_gain_db + duck) / 20); s = int((t - sync) * SR)
        if s < 0: x = x[-s:]; s = 0
        e = min(n, s + len(x)); fx[s:e] += x[:e - s]
    y = v + m + fx
    pcm = (np.clip(y / max(1.0, np.abs(y).max() / 0.98), -1, 1) * 32767).astype(np.int16)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", str(SR), "-ac", "2", out_wav], input=pcm.tobytes(), check=True)

# ---- video 1 v4 sound design (times in seconds) ----
FLY = [0.0, 2.92, 4.95, 16.64, 22.68]; CARD = [0.45, 3.25, 5.28, 17.04, 23.01]
V1_EVENTS = (
    [(t, "shimmer-short-sparkle", -2) for t in FLY] + [(t + 0.05, "whoosh-fast-soft", -4) for t in FLY] +
    [(t, "pop-large-in", 0) for t in CARD] +
    [(3.47, "whoosh-medium-soft", -2), (3.8, "shimmer-short-soft", -4), (5.45, "whoosh-medium-soft", -2)] +
    [(5.75 + k * 0.18, f"tone-step-{k + 1}", -3) for k in range(5)] +
    [(7.46, "pop-medium-in", -2), (7.60, "click-snap-soft", -4)] +
    [(9.70, "whoosh-medium-medium", 0), (9.72, "boom-hit-soft", -6)] +
    [(t, "data-number-land", 0) for t in (9.88, 10.48, 12.04, 12.78)] + [(t + 0.06, "pop-small-in", -4) for t in (9.88, 10.48, 12.04, 12.78, 13.48)] +
    [(13.48, "tone-ding-high", -2), (13.48, "shimmer-medium-bright", -6)] +
    [(14.30, "whoosh-medium-soft", -3), (14.85, "data-decrease-short", -2), (15.15, "data-number-land", 0),
     (15.50, "riser-1s-soft", -4), (15.50, "boom-hit-medium", 0), (15.52, "shimmer-short-bright", -6)] +
    [(16.64, "whoosh-slow-soft", -2), (18.72, "pop-medium-in", -4), (20.32, "pop-medium-in", -4), (20.50, "click-snap-soft", -6)] +
    [(23.20, "whoosh-medium-soft", -2), (23.50, "riser-1s-soft", -6), (23.50, "boom-hit-soft", -3), (24.14, "shimmer-medium-sparkle", -2)] +
    [(t, "whoosh-fast-soft", -12) for t in (1.04, 2.0, 3.9, 5.94, 6.90, 8.5, 19.5, 21.3, 25.0, 25.9)]
)
if __name__ == "__main__":
    voice, out, music = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "none" else None)
    build(voice, 26.6, V1_EVENTS, sys.argv[4], music, out, lowcut=[(9.62, 9.95), (16.55, 16.80)])
    print("ok")
