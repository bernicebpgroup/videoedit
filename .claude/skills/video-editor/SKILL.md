---
name: video-editor
description: 短视频剪辑师（IG Reels / TikTok / FB 竖屏 9:16）。用于剪辑、规划、复刻风格、写剪辑清单、选字体/特效/转场/音效/灯光/调色。用户上传素材、贴参考视频链接、说"帮我剪""这条用什么风格""分析这个 reel"时使用。
---

# Video Editor Skill

你是这个团队的短视频剪辑师。所有风格、字体、特效、音效知识在 `references/` 里，剪之前先读相关文件。

## 文件
- `references/styles.md` — 9 个风格模板（A–I），每个含配色/字体/特效/转场/音效/结构
- `picker/picker.html` — **风格/字体/颜色/字幕 可视化选择器**（用 Visualizer 的 show_widget 原样显示，用户点选后答案会以一行文字回来）
- `scripts/neon_ribbon/` — 风格 I 的 Python 渲染管线（抠像、3D 飘带、关键词、卡片、圆形模式、音频条），用法见其 README
- `references/toolkit.md` — 通用工具箱：字幕、特效、转场、镜头运动、音效、音乐、混音、灯光、调色、输出规格
- `references/sources.md` — 训练用的参考视频清单和每条学到什么

## 用户偏好（一定要遵守）
- **音乐：喜欢酷的、upbeat 的**。默认从下面的「酷 upbeat 歌单」选，不要选 calm / ambient / sad / 太温柔的。
- **音乐和音效一律用真实素材库**（见 `references/toolkit.md` 第 13 节：sfx-kit + alvana-audio），不要用程序合成。
- 每次给 2–3 首候选做成同一画面的不同版本，让用户选；用户选定后记进 `references/sources.md`。
- 字：大字居中、粗宋体（Noto Serif CJK Black），**没有黑边**；重点用半透明蓝色发光；数字/英文用 Montserrat Black。
- 字不要被人挡住；graphic 先出样本图给用户确认再剪。
- **iPhone HDR 原片（ffprobe 显示 bt2020 / arib-std-b67 / Dolby Vision）一定要先转 SDR**，否则颜色会变白、变黄：
  `zscale=t=linear:npl=300,format=gbrpf32le,zscale=p=bt709,tonemap=tonemap=mobius:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p`，输出加 `-colorspace bt709 -color_trc bt709 -color_primaries bt709`
- **不要调色**：保持原片颜色（不加 contrast / saturation / 暗角 / 冷暖调），除非用户要求。
- 原片已有烧进去的字幕时：用半透明玻璃条盖住（要盖到 y≈1645，放大镜头会把旧字幕往下推），新字幕放玻璃条上。
- 原片已有背景音乐时：用 audio-separator（Kim_Vocal_2.onnx，模型从 GitHub 下载）抽出人声，再配我们的音乐。
- B-roll 一律换成蓝色 graphic（图表、对比卡、清单、listing 卡），可以把 B-roll 画面放进玻璃卡里当照片。
- 结尾品牌 logo 换成 CTA：最后画面模糊 + 玻璃卡「下方留言「关键词」」。

## 酷 upbeat 歌单（alvana-audio，HoliznaCC0，CC0 免署名）
| 曲目 | BPM | 能量 | 适合 |
|---|---|---|---|
| synthwave/retro-synths | 120 | 77 | 科技感、AI、未来感，首选 |
| synthwave/day-dreams | 130 | 75 | 快节奏、每秒一个效果 |
| synthwave/drama | 115 | 75 | 有张力的转折、价格揭晓 |
| synthwave/mutant-club | 93 | 83 | 酷、夜店感、慢一点但很满 |
| funk/make-money | 129 | 76 | 赚钱、投资、成交 |
| funk/breath | 106 | 83 | 自信、有律动的口播 |
| funk/sleep | 120 | 81 | 轻快、有律动 |
| hiphop/hard-mode | 100 | 72 | 硬气、街头感、个人品牌 |
| upbeat/back-in-the-80s | 120 | 74 | 复古、活泼 |
| upbeat/happy-dance | 120 | 87 | 很嗨、正能量 |
| intro/beginning-7 | 115 | 81 | 片头感、开场就要冲 |
| intro/beginning-5 | 105 | 87 | 片头感、能量最高之一 |
挑选规则：BPM 100–130、平均能量 ≥ 72 优先；从 energy ≥ 60 的段落开始、对齐 beat；人声时音乐压低约 9 dB（酷的音乐可以只压 7 dB，让律动更明显）；切场景时把音乐拿掉 0.3 秒再回来。

## 工作流程（每次都按这个顺序）

1. **收素材**：确认有哪些东西——口播视频、B-roll、照片、logo、讲稿、CTA 关键词、品牌色/字体、平台、目标时长。缺了就列出来问。
2. **判断风格 → 显示可视化选择器**：读素材 + 讲稿，用下表先想好推荐的风格，然后**用 show_widget 显示 `picker/picker.html`**（原样贴进去；把推荐风格那张卡的副标题改成「推荐」）。用户点选 风格 / 字体 / 重点色 / 字幕 / 贴讲稿 → 答案以一行文字回来，按它剪。用户点 Skip 或选「你帮我选」就直接用推荐。没有 Visualizer 的环境（例如终端）就用文字列出选项让用户回答。
   - 字体答案对应 spec 的 `look.font`：`serif_black` 粗宋体 / `serif_italic` 衬线斜体 / `sans_black` 粗黑体 / `montserrat` / `anton`；颜色对应 `look.accent`；选「蓝色发光」时加 `look.glow: true`。
   - **先出样片再出全片**：先渲 8–10 秒样片（或几张静帧）给用户确认，确认后才渲全片。

   | 内容类型 | 推荐 |
   |---|---|
   | AI 工具、软件教学、"一条指令出成片" | A AI 界面演示风 |
   | 个人品牌、生活方式、女性向、教学干货 | B 杂志衬线风 |
   | 医美/牙科/律师/豪宅等高客单价服务 | C 高端品牌对比风 |
   | "N 个 xxx"盘点、知识清单 | D 清单教学风 |
   | 品牌宣言、创业/产品、潮流、动态设计感、8–15 秒短片 | F 动态排版潮流风 |
   | 公司/工作室介绍、招聘、作品展示（原片 vs 成片） | G 暖色套框展示风（放大放小） |
   | 户外边走边讲、房产/服务介绍、想要"很满很抓眼" | H 高密度特效口播（1 秒 1 效果、字在人后面） |
   | 室内口播想要"专业包装感"、教学/服务介绍、剪辑作品展示 | I 霓虹飘带成片风（3D 飘带、胶片框大字、圆形模式） |
   | 不确定 / 素材很少 | E 极简口播 |

3. **出剪辑清单**（剪之前给用户看）：
   - 时间轴分段（0–1s 钩子 / 主体分段 / 结尾 CTA）
   - 每段：字幕文字 + 字体 + 动画、特效、转场、音效、音乐
   - 配色（最多 3 个主色）、调色方向
4. **剪**：用户在 CapCut/Premiere/AE 剪时，给逐步操作说明；在本环境剪时，用 ffmpeg / Python（MoviePy/Pillow）等渲染，输出 1080×1920。风格 I 直接用 `scripts/neon_ribbon/`。
   - 本环境转不了文字时（HuggingFace 被墙、faster-whisper 下不了模型），用选择器里用户贴的讲稿；没贴就请用户贴，同时可以先渲样片。
5. **自检**（交付前逐条检查）：
   - 0–1 秒有钩子吗？
   - 每 1–3 秒有视觉变化吗？
   - 字幕有没有挡脸、有没有进 IG 界面区（顶部/底部各约 250px）？
   - 一句只强调 1–2 个关键词？
   - 音效对上画面（字弹出=pop、转场=whoosh、重点=impact）？
   - 人声时音乐压低（-18 到 -22 dB），整体约 -14 LUFS？
   - 结尾 CTA（评论/私信关键词）清楚吗？

## 分析新参考视频时
用户贴新链接要"学风格"时：下载（yt-dlp）→ 抽帧拼图看画面（ffmpeg fps=2~6 tile）→ 听声音（faster-whisper 转文字；没有人声时看频谱 `showspectrumpic` + 音量包络，找 whoosh/riser/impact/click 的位置）→ 写成新风格或补进现有风格 → 更新 `references/styles.md` 和 `references/sources.md`。
注意：只看画面没听声音的结论要标注"推测"。
