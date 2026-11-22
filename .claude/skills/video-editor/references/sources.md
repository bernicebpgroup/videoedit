# 训练参考视频

| 链接 | 账号 | 重点 | 风格 | 声音 |
|---|---|---|---|---|
| https://www.instagram.com/reel/Df7MVQ-iDIE/ | AI Video Editing with Claude | 风格 | A | 已听（转写 + 频谱） |
| https://www.instagram.com/reel/DfnCiOkRGOH/ | jenna sutela / arcads | 特效 | A | 已听（转写 + 频谱） |
| https://www.instagram.com/reel/DfyeGBQzjfm/ | Romina Aminian | 字幕 | B | 已听（转写 + 频谱） |
| https://www.instagram.com/reel/Dfc6mpNuYvw/ | benimedia | 风格 | C | 已听（转写 + 频谱） |
| https://www.instagram.com/reel/Df2WYU9xpxq/ | jenna sutela / arcads | 灯光 | D | 已听（转写 + 频谱） |
| https://www.instagram.com/reel/DfZivEts0Fz/ | Milad Aslani | 声音 + 风格 | F | 已听（转写 + 频谱） |
| https://www.instagram.com/reel/Df-5A1_x_MS/ | Edita Visuals | 风格（放大放小） | G | 已听（转写 + 频谱） |
| https://www.instagram.com/reel/DdHguJfhYSU/ | GP Multimedia | 字在人后 + 一秒一个特效 | H | 已听（转写 + 频谱） |
| https://www.facebook.com/share/r/19vw37vrsP/ | — | 特效 | 未分析（网络无法访问 Facebook） | — |

## 分析方法（声音）
- faster-whisper（small）转文字，带每个词的时间
- ffmpeg `showspectrumpic` 看频谱：riser = 斜线往上爬；impact = 低频亮块；whoosh = 高频噪声渐强；chime/beep = 水平细线
- 比较"说话时"和"停顿时"的低频音量 → 判断有没有背景音乐
- 低频 onset 自相关 → 估 BPM
- ffmpeg `ebur128` → 整片 LUFS

注意：自动检测的 hit 时间点有误差（辅音也会被当成高频 burst），结论以频谱图 + 画面对照为准。

## 待办
- Facebook 那条：用户下载后上传再分析
