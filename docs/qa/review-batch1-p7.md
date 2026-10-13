# Part 7 Batch 1 교차 검수 리포트

- 검수자: ai-qa-reviewer-p7 (qa-tester 역할, 작성자 ai-writer-p7과 다름)
- 검수일: 2026-10-13
- 대상: `content/items/p7/p7_batch1.json` (세트 6개, 문항 22개: 단일 4세트 12문항, 이중 1세트 5문항, 삼중 1세트 5문항)
- 기준: `docs/qa/content-standard.md` 3장, 6장, 7장, 8장, 10장 / `content/SCHEMA.md`

## 1. 결론

**판정: 조건부 가능 (교차 검수 통과, 원어민 검수 전)**

- 22문항 모두 정답을 가린 채 먼저 풀었고, 22문항 모두 표시된 정답과 같았습니다. 다른 보기도 정답으로 볼 수 있는 문항은 없었습니다.
- 통과 22 / 수정 후 통과 2 (통과 수에 포함) / 보류 0
- 치명·높음 결함은 없습니다. 함정 코드(trap_code) 2건을 바로 고쳤고 (낮음~보통), 해설 분량이 기준을 조금 넘는 문항 4개는 기록만 하고 그대로 두었습니다 (낮음).
- 22문항 모두 `status: cross_reviewed`로 바꾸고 `reviewer_1_id`와 `originality_check`를 채웠습니다. `native_check_id`는 비워 두었습니다. 9장에 따라 원어민 검수(3-1단계)를 마쳐야 파일럿으로 넘어갈 수 있습니다.
- `python3 db/build_db.py` 결과: `OK: 파일 3개, 세트 10개, 문항 78개 → db/toeic_rc.db` (P5·P6 오류 없음)

## 2. 문항별 판정

| item_id | 세트 | 유형 | 블라인드 답 | 정답 | 판정 | 수정 |
|---|---|---|---|---|---|---|
| RC-P7-000001 | S-0001 | MAIN.PURPOSE | B | B | 통과 | - |
| RC-P7-000002 | S-0001 | INTENT.CHAT | A | A | 통과 (수정) | 보기 C 함정 코드 OPPOSITE_INFO → WRONG_REFERENT, 근거 문장 고침 (v2) |
| RC-P7-000003 | S-0002 | MAIN.PURPOSE | C | C | 통과 | - |
| RC-P7-000004 | S-0002 | DET.FACT | B | B | 통과 | - |
| RC-P7-000005 | S-0002 | INF.IMPLY | D | D | 통과 | - |
| RC-P7-000006 | S-0003 | MAIN.PURPOSE | A | A | 통과 | - |
| RC-P7-000007 | S-0003 | DET.FACT | C | C | 통과 | - (원어민 확인 권장, 아래 5장) |
| RC-P7-000008 | S-0003 | INS.POS | C | C | 통과 | - (해설 462자, 기록만) |
| RC-P7-000009 | S-0004 | MAIN.TOPIC | D | D | 통과 | - |
| RC-P7-000010 | S-0004 | DET.FACT | C | C | 통과 | - |
| RC-P7-000011 | S-0004 | VOC.SYN | D | D | 통과 | - |
| RC-P7-000012 | S-0004 | TF.NOT | A | A | 통과 (수정) | 보기 B·C·D 함정 코드 PARTIAL_INFO → STATED_IN_PASSAGE (v2) |
| RC-P7-000013 | D-0001 | DET.NUM | B | B | 통과 | - |
| RC-P7-000014 | D-0001 | MAIN.PURPOSE | B | B | 통과 | - |
| RC-P7-000015 | D-0001 | LINK.2P | C | C | 통과 | - (해설 533자, 기록만) |
| RC-P7-000016 | D-0001 | LINK.2P | A | A | 통과 | - |
| RC-P7-000017 | D-0001 | INF.IMPLY | D | D | 통과 | - |
| RC-P7-000018 | T-0001 | MAIN.PURPOSE | A | A | 통과 | - |
| RC-P7-000019 | T-0001 | LINK.2P | D | D | 통과 | - (해설 516자, 기록만) |
| RC-P7-000020 | T-0001 | LINK.3P | B | B | 통과 | - (해설 454자, 기록만) |
| RC-P7-000021 | T-0001 | TF.TRUE | C | C | 통과 | - |
| RC-P7-000022 | T-0001 | INF.NEXT (+LINK.3P) | A | A | 통과 | - |

정답 위치 분포: A 6 / B 5 / C 6 / D 5. 한 위치가 35%를 넘지 않습니다 (3.2-4 충족).

## 3. 점검 내용

### 3.1 정답 유일성과 특수 유형
- **연계 문항 (3.1-8)**
  - 15번: 이메일(32명, 원격 참가자, 8:30~4:30)과 웹페이지 표(수용 인원, 장비, 요금)가 둘 다 있어야 Cedar Room 종일 $470이 나옵니다. 2지문 연계가 맞습니다.
  - 16번: 무료 커피·차 조건(종일 예약)은 웹페이지에, 종일 예약이 필요하다는 근거(8:30~4:30)는 이메일에 있습니다. 2지문 연계가 맞습니다.
  - 19번: 일정표(5월 8일 강사 = Okonkwo-Brandt)와 이메일(그 수업 강사가 심사위원)만 있으면 풀립니다. 작성자 노트대로 "실제로 필요한 지문 수" 기준을 받아들여 LINK.2P를 그대로 둡니다.
  - 20번: 이메일(처음 신청한 수업 = 5월 8일), 후기(다른 토요일 오전 수업으로 바꿈), 일정표(5월 15일 = Sunniva Adeyemi)가 모두 필요합니다. 3지문 연계가 맞습니다.
  - 22번: 후기(처음 고른 수업), 이메일(5월 8일), 일정표(Knife Skills)가 모두 필요합니다. 주 유형 INF.NEXT, 보조 태그 LINK.3P가 알맞습니다.
- **NOT 문항 (12번)**: 오답 B·C·D의 근거 위치(2문단 former warehouse / 4문단 previous occupant, 4문단 near the rail line, 2문단 about 120 people)가 해설에 모두 있습니다 (3.1-7 충족). 정답 A(가구 제조)는 지문에 없습니다. 이 회사는 덮개 천을 만듭니다.
- **문장 위치 (8번)**: "With this service"가 가리킬 대상(overnight courier)이 [3] 바로 앞에만 있습니다. [2]는 날짜는 그럴듯하지만 가리킬 서비스가 없고, "your event"도 아직 나오지 않았습니다. 위치는 하나로 정해집니다.
- **요금 계산 (13·15번)**: 3일 전 취소는 "7일 미만"이라 50%입니다. 종일 8:00~5:00 안에 8:30~4:30이 들어가고, 반일은 4시간이라 부족합니다. Juniper Hall에는 화상회의 장비가 없습니다. 계산이 맞습니다.
- **날짜·요일**: 각 지문 안에서 요일과 날짜가 맞습니다.
  - S-0002: 11월 9일 월요일, 11월 20일 금요일 (2026년 달력과 맞음)
  - D-0001: 3월 4일 목요일 (2027년 달력과 맞음)
  - T-0001: 5월 4일 화요일, 6일 목요일, 8일 토요일, 13일 목요일, 15일 토요일, 22일 토요일 (2027년 달력과 맞음). 4/26 이메일 → 5/3 회신 마감 → 5/15 수업 → 5/17 후기 순서도 자연스럽습니다. 바꾼 수업($55)이 원래 수업($60)보다 싸서 차액 환불 규정과도 맞습니다.
  - S-0003: 10/26 → 10/30 완성, 익일 배송으로 10/31 도착, 11/1 행사. 서로 맞습니다.
  - 지문에 연도를 쓰지 않아 세트마다 기준 연도가 달라도 문제는 없습니다.

### 3.2 함정 코드 판단 (작성자 질문에 대한 답)
- **12번 NOT 문항**: PARTIAL_INFO는 "보기가 일부만 맞는 정보"라는 뜻입니다. NOT 문항의 오답 B·C·D는 지문과 **완전히 일치하는** 진술이라 이 코드가 맞지 않습니다. 이대로 두면 약점 리포트에서 "부분 정보 함정에 약함"으로 잘못 집계될 수 있습니다. 기존 예시 코드 14개 중에도 맞는 코드가 없어서 **`STATED_IN_PASSAGE`(지문에 언급된 사실)**로 바꿨습니다.
  - 후속 조치: product-planner가 이 코드를 함정 코드 목록(SCHEMA.md 예시)에 등록할지 정해야 합니다. 등록하지 않기로 하면 null로 바꾸는 것이 차선입니다. 21번 같은 TRUE 문항은 오답이 "언급 없음/반대 정보"라 기존 코드로 충분합니다.
- **2번 보기 C**: Mr. Wrenfield는 "누군가에게 확인하게 하라"고 했을 뿐이라 "본인이 센다"와 정반대(OPPOSITE_INFO)는 아닙니다. 실제로 세는 사람이 Dalia이므로 대상 혼동(WRONG_REFERENT)으로 고치고 근거 문장도 맞췄습니다.
- 그 밖의 함정 코드는 근거 문장과 맞습니다. 20번 C(Murakami, PARTIAL_INFO)는 WRONG_REFERENT로 볼 여지도 있지만, 결함으로 보지 않습니다.

### 3.3 해설·태그·난이도
- 22문항 모두 해설의 정답이 `answer`와 같습니다. 근거 문장 인용, 보기별 오답 이유, key_point, 어휘가 모두 있습니다. 해요체로 통일되어 있고, 금지 표현은 없습니다.
- evidence_quote: 여러 문장을 " / "로 잇는 규칙을 지켰습니다. 모든 인용이 지문 원문과 같습니다 (build_db 검증 통과).
- 해설 분량: 8번(462자), 15번(533자), 19번(516자), 20번(454자)이 권장 상한 450자를 넘습니다. 연계·위치 문항이라 근거를 여러 개 대야 해서 생긴 일이므로 고치지 않았습니다 (낮음).
- 난이도: 독립적으로 매긴 값과 작성자 값의 차이는 최대 1입니다. 7번은 작성자 4, 검수자 3이라 평균을 반올림해 4를 유지했습니다. 태그는 모두 문항이 실제로 묻는 것과 맞습니다.

### 3.4 지문 (7장)

| 세트 | 유형 | 단어 수 | 권장 범위 | 판정 |
|---|---|---|---|---|
| S-0001 | 문자 대화 | 105 | 60~150 | 통과 |
| S-0002 | 공지 | 123 | 60~150 | 통과 |
| S-0003 | 이메일 | 205 | 180~350 | 통과 |
| S-0004 | 기사 | 239 | 180~350 | 통과 |
| D-0001 | 웹페이지 + 이메일 | 147 + 151 = 298 | 250~450 | 통과 |
| T-0001 | 일정표 + 이메일 + 후기 | 123 + 143 + 151 = 417 | 350~600 | 통과 |

- 문서 형식: 이메일에는 수신자, 발신자, 날짜, 제목, 서명이 있습니다. 문자 대화의 시간은 순서대로입니다. 표 구조도 있습니다.
- 미국식 철자로 통일되어 있습니다 (canceled, program, Web site, e-mail).
- 회사·인물·지명은 모두 가상 이름입니다. 전화번호는 555-01xx 형식(가상 번호)입니다.
- 금지 주제(7.2)는 없습니다. 인물 이름은 여러 문화권에서 골랐습니다.
- 참고: URL은 `brindlemoor-example.com`처럼 "이름-example.com" 형식입니다. 7.3이 말하는 "example.com 계열"이지만 실제로 등록할 수 있는 도메인입니다. 법적 위험을 0으로 하려면 `example.com` 하위 도메인(예: `brindlemoor.example.com`)으로 통일하는 것을 검토하세요. P5·P6와 함께 정할 사안이라 이번에는 고치지 않았습니다 (낮음).

## 4. 저작권 점검 결과 (8.3)

- 1단계 작성자 서약: 22문항 모두 `source_note`에 "자체 창작 … 참고 자료 문장 복사 없음"이 있습니다.
- 2단계 문자열 검색: WebSearch를 썼습니다. 세트마다 7단어 이상 구절 2개씩, 모두 12건을 큰따옴표로 검색했습니다.

| 세트 | 검색 구절 | 결과 |
|---|---|---|
| S-0001 | "The driver said he could leave them in the storage room on the second floor" | 일치 없음 |
| S-0001 | "make sure someone signs for them and checks that all twelve are there" | 일치 없음 |
| S-0002 | "only one passenger elevator will be in service at a time" | 일치 없음 (대학 시설 공지 등 주제만 비슷한 결과) |
| S-0002 | "schedule them through the management office at least two business days in advance" | 일치 없음 |
| S-0003 | "one of our large-format presses broke down on Monday" | 일치 없음 (인쇄기 고장 뉴스 등 주제만 비슷한 결과) |
| S-0003 | "though the paper stock may differ slightly from the sample you approved" | 일치 없음 (인쇄업체 FAQ 등 주제만 비슷한 결과) |
| S-0004 | "a maker of upholstery fabric based in Calderby for more than forty years" | 일치 없음 |
| S-0004 | "Our current site is running at capacity six days a week" | 일치 없음 |
| D-0001 | "Groups that book any room for a full day receive complimentary coffee and tea service" | 일치 없음 (회의실 대여 페이지 등 주제만 비슷한 결과) |
| D-0001 | "we will need equipment that allows them to see and hear the presenters" | 일치 없음 |
| T-0001 | "the instructor for this session has been invited to serve as a judge" | 일치 없음 |
| T-0001 | "so I switched to the only other Saturday morning class on the schedule" | 일치 없음 |

  - 한계: 검색 도구는 제목과 URL만 돌려주고, 큰따옴표 정확 일치를 보장하지 않는 것으로 보입니다 (주제가 비슷한 결과가 섞여 나옴). 결과 제목과 URL 중 ETS 또는 TOEIC 교재 출처는 없었습니다. 본문 전체를 대조한 것은 아닙니다.
- 3단계 내부 유사도 검사: 아직 도구가 없어서 하지 않았습니다. 이번 묶음 안에서는 세트끼리 중복이 없습니다.
- 4단계 참고 자료 대조: 작성자가 참고한 공식·경쟁사 자료가 없다고 했으므로 해당 없습니다. 보기 구성도 일반 P7 형식을 따를 뿐, 특정 기출 문항을 떠올리게 하는 조합은 찾지 못했습니다.
- 판정: 22문항 모두 **통과**. `originality_check` = {"result": "통과", "date": "2026-10-13", "method": "AI 블라인드 풀이 + 웹 구절 검색 2건"} (세트당 2건, 모두 12건)

## 5. 원어민 검수 필요 목록

22문항 모두 원어민 검수(블라인드 풀이 + 자연스러움 확인)를 받아야 합니다. 특히 아래 문항을 먼저 확인해 주세요.

| item_id | 확인할 점 |
|---|---|
| RC-P7-000007 | 15% 할인(B)은 모든 고객에게 주는 보상인데, "새 날짜를 받아들일 수 없을 때도 할인은 유지된다"고 보면 B를 고를 수 있다는 반론이 나올 수 있습니다. 질문의 if 조건 때문에 C 하나로 정해진다는 데 동의하는지 확인해 주세요. |
| RC-P7-000002 | "That works for me"가 바로 앞 9:15 제안(창고 보관)에 대한 답으로 자연스럽게 읽히는지 확인해 주세요. |
| RC-P7-000005 | "on weekdays" → "will not be carried out on weekends"가 추론(INF) 문항으로 적당한지, 너무 직접적이지 않은지 확인해 주세요. |
| RC-P7-000017 | branch office → "employees working in more than one location"으로 바꿔 말한 것이 자연스러운지 확인해 주세요. |
| RC-P7-000020 | "the only other Saturday morning class on the schedule"이 (5월 22일로 옮긴 수업을 빼고) 5월 15일 하나만 가리킨다고 읽히는지 확인해 주세요. |
| RC-P7-000022 | "when it is offered again next month"가 5월 22일로 옮긴 수업이 아니라 6월 개설을 가리킨다고 분명하게 읽히는지 확인해 주세요. |
| RC-P7-000015 | "most likely pay"가 종일 요금 $470 하나로 정해지는지 확인해 주세요 (캐터링 등 추가 비용과 헷갈리지 않는지). |

## 6. 후속 조치 요청

1. product-planner: `STATED_IN_PASSAGE` 함정 코드를 목록에 넣을지 정해 주세요 (12번).
2. chief-of-staff: 원어민 검수자를 배정해 주세요 (5장 목록). 배정 전에는 `cross_reviewed`에서 다음 단계로 넘어갈 수 없습니다.
3. 콘텐츠 담당: 가상 URL 형식을 `*.example.com`으로 통일할지 P5·P6와 함께 정해 주세요.
4. 9장 규정: 2차 검수자(reviewer_2_id)는 아직 비어 있습니다. qa-tester 20% 무작위 재검수 대상에 이번 묶음을 넣어 주세요.

## 변경 파일
- `content/items/p7/p7_batch1.json`: 22문항 상태와 검수 필드 갱신, RC-P7-000002와 RC-P7-000012는 version 2
