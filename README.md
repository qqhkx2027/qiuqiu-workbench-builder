# qiuqiu-workbench-builder

秋秋工作台搭建 Skill：把一个模糊的想法，整理成可离线使用、可备份、可分享的个人工作台。

它适合制作待办、记账、习惯打卡、备考、减脂、育儿、自媒体和全能生活工作台。工作台使用单文件 HTML，不需要后端、框架、账号或 CDN，数据默认保存在用户自己的浏览器中。

## 这个 Skill 能做什么

- 根据用户的目标和使用场景设计工作台信息架构
- 用苏格拉底提问法，把“我也说不清楚”变成清晰的模块和字段
- 从一个源模板生成多套主题风格
- 支持手机、电脑和离线使用
- 使用 `localStorage` 保存数据，刷新后不会丢失
- 提供 JSON 导出、导入恢复和清空示例
- 自动生成示例数据、今天要处理、逾期提醒和基础统计
- 使用 Node 冒烟测试检查所有主题和子模块

## 安装

最简单的方式是把下面这句话和仓库地址一起发给你的智能体：

```text
请安装这个技能仓库，并读取其中的 SKILL.md、references/ 和 assets/：
https://github.com/qqhkx2027/qiuqiu-workbench-builder
```

如果智能体不支持从 GitHub 自动安装，也可以下载仓库，将整个目录放入它的 skills 目录。

## 使用示例

安装后，可以直接这样说：

```text
帮我做一个自媒体工作台，包含选题、待发布内容和数据复盘，手机上也要好用。
```

```text
我想做一个减脂工作台，先用苏格拉底提问法，一次只问我一个问题。
```

```text
把我的工作、学习、财务、健康和生活整理成一个个人工作台，先给我一个不超过 4 个核心模块的版本。
```

当需求还不完整时，Skill 会先询问使用人群、最重要的动作、数据来源、使用频率和视觉偏好，而不是直接堆功能。

## 秋秋工作台方法

工作台遵循四步：

1. **打开灵感**：从一个接近需求的模板开始，不追求第一次就完美。
2. **苏格拉底提问**：一次只问一个问题，逐步确认人群、目标、数据和优先级。
3. **完善细节**：把“价值、健康、生活”等大类拆成真正会使用的子模块。
4. **调整美化**：结构和交互稳定后，再处理图标、颜色、动漫形象和主题风格。

可直接复制给 WorkBuddy 的提示词：

```text
我想做一个专属我的 AI 工作台。请先不要写代码，使用苏格拉底提问法，一次只问我一个问题，依次了解：使用人群、每天最重要的动作、需要记录的数据、信息来源、模块优先级、提醒方式和视觉风格。每次得到回答后，先用一句话总结你的理解，再问下一个问题；当你完全理解后，给出不超过 4 个核心模块的页面结构和字段清单。
```

完整的方法提炼见：[references/qiuqiu-workbench-method.md](references/qiuqiu-workbench-method.md)。

## 内置主题和成品

当前内置 4 套主题：

| 文件 | 主题 |
| --- | --- |
| `dist/index.html` | 极简默认主题 |
| `dist/pink.html` | 少女粉主题 |
| `dist/dark.html` | 酷帅黑主题 |
| `dist/cinnamoroll.html` | 玉桂狗蓝主题 |

`assets/qiqiu-workbench-source.html` 是 9 个模块、4 套主题的完整生产范例；新项目建议从 `assets/starter.html` 开始，首版只做 3–4 个核心模块。

## 本地构建

需要 Node.js 18 或更高版本：

```bash
cd qiuqiu-workbench-builder
node scripts/build.js
```

构建完成后会在 `dist/` 生成主题文件，并自动运行所有主题和子标签的冒烟测试。看到下面这行才算通过：

```text
ALL VARIANTS PASSED
```

然后可以直接打开：

```text
dist/index.html
```

## 目录结构

```text
qiuqiu-workbench-builder/
├── SKILL.md                         # 给智能体读取的技能规则
├── agents/openai.yaml               # 技能列表和默认调用提示
├── references/
│   ├── standards.md                 # 工作台设计标准
│   └── qiuqiu-workbench-method.md   # 秋秋方法和提问模板
├── assets/
│   ├── starter.html                 # 轻量起始模板
│   ├── qiqiu-workbench-source.html  # 完整生产范例
│   └── icons/                       # 内置主题图标
├── scripts/build.js                 # 构建和全变体冒烟测试
├── tools/                           # 图标生成与注入工具
└── dist/                            # 构建后的主题成品
```

## 设计原则

- 首屏优先展示“今天要处理”
- 首次打开不能是空白页，要有可清空的示例数据
- 每个主题使用独立的 `localStorage` 前缀，数据互不覆盖
- 首屏提供导出 JSON 和导入恢复
- 移动端按钮至少 44px，输入框字号至少 16px
- 单文件优先，避免外部依赖导致离线失效
- 新增模块按 key 增量初始化，不覆盖老用户数据
- 不预置真实隐私数据，不宣称本地数据具备账号级加密

详细规范见：[references/standards.md](references/standards.md)。

## 隐私说明

工作台的数据默认只保存在当前浏览器的 `localStorage` 中，不会自动上传服务器。换设备前请使用“导出备份”；部署后的页面链接可以公开访问，但每个设备的数据仍然彼此独立。

## 相关链接

- GitHub：[qqhkx2027/qiuqiu-workbench-builder](https://github.com/qqhkx2027/qiuqiu-workbench-builder)
- 在线技能文件：[SKILL.md](https://github.com/qqhkx2027/qiuqiu-workbench-builder/blob/main/SKILL.md)
