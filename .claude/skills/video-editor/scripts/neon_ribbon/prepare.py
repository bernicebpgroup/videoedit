"""Prepare a talking-head clip for render.py.

Usage (run inside a work dir):  python3 prepare.py /path/to/input.mp4
Produces in the current dir:
  src.mp4                  copy of the input
  masks.npz                person matte per frame (30fps, 540x960)
  faces.npy                face centre/size every 0.5s (full-res coords)
  rms.npy                  voice loudness per frame (drives audio bars)
  phrases.json             speech phrases [t0, t1] from silence detection
Models: selfie_segmentation.tflite + face_detection_short_range.tflite are
extracted from the mediapipe 0.10.14 wheel on PyPI (HuggingFace / Google
storage are blocked in the sandbox, PyPI is not).
"""
import sys, os, glob, json, shutil, subprocess, re, wave
import numpy as np, cv2

W, H, FPS = 1080, 1920, 30
src = sys.argv[1]
shutil.copy(src, 'src.mp4')

# ---- models ----
if not (os.path.exists('selfie_segmentation.tflite') and os.path.exists('face_detection_short_range.tflite')):
    os.makedirs('_pkgs', exist_ok=True)
    subprocess.run(['pip', 'download', '--no-deps', '-q', '--only-binary=:all:', '--python-version', '3.11',
                    '--platform', 'manylinux_2_17_x86_64', '-d', '_pkgs', 'mediapipe==0.10.14'], check=True)
    whl = glob.glob('_pkgs/mediapipe-0.10.14*.whl')[0]
    for m in ('selfie_segmentation/selfie_segmentation.tflite', 'face_detection/face_detection_short_range.tflite'):
        subprocess.run(['unzip', '-o', '-q', '-j', whl, f'mediapipe/modules/{m}', '-d', '.'], check=True)

import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions

# ---- matte ----
seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path='selfie_segmentation.tflite'),
    output_confidence_masks=True, running_mode=vision.RunningMode.VIDEO))
det = vision.FaceDetector.create_from_options(vision.FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path='face_detection_short_range.tflite')))
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', 'src.mp4', '-vf', f'fps={FPS},scale={W}:{H}',
                      '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
masks, faces, prev, i = [], [], None, 0
while True:
    buf = p.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    small = np.ascontiguousarray(cv2.resize(np.frombuffer(buf, np.uint8).reshape(H, W, 3), (540, 960), interpolation=cv2.INTER_AREA))
    mimg = mp.Image(image_format=mp.ImageFormat.SRGB, data=small)
    m = seg.segment_for_video(mimg, int(i * 1000 / FPS)).confidence_masks[0].numpy_view()
    if m.ndim == 3: m = m[..., 0]
    m = np.clip(cv2.ximgproc.guidedFilter(small, cv2.resize(m.astype(np.float32), (540, 960)), 8, 1e-3), 0, 1)
    if prev is not None: m = 0.6 * m + 0.4 * prev      # temporal smoothing
    prev = m; masks.append((m * 255).astype(np.uint8))
    if i % (FPS // 2) == 0:
        r = det.detect(mimg)
        if r.detections:
            bb = r.detections[0].bounding_box
            faces.append(((bb.origin_x + bb.width / 2) * 2, (bb.origin_y + bb.height / 2) * 2, bb.width * 2))
        else:
            faces.append((np.nan,) * 3)
    i += 1
np.savez_compressed('masks.npz', m=np.stack(masks))
np.save('faces.npy', np.array(faces))
print('frames', len(masks))

# ---- audio ----
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'src.mp4', '-vn', '-ac', '1', '-ar', '16000', 'audio.wav'], check=True)
w = wave.open('audio.wav'); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
hop = 16000 // FPS; n = len(a) // hop
r = np.array([np.sqrt((a[k * hop:(k + 1) * hop] ** 2).mean()) for k in range(n)])
np.save('rms.npy', np.clip(r / (np.percentile(r, 98) + 1e-9), 0, 1.2))

out = subprocess.run(['ffmpeg', '-i', 'audio.wav', '-af', 'silencedetect=noise=-32dB:d=0.25', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
dur = len(a) / 16000
phr, cur = [], 0.0
for s, e in zip(starts, ends + [dur]):
    if s - cur > 0.3: phr.append([round(cur, 2), round(s, 2)])
    cur = e
if dur - cur > 0.3: phr.append([round(cur, 2), round(dur, 2)])
json.dump(phr, open('phrases.json', 'w'))
print('phrases', phr)
