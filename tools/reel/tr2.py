import sys, numpy as np, subprocess
from faster_whisper import WhisperModel
raw=subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-map","0:a:0","-f","s16le","-ac","1","-ar","16000","-"],capture_output=True).stdout
a=np.frombuffer(raw,np.int16).astype(np.float32)/32768
m=WhisperModel(sys.argv[2] if len(sys.argv)>2 else "small",device="cpu",compute_type="int8")
segs,info=m.transcribe(a,word_timestamps=True,initial_prompt="以下是普通话的句子，关于拍卖、房地产。")
print(info.language, info.language_probability)
for s in segs:
    print(f"[{s.start:.2f}-{s.end:.2f}] {s.text}")
    print("   ", " ".join(f"{w.word}@{w.start:.2f}" for w in s.words))
