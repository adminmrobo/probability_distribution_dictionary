"""판정표(Y·Ŷ) 네 장면을 연구실 픽셀 화풍으로 만든다. 박사·주판봇은 캐릭터 팩 그림, 임신한 환자는 같은 화풍으로 그린다.
python3 gen_cm.py → ../assets/cm_{tn,fp,fn,tp}.png (200×124 픽셀을 3배 확대)"""
import re, io, base64, json, pathlib
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).parent
SP = (HERE/'sprites.js').read_text()
def sprite(k):
    m = re.search('"%s":"data:image/webp;base64,([^"]+)"' % k, SP)
    return Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGBA')
W, H, S = 200, 124, 3
OUT = (42, 34, 48, 255)

def outline(layer, col=OUT):
    a = layer.split()[3]; px = a.load(); w, h = layer.size
    o = Image.new('RGBA', layer.size, (0,0,0,0)); op = o.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == 0:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    X, Y = x+dx, y+dy
                    if 0 <= X < w and 0 <= Y < h and px[X, Y] > 0:
                        op[x, y] = col; break
    o.alpha_composite(layer); return o

def part(size, fn):
    L = Image.new('RGBA', size, (0,0,0,0)); fn(ImageDraw.Draw(L)); return outline(L)

def background():
    im = Image.new('RGBA', (W, H), (238, 242, 248, 255)); d = ImageDraw.Draw(im)
    for y in range(0, H, 12): d.line([(0, y), (W, y)], fill=(229, 234, 243, 255))
    for x in range(0, W, 24): d.line([(x, 0), (x, H)], fill=(232, 237, 245, 255))
    # 창문
    d.rectangle([150, 8, 192, 40], fill=(206, 222, 244, 255), outline=(150, 166, 196, 255))
    d.line([(171, 8), (171, 40)], fill=(150, 166, 196, 255)); d.line([(150, 24), (192, 24)], fill=(150, 166, 196, 255))
    d.line([(154, 12), (160, 12)], fill=(236, 244, 255, 255)); d.line([(154, 13), (157, 13)], fill=(236, 244, 255, 255))
    # 선반과 플라스크
    d.rectangle([4, 22, 52, 24], fill=(176, 150, 120, 255), outline=(120, 98, 76, 255))
    for x, c in ((8, (120, 200, 160)), (22, (230, 150, 190)), (36, (150, 180, 240))):
        d.polygon([(x, 21), (x+8, 21), (x+6, 15), (x+6, 10), (x+2, 10), (x+2, 15)], fill=(250, 252, 255, 255), outline=(110, 120, 140, 255))
        d.rectangle([x+1, 18, x+7, 20], fill=c+(255,))
    # 바닥 띠
    d.rectangle([0, H-10, W, H], fill=(214, 220, 232, 255))
    return im

def woman(mood):
    w, h = 96, 96; base = Image.new('RGBA', (w, h), (0,0,0,0))
    HAIR, HAIRS, HAIRH = (112, 70, 52, 255), (80, 48, 36, 255), (158, 106, 78, 255)
    SKIN, SKINS = (247, 206, 170, 255), (226, 172, 134, 255)
    DRESS, DRESSS, DRESSH = (196, 176, 236, 255), (160, 138, 208, 255), (228, 218, 250, 255)
    def backhair(d):
        d.ellipse([18, 2, 78, 64], fill=HAIR); d.rounded_rectangle([20, 30, 76, 86], 8, fill=HAIR)
        d.rectangle([68, 30, 76, 84], fill=HAIRS)
    base.alpha_composite(part((w, h), backhair))
    def body(d):
        d.rounded_rectangle([26, 60, 70, 104], 12, fill=DRESS)
        d.rectangle([62, 66, 70, 104], fill=DRESSS)
        d.line([(31, 68), (31, 96)], fill=DRESSH)
    base.alpha_composite(part((w, h), body))
    base.alpha_composite(part((w, h), lambda d: d.polygon([(40, 60), (56, 60), (48, 70)], fill=(255, 255, 255, 255))))
    def belly(d):
        d.ellipse([40, 66, 88, 112], fill=DRESS)
        d.chord([40, 66, 88, 112], 290, 80, fill=DRESSS)
        d.arc([46, 72, 74, 98], 200, 255, fill=DRESSH); d.point((50, 76), fill=DRESSH)
    base.alpha_composite(part((w, h), belly))
    def hands(d):
        d.rounded_rectangle([50, 74, 61, 81], 3, fill=SKIN); d.rounded_rectangle([64, 85, 75, 92], 3, fill=SKIN)
    base.alpha_composite(part((w, h), hands))
    d0 = ImageDraw.Draw(base)
    for x in (53, 56, 58): d0.point((x, 80), fill=SKINS)
    for x in (67, 70, 72): d0.point((x, 91), fill=SKINS)
    base.alpha_composite(part((w, h), lambda d: (d.rectangle([43, 50, 53, 62], fill=SKIN), d.rectangle([43, 50, 53, 53], fill=SKINS))))
    def face(d):
        d.ellipse([27, 8, 69, 56], fill=SKIN)
        d.chord([27, 8, 69, 56], 310, 50, fill=SKINS)
    base.alpha_composite(part((w, h), face))
    def bangs(d):
        d.pieslice([25, 4, 71, 48], 180, 360, fill=HAIR)
        d.polygon([(25, 25), (71, 25), (70, 29), (64, 26), (60, 31), (53, 26), (47, 30), (40, 26), (34, 31), (29, 27), (26, 31)], fill=HAIR)
        d.polygon([(25, 26), (31, 26), (30, 56), (25, 52)], fill=HAIR); d.polygon([(65, 26), (71, 26), (71, 52), (66, 56)], fill=HAIRS)
        d.arc([30, 8, 60, 30], 200, 250, fill=HAIRH); d.line([(36, 10), (44, 8)], fill=HAIRH)
    base.alpha_composite(part((w, h), bangs))
    d = ImageDraw.Draw(base)
    EYE, IRIS = (54, 34, 34, 255), (130, 84, 62, 255)
    for ex in (35, 54):
        d.rectangle([ex, 33, ex+6, 41], fill=EYE); d.rectangle([ex+1, 37, ex+5, 40], fill=IRIS)
        d.rectangle([ex+1, 34, ex+2, 35], fill=(255, 255, 255, 255)); d.point((ex+5, 39), fill=(255, 255, 255, 255))
        d.line([(ex-1, 32), (ex+7, 32)], fill=EYE)
    d.rectangle([31, 43, 35, 45], fill=(246, 150, 160, 255)); d.rectangle([61, 43, 65, 45], fill=(246, 150, 160, 255))
    if mood == 'happy':
        d.line([(44, 47), (46, 49), (50, 49), (52, 47)], fill=(160, 60, 60, 255)); d.line([(46, 50), (50, 50)], fill=(230, 120, 130, 255))
    else:
        d.line([(34, 28), (41, 30)], fill=HAIRS); d.line([(55, 30), (62, 28)], fill=HAIRS)
        d.line([(45, 48), (47, 47), (49, 48), (51, 47)], fill=(160, 60, 60, 255))
        d.ellipse([67, 30, 72, 37], fill=(160, 210, 255, 255), outline=(70, 110, 170, 255))
    return base

GLYPH = {
 '?': ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
 '!': ["1", "1", "1", "1", "1", "0", "1"],
 'h': ["0110110", "1111111", "1111111", "0111110", "0011100", "0001000"],
 '.': ["1"],
}
def glyph(d, s, x, y, col, sc=2):
    for ch in s:
        g = GLYPH[ch]
        for r, row in enumerate(g):
            for c, v in enumerate(row):
                if v == '1': d.rectangle([x+c*sc, y+(r if ch != '.' else 6)*sc, x+c*sc+sc-1, y+(r if ch != '.' else 6)*sc+sc-1], fill=col)
        x += (len(g[0])+1)*sc

def bubble(d, x0, y0, x1, y1, tx, ty):
    F, O = (255, 248, 222, 255), (150, 110, 40, 255)
    d.rectangle([x0+2, y0, x1-2, y1], fill=F); d.rectangle([x0, y0+2, x1, y1-2], fill=F); d.rectangle([x0+1, y0+1, x1-1, y1-1], fill=F)
    d.line([(x0+2, y0), (x1-2, y0)], fill=O); d.line([(x0+2, y1), (x1-2, y1)], fill=O)
    d.line([(x0, y0+2), (x0, y1-2)], fill=O); d.line([(x1, y0+2), (x1, y1-2)], fill=O)
    for p in ((x0+1, y0+1), (x1-1, y0+1), (x0+1, y1-1), (x1-1, y1-1)): d.point(p, fill=O)
    # 꼬리 (박사 쪽)
    d.polygon([(tx-4, y1), (tx+3, y1), (tx+6, ty)], fill=F)
    d.line([(tx-4, y1), (tx+6, ty)], fill=O); d.line([(tx+3, y1), (tx+6, ty)], fill=O)
    d.line([(tx-3, y1), (tx+2, y1)], fill=F)

SCENES = {
 'tn': dict(pat='robo_e13', doc='doc_e13', react=None),
 'fp': dict(pat='robo_e14', doc='doc_e08', react=('?!', (200, 120, 0, 255))),
 'fn': dict(pat='woman_sad', doc='doc_e10', react=('?', (42, 100, 200, 255))),
 'tp': dict(pat='woman_happy', doc='doc_e16', react=('h', (210, 66, 127, 255))),
}
BUB = dict(x0=58, y0=3, x1=150, y1=25, tx=138, ty=34)
meta = {}
for key, sc in SCENES.items():
    im = background(); d = ImageDraw.Draw(im)
    if sc['pat'].startswith('woman'):
        p = woman('happy' if sc['pat'].endswith('happy') else 'sad'); im.alpha_composite(p, (4, H-96))
    else:
        im.alpha_composite(sprite(sc['pat']), (4, H-96))
    im.alpha_composite(sprite(sc['doc']), (W-98, H-96))
    bubble(d, **BUB)
    if sc['react']:
        glyph(d, sc['react'][0], 6, 32, sc['react'][1])
    out = im.resize((W*S, H*S), Image.NEAREST).convert('RGB')
    out.save(HERE.parent/'assets'/('cm_%s.png' % key), optimize=True)
meta = dict(w=W, h=H, cx=(BUB['x0']+BUB['x1'])/2, cy=(BUB['y0']+BUB['y1'])/2, bw=BUB['x1']-BUB['x0'])
print(json.dumps(meta))
