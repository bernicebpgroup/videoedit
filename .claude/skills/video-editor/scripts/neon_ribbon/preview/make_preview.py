"""Build the live preview page's media from a prepare.py work dir.

Usage (inside the work dir, after prepare.py):  python3 make_preview.py [start_sec] [dur_sec]
Writes ./preview/{index.html, clip.mp4, data.json}; publish those 3 files as one artifact
(publish_files: index.html, clip.mp4, data.json). clip.mp4 = colour | person-matte side by side,
the page composites them in a canvas so the ribbon can pass behind the head.
The page's timeline (keyword 0.6s, cards 2.8s, circle 5.6s, bars 8.9s) assumes ~11s.
"""
import sys, os, json, shutil, subprocess
import numpy as np
here = os.path.dirname(os.path.abspath(__file__))
T0 = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0
DUR = float(sys.argv[2]) if len(sys.argv) > 2 else 11.33
os.makedirs('preview', exist_ok=True)
f0, n = int(T0 * 30), int(DUR * 30)
m = np.load('masks.npz')['m'][f0:f0 + n]; n = len(m)
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', '540x960', '-r', '30', '-i', '-',
                      '-c:v', 'libx264', '-crf', '24', '-pix_fmt', 'yuv420p', 'preview/_mask.mp4'], stdin=subprocess.PIPE)
p.stdin.write(m.tobytes()); p.stdin.close(); p.wait()
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(T0), '-t', str(n / 30), '-i', 'src.mp4', '-i', 'preview/_mask.mp4',
                '-filter_complex', '[0:v]fps=30,scale=540:960,setsar=1[a];[1:v]format=yuv420p,setsar=1[b];[a][b]hstack=2,format=yuv420p[v]',
                '-map', '[v]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '25', '-preset', 'veryfast', '-c:a', 'aac', '-b:a', '128k',
                '-movflags', '+faststart', 'preview/clip.mp4'], check=True)
os.remove('preview/_mask.mp4')
faces = np.load('faces.npy'); rms = np.load('rms.npy')[f0:f0 + n]
fx = np.nan_to_num(faces[:, 0], nan=np.nanmean(faces[:, 0])); fy = np.nan_to_num(faces[:, 1], nan=np.nanmean(faces[:, 1]))
i0 = int(T0 * 2); i1 = i0 + int(DUR * 2) + 2
json.dump({'fps': 30, 'dur': n / 30, 'face': [[round(float(a) / 2, 1), round(float(b) / 2, 1)] for a, b in zip(fx[i0:i1], fy[i0:i1])],
           'rms': [round(float(x), 3) for x in rms]}, open('preview/data.json', 'w'))
shutil.copy(os.path.join(here, 'index.html'), 'preview/index.html')
print('preview/ ready:', os.listdir('preview'))
