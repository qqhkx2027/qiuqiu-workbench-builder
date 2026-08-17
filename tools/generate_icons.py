import os, base64, json
from PIL import Image, ImageDraw

# ── 可编辑配置 ──────────────────────────────────────────────
# SRC_DIR：你的三丽鸥原图文件夹（改成自己的路径；图片需是 3×3 九宫格或单张大图）。
SRC_DIR = '/Users/a1-6/Desktop/配图/三丽鸥'
# 输出目录自动指向本 skill 的 assets/icons（移动 skill 也不受影响）。
HERE = os.path.dirname(os.path.abspath(__file__))
out_dir = os.path.join(HERE, '..', 'assets', 'icons')
os.makedirs(out_dir, exist_ok=True)

def save_base64(img):
    path = os.path.join(out_dir, 'tmp.png')
    img.save(path, 'PNG')
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')

def remove_bg(img, white_thresh=250, black_thresh=None):
    """把接近白色背景改为透明；可选把黑色水印文字也去掉。"""
    img = img.convert('RGBA')
    data = list(img.getdata())
    new_data = []
    for r, g, b, a in data:
        is_white = r > white_thresh and g > white_thresh and b > white_thresh
        is_black = black_thresh is not None and r < black_thresh and g < black_thresh and b < black_thresh
        if is_white or is_black:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    return img

def make_circle(img, size=120, white_thresh=250, black_thresh=None, pad=1.15):
    """去背景、按内容 bbox 居中、做成圆形透明 PNG。"""
    img = remove_bg(img, white_thresh, black_thresh)
    bbox = img.getbbox()
    if bbox:
        x1, y1, x2, y2 = bbox
        bw = x2 - x1; bh = y2 - y1
        s = int(max(bw, bh) * pad)
        cx = (x1 + x2) // 2; cy = (y1 + y2) // 2
        x1 = cx - s // 2; y1 = cy - s // 2; x2 = x1 + s; y2 = y1 + s
        w, h = img.size
        if x1 < 0: x1 = 0; x2 = min(s, w)
        if y1 < 0: y1 = 0; y2 = min(s, h)
        if x2 > w: x2 = w; x1 = max(0, w - s)
        if y2 > h: y2 = h; y1 = max(0, h - s)
        img = img.crop((x1, y1, x2, y2))
    else:
        w, h = img.size
        s = int(min(w, h) * 0.92)
        left = (w - s) // 2; top = (h - s) // 2
        img = img.crop((left, top, left + s, top + s))
    img = img.resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    out = Image.new('RGBA', (size, size), (255, 255, 255, 0))
    out.paste(img, (0, 0), mask)
    return out

def find_splits(proj, n):
    """按投影找 n-1 条最佳分割线（投影局部最小值）。"""
    total = len(proj)
    min_dist = total // (n * 2)
    minima = []
    for i in range(1, len(proj) - 1):
        if proj[i] < proj[i-1] and proj[i] <= proj[i+1]:
            minima.append((proj[i], i))
    minima.sort()
    chosen = []
    for v, i in minima:
        if all(abs(i - c) > min_dist for c in chosen):
            chosen.append(i)
        if len(chosen) >= n - 1:
            break
    chosen.sort()
    return chosen

def split_grid_smart(path, rows, cols, white_thresh=250, inset=0.03):
    """按行列投影自动找分割线，再内缩裁掉相邻图案边缘。"""
    img = Image.open(path).convert('RGBA')
    w, h = img.size
    hproj = []
    for y in range(h):
        cnt = 0
        for x in range(w):
            r, g, b, a = img.getpixel((x, y))
            if r < white_thresh or g < white_thresh or b < white_thresh:
                cnt += 1
        hproj.append(cnt)
    vproj = []
    for x in range(w):
        cnt = 0
        for y in range(h):
            r, g, b, a = img.getpixel((x, y))
            if r < white_thresh or g < white_thresh or b < white_thresh:
                cnt += 1
        vproj.append(cnt)
    hsplits = find_splits(hproj, rows)
    vsplits = find_splits(vproj, cols)
    hb = [0] + hsplits + [h]
    vb = [0] + vsplits + [w]
    tiles = []
    for r in range(rows):
        for c in range(cols):
            cw = vb[c+1] - vb[c]; ch = hb[r+1] - hb[r]
            x1 = vb[c] + int(cw * inset)
            y1 = hb[r] + int(ch * inset)
            x2 = vb[c+1] - int(cw * inset)
            y2 = hb[r+1] - int(ch * inset)
            tile = img.crop((x1, y1, x2, y2))
            tiles.append(((r, c), tile))
    return tiles

def split_grid_uniform(path, rows, cols, inset=0.04):
    """均匀网格切分，适合排列规整的图。"""
    img = Image.open(path).convert('RGBA')
    w, h = img.size
    tile_w = w // cols; tile_h = h // rows
    tiles = []
    for r in range(rows):
        for c in range(cols):
            left = c * tile_w; upper = r * tile_h
            iw = int(tile_w * inset); ih = int(tile_h * inset)
            tile = img.crop((left + iw, upper + ih, left + tile_w - iw, upper + tile_h - ih))
            tiles.append(((r, c), tile))
    return tiles

# -------------------------
# 库洛米：3 张九宫格，跳过相机 cell，用投影分割
# -------------------------
kuromi_files = ['IMG_0812.JPG', 'IMG_0813.JPG', 'IMG_0814.JPG']
kuromi_skip = {
    'IMG_0812.JPG': {(1, 1)},
    'IMG_0813.JPG': {(1, 1)},
    'IMG_0814.JPG': {(1, 1), (0, 2)},
}
kuromi_tiles = []
for f in kuromi_files:
    for pos, tile in split_grid_smart(os.path.join(SRC_DIR, f), 3, 3, inset=0.03):
        if pos not in kuromi_skip[f]:
            kuromi_tiles.append(tile)

# -------------------------
# 美乐蒂：12 张单图取前 10 个
# -------------------------
pink_files = [
    'IMG_0787.JPG','IMG_0788.JPG','IMG_0789.JPG','IMG_0790.JPG','IMG_0791.JPG','IMG_0792.JPG',
    'IMG_0794.PNG','IMG_0795.PNG','IMG_0796.PNG','IMG_0797.PNG','IMG_0798.PNG','IMG_0799.PNG'
]
pink_imgs = [make_circle(Image.open(os.path.join(SRC_DIR, f)), black_thresh=35) for f in pink_files[:10]]

# -------------------------
# 玉桂狗：1 张 4x3 网格取前 10 个，均匀切分
# -------------------------
cinna_tiles = [tile for _, tile in split_grid_uniform(os.path.join(SRC_DIR, 'IMG_0805.JPG'), 4, 3, inset=0.05)][:10]

module_order = ['home','todo','create','media','ledger','health','diary','finance','ai']

# 保存视觉检查图
for i, tile in enumerate(kuromi_tiles[:10], 1):
    make_circle(tile, 120).save(os.path.join(out_dir, f'kuromi_{i:02d}.png'))
for i, img in enumerate(pink_imgs, 1):
    img.save(os.path.join(out_dir, f'melody_{i:02d}.png'))
for i, tile in enumerate(cinna_tiles, 1):
    make_circle(tile, 120).save(os.path.join(out_dir, f'cinna_{i:02d}.png'))

# 生成图标映射
def build_icons(items):
    icons = {}
    for i, key in enumerate(module_order, 1):
        icons[key] = save_base64(make_circle(items[i-1], 120))
    icons['brand'] = save_base64(make_circle(items[9], 120))
    return icons

dark_icons = build_icons(kuromi_tiles)
pink_icons = build_icons(pink_imgs)
cinna_icons = build_icons(cinna_tiles)

minimal_icons = {
    'home':'🏠','todo':'📝','create':'🎨','media':'📚','ledger':'💳','health':'🥗','diary':'🌙','finance':'💰','ai':'🤖'
}

icons_js = {
    'minimal': minimal_icons,
    'dark': dark_icons,
    'pink': pink_icons,
    'cinnamoroll': cinna_icons
}
icons_js['minimal']['brand'] = '🐧'

out_js = os.path.join(out_dir, 'icons.js')
with open(out_js, 'w', encoding='utf-8') as f:
    f.write('const ICON_IMGS=' + json.dumps(icons_js, ensure_ascii=False, separators=(',',':')) + ';\n')

# 单独保存 brand 图
make_circle(kuromi_tiles[9], 120).save(os.path.join(out_dir, 'kuromi_brand.png'))
pink_imgs[9].save(os.path.join(out_dir, 'melody_brand.png'))
make_circle(cinna_tiles[9], 120).save(os.path.join(out_dir, 'cinna_brand.png'))

print('saved', out_js)
print('kuromi tiles:', len(kuromi_tiles), 'pink imgs:', len(pink_imgs), 'cinna tiles:', len(cinna_tiles))
