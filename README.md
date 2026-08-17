<div align="center">

# 秋秋工作台搭建器

把一个模糊的想法，变成一个真正每天都能打开、能记录、能执行的个人工作台。

个人效率 · 生活管理 · 内容创作 · WorkBuddy Skill

[![GitHub](https://img.shields.io/badge/GitHub-qqhkx2027-181717?style=flat-square&logo=github)](https://github.com/qqhkx2027/qiuqiu-workbench-builder)
[![Skill](https://img.shields.io/badge/Skill-可安装-ef7899?style=flat-square)](https://github.com/qqhkx2027/qiuqiu-workbench-builder/blob/main/SKILL.md)

[安装给智能体](#安装给智能体)　·　[查看主题](#主题预览)

</div>

---

## 这是什么

秋秋工作台搭建器是一套可分发的 Skill，也是一份可以直接运行的单文件工作台模板。

你只需要描述“想管理什么、每天要看什么”，智能体就可以先提问、再整理信息架构，最后生成一个适合你的工作台。它适合：

- 待办、日程与目标管理
- 记账、资产与投资记录
- 学习、书影音与习惯打卡
- 健康、饮食与运动记录
- 自媒体选题、排期与复盘
- 家庭、生活和个人信息中枢

核心思路很简单：先把真正会使用的内容放进去，再用主题、图标和布局完成个性化。

### 主题预览

| 主题 | 风格 | 适合场景 |
| --- | --- | --- |
| [秋秋同款粉色](https://qqhkx2027.github.io/qiuqiu-workbench-builder/pink.html) | 柔和、轻盈 | 日常生活与内容创作 |
| [极简兼容](https://qqhkx2027.github.io/qiuqiu-workbench-builder/) | 清爽、克制 | 第一次使用或自定义主题 |
| [酷帅黑](https://qqhkx2027.github.io/qiuqiu-workbench-builder/dark.html) | 深色、高对比 | 长时间查看与夜间使用 |
| [玉桂狗蓝](https://qqhkx2027.github.io/qiuqiu-workbench-builder/cinnamoroll.html) | 蓝白、清新 | 学习与轻量记录 |
| [POP MART 糖果色](https://qqhkx2027.github.io/qiuqiu-workbench-builder/popmart.html) | 玩具感、彩色 | 喜欢收藏和视觉装饰 |
| [Kuromi 紫夜](https://qqhkx2027.github.io/qiuqiu-workbench-builder/kuromi.html) | 深紫、个性 | 喜欢暗色与潮流风格 |

## 安装给智能体

最简单的方式，是把下面这段话和仓库地址一起发给你的智能体：

```text
请安装这个 Skill，并读取其中的 SKILL.md、references/ 和 assets/，
然后根据我的需求搭建或修改一个个人工作台：
https://github.com/qqhkx2027/qiuqiu-workbench-builder
```

安装后可以直接这样说：

```text
帮我做一个自媒体工作台，包含选题、排期、待发布内容和数据复盘，手机上也要好用。
```

```text
我想做一个减脂工作台，请先用苏格拉底提问法，一次只问我一个问题。
```

## 秋秋工作法

Skill 默认按四步推进，避免一上来就堆功能：

1. **打开灵感**：从一个接近目标的模板开始。
2. **苏格拉底提问**：一次只问一个问题，确认人群、目标、数据和优先级。
3. **完善细节**：把大方向拆成真正会使用的模块和字段。
4. **调整美化**：结构稳定后，再选择主题、图标、颜色和布局。

可以直接复制这段提示词：

```text
我想做一个专属我的 AI 工作台。请先不要写代码，使用苏格拉底提问法，一次只问我一个问题，
依次了解：使用人群、每天最重要的动作、需要记录的数据、信息来源、模块优先级、提醒方式和视觉风格。
每次得到回答后，先用一句话总结你的理解，再问下一个问题；当你完全理解后，给出不超过 4 个核心模块的页面结构和字段清单。
```

详细方法见：[秋秋工作台方法](references/qiuqiu-workbench-method.md)。

## 内置能力

| 能力 | 说明 |
| --- | --- |
| 本地数据 | 使用浏览器 `localStorage` 保存，刷新后不丢失 |
| 增删改查 | 待办、目标、日程、资讯、账本、媒体、日记等模块支持编辑和删除 |
| 数据备份 | 支持 JSON 导出、导入恢复和清空示例 |
| 今日入口 | 优先展示逾期、今天和临近到期事项 |
| 移动适配 | 手机单列布局、较大的点击区域和底部安全区 |
| 多主题 | 同一份工作台生成多套视觉变体，数据前缀相互隔离 |
| 离线文件 | 生成后的 HTML 不依赖后端、框架、CDN 或账号系统 |

## 数据与隐私

- 工作台数据默认只保存在当前浏览器，不会自动上传到项目服务器。
- 换设备前，请先使用“导出备份”；不同设备的本地数据彼此独立。
- 公开的 GitHub Pages 只负责提供页面文件，不代表账号级数据同步或加密存储。
- 项目示例不包含真实个人隐私数据。

<details>
<summary><strong>给贡献者：项目结构、构建和主题扩展</strong></summary>

## 项目结构

项目采用“一份源模板，多套主题输出”的方式维护：

```text
自然语言需求
      ↓
SKILL.md + references/
      ↓
assets/qiuqiu-workbench-source.html
      ↓ 主题令牌 + 图标映射
dist/*.html
```

```text
qiuqiu-workbench-builder/
├── SKILL.md                         # 智能体读取的核心技能规则
├── agents/openai.yaml               # 技能元数据
├── references/
│   ├── standards.md                 # 工作台设计、数据和主题标准
│   └── qiuqiu-workbench-method.md   # 秋秋方法与提问模板
├── assets/
│   ├── starter.html                 # 轻量起始模板
│   ├── qiqiu-workbench-source.html  # 完整生产源文件
│   └── icons/                       # PNG 预览、brand 和 icons.js 运行时清单
├── scripts/build.js                 # 构建所有主题并运行冒烟测试
├── tools/generate_theme_icons.py    # 生成图片主题图标
└── dist/                            # GitHub Pages 使用的静态 HTML
```

### 本地检查

修改源文件或主题后运行：

```bash
node scripts/build.js
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

构建成功必须看到：

```text
ALL VARIANTS PASSED
Skill is valid!
```

</details>

## 相关链接

- [GitHub 仓库](https://github.com/qqhkx2027/qiuqiu-workbench-builder)
- [SKILL.md](https://github.com/qqhkx2027/qiuqiu-workbench-builder/blob/main/SKILL.md)

<div align="center">

如果这个项目对你有帮助，欢迎试用、提出建议，或者把它交给你的智能体继续定制。

</div>
