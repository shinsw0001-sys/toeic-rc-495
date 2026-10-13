# Sprint 1 리뷰 (2026-10-13)

## 결론
- 목표였던 "이길 지점 3개 + MVP 범위"를 근거와 함께 정했습니다. 11개 작업 중 10개 완료, 이 리뷰(S1-11)는 사용자 승인 대기입니다.
- 제품 방향: **RC 전용 웹 서비스**. 총점이 아니라 RC 구간 점수를 시험일까지 올리는 상품.
- Phase 1(정의) 진입 승인을 요청합니다.

## 이길 지점 3개 (docs/specs/vision.md)
| # | 이길 지점 | 근거 요약 |
|---|---|---|
| W1 | RC 구간 트랙 + 시험일 마감형 플랜 (하루 25분) | 경쟁사 상품은 모두 총점 기준. 한국 평균 RC 303점(ETS 2024) |
| W2 | 틀린 이유까지 가르치는 검수된 문항 (근거 하이라이트, 오답 함정 이름, 오답 원인 복습) | 산타 문항 오류·반복 불만, 해커스 해설 동선 불만 |
| W3 | 범위와 근거로 보여주는 RC 예측, 정확도 공개 | 산타 "예측이 후하다" 불만, 경쟁사 모두 오차 미공개 |

뺀 후보: 정직한 가격·환불(대형사가 쉽게 따라 해서 차별점 대신 기본 원칙), 웹 장문 화면·고득점 함정 훈련(W2에 흡수), 인강 플레이어(강의 안 함).

## MVP 범위 (docs/roadmap.md)
F1 진단 30문항 · F2 트랙·마감형 플랜 · F3 웹 분할 풀이 · F4 근거 해설 · F5 오답 원인 복습 · F6 RC 모의고사 1회 · F7 범위·근거 예측 · F8 실제 성적 입력 · F9 문항 오류 신고 · F10 계정·단일 상품 결제.
제외: LC, 450→495 트랙(Next), 강의, AI 튜터 채팅, 네이티브 앱, 환급형 상품.
첫 문항 세트 약 830문항(베타 1차 약 140문항). 제작 속도는 S2에서 30문항 시험 제작으로 측정.

## 역할별 산출물
| 역할 | 산출물 |
|---|---|
| Market Researcher | docs/research/competitors.md, docs/research/personas.md |
| CS Manager | docs/cs/competitor-complaints.md |
| QA Tester | docs/qa/content-standard.md |
| Product Planner | docs/specs/vision.md, docs/roadmap.md |
| UX/UI Designer | docs/design/core-flow.md, prototypes/part7-split.html |
| Developer | docs/architecture.md (추천: Next.js + Supabase + Vercel + 토스페이먼츠) |
| Marketer | docs/marketing/positioning.md |

## CoS 검토 메모
- 마케터 지적 반영: vision.md 실험 문구의 "+50점"을 점수 약속으로 읽히지 않게 "목표"로 바꿈.
- 디자이너 명세 수정안 R1~R4(세트 채점, 확신 없음 토글, 재배분 되돌리기, 찍기 감지)는 Phase 1에서 PRD에 반영.
- 근거 하이라이트용 문장 ID는 architecture.md에 이미 반영됨.
- 프로토타입은 헤드리스 브라우저에서 오류 없이 열림 확인(prototypes/part7-split.png).

## 리스크
- 2026년 자소서 어학 성적에서 스피킹이 토익을 앞섬 → 공무원·공기업·승진·졸업 인증 수요에 집중.
- 경쟁사 가격(해커스·YBM·영단기), 일부 앱 평점은 확인 못 함.
- PLAN.md 미반영(저장소 접근 권한 없음).
- 콘텐츠 제작 인력·속도가 일정의 가장 큰 변수.

## 사용자 결정 필요
1. Phase 1 진입: 이길 지점 3개와 MVP 범위 승인
2. MVP 트랙 범위: 300→400, 400→450 두 개 (추천)
3. 가격: 6주 트랙권, ₩59,000 이하에서 S2 설문으로 결정 (추천)
4. 환불: 7일 무조건 환불 + 일할 환불 + 졸업 조건 미달 시 6주 무료 연장, 환급형 안 함 (추천, 법률 검토 필요)
5. 기술 스택: Next.js + Supabase (추천)
6. 콘텐츠 제작 인력과 생성형 AI 초안 허용 범위

## Sprint 2 안 (Phase 1 정의)
가설 검증(대기자 랜딩 A/B, 설문 20~30명, 인터뷰 5명), PRD 확정, 30문항 시험 제작으로 속도 측정, 커리큘럼·태그 체계 확정.
