# 风格 A–I 引擎（预览 + 成片同一套画法）

`engine.js` 把 9 种风格都画在 canvas 上（540×960 坐标，成片时放大 2 倍 = 1080×1920）。
来源影片 = 左边原画面 | 右边人像遮罩（并排），所以能做"字在人后面"、背景模糊、飘带从头后穿过。

## 流程
```bash
mkdir work && cd work
python3 <skill>/scripts/neon_ribbon/prepare.py /path/to/input.mp4      # 抠像、人脸、音量、phrases.json
python3 <skill>/scripts/web/make_preview.py [开始秒] [长度秒]            # → preview/，发成 artifact 给用户点选
python3 <skill>/scripts/web/render_web.py spec.json out.mp4 [T0 T1]      # 成片（先渲一段样片）
```
需要：google-chrome、python playwright、`pip install rangehttpserver`、ffmpeg。

## spec.json
```json
{"look": {"style": "H", "font": "anton", "accent": "#FF7A1A", "glow": false, "stroke": false, "subs": true},
 "events": [
  {"type": "hook", "t0": 0.6, "t1": 2.5, "big": "关键词", "small": "引导小字", "label": "标签/评论气泡"},
  {"type": "cards", "t0": 2.8, "t1": 5.4, "items": ["重点1", "重点2", "重点3"], "label": "标签", "num": "10", "count": 450000},
  {"type": "feature", "t0": 5.6, "t1": 8.8, "text": "重点段文字", "label": "大字", "items": ["清单1", "清单2", "清单3", "清单4"], "quote": "金句"},
  {"type": "outro", "t0": 8.9, "t1": 11.3, "cta": "留言关键词", "brand": "名字/品牌", "phone": "电话", "ctaLine": "Follow & comment “关键词”"},
  {"type": "sub", "t0": 0.3, "t1": 3.0, "text": "每一句口播（字幕逐词跟上）"}
 ]}
```
- 同一种 event 可以出现很多次（50 秒影片放 3–5 组 hook/cards/feature，最后一个 outro）；`sub` 每句一个，时间用 `phrases.json`。
- `font`：serif_black 粗宋体 / serif_italic 衬线斜体 / playfair_italic / sans_black 粗黑体 / montserrat / montserrat_italic / anton / mono
- 每种风格怎么用这些 event：

| 风格 | hook | cards | feature | outro |
|---|---|---|---|---|
| A AI 界面 | 评论气泡 + 大字在人后（发光） | 打勾清单逐条弹出 | `/effects` 指令打字 + 卡片推近震动 | CTA 按钮 + 鼠标点 → Saved |
| B 杂志衬线 | 编号方块 + 细线 + 衬线斜体标题 | 逐词出现（灰→实、上浮去模糊），中间那个放大花体 | 墨绿章节卡 "01" 从下长出 → 米白金句屏 | Comment + 大号斜体关键词 |
| C 高端对比 | 小细字引导 + 擦出粗体品牌色关键词 + 发光下划线 | 玻璃信息卡逐张滑入 | 薄荷→白大数字 "1" + 两种字重句子 | 白闪 + 白色 CTA 卡 |
| D 清单教学 | 左上清单出现 | 每 0.8 秒换一种"布光"+ 高亮当前项 + 左下参考小窗 | 同上继续 | 打字机关键词 + 光标 |
| E 极简口播 | 大字关键词 | 一次一个重点大字 | 小卡片 B-roll + 大字 | 品牌色 CTA 胶囊；全程逐词字幕 |
| F 动态排版 | 乱码解码 + 角标框 + 贴纸标签 | 对比卡 ♡ vs ♥ | 滚轮选择器 + 像素粒子 | 极简 logo 卡 + 贴纸 |
| G 暖色套框 | 大字逐字母打出 + 像素方块，之后整个画面缩成卡片 | 墙上照片卡 | 白色波浪线画出 + 卡片里推近 | 照片卡弹出；底部 CTA 全程 |
| H 高密度特效 | 三色叠字 → 大字在人后 | 圆形擦出 + 大数字在人后 → 数字跳动 + 爱心 + 作品卡 | 黑白双色字 → 字在人后 → 白闪 → 逐词 | 来电卡片 → "DM ME" 在人后 + CTA 大字 |
| I 霓虹飘带 | 3D 飘带 + 胶片框关键词 | 白卡片 + 标签 | 圆形模式（环形字 + 进度环） | 音频条 + CTA |

字体文件在 `fonts/`（SIL OFL）；中文用系统 Noto CJK（预览网页从 Google Fonts 加载 Noto Serif/Sans SC）。
