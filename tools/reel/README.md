# Reel 渲染工具（影片 2：拍卖得标 RM280千）

## 素材
Google Drive 文件 ID：`1xXeRe2I0kUsYucmDgswK-1PSRGvoje-i`（360MB，51.8 秒，1080x1920 60fps）
下载：
    mkdir -p src2 && curl -L -o src2/src.mp4 "https://drive.usercontent.google.com/download?id=1xXeRe2I0kUsYucmDgswK-1PSRGvoje-i&export=download&confirm=t"

## 依赖
    apt-get install -y fonts-noto-cjk
    pip install scipy pillow numpy faster-whisper mediapipe
    apt-get install -y libegl1 libgles2          # mediapipe 需要
    mkdir -p models && curl -sSfL -o models/selfie_multiclass_256x256.tflite \
      https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite

## 运行（在放 src2/ 和 frames/ 的工作目录里）
    cp -r tools/reel/frames .   # shot.png = 手机价格截图（已裁剪拉直）
    python3 tools/reel/preview.py $(pwd)/tools/reel previews/x.jpg 2 "13.5,14.9,33.4"   # 预览帧
    python3 tools/reel/build.py  $(pwd)/tools/reel 2 out/v2_auction.mp4                  # 完整渲染

- `specs.py`：时间轴（字幕、特效、镜头推拉、音效时间点），V2 / v2_elements / V2_SFX
- `reel.py`：渲染引擎（字体、配色、动画、合成音乐和音效、-14 LUFS 混音）

## 当前确认的设定
- 风格：C 高端对比 + A 界面；配色 **蓝色**（GOLD 变量现在是蓝色 (88,178,255)，BLUEBG (28,118,240)）
- 字体：用户最新要求 **全部改宋体**（reel.py 里 FONT_SANS 已指向 NotoSerifCJK-Bold.ttc），还没出预览给用户确认
- 13.4s：点击价格 → 拍照闪光 → 截图卡片弹出放大 + 蓝框圈出 280,000.00
- 字幕/卡片入场改成**弹簧弹跳**（`spring()`：阻尼比 0.45、3.5Hz，冲过头约 20%，0.4s 停住），学自风格 H
- **字在人后**：`El(..., behind=True)` 的元素画在背景和人之间（MediaPipe 人像分割，每帧抠图 + 羽化 + 时间平滑）。用在 1.0s「得标！」和 47.2s「50%」
- **字幕风格 I（高级感）**：所有字无描边，只有淡柔光阴影；一句只放重点 `stack()`（小字细宋体 + 大字粗宋体，居中）；其他话用 `words()` 细字半透明逐段出；毛玻璃卡片 `Glass` / `glass_label()` + `icon()`；幽灵大字「280」「经营者」半透明放人后
- 剪掉开头 1 秒；音乐 2.14s「得标」才进来
- 转写更正：Arte Plus、Jalan Ampang；「内容才标280千」原话不确定，字幕写「才标280千」
