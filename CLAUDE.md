# 온라인 TOEIC 교재 프로젝트

목표: 산타토익·해커스토익보다 뛰어난 콘텐츠와 UX/UI를 갖춘 대한민국 최고의 온라인 TOEIC 교재.
타깃: 취업 준비생·직장인. 트랙: 300→400, 400→450, 450→495. 웹 우선.
설계 기준 문서: `PLAN.md`.

## 에이전트 팀

`.claude/agents/`에 8개 역할 에이전트가 있고, **Chief of Staff가 전체를 총괄**합니다.

| # | 에이전트 | 역할 |
|---|---|---|
| 1 | `chief-of-staff` | 총괄. 요청 해석, 업무 분배, 결과 검토·취합, 의사결정 기록, 현황 보고 |
| 2 | `product-planner` | PRD, 기능 명세, 커리큘럼, 로드맵·우선순위 |
| 3 | `market-researcher` | 경쟁사·사용자·시장 조사 |
| 4 | `ux-ui-designer` | 사용자 흐름, 화면 명세, 디자인 시스템 |
| 5 | `developer` | 아키텍처, 구현, 학습 로직, 테스트 코드 |
| 6 | `qa-tester` | 기능·회귀·콘텐츠 검수, 출시 판정 |
| 7 | `marketer` | 포지셔닝, 런칭, 채널, 카피, 그로스 |
| 8 | `cs-manager` | FAQ, 응대 템플릿, 정책 초안, 피드백 루프 |

## 사용법
- `.claude/settings.json`의 `"agent": "chief-of-staff"` 설정으로, 이 저장소에서 Claude Code를 열면 Chief of Staff가 메인 에이전트로 시작합니다. 요청은 그냥 말하면 Chief of Staff가 팀원에게 나눠 맡깁니다.
- 특정 역할에 직접 맡기려면: "market-researcher 에이전트로 산타토익 가격 정책 조사해줘" 처럼 이름을 부르면 됩니다.
- 기본 작업 흐름: 시장조사 → 기획 → 디자인 → 개발 → QA → 마케팅·CS 준비.

## 문서 위치
`docs/research/`, `docs/specs/`, `docs/curriculum/`, `docs/design/`, `docs/architecture.md`, `docs/qa/`, `docs/marketing/`, `docs/cs/`, `docs/decisions/`, `docs/status.md`

## 공통 원칙
- 사용자 보고는 한국어, 결론부터.
- main push, PR 병합, 배포, 외부 발송, 광고 집행, 가격·정책 확정은 사용자 승인 후 진행.
- ETS 기출 문항을 복제하지 않고 자체 제작 문항만 사용.
