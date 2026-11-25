# 확률분포 딕셔너리와 분포표 연구실

확률분포 21종의 관계를 3D 지도로 보는 딕셔너리(1편)와, 분포표 읽는 법·단측과 양측검정·가설검정과 신뢰구간·1종과 2종 오류·검정력을 다루는 연구실 해설(2편)입니다. 2편은 v2.0에서 Z·t·χ²·F 네 표, 부록 자유도, 해석의 함정(1종·2종 오류) 구성으로 다시 짰습니다.

| 편 | 파일 | 내용 |
|---|---|---|
| 목차 | `index.html` | 두 편으로 가는 첫 화면 |
| 1편 | `dictionary.html` | 이산확률분포의 세계와 연속확률분포의 세계로 나눈 3D 관계 지도(분포마다 3D 그래프, 두 세계를 잇는 다리), 분포별 식·용도·파이썬 호출·생성 AI 프롬프트 |
| 2편 목차 | `tables.html` | 장 카드, 연구실 식구, 말과 기호, 정리 표 (예전 `tables.html#table-z` 같은 링크는 해당 장으로 넘어감) |
| 2편 1장 | `table_z.html` | Z분포 |
| 2편 2장 | `table_t.html` | t분포 — 자유도가 커지면 t값 → z값 |
| 2편 3장 | `table_chi2.html` | 카이제곱분포 |
| 2편 4장 | `table_f.html` | F분포 |
| 2편 부록 | `appendix_df.html` | 자유도란 무엇인가, 왜 n − 1인가 (쉬운 5단계) |
| 2편 함정 | `trap_errors.html` | 1종·2종 오류, 판정표 Y·Ŷ(픽셀 그림 `assets/cm_*.png`, `build/gen_cm.py`), 분포표 주의사항 |
| (옛 설명) | — | 분포표 읽기: ① Z분포 ② t분포(자유도가 커지면 t값 → z값) ③ 카이제곱분포 ④ F분포, 부록 자유도(왜 표본 수 − 1인가), 해석의 함정 1종·2종 오류(판정표 Y·Ŷ, 기준이 뚫리는 모의실험, 다중검정, 거짓 발견 비율, 검정력)와 분포표 주의사항. 흰 배경. **일반 설명 / 쉬운 설명(연구실 식구 총출동)** 선택 |

- 검토 기록: `review/persona_review.md`
- 다시 만들기: `build/` (`gen_data.py`로 표 값 계산 → `gen_cm.py`로 판정표 픽셀 그림 → `build.py`가 `tables.src.html` 하나에서 목차와 장 페이지 7개를 만들고 지식 색인을 다시 붙임)
- 표 값은 scipy 1.18.1로 계산했습니다.

## 표지 그림 프롬프트 (2편, 16:9)

16-bit RPG pixel art, night research lab with indigo-violet background and teal monitor glow. A huge glowing statistics table on the back wall drawn only as a grid of light cells (no letters or numbers), one cell highlighted in neon green with a cross-shaped path of lighter cells. In front: chibi scientist (thin teal rectangular glasses, spiky black hair with one white streak, small ponytail, white lab coat over black vest and tie) pointing at the bell curve; girl researcher (long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans) holding a clipboard; anthropomorphic fruit fly researcher (black body, big red compound eyes, blue helmet with gold stripe and pink and blue cables, white lab coat over black vest, black gloves) holding a magnifying glass; boxy beige retro CRT-monitor robot with mint pixel face, abacus-bead antenna and tank treads, holding a wooden abacus; two maid interns at the side, one with long straight black hair waving a small signal flag, one with ash-beige wavy hair and white frilled headband holding a pink teacup. A glowing bell curve floats in the middle with both tails shaded red. No text, no logos. 16:9.

## 저작권

캐릭터 이름·설정·그림은 저작권자 안상선의 허락 없이 사용할 수 없습니다.

글 · 안상선 ((주)M-Robo 대표) · [저자 소개](https://adminmrobo.github.io/who_am_i/who_am_i.html)
