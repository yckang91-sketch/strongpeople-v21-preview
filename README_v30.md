# STRONG PEOPLE — 홈페이지 v3.0 (브랜드 화보집 / Editorial Lookbook)

`index.html` 단일 파일 + `assets/` 구성. GitHub Pages `https://yckang91-sketch.github.io/strongpeople-v21-preview/` 로 배포한다.

## v3.0 (2026-11-27) 변경

1. **구조 전면 재설계** — 균등 카드 그리드·박스 쌓기를 버리고 6개 챕터의 에디토리얼 룩북으로 재구성.
   `HERO` → `ONE-TEAM CHAIN` → `LOOKBOOK`(Chapter I·II·III) → `OWNED MEDIA` → `ALL SERVICES`(타이포 인덱스) → `PROCESS & FAQ` → `FREE SAMPLE` → `CONTACT`.
   기존 `INDEX`(서비스 4줄 목차)와 `WORK`(9장 균등 그리드)의 중복을 없애고, 9개 상품을 3개 챕터 화보로 통합.
2. **화보 전면 교체** — v2.2 정물(노트북·선물상자·타자기·신문지) 폐기. `images` CLI 로 인물·실루엣·건축적 빛·스튜디오 필름 연작 12컷을 새로 생성(`assets/v3-*.jpg`), 히어로 영상과 톤 통일. 문자·로고·프레임선 0%.
3. **움직임 3곳** —
   - `01 네이버 카페 바이럴`: `@keyframes slowZoom` 시네마틱 슬로우 줌 + 호버 시 콘트라스트/스케일 전환.
   - `04 인스타그램 파워페이지`: 3프레임 크로스페이드 시퀀스(24s) + Ken Burns + 펄스 라벨(Live Feed).
   - `07 숏폼·브랜드 필름`: 실제 `<video autoplay muted loop playsinline>` 로 `assets/hero_loop_720.mp4` 직접 루프.
4. **폰트 교체** — Pretendard Variable(한글) + Instrument Serif(디스플레이/이탤릭) + Archivo(라벨) + JetBrains Mono(스펙 캡션). Anton·Noto Sans KR 조합 폐기.
5. **GEO·버그 수정** —
   - `tel:180090014` → `tel:18009014`.
   - JSON-LD `hasOfferCatalog` 10종(9개 상품 + 통합 패키지) 완비.
   - H1·H2 에 한국어 핵심 키워드(sr-only 포함), 루트에 `llms.txt`·`sitemap.xml`·`robots.txt` 추가.
   - Tally 섹션 문구를 "문의 전 먼저 확인하는 맞춤 원고 샘플 1건" 으로 수정.
6. **신뢰 팩트** — 자사 인스타 8개 채널 220만+, 재계약률 90%+, 벤처기업 인증(2024-10), 2020 팀 시작·2024-06 법인 설립, 자체 촬영 스튜디오. 업종 8개 실행 조합과 브랜드사 직접/대행사 트랙 분리.
7. **영상 레터박스 제거** — 원본 필름에 박혀 있던 상하 레터박스를 `transform: scale()` 로 크롭해 풀블리드 유지(히어로·필름 카드·컨택트).

## 유지 규칙 (대외 금기)

- 카페 단가 **건당 13,000원** 통일. `19,000원` 표기 금지.
- 내부 카페 풀 수치(`3,000+` 등), `그느드컴퍼니` 실명, `삭제불가` 보장, `스타터`/`풀퍼널` 용어, 인스타·영수증리뷰 미확정 단가 사용 금지.
- 모바일 히어로 영상: `assets/hero_loop_720.mp4` 1순위 + `charlla.io` 폴백 로직 유지.

## 검수

`capture_v30.py` — 라이브 URL 기준 PC 1440×900 / MO 390×844 캡처. 이미지 로딩(`naturalWidth`), JSON-LD 파싱·오퍼 수, 금기 문구, 콘솔/HTTP 오류, 오버플로, 모바일 영상 재생, Tally 임베드 로딩을 함께 출력한다.

```bash
PLAYWRIGHT_BROWSERS_PATH=/workspace/.pw-browsers LD_LIBRARY_PATH=/workspace/.libs/root/usr/lib/x86_64-linux-gnu:/workspace/.libs/root/lib/x86_64-linux-gnu \
python3 capture_v30.py https://yckang91-sketch.github.io/strongpeople-v21-preview/ preview_v30
```

헤드리스 셸에서 `device_scale_factor ≠ 1` 이면 cross-origin iframe 내부가 잘못 스케일되는 현상이 있어, 모바일 캡처는 `device_scale_factor=1` 로 촬영한다(실기기 렌더링과 동일).
