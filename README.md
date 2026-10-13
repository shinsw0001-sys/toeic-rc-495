# toeic-rc-495
토익교재저장소

토익 RC 전용 온라인 과정의 기획 문서, 창작 문항, 어휘 카드, 화면 시안을 모아 둔 저장소입니다. 모든 문항과 지문은 새로 쓴 창작물이며 ETS 기출이나 시판 교재를 옮기지 않았습니다.

## 구성
- `.claude/agents/`: 역할별 에이전트 8개 (Chief of Staff가 총괄). 팀 사용법은 `CLAUDE.md` 참고
- `docs/`: 현황(`status.md`), 백로그, 결정 기록, 조사, 명세(PRD v1 포함), 설계, 마케팅, QA 기준과 검수 보고서
- `content/items/`: Part 5·6·7 창작 문항 (JSON, 형식은 `content/SCHEMA.md`)
- `content/vocab/`: 어휘 카드 (기초, 400)
- `content/forms/`: 배치고사 폼
- `db/`: 검증·적재 스크립트와 추천 로직 참고 구현
- `prototypes/`: 화면 시안 (HTML, 캡처)

## DB 만들기
```
python3 -B db/build_db.py      # 검증 후 db/toeic_rc.db 생성, db/REPORT.md 갱신
python3 -B db/export_xlsx.py   # db/toeic_rc_items.xlsx 생성
```
