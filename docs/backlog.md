# 백로그

| ID | 작업 | 담당 | 산출물 | 선행 | 상태 |
|---|---|---|---|---|---|
| S1-01 | 운영 문서 초기화 | chief-of-staff | docs/status.md, docs/backlog.md | - | 완료 |
| S1-02 | 경쟁사 심층 분석(산타, 해커스, YBM, 영단기) | market-researcher | docs/research/competitors.md | - | 완료 |
| S1-03 | 타깃 페르소나와 페인포인트 | market-researcher | docs/research/personas.md | - | 완료 |
| S1-04 | 기회 영역 3개와 제품 비전 | product-planner | docs/specs/vision.md | S1-02, S1-03 | 완료 |
| S1-05 | MVP 범위와 로드맵 초안 | product-planner | docs/roadmap.md | S1-04 | 완료 |
| S1-06 | 핵심 학습 흐름 스케치 | ux-ui-designer | docs/design/core-flow.md | S1-04 | 완료 |
| S1-07 | 기술 스택 후보와 문항 데이터 모델 | developer | docs/architecture.md | S1-05 | 완료 |
| S1-08 | 문항 검수 기준 | qa-tester | docs/qa/content-standard.md | - | 완료 |
| S1-09 | 포지셔닝과 대기자 모집 아이디어 | marketer | docs/marketing/positioning.md | S1-04 | 완료 |
| S1-10 | 경쟁사 리뷰 불만 유형 분류 | cs-manager | docs/cs/competitor-complaints.md | - | 완료 |
| S1-11 | 스프린트 리뷰와 Phase 1 진입 승인 요청 | chief-of-staff | docs/reports/sprint-1.md | 전부 | 진행 |
| S1-12 | 배치고사·필수 학습 범위·어휘 추천 명세 (사용자 요청 2026-10-13) | product-planner | docs/specs/placement-and-vocab.md | - | 완료 |
| S1-13 | 배치 결과·범위·어휘 화면 설계 | ux-ui-designer | docs/design/placement-vocab-flow.md | S1-12 | 완료 |
| S1-14 | 배치·추천·어휘 데이터 모델과 로직 | developer | docs/architecture-placement-vocab.md, db/logic_v0.py | S1-12 | 완료 |
| S1-15 | 배치고사·어휘 콘텐츠 검수 기준 | qa-tester | docs/qa/content-standard.md 보강 | S1-12 | S2-04로 이관 |
| S1-16 | 창작 문항 1차 묶음 (P5 40, P6 16, P7 22) | content writers | content/items/ | - | 완료 |
| S1-17 | 문항 DB 적재와 Part·유형별 현황 | chief-of-staff | db/toeic_rc.db, db/REPORT.md | S1-16 | 완료 |
| S2-01 | 배치고사 A폼 Part 5·6 (24문항) | content writer | content/items/p5, p6 | - | 진행 |
| S2-02 | 배치고사 A폼 Part 7 (9세트 30문항) | content writer | content/items/p7 | - | 진행 |
| S2-03 | 어휘 카드 1차 380개 (기초 150, 400 레벨 230) | content writers | content/vocab/ | - | 작성 완료, 검수 중 |
| S2-04 | 어휘 카드·어휘 체크 검수 기준 (S1-15 흡수) | qa-tester | docs/qa/vocab-standard.md | - | 완료 |
| S2-05 | PRD v1 (비전·로드맵·배치·어휘·디자인 수정안 통합) | product-planner | docs/specs/prd-v1.md | - | 진행 |
| S2-06 | 대기자 랜딩 초안 (게시 안 함) | marketer | prototypes/landing.html | - | 완료 |
| S2-07 | 배치고사 폼 구성 파일과 DB 적재 | chief-of-staff | content/forms/, db/ | S2-01, S2-02 | 대기 |
| S2-08 | 어휘 체크 A폼 20문항 | content writer | content/forms/ | S2-03 | 대기 |
| S2-09 | 배치고사 문항·어휘 카드 교차 검수 | qa-tester | docs/qa/ | S2-01~03 | 대기 |
