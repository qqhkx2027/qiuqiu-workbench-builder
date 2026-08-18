---
name: qiuqiu-workbench-builder
description: 把个人效率、生活管理或内容创作需求整理成可离线使用、可备份、可分享的单文件 HTML 工作台，并提供统一的新增、查看、编辑、删除和主题扩展流程。适用于待办、记账、学习、健康、自媒体、家庭和 WorkBuddy 工作台；当用户希望手机电脑都能用、刷新不丢数据、导出备份或部署分享时使用。
---

# 秋秋工作台搭建技能

优先复用本技能的模板和数据模型，把模糊想法交付成一个打开就能用的单文件 HTML。先保证信息结构，再处理视觉主题。

## 快速判断

- **只想查看或试用**：直接给在线预览，不要求安装 Node 或本地构建。
- **想新建工作台**：先确认人群、目标和最常用的 3–4 个模块，再从模板开始。
- **想修改已有工作台**：先定位模块和数据字段，只改相关源文件，保留旧 localStorage key。
- **想删除内容**：区分“删除单条记录”和“清空示例”；清空前必须二次确认。
- **想备份或迁移**：使用页面的“导出备份 / 导入恢复”，不要把真实隐私数据写进示例或仓库。

默认在线入口：[秋秋工作台](https://qqhkx2027.github.io/qiuqiu-workbench-builder/)。

## 秋秋工作法

1. **打开灵感**：选一个接近需求的模板作为底板。
2. **苏格拉底提问**：一次只问一个问题，依次明确使用人群、每天最重要的动作、数据来源、优先级和提醒方式。
3. **完善细节**：把“价值、健康、生活”等大类拆成真正会使用的子模块。
4. **调整美化**：结构稳定后，再选择主题、图标、颜色和布局。

当用户说不清楚模块时，先使用：

> 现在的风格和排版我不太喜欢，请用苏格拉底提问法向我提问，一次只问一个问题，直到你完全理解我想要的工作台。

详细提问模板见 [秋秋工作台方法](references/qiuqiu-workbench-method.md)；设计与数据标准见 [standards.md](references/standards.md)。

## 用户操作契约（CRUD）

| 操作 | 页面行为 | 实现约束 |
| --- | --- | --- |
| 新增 Create | 使用模块卡片的“+ 添加 / 记一笔” | 表单保存后立即刷新当前模块并提示结果 |
| 查看 Read | 首页概览、模块列表、详情弹窗和子标签 | 空列表显示下一步提示，不显示空白页 |
| 修改 Update | 列表中的“编辑”、状态切换、表单保存 | 只更新目标记录，不覆盖同模块其他数据 |
| 删除 Delete | 列表中的“删除 / ×” | 只删除目标记录；“清示例”必须二次确认 |
| 备份 Restore | “导出备份 / 导入恢复” | JSON 仅在当前浏览器读写，导入失败要给出提示 |

首次打开不能是空白页：每个核心模块提供 3–5 条示例，其中至少 1 条展示待处理状态，并提供清空示例入口。

## 实现规则

- 首版最多 3–4 个核心模块；新增模块按 key 增量 seed，不覆盖旧数据。
- 数据默认保存在浏览器 `localStorage`，每套主题使用独立前缀；不上传用户数据。
- 首屏优先展示今天、逾期或临近到期事项；移动端使用单列布局和至少 44px 点击区。
- 单文件优先：CSS、JS、SVG、图标全部内联，不依赖 CDN、框架、远程字体或账号系统。
- 记账使用 `¥`、`YYYY-MM-DD`，支出红色、收入绿色；表格在窄屏可横向滚动或转卡片。

## 维护者工作流

1. 只修改 `assets/qiuqiu-workbench-source.html` 这一份业务源文件；保留 `{{THEME}}`、`{{PREFIX}}`、`{{TITLE}}` 三个令牌。
2. 新增主题时同时补齐 `scripts/build.js` 变体、源文件 `data-theme` CSS 和 `assets/icons/icons.js` 图标集合。
3. 图片主题使用（同时生成 PNG 预览和运行时图标清单）：

   ```bash
   python3 tools/generate_theme_icons.py <theme> "/path/to/images" [--brand-index N]
   python3 tools/patch_icons.py
   node scripts/build.js
   ```

   脚本按文件名读取至少 9 张 JPG/PNG/WEBP 图片，把统一裁切的 120px PNG 保存到 `assets/icons/`，再把同一批图标写成 data URI；原图可以留在仓库外。

4. 构建脚本会生成 `dist/` 下的每套主题，并对所有模块和子标签运行 Node `vm` 冒烟测试。必须看到 `ALL VARIANTS PASSED`。
5. 运行 Skill 校验：

   ```bash
   python3 tools/validate_skill.py .
   ```

6. 人工检查移动窄屏、主题图标、增删改、导入导出、清空确认和示例数据，再分享在线链接；不要把 `file://` 当作分享链接。

## 当前主题

`minimal`（极简兼容） · `pink`（秋秋粉色） · `dark`（旧版深色） · `cinnamoroll`（玉桂狗蓝） · `popmart`（POP MART 糖果色） · `kuromi`（Kuromi 紫夜）。每套主题都有独立 localStorage 前缀。

## 文件导航

- `assets/qiuqiu-workbench-source.html`：9 个模块、6 套主题的生产源文件。
- `assets/starter.html`：从零搭建轻量工作台的起始模板。
- `scripts/build.js`：生成所有离线 HTML 并运行全量冒烟测试。
- `tools/generate_theme_icons.py`：统一生成图片主题 PNG 预览和 `icons.js` 映射；`tools/generate_icons.py`：旧版三丽鸥九宫格兼容流水线。
- `tools/patch_icons.py`：把图标映射和图片导航注入源文件。
- `references/standards.md`：详细设计、数据兼容和主题标准。
- `references/qiuqiu-workbench-method.md`：秋秋工作法、提问模板和示例信息架构。
