import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
root = os.path.join(HERE, '..')

with open(os.path.join(root, 'assets/icons/icons.js'), 'r', encoding='utf-8') as f:
    icons_js = f.read().strip()

with open(os.path.join(root, 'assets/qiqiu-workbench-source.html'), 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 替换 ICON_IMGS 定义（source.html 中已存在，安全替换整行）
html = re.sub(r"const ICON_IMGS=.*?;\n", icons_js + '\n', html, count=1)

# 2. 替换 MODULES，使用 ICON_IMGS[THEME].key
module_order = ['home','todo','create','media','ledger','health','diary','finance','ai']
names = ['秋秋工作台','我的待办','创作输出','书影学习','记账资产','健康生活','日记反思','财经资讯','AI资讯']
new_modules = "const MODULES=[\n"
for k,n in zip(module_order, names):
    new_modules += f"  {{key:'{k}',name:'{n}',icon:(ICON_IMGS[THEME]||ICON_IMGS['minimal'])['{k}']}},\n"
new_modules += "]\n"
html = re.sub(r"const MODULES=\[[\s\S]*?\];?\n", new_modules, html, count=1)

# 3. 替换 renderNav，支持 img 图标
old_renderNav = '''function renderNav(){
  const html=MODULES.map(m=>`<div class="navitem ${state.view===m.key?'active':''}" data-key="${m.key}" onclick="switchView('${m.key}')">${m.icon?`<span>${m.icon}</span>`:''}<span>${m.name}</span></div>`).join('');
  $('nav').innerHTML=html;
  $('drawerNav').innerHTML=html;
}'''
new_renderNav = '''function renderNav(){
  const html=MODULES.map(m=>{
    const icon=m.icon && m.icon.startsWith('data:') ? `<img class="nav-icon-img" src="${m.icon}" alt="">` : (m.icon?`<span>${m.icon}</span>`:'');
    return `<div class="navitem ${state.view===m.key?'active':''}" data-key="${m.key}" onclick="switchView('${m.key}')">${icon}<span>${m.name}</span></div>`;
  }).join('');
  $('nav').innerHTML=html;
  $('drawerNav').innerHTML=html;
}'''
html = html.replace(old_renderNav, new_renderNav)

# 4. 更新 CSS：图标圆形 + dark 更大 + pink 渐变面板
extra_css = '''
/* 图标统一圆形 */
.nav-icon-img,.ring-icon img,.page-icon{border-radius:50% !important;}
/* dark 主题图标更大 */
body[data-theme="dark"] .nav-icon-img{width:32px;height:32px;margin-right:10px;}
body[data-theme="dark"] .ring-icon img{width:44px;height:44px;}
body[data-theme="dark"] .page-icon{width:34px;height:34px;}
/* pink 主题粉紫渐变面板 */
body[data-theme="pink"] .sidebar{background:linear-gradient(180deg,#fff0f5 0%,#f5e6ff 100%);}
body[data-theme="pink"] .topbar{background:linear-gradient(90deg,#fff5f7 0%,#f8eeff 100%);}
body[data-theme="pink"] .card{background:linear-gradient(180deg,#fff5f7 0%,#fff0fb 100%);}
body[data-theme="pink"] .quote-card{background:linear-gradient(180deg,#fff5f7 0%,#fff0fb 100%);}
body[data-theme="pink"] .navitem.active{background:rgba(255,133,162,0.12);}
'''

# 如果已经存在这些 CSS，先移除旧版本（用简单标记）
html = re.sub(r'/\* 图标统一圆形 \*/[\s\S]*?body\[data-theme="pink"\] \.navitem\.active\{[^}]*\}\n', '', html)
html = html.replace('</style>', extra_css + '\n</style>')

with open(os.path.join(root, 'assets/qiqiu-workbench-source.html'), 'w', encoding='utf-8') as f:
    f.write(html)

print('patched qiqiu-workbench-source.html')
