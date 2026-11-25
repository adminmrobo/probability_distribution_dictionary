"""tables.src.html 하나에서 분포표 읽기 연구실의 장 페이지들을 만든다.

  python3 build.py

- tables.html          : 목차(허브) — 장 카드, 연구실 식구, 말과 기호, 정리
- table_z.html         : 1장 Z분포
- table_t.html         : 2장 t분포
- table_chi2.html      : 3장 카이제곱분포
- table_f.html         : 4장 F분포
- appendix_df.html     : 부록 자유도
- trap_errors.html     : 해석의 함정 1종·2종 오류 (+ 아웃트로)
스크립트는 모든 장이 같고, 페이지에 있는 요소만 그린다.
"""
import re, pathlib, html
HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
src = (HERE/'tables.src.html').read_text()
sp = (HERE/'sprites.js').read_text()
data = (HERE/'data.json').read_text()

head = src[:src.index('<body>')]
script = src[src.index('<script>\n/*@@SPRITES@@*/'):src.index('</body>')]
script = script.replace('/*@@SPRITES@@*/', sp).replace('/*@@DATA@@*/', data)
footer = src[src.index('<footer>'):src.index('</footer>')+len('</footer>')]

def sec(i):
    m = re.search(r'<section class="sec[^"]*" id="%s"' % i, src)
    a = m.start(); b = src.index('</section>', a)+len('</section>')
    return src[a:b]
hero_hub = src[src.index('<header class="hero">'):src.index('</header>')+len('</header>')]

URL = 'https://adminmrobo.github.io/probability_distribution_dictionary/'
CH = [
 dict(f='table_z.html', sid='s-z', no='1장', short='Z분포', thumb='ch_z',
      desc='표준정규분포표 읽기: 표준화, 왼쪽 넓이, 단측·양측 경계값 1.645·1.96·2.576.',
      three=['<b>무엇을</b>: Z표에서 값 → 왼쪽 넓이를 읽고, 거꾸로 경계값을 찾습니다.',
             '<b>핵심</b>: 표 안의 숫자는 “z보다 왼쪽에 있을 확률”입니다. 오른쪽 꼬리는 1에서 뺍니다.',
             '<b>다음 장과의 관계</b>: σ를 모르면 Z 대신 t표를 씁니다.']),
 dict(f='table_t.html', sid='s-t', no='2장', short='t분포', thumb='ch_t',
      desc='t분포 그리기와 t표 읽기. 자유도가 커지면 표의 t값이 z값 1.96에 다가간다.',
      three=['<b>무엇을</b>: t분포를 그리고, t표에서 자유도와 꼬리 넓이로 경계값을 찾습니다.',
             '<b>핵심</b>: 자유도가 작으면 꼬리가 두꺼워 경계가 멉니다(df 1: 12.706). 자유도가 커지면 Z의 1.960에 다가갑니다.',
             '<b>왜</b>: 표본 표준편차 s의 흔들림이 표본이 커질수록 줄어들기 때문입니다.']),
 dict(f='table_chi2.html', sid='s-c', no='3장', short='카이제곱분포', thumb='ch_c',
      desc='카이제곱분포 그리기와 χ²표 읽기. 적합도·독립성 검정, 분산의 신뢰구간.',
      three=['<b>무엇을</b>: 카이제곱분포를 그리고, χ²표에서 자유도와 오른쪽 꼬리 넓이로 경계값을 찾습니다.',
             '<b>핵심</b>: 0에서 시작해 오른쪽으로 늘어진 모양이라 왼쪽·오른쪽 경계를 따로 읽습니다.',
             '<b>일에서는</b>: 설문 교차표, 주사위·불량 비율이 예상과 맞는지 볼 때 씁니다.']),
 dict(f='table_f.html', sid='s-f', no='4장', short='F분포', thumb='ch_f',
      desc='F분포 그리기와 F표 읽기. 분자·분모 자유도, α별 표, 분산분석.',
      three=['<b>무엇을</b>: F분포를 그리고, α별 F표에서 분자(열)·분모(줄) 자유도로 경계값을 찾습니다.',
             '<b>핵심</b>: 분자와 분모를 바꾸면 값이 달라집니다. (5, 10)은 3.33, (10, 5)는 4.74.',
             '<b>일에서는</b>: 세 집단 이상의 평균 비교(분산분석)에 씁니다.']),
 dict(f='appendix_df.html', sid='s-df', no='부록', short='자유도', thumb='ch_df',
      desc='자유도란 무엇인가, 왜 표본 수 − 1인가. 피자값 나누기와 직접 해 보는 실험.',
      three=None),
 dict(f='trap_errors.html', sid='s-trap', no='해석의 함정', short='1종·2종 오류', thumb='ch_trap',
      desc='판정표(실제 Y, 판정 Ŷ)와 1종·2종 오류. 표의 기준을 넘어도 뚫리는 이유, 다중검정, 거짓 발견 비율, 검정력, 분포표 주의사항.',
      three=['<b>무엇을</b>: 분포표대로 판정해도 틀리는 두 가지 방식, 1종 오류와 2종 오류를 봅니다.',
             '<b>핵심</b>: 기각역은 드문 곳이지 불가능한 곳이 아닙니다. α를 아무리 낮춰도 뚫리고, 너무 낮추면 진짜를 놓칩니다.',
             '<b>마지막에</b>: 분포표를 쓸 때 주의사항 8가지를 정리합니다.']),
]

def nav(cur):
    links = ''.join('<a href="%s"%s>%s %s</a>' % (c['f'], ' aria-current="page"' if c['f']==cur else '', c['no'], c['short']) for c in CH)
    return f'''<nav class="top" aria-label="장 차례">
  <div class="row">
    <a class="logo" href="tables.html" style="color:inherit;text-decoration:none">분포표 읽기 연구실</a>
    <div class="links">
      {links}<a href="index.html">전체 목차</a><a href="dictionary.html">분포 딕셔너리</a>
    </div>
    <div class="mode" role="group" aria-label="설명 방식">
      <button id="m-general" aria-pressed="false">일반 설명</button>
      <button id="m-easy" aria-pressed="true">쉬운 설명</button>
    </div>
  </div>
</nav>
'''

def set_head(title, desc, thumb):
    h = head
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % html.escape(title), h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % html.escape(desc), h, count=1)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % html.escape(title), h, count=1)
    h = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % html.escape(desc), h, count=1)
    h = re.sub(r'<meta property="og:image" content="[^"]*">', '<meta property="og:image" content="%sthumbs/%s.webp">' % (URL, thumb), h, count=1)
    return h

cast_words = '''<details class="fold ez" id="castfold"><summary>연구실 식구와 말·기호 (처음이면 펼쳐 보세요)</summary>
<div class="cast" id="castgrid" style="margin-top:10px"></div>
''' + src[src.index('<div class="gloss">', src.index('id="words"')):src.index('</div>\n</section>', src.index('id="words"'))+6] + '\n</details>'

out = []
for i, c in enumerate(CH):
    s = sec(c['sid'])
    m = re.search(r'<h2 id="(h-[a-z]+)">(.*?)</h2>', s)
    hid, inner = m.group(1), m.group(2)
    title_txt = re.sub(r'<[^>]+>', '', re.sub(r'<span class="hex[^"]*">.*?</span>', '', inner)).strip()
    hexspan = re.search(r'<span class="hex[^"]*">.*?</span>', inner).group(0)
    s = s.replace(m.group(0), '', 1).replace('class="sec"', 'class="sec first"', 1)
    ikey = {'ch_z': 'z', 'ch_t': 't', 'ch_c': 'c', 'ch_f': 'f', 'ch_df': 'df', 'ch_trap': 'trap'}[c['thumb']]
    info = '<figure class="info"><img src="assets/info_%s.png" width="960" height="540" alt="%s 한눈에 보기 인포그래픽. %s"><figcaption>한눈에 보기 — 이 장의 내용을 그림 한 장으로 먼저 훑어보세요.</figcaption></figure>' % (
        ikey, html.escape(title_txt), html.escape(' '.join(re.sub('<[^>]+>', '', t) for t in (c['three'] or [c['desc']]))))
    three = ''
    if c['three']:
        three = '<div class="three"><b>이 장을 3줄로</b><ol>%s</ol></div>' % ''.join('<li>%s</li>' % t for t in c['three'])
    prev = CH[i-1] if i > 0 else None; nxt = CH[i+1] if i+1 < len(CH) else None
    pager = '<nav class="pager" aria-label="앞뒤 장">%s<a href="tables.html" class="mid">목차</a>%s</nav>' % (
        '<a href="%s">← %s %s</a>' % (prev['f'], prev['no'], prev['short']) if prev else '<span></span>',
        '<a href="%s" class="nx">%s %s →</a>' % (nxt['f'], nxt['no'], nxt['short']) if nxt else '<span></span>')
    outro = sec('outro') if c['sid'] == 's-trap' else ''
    page = (set_head('%s %s — 분포표 읽기 연구실' % (c['no'], title_txt), c['desc'], c['thumb']) + '<body>\n' + nav(c['f']) +
        '<div class="wrap">\n<header class="hero chap">\n  <div class="eyebrow"><a href="tables.html">분포표 읽기 연구실</a> · %s</div>\n  <h1 id="%s">%s%s</h1>\n  <div class="byline">글 · 안상선 ((주)M-Robo 대표)</div>\n  %s\n  %s\n  %s\n</header>\n' % (c['no'], hid, hexspan, title_txt, info, three, cast_words) +
        s + '\n' + outro + '\n' + pager + '\n' + footer + '\n</div>\n' + script + '</body>\n</html>\n')
    (ROOT/c['f']).write_text(page)
    out.append(c['f'])

# 허브
cards = ''.join('<a class="chcard" href="%s"><img src="thumbs/%s.webp" width="960" height="540" alt="%s 화면"><div><b>%s</b><h3>%s</h3><p>%s</p></div></a>' % (
    c['f'], c['thumb'], html.escape(c['short']), c['no'], c['short'], html.escape(c['desc'])) for c in CH)
hub_hero = hero_hub.replace('<div class="byline">글 · 안상선 ((주)M-Robo 대표)</div>', '<div class="byline">글 · 안상선 ((주)M-Robo 대표)</div>\n  <figure class="info"><img src="assets/info_hub.png" width="960" height="540" alt="분포표 읽기 연구실 한눈에 보기 인포그래픽. 1~4장 Z·t·카이제곱·F, 부록 자유도, 해석의 함정 1종·2종 오류."><figcaption>한눈에 보기 — 2편 전체를 그림 한 장으로.</figcaption></figure>', 1)
hub = (set_head('분포표 읽기 연구실', 'Z분포·t분포·카이제곱분포·F분포를 장마다 따로 읽고, 부록 자유도와 해석의 함정(1종·2종 오류)까지. 일반 설명과 쉬운 설명.', 'part2') +
    '<body>\n' + nav('tables.html') + '<div class="wrap">\n' + hub_hero +
    '\n<section class="sec" id="chapters" aria-labelledby="h-chapters">\n  <h2 id="h-chapters">장 고르기</h2>\n  <p class="lead">장마다 독립된 페이지입니다. 어느 장부터 읽어도 됩니다. 처음이면 1장부터 차례로 읽기를 권합니다.</p>\n  <div class="chcards">' + cards + '</div>\n' +
    src[src.index('<div class="explain">', src.index('id="map"')):src.index('</div>\n</section>', src.index('id="map"'))+6] + '\n</section>\n' +
    sec('cast') + '\n' + sec('words') + '\n' + sec('sum') + '\n' + footer + '\n</div>\n' + script + '</body>\n</html>\n')
(ROOT/'tables.html').write_text(hub)
out.append('tables.html')
print('pages:', ', '.join(out))

# ── 지식 색인 다시 덧붙이기 (kg/pages/, ai-lab-retrofit autokg) ──
if __name__ == "__main__":
    import os as _os, sys as _sys, subprocess as _sp
    _r = str(ROOT)
    if _os.path.exists(_os.path.join(_r, "kg", "reapply.py")):
        _sp.run([_sys.executable, _os.path.join(_r, "kg", "reapply.py"), _r])
