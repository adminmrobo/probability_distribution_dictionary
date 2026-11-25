"""장마다 첫머리 인포그래픽(16비트 RPG 픽셀 화풍)을 만든다. 같은 그림을 장 썸네일로도 쓴다.
python3 gen_info.py → ../assets/info_<장>.png (960×540) , ../thumbs/ch_<장>.webp
글꼴: 갈무리(Galmuri, SIL OFL 1.1) build/fonts/"""
import re, io, json, base64, math, pathlib
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent; ROOT = HERE.parent
SP = (HERE/'sprites.js').read_text()
ALIAS = json.loads(re.search(r'SPRITE_ALIAS\s*=\s*(\{[^}]*\})', SP).group(1))
def sprite(k):
    k = ALIAS.get(k, k)
    m = re.search('"%s":"data:image/webp;base64,([^"]+)"' % k, SP)
    return Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGBA')
F = lambda n, s: ImageFont.truetype(str(HERE/'fonts'/n), s)
F9, F11, F11B, F14 = F('Galmuri9.ttf', 10), F('Galmuri11.ttf', 12), F('Galmuri11-Bold.ttf', 12), F('Galmuri14.ttf', 15)
W, H, S = 480, 270, 2
INK = (36, 30, 48); MUT = (96, 100, 122); RULE = (210, 214, 226); PANEL = (246, 247, 251); WHITE = (255, 255, 255)
def rgb(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def light(c, k=.82): return tuple(int(v + (255-v)*k) for v in c)
def dark(c, k=.55): return tuple(int(v*k) for v in c)

def pbox(d, x0, y0, x1, y1, fill, out=INK, shadow=True):
    if shadow: d.rectangle([x0+2, y0+2, x1+2, y1+2], fill=RULE)
    d.rectangle([x0+1, y0, x1-1, y1], fill=fill); d.rectangle([x0, y0+1, x1, y1-1], fill=fill)
    d.line([(x0+1, y0), (x1-1, y0)], fill=out); d.line([(x0+1, y1), (x1-1, y1)], fill=out)
    d.line([(x0, y0+1), (x0, y1-1)], fill=out); d.line([(x1, y0+1), (x1, y1-1)], fill=out)

from fontTools.ttLib import TTFont
CMAP = {}
def has(font, ch):
    p = font.path
    if p not in CMAP: CMAP[p] = TTFont(p).getBestCmap()
    return ord(ch) in CMAP[p]
FALL = {}
def text(d, xy, s, font=F11, fill=INK, anchor='la'):
    """굵은 글꼴에 없는 글자(그리스 문자 등)는 같은 크기의 보통 글꼴로 바꿔 그린다."""
    fb = FALL.setdefault(font.path, ImageFont.truetype(str(HERE/'fonts'/'Galmuri11.ttf'), font.size) if not font.path.endswith('Galmuri11.ttf') else font)
    segs = []
    for ch in s:
        f = font if has(font, ch) else fb
        if segs and segs[-1][1] is f: segs[-1][0] += ch
        else: segs.append([ch, f])
    w = sum(d.textlength(t, font=f) for t, f in segs)
    x, y = xy; h, v = anchor[0], anchor[1]
    if h == 'm': x -= w/2
    elif h == 'r': x -= w
    for t, f in segs:
        d.text((round(x), y), t, font=f, fill=fill, anchor='l'+v); x += d.textlength(t, font=f)

def curve(d, f, x0, x1, X, Y, col, w=2, fill_to=None, fill_col=None, dash=False):
    pts = []
    n = int(X(x1) - X(x0))
    for i in range(n+1):
        x = x0 + (x1-x0)*i/n; pts.append((round(X(x)), round(Y(f(x)))))
    if fill_to:
        a, b = fill_to
        poly = [(round(X(a)), round(Y(0)))] + [p for p in pts if X(a) <= p[0] <= X(b)] + [(round(X(b)), round(Y(0)))]
        if len(poly) > 2: d.polygon(poly, fill=fill_col)
    if dash:
        for i in range(0, len(pts)-1, 6): d.line(pts[i:i+4], fill=col, width=w)
    else:
        d.line(pts, fill=col, width=w)

phi = lambda z: math.exp(-z*z/2)/math.sqrt(2*math.pi)
def tpdf(x, v): return math.exp(math.lgamma((v+1)/2)-math.lgamma(v/2))/math.sqrt(v*math.pi)*(1+x*x/v)**(-(v+1)/2)
def c2(x, k): return 0 if x <= 0 else math.exp((k/2-1)*math.log(x)-x/2-(k/2)*math.log(2)-math.lgamma(k/2))
def fpdf(x, a, b):
    if x <= 0: return 0
    return math.exp(0.5*(a*math.log(a*x)+b*math.log(b)-(a+b)*math.log(a*x+b))-math.log(x)-(math.lgamma(a/2)+math.lgamma(b/2)-math.lgamma((a+b)/2)))

def axes(d, x0, y0, x1, y1):
    d.line([(x0, y1), (x1, y1)], fill=INK)

# ---- 장별 그림 ----
def ill_z(d, c, box):
    x0, y0, x1, y1 = box
    px0, px1, py0, py1 = x0+6, x0+148, y0+22, y1-16
    X = lambda x: px0+(x+3.5)/7*(px1-px0); Y = lambda y: py1-y/0.42*(py1-py0)
    axes(d, px0, py0, px1, py1)
    curve(d, phi, -3.5, 3.5, X, Y, c, fill_to=(-3.5, 1.96), fill_col=light(c, .6))
    d.line([(X(1.96), py0+6), (X(1.96), py1)], fill=(207, 58, 40), width=2)
    text(d, (X(1.96), py1+3), '1.96', F9, (207, 58, 40), 'ma')
    text(d, (X(0), py1+3), '0', F9, MUT, 'ma')
    text(d, (X(-0.5), Y(0.13)), '0.975', F11B, dark(c, .6), 'mm')
    text(d, (px0, y0+6), '표 안의 숫자 = 왼쪽 넓이', F11B, dark(c, .7))
    # 작은 표
    tx, ty = x0+152, y0+30; cw, rh = 30, 16
    cols, rows = ['.05', '.06', '.07'], ['1.8', '1.9', '2.0']
    vals = [['.9678', '.9686', '.9693'], ['.9744', '.9750', '.9756'], ['.9798', '.9803', '.9808']]
    cw = 31
    d.rectangle([tx, ty, tx+28+cw*3, ty+rh*4], fill=WHITE, outline=INK)
    d.rectangle([tx+1, ty+1, tx+28+cw*3-1, ty+rh-1], fill=(232, 236, 244))
    d.rectangle([tx+1, ty+1, tx+27, ty+rh*4-1], fill=(232, 236, 244))
    for j, h in enumerate(cols): text(d, (tx+28+cw*j+cw//2, ty+3), h, F9, MUT, 'ma')
    for i, r in enumerate(rows):
        text(d, (tx+14, ty+rh*(i+1)+3), r, F9, MUT, 'ma')
        for j in range(3):
            hit = (i == 1 and j == 1)
            if hit: d.rectangle([tx+28+cw*j+1, ty+rh*(i+1)+1, tx+28+cw*(j+1)-1, ty+rh*(i+2)-1], fill=c)
            elif i == 1 or j == 1: d.rectangle([tx+28+cw*j+1, ty+rh*(i+1)+1, tx+28+cw*(j+1)-1, ty+rh*(i+2)-1], fill=light(c, .75))
            text(d, (tx+28+cw*j+cw//2, ty+rh*(i+1)+3), vals[i][j], F9, WHITE if hit else INK, 'ma')
    text(d, (tx+(28+cw*3)//2, ty+rh*4+6), '1.9 줄 × .06 열', F9, dark(c, .7), 'ma')

def ill_t(d, c, box):
    x0, y0, x1, y1 = box
    px0, px1, py0, py1 = x0+6, x0+150, y0+22, y1-16
    X = lambda x: px0+(x+4.5)/9*(px1-px0); Y = lambda y: py1-y/0.42*(py1-py0)
    axes(d, px0, py0, px1, py1)
    curve(d, phi, -4.5, 4.5, X, Y, (23, 137, 79), w=2, dash=True)
    curve(d, lambda x: tpdf(x, 1), -4.5, 4.5, X, Y, (207, 58, 40), w=2)
    curve(d, lambda x: tpdf(x, 5), -4.5, 4.5, X, Y, c, w=2)
    text(d, (px0, y0+6), '꼬리가 두꺼운 t, 점선은 Z', F11B, dark(c, .7))
    text(d, (X(2.3), Y(0.22)), 'df 5', F9, c, 'la'); text(d, (X(-4.4), Y(0.16)), 'df 1', F9, (207, 58, 40), 'la')
    text(d, (X(-4.4), Y(0.36)), 'Z', F9, (23, 137, 79), 'la')
    lx, ly = x0+158, y0+28
    pbox(d, lx, ly, x1-8, ly+92, WHITE, shadow=False)
    text(d, (lx+6, ly+5), '양측 95% 경계', F9, MUT)
    rows = [('df 1', '12.706'), ('df 5', '2.571'), ('df 30', '2.042'), ('∞ = Z', '1.960')]
    for i, (a, b) in enumerate(rows):
        y = ly+20+i*17; last = i == 3
        if last: d.rectangle([lx+3, y-2, x1-11, y+12], fill=light((23, 137, 79), .7))
        text(d, (lx+8, y), a, F9, INK); text(d, (x1-14, y), b, F11B if last else F11, dark((23, 137, 79), .7) if last else c, 'ra')
    for i in range(3):
        y = ly+31+i*17; text(d, (lx+44, y-1), '↓', F9, MUT, 'ma')

def ill_c(d, c, box):
    x0, y0, x1, y1 = box
    px0, px1, py0, py1 = x0+8, x1-10, y0+24, y1-16
    X = lambda x: px0+x/22*(px1-px0); Y = lambda y: py1-min(y, .5)/0.5*(py1-py0)
    axes(d, px0, py0, px1, py1)
    cols = [(207, 58, 40), c, (23, 137, 79), (42, 100, 200)]
    for k, col in zip([1, 2, 4, 8], cols):
        curve(d, lambda x: c2(max(x, 0.05), k), 0.05, 22, X, Y, col, w=2,
              fill_to=(15.507, 22) if k == 8 else None, fill_col=light((42, 100, 200), .5))
    for (k, x, y, col) in [(1, .7, .46, cols[0]), (2, 1.8, .38, cols[1]), (4, 3.6, .2, cols[2]), (8, 7.6, .14, cols[3])]:
        text(d, (X(x), Y(y)), 'df %d' % k, F9, col, 'la')
    d.line([(X(15.507), py0+30), (X(15.507), py1)], fill=(42, 100, 200), width=1)
    text(d, (X(15.507), py0+18), '15.507 → 꼬리 5%', F9, (42, 100, 200), 'ma')
    text(d, (px0, y0+6), '0에서 시작, 오른쪽으로 늘어진 모양', F11B, dark(c, .7))
    text(d, (X(0), py1+3), '0', F9, MUT, 'ma'); text(d, (X(10), py1+3), '10', F9, MUT, 'ma'); text(d, (X(20), py1+3), '20', F9, MUT, 'ma')

def ill_f(d, c, box):
    x0, y0, x1, y1 = box
    px0, px1, py0, py1 = x0+6, x0+140, y0+24, y1-16
    X = lambda x: px0+x/5*(px1-px0); Y = lambda y: py1-min(y, .9)/0.9*(py1-py0)
    axes(d, px0, py0, px1, py1)
    curve(d, lambda x: fpdf(max(x, .02), 5, 10), .02, 5, X, Y, c, w=2, fill_to=(3.33, 5), fill_col=light((207, 58, 40), .45))
    d.line([(X(3.33), py0+20), (X(3.33), py1)], fill=(207, 58, 40))
    text(d, (X(3.33), py0+8), '3.33', F9, (207, 58, 40), 'ma')
    text(d, (X(1), py1+3), '1', F9, MUT, 'ma')
    text(d, (px0, y0+6), 'F(5, 10), 오른쪽 꼬리 5%', F11B, dark(c, .7))
    tx, ty = x0+148, y0+30; cw, rh = 30, 16
    d.rectangle([tx, ty, tx+36+cw*3, ty+rh*4], fill=WHITE, outline=INK)
    d.rectangle([tx+1, ty+1, tx+36+cw*3-1, ty+rh-1], fill=(232, 236, 244)); d.rectangle([tx+1, ty+1, tx+35, ty+rh*4-1], fill=(232, 236, 244))
    text(d, (tx+18, ty+3), '분모', F9, MUT, 'ma')
    for j, h in enumerate(['4', '5', '6']): text(d, (tx+36+cw*j+cw//2, ty+3), h, F9, MUT, 'ma')
    vals = [['3.63', '3.48', '3.37'], ['3.48', '3.33', '3.22'], ['3.36', '3.20', '3.09']]
    for i, r in enumerate(['9', '10', '11']):
        text(d, (tx+18, ty+rh*(i+1)+3), r, F9, MUT, 'ma')
        for j in range(3):
            hit = i == 1 and j == 1
            if hit: d.rectangle([tx+36+cw*j+1, ty+rh*(i+1)+1, tx+36+cw*(j+1)-1, ty+rh*(i+2)-1], fill=c)
            text(d, (tx+36+cw*j+cw//2, ty+rh*(i+1)+3), vals[i][j], F9, WHITE if hit else INK, 'ma')
    text(d, (tx+(36+cw*3)//2, ty-12), '↓ 분자 (열)', F9, dark(c, .7), 'ma')
    text(d, (tx+(36+cw*3)//2, ty+rh*4+6), 'α = 0.05 표', F9, dark(c, .7), 'ma')

def ill_df(d, c, box):
    x0, y0, x1, y1 = box
    text(d, (x0+8, y0+6), '피자값 3만 원을 세 명이 나누면', F11B, dark(c, .7))
    items = [('1번', '8천', '자유', (42, 100, 200)), ('2번', '1만5천', '자유', (42, 100, 200)), ('3번', '7천', '고정', (207, 58, 40))]
    for i, (who, val, tag, col) in enumerate(items):
        bx = x0+12+i*90; by = y0+22
        pbox(d, bx, by, bx+78, by+60, light(col, .85))
        # 피자 조각 (픽셀)
        cx = bx+39
        d.polygon([(cx-14, by+10), (cx+14, by+10), (cx, by+34)], fill=(240, 190, 90), outline=INK)
        d.line([(cx-14, by+10), (cx+14, by+10)], fill=(190, 120, 60), width=3)
        for (ox, oy) in ((-5, 16), (4, 18), (0, 25)): d.rectangle([cx+ox, by+oy, cx+ox+2, by+oy+2], fill=(200, 60, 50))
        text(d, (cx, by+35), val, F11B, INK, 'ma')
        text(d, (cx, by+49), who, F9, MUT, 'ma')
        pbox(d, bx+18, by+65, bx+60, by+79, col, shadow=False); text(d, (bx+39, by+67), tag, F9, WHITE, 'ma')
        if tag == '고정':
            lx, ly = bx+64, by+4
            d.rectangle([lx, ly+5, lx+11, ly+14], fill=(220, 170, 40), outline=INK); d.arc([lx+2, ly, lx+9, ly+10], 180, 360, fill=INK, width=2)
    text(d, ((x0+x1)//2, y1-4), '마음대로 정한 사람 = 3 − 1 = 2명 → 자유도 2', F11B, (207, 58, 40), 'ms')

def ill_trap(d, c, box):
    x0, y0, x1, y1 = box
    text(d, (x0+8, y0+6), '판정표: 실제 Y × 판정 Ŷ', F11B, dark(c, .7))
    gx, gy, cw, ch = x0+30, y0+40, 62, 34
    text(d, (gx+cw//2, gy-12), 'Ŷ=0', F9, MUT, 'ma'); text(d, (gx+cw+cw//2, gy-12), 'Ŷ=1', F9, MUT, 'ma')
    text(d, (gx-6, gy+ch//2-4), 'Y=0', F9, MUT, 'ra'); text(d, (gx-6, gy+ch+ch//2-4), 'Y=1', F9, MUT, 'ra')
    cells = [('TN', '맞음', (42, 100, 200)), ('FP', '1종 α', (207, 58, 40)), ('FN', '2종 β', (207, 58, 40)), ('TP', '검정력', (42, 100, 200))]
    for k, (a, b, col) in enumerate(cells):
        cx, cy = gx+(k % 2)*cw, gy+(k//2)*ch
        d.rectangle([cx+1, cy+1, cx+cw-2, cy+ch-2], fill=light(col, .82), outline=col)
        text(d, (cx+cw//2, cy+5), a, F11B, dark(col, .8), 'ma'); text(d, (cx+cw//2, cy+19), b, F9, dark(col, .8), 'ma')
    # 100번 실험 점
    ox, oy = x0+170, y0+36
    text(d, (ox, oy-14), '효과 없는데 100번', F9, MUT)
    red = {7, 23, 48, 61, 89}
    for i in range(100):
        x, y = ox+(i % 10)*9, oy+(i//10)*8
        d.rectangle([x, y, x+5, y+5], fill=(207, 58, 40) if i in red else (200, 206, 222))
    text(d, (ox+43, oy+82), '5번은 뚫린다 (α 5%)', F9, (207, 58, 40), 'ma')

CH = {
 'z': dict(no='1장', title='Z분포 — 표준정규분포표', col='#17894f', ill=ill_z, who='asst_report',
           say='1.9 줄과 .06 열이 만나면\n0.9750이에요!',
           pts=[('Z = (X − μ) / σ', '어떤 정규분포든\n한 장의 표로 읽는다'), ('숫자 = 왼쪽 넓이', '줄은 앞 두 자리(1.9)\n열은 끝자리(.06)'), ('95% 구간 → 0.975', '양쪽 꼬리 2.5%씩\n왼쪽 넓이 0.975 → ±1.96')]),
 't': dict(no='2장', title='t분포 — 자유도가 커지면 Z가 된다', col='#a23fa3', ill=ill_t, who='robo_happy',
           say='사람이 늘면\nt값이 1.96으로!',
           pts=[('σ를 모를 때', '표본의 s로 재니\n꼬리가 두껍다'), ('줄 = 자유도 n − 1', '양측 0.05 = 단측 0.025\n두 열 머리를 확인'), ('df ↑ → t값 → z값', '12.706 → 2.228\n→ 2.042 → 1.960')]),
 'c': dict(no='3장', title='카이제곱분포 — 어긋남을 모은 점수', col='#a86a00', ill=ill_c, who='fly_magnify',
           say='어긋난 만큼 제곱해서\n다 더해 봐.',
           pts=[('Z²를 k개 더한 분포', '평균 = 자유도 k\n0보다 작아질 수 없다'), ('열 = 오른쪽 꼬리', '왼쪽 경계는\n0.95 열에서 따로'), ('적합도·독립성', '교차표 자유도\n(행 − 1) × (열 − 1)')]),
 'f': dict(no='4장', title='F분포 — 두 흩어짐의 비율', col='#2a64c8', ill=ill_f, who='doc_think',
           say='분자는 위쪽 열,\n분모는 왼쪽 줄입니다.',
           pts=[('두 분산의 비율', '1 근처면\n집단 차이가 없다'), ('α마다 표가 한 장', '분자·분모를 바꾸면\n값이 달라진다'), ('분산분석에 쓴다', '집단 k개, 전체 N명\n→ (k − 1, N − k)')]),
 'df': dict(no='부록', title='자유도란? 왜 표본 수 − 1인가', col='#3f5f8f', ill=ill_df, who='moa_report',
           say='마지막 사람은\n고를 수가 없어요.',
           pts=[('마음대로 고르는 개수', '그 개수가\n자유도다'), ('평균이 하나를 묶는다', '평균과의 차이를\n다 더하면 늘 0'), ('그래서 n − 1', '분산도, t표의 줄도\nn − 1')]),
 'trap': dict(no='해석의 함정', title='1종 오류와 2종 오류', col='#cf3a28', ill=ill_trap, who='fly_point',
           say='표의 기준을 넘어도\n틀릴 수 있어!',
           pts=[('1종: 없는데 있다', 'α = 5%면 100번에 5번\n기준은 뚫린다'), ('검정 20번 → 64%', '여러 번 보면\n헛경보가 쌓인다'), ('2종: 있는데 놓침', '너무 엄격하면(β↑)\n진짜도 놓친다')]),
}

def make(key, spec):
    c = rgb(spec['col'])
    im = Image.new('RGBA', (W, H), WHITE + (255,)); d = ImageDraw.Draw(im); d.fontmode = '1'
    for y in range(0, H, 10): d.line([(0, y), (W, y)], fill=(248, 249, 252))
    for x in range(0, W, 10): d.line([(x, 0), (x, H)], fill=(248, 249, 252))
    # 제목 띠
    pbox(d, 6, 6, W-8, 38, c)
    pbox(d, 12, 11, 12+d.textlength(spec['no'], font=F11B)+14, 33, WHITE, shadow=False)
    text(d, (19, 16), spec['no'], F11B, dark(c, .7))
    text(d, (12+d.textlength(spec['no'], font=F11B)+24, 13), spec['title'], F14, WHITE)
    text(d, (W-14, 17), '분포표 읽기 연구실', F9, light(c, .7), 'ra')
    # 그림 영역
    box = (6, 46, 286, 176); pbox(d, *box, PANEL)
    spec['ill'](d, c, box)
    # 핵심 3가지
    for i, (a, b) in enumerate(spec['pts']):
        y = 46+i*74; pbox(d, 294, y, W-8, y+66, WHITE)
        d.rectangle([300, y+8, 316, y+24], fill=c); text(d, (308, y+11), str(i+1), F11B, WHITE, 'ma')
        text(d, (322, y+10), a, F11B, INK)
        d.line([(300, y+30), (W-14, y+30)], fill=light(c, .7))
        for j, line in enumerate(b.split('\n')): text(d, (300, y+35+j*14), line, F9, MUT)
    # 캐릭터와 말풍선
    sp = sprite(spec['who']); im.alpha_composite(sp, (8, H-96)); d = ImageDraw.Draw(im); d.fontmode = '1'
    bx0, by0, bx1, by1 = 108, 192, 286, 236
    pbox(d, bx0, by0, bx1, by1, (255, 248, 222), out=(150, 110, 40))
    d.polygon([(bx0, by0+16), (bx0-9, by0+24), (bx0, by0+26)], fill=(255, 248, 222)); d.line([(bx0, by0+16), (bx0-9, by0+24), (bx0, by0+26)], fill=(150, 110, 40))
    for j, line in enumerate(spec['say'].split('\n')): text(d, ((bx0+bx1)//2, by0+(12 if '\n' in spec['say'] else 20)+j*16), line, F11B, INK, 'mm')
    text(d, (bx1, H-10), '글 · 안상선 ((주)M-Robo 대표)', F9, MUT, 'ra')
    out = im.resize((W*S, H*S), Image.NEAREST).convert('RGB')
    out.save(ROOT/'assets'/('info_%s.png' % key), optimize=True)
    out.save(ROOT/'thumbs'/('ch_%s.webp' % ('trap' if key == 'trap' else key)), quality=90)
for k, v in CH.items(): make(k, v)
print('ok', list(CH))
