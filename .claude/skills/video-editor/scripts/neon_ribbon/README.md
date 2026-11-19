# 风格 G 渲染管线（霓虹飘带成片风）

Python + ffmpeg 在本环境直接把口播视频渲染成风格 G 成片（1080×1920 / 30fps / H.264 + 原声）。

## 步骤
```bash
mkdir work && cd work
python3 <skill>/scripts/neon_ribbon/prepare.py /path/to/input.mp4   # ~1 分钟 / 50 秒素材
# 按 phrases.json 的句子时间 + 讲稿，写 spec.json（格式见 example_spec.json）
python3 <skill>/scripts/neon_ribbon/render.py spec.json out.mp4 [T0] [T1]   # ~6–7 秒渲染 1 秒素材（2 核）
```
- `prepare.py`：人像抠图（mediapipe selfie segmentation + guided filter + 时间平滑）、人脸位置、音量包络、按停顿切句。模型从 PyPI 的 mediapipe 0.10.14 wheel 里解出来（沙盒里 HuggingFace / Google storage 被墙）。
- `render.py`：读 spec 渲染；`T0 T1` 可只渲一段做样片。spec 里 `snaps` 列出的秒数会存成 `snap_XXXXX.jpg` 方便自检。
- `engine.py`：所有图形元件（飘带、关键词、胶片框、卡片、图标、标签、圆形模式、音频条）。

## spec.json 字段
| 字段 | 格式 | 说明 |
|---|---|---|
| `zooms` | `[[t, 倍数], …]` | 每句换一次推/拉（1.0 ↔ 1.1），以脸为中心，0.18s 缓出 |
| `ribbon` | `[[t0, t1, {in, phase, turns, R, w, dx, top, len}], …]` | 黄绿 3D 飘带绕人螺旋，`in` 秒画出、结束 0.6s 收尾；z>0 的段在人前面，z<0 的段在头后面 |
| `keywords` | `{t0,t1,big,small[],small_pos,size,y,film,rot}` | 衬线粗斜体荧光大字（中文用 Noto Serif CJK Black + 仿斜体），可垫胶片框；`small` 是白色小字引导词 |
| `cards` | `{t0,t1,items:[[icon,label]],y,arc}` | 白色圆角卡片 + 荧光圆形图标，依次弹出、轻浮动 |
| `pills` | `{t0,t1,text,x,y}` | 白色胶囊标签 + 荧光圆点 |
| `circle` | `{t0,t1,ring,pill,items}` | 圆形模式：画面虹膜收成圆 → 外圈旋转环形字 + 进度环 + 标签 + 卡片 |
| `bars` | `[[t0,t1,y]]` | 深色圆角条 + 荧光音频条，跟真实人声音量跳 |
| `subs` | `{t0,t1,text,y}` | 可选底部完整字幕（白字黑描边） |

图标可选：`pin house search gavel doc money web check people`（在 `engine.icon()` 里加新的）。

## 注意
- 抠图模型会把桌子/手臂当成前景：所以背景只做柔焦提亮，不整片换背景；飘带只从头后面穿。
- 没有语音识别模型时（faster-whisper 需要 HuggingFace），**先请用户贴讲稿**，再按 `phrases.json` 对时间。
- 关键词放在胸口（y≈1150–1250），避开脸（脸一般在 y 450–900）和 IG 底部 UI 区。
