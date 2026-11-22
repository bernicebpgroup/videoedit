import sys,subprocess,numpy as np
from faster_whisper import WhisperModel
p=sys.argv[1]; sr=22050
raw=subprocess.run(["ffmpeg","-v","error","-i",p,"-f","s16le","-ac","1","-ar",str(sr),"-"],capture_output=True).stdout
a=np.frombuffer(raw,np.int16).astype(np.float32)/32768
a16=a[::1]
# words
import scipy.signal as ss
w16=ss.resample_poly(a,16000,sr).astype(np.float32)
m=WhisperModel("small",device="cpu",compute_type="int8")
segs,_=m.transcribe(w16,word_timestamps=True)
words=[(w.start,w.end,w.word) for s in segs for w in s.words]
dur=len(a)/sr
hop=512; n=2048
f,t,Z=ss.stft(a,sr,nperseg=n,noverlap=n-hop); M=np.abs(Z)+1e-9
def band(lo,hi): return 20*np.log10(np.sqrt((M[(f>=lo)&(f<hi)]**2).mean(0)))
low=band(20,120); mid=band(300,3000); hi=band(5000,11000); full=20*np.log10(np.sqrt((M**2).mean(0)))
speech=np.zeros_like(t,bool)
for s,e,_ in words: speech|=(t>=s-0.05)&(t<=e+0.05)
print(f"dur={dur:.1f}s words={len(words)}")
print(f"level speech={np.median(full[speech]):.1f}dB  gaps={np.median(full[~speech]) if (~speech).any() else float('nan'):.1f}dB  low(<120Hz) speech={np.median(low[speech]):.1f} gaps={np.median(low[~speech]) if (~speech).any() else float('nan'):.1f}")
# tempo from low-band onset envelope
flux=np.maximum(0,np.diff(np.log(M),axis=1)).sum(0); flux=np.r_[0,flux]
lf=np.maximum(0,np.diff(low)); lf=np.r_[0,lf]
env=lf-lf.mean(); ac=np.correlate(env,env,'full')[len(env)-1:]
fps=sr/hop; lags=np.arange(len(ac))/fps; ok=(lags>0.3)&(lags<1.2)
L=lags[ok][np.argmax(ac[ok])]; print(f"tempo guess={60/L:.0f} BPM (beat strength {ac[ok].max()/ac[0]:.2f})")
# events
def peaks(x,thr,dist):
    pk,_=ss.find_peaks(x,height=np.median(x)+thr,distance=int(dist*fps)); return t[pk]
hb=peaks(np.r_[0,np.maximum(0,np.diff(hi))],12,0.15)
lb=peaks(np.r_[0,np.maximum(0,np.diff(low))],10,0.25)
def tag(x):
    for s,e,w in words:
        if s-0.15<=x<=e+0.15: return w.strip()
    return "-"
print("HIGH bursts (click/whoosh/sparkle):"," ".join(f"{x:.2f}[{tag(x)}]" for x in hb))
print("LOW hits (impact/kick):"," ".join(f"{x:.2f}[{tag(x)}]" for x in lb))
# risers: sustained rising hi band over >0.8s
sm=np.convolve(hi,np.ones(int(fps*0.3))/int(fps*0.3),'same')
win=int(fps*1.0); r=[]
for i in range(0,len(sm)-win,int(fps*0.25)):
    if sm[i+win]-sm[i]>15: r.append(t[i])
print("risers start ~:"," ".join(f"{x:.1f}" for x in r[:15]))
# silences of everything (music stops)
q=full<np.median(full)-25
st=[t[i] for i in range(1,len(q)) if q[i] and not q[i-1]]
print("dropouts:"," ".join(f"{x:.2f}" for x in st[:20]))
