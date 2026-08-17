<div align="center">

# 秋秋工作台搭建器

把一个模糊的想法，变成一个真正能每天使用的个人工作台。

个人效率 · 生活管理 · 内容创作 · WorkBuddy Skill

[在线预览](https://qqhkx2027.github.io/qiuqiu-workbench-builder/) · [安装 Skill](#安装) · [GitHub](https://github.com/qqhkx2027/qiuqiu-workbench-builder)

</div>

---

## 先打开看看

当前版本已经部署好，普通用户不需要安装 Node.js，也不需要本地构建。

**主预览：** [打开秋秋工作台](https://qqhkx2027.github.io/qiuqiu-workbench-builder/)

| 主题 | 预览 |
| --- | --- |
| 默认极简 | [打开](https://qqhkx2027.github.io/qiuqiu-workbench-builder/) |
| 秋秋粉色 | [打开](https://qqhkx2027.github.io/qiuqiu-workbench-builder/pink.html) |
| 酷帅黑 | [打开](https://qqhkx2027.github.io/qiuqiu-workbench-builder/dark.html) |
| 玉桂狗蓝 | [打开](https://qqhkx2027.github.io/qiuqiu-workbench-builder/cinnamoroll.html) |
| POP MART 糖果色 | [打开](https://qqhkx2027.github.io/qiuqiu-workbench-builder/popmart.html) |
| Kuromi 紫夜 | [打开](https://qqhkx2027.github.io/qiuqiu-workbench-builder/kuromi.html) |

POP MART 主题使用你提供的 10 张图片生成 9 个导航图标和 1 个工作台头像；Kuromi 主题使用 9 张图片生成对应图标。原图不写入成品，图标会压缩后内联到单文件 HTML。

也可以直接打开 WorkBuddy 版本：[秋秋工作台 · pink](https://eee341961ba346b4be4538e1e8703b3e.app.workbuddy.link/pink.html)

## 这是什么

`qiuqiu-workbench-builder` 是一个可分发的 Skill，帮助智能体把用户的目标整理成可使用的个人工作台。

它不要求用户会写代码，适合制作：

- 待办与日程工作台
- 记账与资产工作台
- 学习、备考与习惯打卡工作台
- 健身、减脂与健康管理工作台
- 自媒体选题、发布与复盘工作台
- 家庭、育儿和全能生活工作台

## 安装

最简单的方式：把下面这段话和仓库地址一起发给你的智能体。

```text
请安装这个 Skill，并读取其中的 SKILL.md、references/ 和 assets/：
https://github.com/qqhkx2027/qiuqiu-workbench-builder
```

安装后，直接用自然语言描述你的需求即可：

```text
帮我做一个自媒体工作台，包含选题、待发布内容和数据复盘，手机上也要好用。
```

```text
我想做一个减脂工作台，请先用苏格拉底提问法，一次只问我一个问题。
```

## 怎么使用

普通用户直接打开在线预览，或把仓库地址交给智能体安装 Skill：

| 目的 | 可以这样说 | 结果 |
| --- | --- | --- |
| 查看 | “打开秋秋工作台的 Kuromi 主题” | 返回对应在线页面 |
| 新增 | “新增一个自媒体排期，包含平台、日期和状态” | 弹窗填写后保存到当前浏览器 |
| 修改 | “把这条排期改成已发布” | 只更新选中的记录 |
| 删除 | “删除这条排期” | 只删除目标记录并刷新列表 |
| 备份 | “导出我的工作台数据” | 下载 JSON，可在另一台设备导入 |

数据只保存在当前浏览器。清空示例会同时清除当前浏览器中的个人记录，操作前会二次确认。

## 秋秋工作法

工作台不是功能越多越好，而是打开后能立刻处理最重要的事情。Skill 默认按四步推进：

1. **打开灵感**：从一个接近需求的模板开始。
2. **苏格拉底提问**：一次只问一个问题，确认人群、目标、数据和优先级。
3. **完善细节**：把“价值、健康、生活”等大类拆成真正会使用的模块。
4. **调整美化**：结构稳定后，再处理图标、颜色和主题风格。

可直接复制给 WorkBuddy：

```text
我想做一个专属我的 AI 工作台。请先不要写代码，使用苏格拉底提问法，一次只问我一个问题，依次了解：使用人群、每天最重要的动作、需要记录的数据、信息来源、模块优先级、提醒方式和视觉风格。每次得到回答后，先用一句话总结你的理解，再问下一个问题；当你完全理解后，给出不超过 4 个核心模块的页面结构和字段清单。
```

详细方法见：[秋秋工作台方法](references/qiuqiu-workbench-method.md)。

## 内置能力

| 能力 | 说明 |
| --- | --- |
| 本地数据 | 使用浏览器 `localStorage` 保存，刷新后不丢失 |
| 数据备份 | 首屏提供 JSON 导出、导入恢复和清空示例 |
| 今日入口 | 优先显示逾期、今天和临近到期事项 |
| 移动适配 | 手机单列布局、44px 点击区、底部安全区 |
| 多主题 | 一份源模板生成多套视觉变体（含 POP MART、Kuromi），数据前缀相互隔离 |
| 离线文件 | 生成后的单文件 HTML 不依赖后端、框架或 CDN |

## 项目结构

```text
qiuqiu-workbench-builder/
├── SKILL.md                         # 智能体读取的核心技能规则
├── agents/openai.yaml               # 技能列表元数据
├── references/
│   ├── standards.md                 # 工作台设计标准
│   └── qiuqiu-workbench-method.md   # 秋秋方法与提问模板
├── assets/
│   ├── starter.html                 # 轻量起始模板
│   ├── qiqiu-workbench-source.html  # 完整生产范例
│   └── icons/                       # 主题图标资源（含 POP MART、Kuromi 优化图标）
├── scripts/build.js                 # 维护者构建与冒烟测试
├── tools/generate_theme_icons.py    # 统一生成图片主题图标
├── tools/generate_icons.py          # 旧版九宫格图标兼容脚本
└── dist/                            # 已生成的在线预览文件
```

## 普通用户不需要本地构建

直接使用上面的在线预览即可。

`assets/`、`scripts/` 和 `dist/` 主要服务于技能维护者：当需要修改模板、增加主题或生成离线 HTML 时，维护者才需要运行构建脚本。它不是普通用户的安装前置条件。

## 数据与隐私

- 工作台数据默认只保存在当前浏览器中，不会自动上传。
- 换设备前，请先使用“导出备份”。
- 部署后的页面链接可以公开访问，但不同设备的本地数据彼此独立。
- 项目不预置真实个人隐私数据，也不把 `localStorage` 宣称为账号级加密。

## 维护者检查

修改模板后运行：

```bash
node scripts/build.js
```

构建脚本会检查所有主题和子模块，必须看到：

```text
ALL VARIANTS PASSED
```

技能元数据可用以下命令检查：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## 相关链接

- [GitHub 仓库](https://github.com/qqhkx2027/qiuqiu-workbench-builder)
- [Skill 文件](https://github.com/qqhkx2027/qiuqiu-workbench-builder/blob/main/SKILL.md)
- [在线预览](https://qqhkx2027.github.io/qiuqiu-workbench-builder/)
