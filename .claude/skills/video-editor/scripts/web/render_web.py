"""Final 1080x1920 render with the same engine as the live preview (styles A–I).

Run inside a prepare.py work dir (src.mp4, masks.npz, faces.npy, rms.npy):
    python3 render_web.py spec.json out.mp4 [T0 T1]
spec.json = {"look": {"style": "H", "font": "anton", "accent": "#FF7A1A", "glow": false, "stroke": false, "subs": true},
             "events": [{"type": "hook", "t0": .., "t1": .., "big": .., "small": .., "label": ..},
                        {"type": "cards", ..., "items": [..3..], "label": .., "num": "10", "count": 450000},
                        {"type": "feature", ..., "text": .., "label": .., "items": [..4..], "quote": ..},
                        {"type": "outro", ..., "cta": .., "brand": .., "phone": .., "ctaLine": ..},
                        {"type": "sub", "t0": .., "t1": .., "text": "one spoken line"}, ...]}
Events may repeat (e.g. several hook/cards blocks across a 50s video); times are seconds in the source.
Needs: google-chrome + playwright (python), rangehttpserver (pip), ffmpeg.
"""
import sys, os, json, base64, shutil, subprocess, time, socket, asyncio
import numpy as np

here = os.path.dirname(os.path.abspath(__file__))
spec_path, out = sys.argv[1], sys.argv[2]
T0 = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
masks = np.load('masks.npz')['m']
n_all = len(masks)
T1 = float(sys.argv[4]) if len(sys.argv) > 4 else n_all / 30
srv = os.path.abspath('_render_srv'); os.makedirs(srv, exist_ok=True)
for f in ('engine.js', 'render.html'): shutil.copy(os.path.join(here, f), srv)
if not os.path.exists(os.path.join(srv, 'fonts')): shutil.copytree(os.path.join(here, 'fonts'), os.path.join(srv, 'fonts'))
shutil.copy(spec_path, os.path.join(srv, 'spec.json'))

# data.json (face track in 540-space, loudness per frame)
faces = np.load('faces.npy'); rms = np.load('rms.npy')
fx = np.nan_to_num(faces[:, 0], nan=np.nanmean(faces[:, 0])); fy = np.nan_to_num(faces[:, 1], nan=np.nanmean(faces[:, 1]))
json.dump({'fps': 30, 'face': [[round(float(a) / 2, 1), round(float(b) / 2, 1)] for a, b in zip(fx, fy)],
           'rms': [round(float(x), 3) for x in rms]}, open(os.path.join(srv, 'data.json'), 'w'))

# full-res colour|matte, every frame a keyframe so seeking is exact
full = os.path.join(srv, 'full.mp4')
if not os.path.exists(full):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', '540x960', '-r', '30', '-i', '-',
                          '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', os.path.join(srv, '_mask.mp4')], stdin=subprocess.PIPE)
    p.stdin.write(masks.tobytes()); p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', 'src.mp4', '-i', os.path.join(srv, '_mask.mp4'), '-filter_complex',
                    '[0:v]fps=30,scale=1080:1920,setsar=1[a];[1:v]scale=1080:1920,format=yuv420p,setsar=1[b];[a][b]hstack=2[v]',
                    '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-g', '1', '-pix_fmt', 'yuv420p', full], check=True)

sock = socket.socket(); sock.bind(('', 0)); port = sock.getsockname()[1]; sock.close()
server = subprocess.Popen([sys.executable, '-m', 'RangeHTTPServer', str(port)], cwd=srv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

async def main():
    from playwright.async_api import async_playwright
    f0, f1 = int(T0 * 30), min(n_all, int(T1 * 30))
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'image2pipe', '-c:v', 'mjpeg', '-r', '30', '-i', '-',
                            '-ss', str(T0), '-t', str((f1 - f0) / 30), '-i', 'src.mp4', '-map', '0:v', '-map', '1:a?',
                            '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=shutil.which('google-chrome') or shutil.which('chromium'))
        pg = await b.new_page(viewport={'width': 1100, 'height': 1950})
        pg.on('pageerror', lambda e: print('page error:', e))
        await pg.goto(f'http://localhost:{port}/render.html')
        await pg.wait_for_function('window.READY === true', timeout=120000)
        t_start = time.time()
        for fi in range(f0, f1):
            url = await pg.evaluate(f'renderAt({fi / 30 + 0.001})')
            enc.stdin.write(base64.b64decode(url.split(',', 1)[1]))
            if fi % 90 == 0: print(f'{fi / 30:.1f}s  ({(fi - f0 + 1) / (time.time() - t_start):.1f} fps)', flush=True)
        await b.close()
    enc.stdin.close(); enc.wait()

try:
    asyncio.run(main())
finally:
    server.terminate()
print('done', out)
