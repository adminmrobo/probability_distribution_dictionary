# 확률분포 딕셔너리와 분포표 연구실

확률분포 21종의 관계를 3D 지도로 보는 딕셔너리(1편)와, 분포표 읽는 법·단측과 양측검정·가설검정과 신뢰구간·1종과 2종 오류·검정력을 다루는 연구실 해설(2편)입니다.

| 편 | 파일 | 내용 |
|---|---|---|
| 목차 | `index.html` | 두 편으로 가는 첫 화면 |
| 1편 | `dictionary.html` | 이산확률분포의 세계와 연속확률분포의 세계로 나눈 3D 관계 지도(분포마다 3D 그래프, 두 세계를 잇는 다리), 분포별 식·용도·파이썬 호출·생성 AI 프롬프트 |
| 2편 | `tables.html` | Z·t·χ²·F·이항·포아송 표 읽기, 단측·양측, 검정 ⇔ 신뢰구간, 오류와 검정력. **일반 설명 / 쉬운 설명(연구실 식구 총출동)** 선택 |

- 검토 기록: `review/persona_review.md`
- 다시 만들기: `build/` (`gen_data.py`로 표 값 계산 → `build.py`로 캐릭터 그림과 표 값을 `tables.src.html`에 넣어 `tables.html` 생성)
- 표 값은 scipy 1.18.1로 계산했습니다.

## 표지 그림 프롬프트 (2편, 16:9)

16-bit RPG pixel art, night research lab with indigo-violet background and teal monitor glow. A huge glowing statistics table on the back wall drawn only as a grid of light cells (no letters or numbers), one cell highlighted in neon green with a cross-shaped path of lighter cells. In front: chibi scientist (thin teal rectangular glasses, spiky black hair with one white streak, small ponytail, white lab coat over black vest and tie) pointing at the bell curve; girl researcher (long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans) holding a clipboard; anthropomorphic fruit fly researcher (black body, big red compound eyes, blue helmet with gold stripe and pink and blue cables, white lab coat over black vest, black gloves) holding a magnifying glass; boxy beige retro CRT-monitor robot with mint pixel face, abacus-bead antenna and tank treads, holding a wooden abacus; two maid interns at the side, one with long straight black hair waving a small signal flag, one with ash-beige wavy hair and white frilled headband holding a pink teacup. A glowing bell curve floats in the middle with both tails shaded red. No text, no logos. 16:9.

## 저작권

캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다.

글 · 안상선 ((주)M-Robo 대표) · [저자 소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)
