# STRONG PEOPLE — 홈페이지 v2.2

`index.html` 단일 파일 + `assets/` 구성. GitHub Pages `https://yckang91-sketch.github.io/strongpeople-v21-preview/` 로 배포한다.

## v2.2 (2026-11-27) 변경

1. **화보 교체** — WORK 카드 9장을 문자·로고·프레임선 0% 흑백 에디토리얼 화보(`assets/work-v22-01.png`~`work-v22-09.png`)로 전면 교체. `og:image` 도 `assets/og-v22.png`(1200×630)로 교체.
2. **신뢰 팩트** — 자사 인스타그램 8개 채널 팔로워 합계 220만+, 벤처기업 인증(2024-10), `2020 팀 시작 · 2024-06 법인 설립` 표기를 HERO·TRUST STRIP·ABOUT·FOOTER·JSON-LD·meta description에 반영.
3. **무료 원고 샘플** — `#sample` 섹션에 Tally 폼(`https://tally.so/r/EqWQ7N`) 임베드. 히어로·네비(Free Sample)·모달 CTA·컨택트 버튼에서 연결. 폼 미표시 시 새 창 폴백 링크 제공.
4. **Process 4단계** — `#process` 섹션(업종·경쟁사 진단 → 맞춤 원고·촬영 → 채널 등급별 실행 → URL·반응 리포트).
5. **상품 스펙 구체화** — WORK 카드 02~09의 `단가/제안서 기준` 반복을 산출물·납기·트랙 중심으로 교체. 미확정 가격은 표기하지 않음.
6. **ARCHIVE 클릭** — 마퀴 항목 클릭 시 해당 상품 모달(상담 안내 포함)이 열린다.

## 유지 규칙 (대외 금기)

- 카페 단가 **건당 13,000원** 통일. `19,000원` 표기 금지.
- 내부 카페 풀 수치(`3,000+` 등), `그느드컴퍼니` 실명, `삭제불가` 보장, `스타터`/`풀퍼널` 용어, 인스타·영수증리뷰 미확정 단가 사용 금지.
- 모바일 히어로 영상: `assets/hero_loop_720.mp4` 1순위 + `charlla.io` 폴백 로직 유지.

## 검수

`capture_v22.py` — 라이브 URL 기준 PC 1440×900 / MO 390×844 캡처. 이미지 로딩(`naturalWidth`), JSON-LD, 콘솔 에러, 모바일 영상 재생, `19,000원` 0건을 함께 출력한다.

```bash
PLAYWRIGHT_BROWSERS_PATH=/workspace/.pw-browsers LD_LIBRARY_PATH=/workspace/.libs/root/usr/lib/x86_64-linux-gnu:/workspace/.libs/root/lib/x86_64-linux-gnu \
python3 capture_v22.py https://yckang91-sketch.github.io/strongpeople-v21-preview/ preview_v22
```

헤드리스 셸에서 `device_scale_factor ≠ 1` 이면 cross-origin iframe 내부가 잘못 스케일되는 현상이 있어, 모바일 캡처는 `device_scale_factor=1` 로 촬영한다(실기기 렌더링과 동일).
