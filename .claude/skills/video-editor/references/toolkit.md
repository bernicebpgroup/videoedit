# 剪辑工具箱（通用）

## 0. 开剪前收集
- 原始素材：口播、B-roll、照片、logo
- 资料：行业、目标观众、平台（IG Reels / TikTok / FB）、时长
- 文案：讲稿、关键词、CTA 词（EDIT / CUT / LIGHT / BRAND …）
- 品牌：品牌色、字体、logo、水印

## 1. 字体库
| 用途 | 字体（免费优先） |
|---|---|
| 科技 / UI | Inter, Geist, SF Pro |
| 杂志衬线 | Playfair Display, Bodoni Moda, DM Serif Display |
| 花体斜体关键词 | Cormorant Garamond Italic, Playfair Display Italic |
| 高端几何 | Montserrat, Poppins |
| 等宽 / 潮流 | Space Mono, JetBrains Mono, Geist Mono |
| 像素 | Press Start 2P, Silkscreen |
| CTA 大字 | Anton, Archivo Black（白字黑描边） |

规则：
- 两层字幕：小字引导 + 大字关键词
- 一句只强调 1–2 个关键词
- 字幕不挡脸，不进 IG 界面区（顶部/底部各约 250px）
- 一条片最多 2 种字体家族

## 2. 字幕动画
- 逐词出现（模糊 + 淡入 + 轻微上浮）
- 打字机 + 闪光标
- 乱码解码（text scramble）
- 扫光擦出 / 发光色块下划线
- 关键词缩放回弹（1.05 → 1.0）
- 文字在人物背后（人像抠图分层：rembg u2net_human_seg / MediaPipe selfie segmenter 逐帧抠人，背景 → 文字 → 人物三层叠合）
- 台词字面视觉化：说"all day"就换天空白天→夜晚；说"views"就数字跳动 + 爱心；说"call me"就弹出来电卡片
- 倾斜荧光贴纸标签、四角括号选中框

## 3. 特效
- 画中画：AI 聊天界面套框；"修改前 vs 修改后"双窗
- orbit 卡片环绕；glass widgets 毛玻璃卡片；white collage 黑白海报
- 评论框 / 私信气泡 / 按钮（Download → Saved）
- 打勾清单逐条弹出
- iOS 滚轮选择器列表
- 线稿 → 实景插图
- 3D 产品卡片、对比卡片网格
- 像素粒子爆发（带外发光）
- 角落清单逐项点亮 + 参考小窗

## 4. 转场
- 推镜头 + 运动模糊 + 震动（重点句）
- 甩镜 whip pan
- 纯色画面过渡（视觉喘息）
- 白闪（暗 → 亮）
- 章节卡：数字渐变透明从下长出，标题逐词加
- logo 运动模糊飞入
- 像素粒子遮罩
- 原则：克制，don't overdo it

## 5. 镜头运动
- 慢推 push-in；重点 punch-in（1.0 → 1.15 瞬切）；shake
- 画面整体缩小/推走 → 下一画面
- **放大放小（G 风格）**：全屏 → 0.3 秒缩小成圆角卡片，露出后面的展示台（原片小卡、徽章、底部固定 CTA）；外框不动、卡片里面继续推近
- 新图片以小卡片"弹出 + 放大"叠上来；切场景用一张深色卡闪一下

## 6. 音效（对画面动作）
| 画面动作 | 音效 |
|---|---|
| 字幕/元素弹出 | pop、soft click |
| 打字机 / 乱码解码 | 键盘声、密集 tick/glitch |
| 转场 | whoosh（噪声渐强） |
| 转场前铺垫 | riser（音调往上爬） |
| 关键词 / 大字砸下 | impact、bass drop、boom |
| 列表一项项切换 | UI beep（短方波，一格一声）、ding |
| 按钮 | mouse click |
| 像素 / 8-bit 元素 | 颤音电子 bleep、8-bit 音 |
| 灯光/画面切换 | tick、camera shutter |
| 画面缩小成卡片 / 放大回全屏 | 上扬 whoosh |
| 进入梦幻/新场景 | 低通滤波（高频切掉一下再打开） |
| 片头深色画面 | 低频轰鸣 sub boom |

规则（来自 6 条参考视频实测）：
- 每个画面动作都配一个音效，但音量有层次：pop/click 很轻，hit/impact 只给章节卡和转折词
- **开场 riser 跟钩子句一样长，句子说完正好到顶 → 切进正片**（B 风格）
- **前 1–1.5 秒先不放音乐，第一个"哇"画面出现时音乐低音进来**（beat drop，A 风格）
- **章节卡 = 低频 hit**；转折词（but / 但是）= hit
- 列表/清单逐项出现 = 每项一个短音（ding / beep / sparkle）
- 赠品、奖励、价值点出现 = 高频 chime（叮）
- 整片音量要有"紧-松-紧"的起伏，中段留喘息
- 全片最响的点只给一个最重要的转折（如 "But"）
- 音乐可以在后半段逐渐变满，推情绪到 CTA

## 7. 音乐
| 风格 | 音乐（实测） |
|---|---|
| A 科技 | 偏快有鼓点，约 110–136 BPM，低音重；开头可以先空 1.5 秒再进 |
| B 杂志 | 轻、中速，全程铺底；开场配 riser |
| C 高端 | 慢、稳，约 80 BPM，电影感/企业高端，后半段逐渐变满 |
| D 清单 | **不放音乐**，干净人声 + 快速跳切 |
| F 潮流 | 数字/故障电子，8-bit 元素，**无旁白**，音效是主角 |

## 8. 混音
- 有人声时：音乐压低 18–22 dB（ducking）
- 整片：约 -14 LUFS，true peak ≤ -1 dBTP（6 条参考视频实测全部在 -14.1 到 -14.4 LUFS）
- 有音乐的口播：人声比音乐高约 3–6 dB（在停顿处测），音乐一直听得到但不抢话
- 无旁白（F 风格）：音效就是主角，音乐可以更响

## 9. 灯光（拍摄）
20 种布光：
1. 低调光 Low-key　2. 高调光 High-key　3. 蝴蝶光 Butterfly　4. 剪影 Silhouette　5. 分割光 Split　6. 窄光 Short　7. 明暗对比 Light-dark　8. 轮廓光 Rim　9. 硬光 Hard　10. 柔光 Soft　11. 反射光 Bounce　12. 顶光 Top　13. 黄金时段 Golden hour　14. 日拍夜 Day for night　15. 月光 Moonlight　16. 窗光 Window　17. 实景光源 Practical　18. 体积光 Volumetric　19. 青橙色调 Teal & orange　20. 舞台光 Theatrical

常用搭配：
- 口播默认：柔光主光 45° + 轮廓光分离背景
- 高端：低调光 + 暗角
- 潮流 F：白色无缝背景 + 高调光（几乎无阴影）

## 10. 调色
- A：深色、青蓝
- B：暖色、低饱和
- C：人物冷调、背景压暗、暗角
- D：跟着每段布光走
- F：高亮白、干净、对比适中

## 11. 输出
- 1080×1920（9:16），30fps，H.264，约 10–16 Mbps
- 安全区：顶部/底部各约 250px，右侧约 120px（IG 按钮）

## 12. 结构公式
- 0–1s 钩子（质疑句、"Congrats! / But…"、标题 + 清单、地点"If you live in…"）
- 主体：每 1–3 秒一次视觉变化（F 风格 0.3–0.6 秒）
- 章节编号 1、2、3…
- 结尾 CTA：评论/私信关键词
