# video-editor-skill

我们团队的短视频剪辑 Skill（给 Claude 用）。

- `.claude/skills/video-editor/SKILL.md`：工作流程和风格判断
- `.claude/skills/video-editor/references/styles.md`：风格模板 A–I
- `.claude/skills/video-editor/picker/picker.html`：风格/字体/颜色可视化选择器
- `.claude/skills/video-editor/scripts/neon_ribbon/`：风格 I 渲染脚本（Python + ffmpeg）
- `.claude/skills/video-editor/references/toolkit.md`：字体、特效、转场、音效、音乐、灯光、调色、输出
- `.claude/skills/video-editor/references/sources.md`：参考视频清单

用法：在 Claude Code 开新 session 时选这个仓库，Claude 会自动加载这个 skill。

## 怎么用（新 chat）
1. 开新 chat 时选/加上这个仓库（bernicebpgroup/videoedit）
2. 上传口播视频，说「帮我剪」，可以顺便贴讲稿
3. Claude 显示可视化选择器 → 点选风格、字体、颜色、字幕
4. Claude 先出 8–10 秒样片 → 你确认 → 出完整 mp4（1080×1920）
