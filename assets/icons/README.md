# 主题图标资源

这个目录同时保存两种东西：

- `*_01.png` 到 `*_09.png`：经过统一裁切的 120px 预览文件，方便在 GitHub 上检查每个主题的图标顺序。
- `*_brand.png`：工作台左上角头像使用的图标。
- `icons.js`：运行时图标清单。它把每套主题的 9 个模块图标和 `brand` 写成内联 PNG Base64，构建时注入单文件 HTML。

模块顺序固定为：

`home`（首页）→ `todo`（待办）→ `create`（创作）→ `media`（书影）→ `ledger`（记账）→ `health`（健康）→ `diary`（日记）→ `finance`（财经）→ `ai`（AI）。

因此，普通用户不需要下载这个目录里的图片；在线页面和导出的 HTML 使用的是 `icons.js` 中的内联数据，断网也能显示。新增主题时，使用统一脚本会同时生成预览 PNG 和运行时映射：

```bash
python3 tools/generate_theme_icons.py <theme> "/path/to/images" [--brand-index N]
python3 tools/patch_icons.py
node scripts/build.js
```

原始照片只作为本地输入，不提交到仓库；仓库内只保留压缩后的图标成品。
