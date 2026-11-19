# 风格模板 A–F

每个风格都写：适合 / 配色 / 字体 / 字幕动画 / 特效 / 转场 / 音效与音乐 / 结构。

---

## A. AI 界面演示风（Tech Demo）
**来源**：Df7MVQ-iDIE（Claude 剪房产）、DfnCiOkRGOH（/effects 指令）
- **适合**：AI 工具、软件、自动化教学，"一条指令→成片"
- **配色**：深色底 + 青蓝竖条光栅渐变；强调色黄绿 / 荧光绿；UI 用深灰卡片
- **字体**：无衬线（Inter / SF Pro / Geist）；关键词大号黄绿 + 外发光
- **字幕**：小字引导（"on nearly three"）+ 大字关键词（"acres"）；关键词放在人物背后（人像抠图，文字夹中间）
- **特效**：
  - 仿 AI 聊天界面套框：输入区（素材缩略图、技能标签、指令）→ "Here is your reel" → 成片预览 + 功能清单打勾
  - 打字机打指令 `/effects orbit` + 闪光标
  - orbit（照片卡片绕人旋转）、glass widgets（毛玻璃数据卡）、white collage（黑白人像+粗体大字）、comment box（评论/私信气泡）
  - 打勾清单逐条弹出（✓ Nearly 3 acres / ✓ Fully fenced / ✓ Gated land）
  - 鼠标点 Download → 变 Saved（完成闭环）
- **转场**：推镜头 + 运动模糊 + 震动；预览卡片扇形堆叠
- **声音（实测）**：
  - **Df7 房产**：人声口播 + **全程背景音乐**（低频在说话和停顿时一样大 → 音乐一直铺着），约 136 BPM 偏快、有鼓点；整片 -14 LUFS
    - 0.98–1.25s 高频 pop：对上 "unique" 大字在人物背后弹出
    - 4.0–5.6s 高频闪烁音（约 15kHz 细线，sparkle/twinkle）：对上打勾清单逐条弹出
    - 4.67s 低频 hit：对上 "fully fenced" 打勾
    - 5.85s 低频 impact（在两句之间的停顿里）：对上推镜头 + 运动模糊转场
    - 8.08s 低频 hit：对上结尾 CTA 按钮出现
  - **Dfn 特效指令**：
    - 前 1.5 秒只有人声、几乎没有音乐 → **1.6s 音乐低音进来（beat drop）**，正好是第一个特效预览弹出的时刻
    - 之后低音音乐很重（这几条里最响的低频），约 112 BPM
    - 大约每 1.3 秒一次 7kHz 左右的高频短音（打字/whoosh），对上每条 `/effects` 指令打完、预览窗弹出
    - 口播是重复的节奏句（转写为 "Write this to get this" ×4，实际可能是 "Type this, get this"），每说一次换一个特效 → **用重复句子做节奏钩子**
    - 10s 后切到第二段："Comment CUT and I'll send you the guide"
- **结构**：顶部评论气泡钩子（"AI can't edit real estate videos."）→ 指令 → 成片演示 → CTA 气泡/按钮（"Contact me today ▸"）→ COMMENT "关键词"

## B. 杂志衬线风（Editorial Serif）
**来源**：DfyeGBQzjfm（5 easy edits）
- **适合**：个人品牌、生活方式、女性向、教学干货
- **配色**：墨绿 #445A3F 左右 + 米白 #F8F5DC 左右；暖色室内光；可加一个人物服装点缀色（红）
- **字体**：高对比衬线（Playfair Display / Bodoni Moda / Didot 类）+ 花体斜体关键词（Cormorant Garamond Italic / Playfair Italic）；负字距（挤一点）
- **字幕动画**：逐词出现，新词先半透明灰 → 变实色，带轻微模糊和上浮；关键词换大号花体（*visual break*、*memes*、*song*）
- **字幕位置**：跟手势和语义走（说"right there"字就在手指的地方；说"move it around"字真的换位置）
- **特效**：开场编号方块（1–5 绿色小方块 + 细线连到标题）
- **章节卡**：墨绿底 + 米白大号衬线数字，数字下方渐变透明（像从下面长出来）；标题逐词加
- **转场**：纯色画面（墨绿/米白交替）当"视觉喘息"、单独展示重点句；偶尔粉紫渐变画面换节奏
- **声音（实测）**：人声口播 + 全程背景音乐（偏轻、中速），整片 -14 LUFS
  - **0–4.7s 开场 riser**：频谱上两条音调从约 1kHz 一路爬到 10kHz，跟开场那句 "Here are five easy edits…" 一样长，**正好在句子结束时到顶** → 切进第 1 章
  - **每张章节卡都有低频 hit**：5.55s（第 1 章 font pairing）、15.74s（"blank colour screen"）、23.96s（第 3 章 music）、37.73s（第 5 章 animations）
  - 34.60s "**but** don't overdo it" 也有一个 hit → 强调转折词
  - 关键词弹出时有轻的高频 pop/click（1.39 "easy"、8.45 "fonts"、11.40 "like"、19.64 "important"、26.26 "right"…）
  - 她讲的第 4 个技巧"用音效强调转场、文字、关键动作，但别过度"，她自己就是这样做的：hit 只给章节卡和转折词，pop 很轻
- **结构**：标题"5 easy edits for instant engagement"→ 1–5 章节，每章 = 章节卡 + 口播示范 → CTA "Comment 'edit'"
- **原则**：subtle transitions，不要过度

## C. 高端品牌对比风（Premium Before/After）
**来源**：Dfc6mpNuYvw（Beni Media 牙科）
- **适合**：医美、牙科、律所、豪宅、高客单价服务；剪辑公司作品展示
- **配色**：薄荷/蒂芙尼绿 + 白 + 深海军蓝底；人物冷调，背景压暗，重暗角
- **字体**：几何无衬线（Montserrat / Poppins），细体 + 粗体强对比
- **字幕**：小字引导（"I'm" / "before you let"）+ 大号粗体关键词加品牌色（**Dr Naz**、**ANYONE**、**APPROVAL**）；扫光擦出、发光色块下划线显字
- **外层框架**：左小窗"NO Edit"原片 + 右大窗"FINAL"成片；圆角卡片 + 玻璃光晕；标签"PREMIUM PERCEPTION"
- **特效**：
  - 地名插图：线稿/冷色 → 真实照片
  - 3D 产品渲染（贴片、牙齿）+ UI 信息卡
  - 问题对比卡片网格（图标 + 照片，逐张往下排）
  - AI 情绪图（偏青色、戏剧化）制造"竞争对手很可怕"的对比
  - ⓘ 小图标点缀；半透明品牌水印
- **章节卡**：薄荷→白渐变底 + 大数字；"You should **never** have to guess"两种字重
- **转场**：白闪、渐变卡片滑入
- **声音（实测）**：人声口播 + 全程背景音乐，整片 -14 LUFS
  - 音乐约 **81 BPM**，慢、稳、有底鼓（低频每 0.74 秒一拍），是电影感/企业高端的铺底
  - 人声只比停顿时高约 3 dB → 音乐压得低但一直存在，撑"高级感"
  - **后半段音乐逐渐变满**（约 34s 后低频更厚），对上第 3 点"奖励"和结尾 → 情绪往上推
  - **43–55s 一串高频音调短音（chime/sparkle，叮）**：对上礼物盒、Sonicare 牙刷、美白套装等赠品图标一个个出现
  - 章节数字卡、扫光显字时有轻 whoosh
- **结构**：地点钩子"If you live in Plano…"→ 自我介绍 → "3 things I want you to know" 1/2/3 → CTA

## D. 清单教学风（Listicle）
**来源**：Df2WYU9xpxq（20 AI lighting setups）
- **适合**："N 个 xxx 你必须知道"类盘点
- **核心技巧**：同人、同机位、同姿势，每 ~1 秒切换一种状态（这里是布光），产生"瞬间变换"魔术感
- **画面布局**：左上角清单 1–20，讲到哪项点亮哪项（已讲变高亮白）；左下小窗放对应参考（AI 生成画面 + 来源标注）
- **字体**：白色小号无衬线
- **结尾**：白色逐词小字幕；logo 带运动模糊飞入；关键词打字机 + 光标（"LIGHT"）
- **声音（实测）**：**没有背景音乐**（低频几乎是 0，停顿时接近静音），整片 -14 LUFS
  - 节奏完全靠人声：0–16s 一口气把 20 个名字念完，平均约 0.8 秒一个，每念一个就跳切换一种布光
  - 词与词之间几乎没有空隙（跳切剪掉了所有停顿）
  - 没有明显的 whoosh/impact，只有切点上很轻的高频 click
  - 16s 后放慢语速讲 CTA："I created all these setups using arcads… comment LIGHT"
  - **结论**：内容本身够有冲击力（画面变化）时，可以完全不放音乐，干净人声 + 快速跳切更有"专业教学"感
- **结构**：标题 + 清单一屏 → 快速轮播 → "I created all these using X" → Comment "关键词"

## E. 极简口播（Default）
- 干净口播 + 逐词字幕（白字黑描边或白字阴影）+ 每 2–3 秒一次 punch-in + 1–2 张 B-roll + 结尾 CTA
- 素材少或不确定时用这个打底，再加其他风格的一两个元素

## F. 动态排版潮流风（Kinetic Type / Motion Design）
**来源**：DfZivEts0Fz（Milad Aslani，约 9 秒，**已听声音**）
- **适合**：品牌宣言、创业/产品、潮流、动态设计作品、8–15 秒超短片
- **画面**：纯白无缝背景（白色影棚），人物全身坐地、抠像感强，大量留白；人物缩放、推拉配合文字
- **配色**：白底 + 深灰文字 + **荧光柠檬绿 #D4FF00 左右** 单一强调色
- **字体**：细瘦的等宽/怪诞无衬线（Space Mono / JetBrains Mono / Geist Mono / Neue Machina 类），字距很紧；搭配**像素字体**（"But"、"?"、像素爱心图标 —— Press Start 2P / Silkscreen）
- **字幕/文字特效**：
  - **乱码解码（text scramble）**：随机字母快速跳动 → 解码成目标词（"rxyrnyt"→"qut j cnf"→"product"）
  - **荧光绿贴纸标签**：倾斜 -5° 到 -10° 的绿底黑字小标签（"Congrats!"、"why it"、"edits"），像贴上去的胶带
  - **角标框**：关键词四角加荧光绿 L 形括号 `⌐ ¬`，像取景框/选中框
  - 句尾荧光绿句点
  - **滚轮选择器（iOS picker）**：列表上下滚动，绿色箭头 ▸ 指着当前项（value → difference → advantage → uniqueness），未选中项变灰变小
  - 对比卡："♡ Competitor's" vs "♥ Your's"（绿底黑心＝你的更好）
  - **像素粒子爆发**：荧光绿像素方块带外发光从人物头部炸开（转场用）
  - 逐词打出（"let's show the world" → "why it" 标签 → "matters" 字母逐个落下）
- **转场**：快速甩镜（whip）+ 运动模糊、画面整体缩小/推走、像素粒子遮罩
- **结尾**：极简 logo 卡——"aslani" + 绿色 "edits" 标签，停留约 1.5 秒
- **节奏**：约 0.3–0.6 秒一个视觉变化，全片 9 秒
- **声音（实测分析）**：**全片没有人声旁白**（转写不到语音），完全由音乐 + 音效设计驱动：
  - 0–1.3s：一连串很密的 **tick/click 故障音**，对上乱码解码字母跳动；夹着 **颤音电子 bleep**（约 1.1kHz 和 5kHz 的锯齿波颤音，8-bit 游戏感）
  - 1.3–1.8s：**上升 riser**（音调往上爬），铺垫
  - ~1.95s：**全片最响的低频 impact / bass drop**，对上像素 "But" 砸下来
  - 2.0–3.4s：**噪声 whoosh 渐强**（高频沙沙声越来越密），对上画面推走转场，3.2s 左右到顶
  - 3.5–4.2s：**阶梯式 UI beep**（约 1kHz 方波短音，一格一声），对上滚轮选择器一项一项切换
  - 4.2–6.6s：音量降下来，轻节奏 click，对上逐词打字（给耳朵喘息）
  - 6.7–7.2s：**第二次 whoosh + impact**，对上 "matters" 落下
  - 7.5–8.8s：故障 tick + 颤音 bleep 回来，对上 logo 收尾
  - **规律**：每个画面动作都有对应音效；"紧-松-紧"三段起伏；整体偏数字/故障/8-bit 音色
- **结构**：钩子"Congrats! You built a product." → 转折"But…"（竞争对手 vs 你的）→ 问题"does anyone understand its value/difference/advantage/uniqueness?" → 宣言"let's show the world why it matters." → logo
