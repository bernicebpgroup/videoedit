# 风格模板 A–I

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

## G. 暖色套框展示风（Warm Studio Showcase / 放大放小）
**来源**：Df-5A1_x_MS（Edita Visuals，约 9.5 秒，**已听声音**）
- **适合**：工作室/公司介绍、招聘、"AI 帮我剪的"作品展示、个人品牌自我介绍
- **核心技巧：放大放小（scale in / scale out）**
  - 0–1.8s 全屏正常播放（人物坐在单人沙发，大全景）
  - **约 1.8–2.1s 整个画面缩小成一张圆角卡片（约 0.3 秒，先快后慢 ease-out）**，露出浅灰底的"展示台"：左后方一张黑白小卡"Raw footage"（原片），顶部徽章"Opus 5.5"，底部固定文案 "Follow & comment "CLAUDE" for the full guide"
  - 卡片里的内容继续播放，里面再做推近（机器人画面慢慢放大）→ **外框不动、里面在动**，层次感强
  - 切场景时用一张深色卡（发光蓝色 3D 像素人偶）闪一下，跟片头呼应
  - 结尾新图片以小卡片"弹出 + 放大"叠在主画面上
- **配色**：暖米色墙 + 陶土橘/赤陶色 #B4552F 左右（大字、像素方块）+ 白 + 浅灰展示台；Claude 橘色点缀
- **字体**：超粗斜体无衬线大字（Archivo Black Italic / Inter Black Italic 类），字很大、放在人物上方的墙面；搭配细斜体小字引导（"My name is"、"The AI"、"Who can edit with"）
- **文字特效**：
  - 大字逐字母打出（E → Ed → Edi → Edita），字母之间有错位/重影
  - 陶土色**像素小方块**散落在字周围，像数字碎片
  - 一条白色波浪线从上往下画出（line draw 转场）
  - 墙上弹出照片卡（白框、有阴影），像挂在墙上的画
  - 招聘句："Right now we're hiring **CREATIVE** **AMBITIOUS EDITORS**"，关键词超粗大写，配纸飞机、播放键小图标
- **画面素材**：真人口播大全景 + AI 生成画面（云中 3D 机器人）+ AI 人像照片卡
- **声音（实测）**：**没有旁白**（转写不到语音），音乐 + 音效驱动，整片 -14.1 LUFS
  - 0–1.4s：**很重的低频轰鸣（sub boom）**，对上片头深色 3D 人偶 → 一开场就"震"一下
  - 开头和 5.3s、7.4s：高频**下滑闪烁音**（频谱上一串往下的斜线，sparkle swish），对上画面切换
  - 全程：短促的**拨弦/plucky 旋律**（600–1100Hz 短音，带滑音），轻快
  - 1.5–1.9s：密集 click，对上像素方块和字母出现
  - 约 2.2–2.4s：上扬 whoosh，对上**画面缩小成卡片**
  - 约 3.9–4.7s：**高频突然被切掉（低通滤波）**，对上进入云朵机器人场景 → 声音"闷"一下制造空间感，再打开
  - 结尾：click + 闪烁音配合卡片弹出
- **结构**：自我介绍"My name is Edita"→ 身份"OWNER"→ 缩小成展示卡 →"The AI Editing Studio"→ 招聘"Right now we're hiring creative ambitious editors"→"Who can edit with Claude"→ 底部 CTA 全程挂着

## H. 高密度特效口播（1 秒 1 个效果 / 字在人后面）
**来源**：DdHguJfhYSU（GP Multimedia，房产视频服务商，26.7 秒，已听声音）
- **适合**：房产经纪、个人品牌、服务介绍；边走边讲的户外口播（人物从远处走向镜头）
- **核心节奏**：**大约每 1 秒换一个视觉效果**，每个效果都"把那句话画出来"（字面意思视觉化）
- **核心技巧：字在人后面（text behind person）**：人像抠图（segmentation），大字放在背景和人物之间，人走动时会挡住部分字母 → 立体感、高级感
- **逐秒拆解（实测）**：
  | 时间 | 台词 | 效果 |
  |---|---|---|
  | 0–0.8s | I can tell you my videos | 三色叠字：小白字 + 橘色 "tell you" + 蓝色大字 "MY VIDEOS" |
  | 1.0s | work | 黑色粗体 "WORK"，**在人后面** |
  | 1.25–1.75s | all day | **天空替换：白天 → 夕阳 → 黄昏 → 夜晚**（"all day" 字面化），大字 "ALL"、"DAY" 在人后面 |
  | 2.0s | or | 银色金属质感 "OR" |
  | 2.5s | I can show you | 橘色字 |
  | 3.25–4.25s | in less than 10 seconds | 橘色圆形擦出 → 巨大橘色 "10" **在人后面** → "SECONDS" |
  | 4.5s | — | **甩镜 + 运动模糊**切到新地点 |
  | 4.75–6.75s | 450,000 views | 两张作品截图浮在头顶 + **数字从 0 跳到 450,000** + 红色爱心一颗颗飘出 |
  | 6.75–7.25s | my business | 品牌 logo "GP Multimedia"（打字机衬线字）出现在头顶 |
  | 7.5–9.0s | as a young entrepreneur | **画面变黑白**，橘+蓝双色字 "YOUNG ENTREPRENEUR" |
  | 9.0–9.5s | that kind of reach | **颜色回来**，黑色大字 "REACH" 在人后面 |
  | 9.75s | — | 白闪 |
  | 10–12s | has completely changed… | 小号逐词字幕（一次一个词，放在胸口），给眼睛休息 |
  | 12.0–13.3s | but that didn't happen by accident | 换地点；酒红色巨字 "DIDN'T" 在人后面 + "BY ACCIDENT" |
  | 13.5s | — | 过曝白光 / 黄色漏光转场 |
  | 14–15s | the hooks, the pacing, the edits | 头顶出现一圈**蓝色发光 3D 图标**（相机、手机、剪辑） |
  | 15.25–16s | everything | 青色发光 3D 大字 "EVERYTHING" |
  | 17.25–18.5s | and that attention | 橘色小字 + 蓝色大字 "ATTENTION" 在头顶 |
  | 18.75–19.5s | real leads, real opportunities | 腰部位置弹出 UI 小标签 "Real Leads" |
  | 20.75s | — | 运动模糊转场到第三个地点 |
  | 21–23.5s | if you're ready… | 小号逐词字幕 |
  | 23.75–25s | my number's right here | 肩膀旁边浮出**来电卡片**（头像 + 电话号码 + 绿色接听键） |
  | 25.25–26.7s | DM me "VIDEO" | 黑色粗体 "DM ME" 滑入（在人后面）+ 白色粗体 "VIDEO" |
- **规律**：
  - 大效果（字在人后、天空替换、数字跳动）和小字幕（一次一个词）**交替**，不会一直很满
  - 每 4–8 秒**换一个拍摄地点**，用甩镜/运动模糊/白闪接
  - 颜色固定 3 个：橘、蓝、黑（加白）
  - 字体：超粗无衬线（类似 Montserrat Black / Anton），全大写；品牌 logo 用打字机衬线
- **拍摄要求**：人物边走边讲、从远走近、背景开阔（天空多）→ 方便字放在人后面、方便换天空
- **声音（实测）**：人声 + 全程背景音乐（低频一直在），整片 -14.1 LUFS；约 6.5–7.2s 有高频闪烁音（数字停在 450,000、logo 出现时）；转场有 whoosh
- **技术做法**：人像分割模型（rembg u2net_human_seg / MediaPipe selfie segmenter / RMBG）逐帧抠人 → 背景层 + 文字层 + 人物层叠合；天空替换 = 天空分割 + 换天空素材

## I. 霓虹飘带成片风（Neon Ribbon Showcase）
**来源**：DfsjIgTj8-9（eightsenses.media，约 10 秒，**声音未听**：只看了静音画面，声音部分为推测）
- **适合**：口播教学、服务介绍、个人品牌；想让普通白墙/办公室口播"看起来像专业剪辑师做的"；也适合做"Before/After 剪辑展示"帖
- **画面**：人物抠像，背景柔焦提亮（原片是白色影棚）；一条**黄绿 3D 飘带**绕着人螺旋，从头后面穿过、从身前绕出（真实前后遮挡）
- **配色**：米白/浅灰底 + **荧光黄绿 #D4F23A 左右** 单一强调色 + 深墨色 UI；飘带用亮面黄绿 / 暗面橄榄绿做明暗
- **字体**：关键词 = 粗衬线斜体（Crimson Text Bold Italic / Playfair Italic；中文 Noto Serif CJK Black + 仿斜体），荧光黄绿 + 深色描边阴影；引导小字 = 白色粗无衬线（Inter ExtraBold），放在关键词左上/右下
- **字幕/元素**：
  - 关键词大字垫**胶片框**（深色圆角条 + 上下齿孔，里面是模糊画面），回弹弹出
  - **白色卡片 + 荧光圆形图标**（地点/房子/搜索/拍卖槌…）依次弹出、上下浮动、扇形微旋转
  - **白色胶囊标签**（荧光圆点 + 文字），如 "hard-working"
  - **圆形模式**：画面收成圆形人像，外圈**旋转环形字** + 荧光进度环，下面接标签和一排人物/图标卡片
  - **音频条/时间轴**：深色圆角条里一排荧光竖条，跟人声音量跳
  - 社媒图标（IG/FB）+ 视频缩略图卡片在人物身后浮出（讲到 marketing 时）
- **转场**：每句一次推/拉（1.0↔1.1）；圆形虹膜收/放；元素都是 back-out 回弹
- **节奏**：约每 1.5–2 秒换一种图形包装，基本没有"只有人在说话"的空镜
- **声音（推测，未实测）**：轻电子/科技感背景音乐；元素弹出配 pop/click，圆形转场配 whoosh
- **展示帖包装（可选）**：深灰金属竖条纹底 + 铬银大标题 "CLAUDE"、仿评论气泡钩子 "AI can't do this effect."、左 BEFORE 右 AFTER 卡片、仿终端窗口 "Render reel.mp4? › 1. Yes"、"Claude Skill" 标签；文案 "Comment EDIT…" 评论引流（这条评论 9.9k > 点赞 4.8k）
- **本环境渲染**：`scripts/neon_ribbon/`（prepare.py → spec.json → render.py），说明见该目录 README。字体/重点色/发光可换（spec 的 `look`），默认不调色（`bg_lift: 0`）、大字无黑边，符合团队偏好
- **结构**：钩子关键词（0–2s）→ 卡片/图标解释 → 圆形模式强调重点 → 音频条/关键词收尾 → CTA
