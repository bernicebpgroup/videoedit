"""Person masks for every output frame (30fps) -> uint8 memmap [N,960,540]."""
import sys, subprocess, time, numpy as np, onnxruntime as ort
from PIL import Image
src, t0, dur, model, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
so = ort.SessionOptions(); so.intra_op_num_threads = 8
sess = ort.InferenceSession(model, so); name = sess.get_inputs()[0].name
W, H = 540, 960
dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", str(t0), "-t", str(dur), "-i", src, "-map", "0:v:0",
                        "-vf", f"fps=30,scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
N = int(round(dur * 30)) + 2
mm = np.lib.format.open_memmap(out, mode="w+", dtype=np.uint8, shape=(N, H, W))
mean = np.array([0.485, 0.456, 0.406], np.float32); std = np.array([0.229, 0.224, 0.225], np.float32)
i = 0; ts = time.time()
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    im = Image.frombuffer("RGB", (W, H), buf)
    x = np.asarray(im.resize((320, 320), Image.LANCZOS), np.float32) / 255.0
    x = x / x.max() if x.max() > 0 else x
    x = ((x - mean) / std).transpose(2, 0, 1)[None]
    p = sess.run(None, {name: x})[0][0, 0]
    p = (p - p.min()) / (p.max() - p.min() + 1e-8)
    mm[i] = np.asarray(Image.fromarray((p * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)); i += 1
    if i % 100 == 0: print(i, "frames", round(time.time() - ts), "s", flush=True)
mm.flush(); print("done", i, "frames", round(time.time() - ts), "s")
