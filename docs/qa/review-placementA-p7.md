# 배치고사 A폼 Part 7 교차 검수 리포트 (S2-09)

- 검수자: ai-qa-pl-p7 (qa-tester 역할, 작성자 ai-writer-pl-p7과 다름)
- 검수일: 2026-10-13
- 대상: `content/items/p7/p7_placementA.json` (세트 8개, 문항 30개: RC-P7-000023~052)
  - 기초 모듈(23~32): S-0005 문자 대화, S-0006 청구서, S-0007 공지
  - 중간 모듈(33~42): S-0008 웹페이지, S-0009 온라인 채팅, D-0002 신청서 + 이메일
  - 상위 모듈(43~52): D-0003 기사 + 메모, T-0002 웹페이지 + 이메일 + 청구서
- 기준: `docs/qa/content-standard.md` 3·5·6·7·8·10장, `content/SCHEMA.md`, `docs/specs/placement-and-vocab.md` 1.3(모듈 난이도)

## 1. 결론

**판정: 조건부 가능 (교차 검수 통과, 원어민 검수 전)**

- 정답을 가린 채 30문항을 먼저 풀었고, 30문항 모두 표시된 정답과 같았습니다. 정답 오류는 없습니다.
- 통과 30 / 수정 후 통과 5 (통과 수에 포함: 39, 44, 45, 46, 52) / 보류 0
- 치명 결함은 없습니다. 고친 것은 보통 2건(D-0003 날짜 앞뒤 안 맞음, 52번 단체 사진 해석 여지)과 낮음 2건(함정 코드)입니다.
- 정답 글자(answer)는 하나도 바꾸지 않았습니다.
- 30문항 모두 `status: cross_reviewed`로 바꾸고 `reviewer_1_id: ai-qa-pl-p7`와 `originality_check`를 채웠습니다. `native_check_id`는 비워 두었습니다 (원어민 검수 대기).
- `python3 -B db/build_db.py`: 실패 11건이 나왔지만 모두 `content/vocab`의 어휘 카드 중복입니다 (다른 담당자가 고치는 중). 이 파일 문항에 대한 오류는 없습니다.

## 2. 문항별 판정

| item_id | 모듈 | 유형 | 난이도(작성/검수→확정) | 블라인드 답 | 정답 | 판정 | 수정 |
|---|---|---|---|---|---|---|---|
| 000023 | 기초 | MAIN.PURPOSE | 1/1→1 | B | B | 통과 | - |
| 000024 | 기초 | INTENT.CHAT | 2/2→2 | A | A | 통과 | - |
| 000025 | 기초 | DET.FACT | 1/1→1 | C | C | 통과 | - |
| 000026 | 기초 | DET.NUM | 2/2→2 | D | D | 통과 | - |
| 000027 | 기초 | INF.WHO | 2/2→2 | B | B | 통과 | - |
| 000028 | 기초 | TF.TRUE | 2/2→2 | A | A | 통과 | - |
| 000029 | 기초 | MAIN.TOPIC | 1/1→1 | C | C | 통과 | - |
| 000030 | 기초 | DET.FACT | 1/1→1 | B | B | 통과 | - |
| 000031 | 기초 | TF.NOT | 2/2→2 | D | D | 통과 | - |
| 000032 | 기초 | VOC.SYN | 2/2→2 | A | A | 통과 | - |
| 000033 | 중간 | TF.TRUE | 3/3→3 | C | C | 통과 | - |
| 000034 | 중간 | DET.NUM | 3/3→3 | A | A | 통과 | - |
| 000035 | 중간 | INS.POS | 3/3→3 | D | D | 통과 | - |
| 000036 | 중간 | INTENT.CHAT | 3/3→3 | B | B | 통과 | - |
| 000037 | 중간 | INF.NEXT | 3/3→3 | C | C | 통과 | - |
| 000038 | 중간 | MAIN.PURPOSE | 2/2→2 | A | A | 통과 | - (아래 4장) |
| 000039 | 중간 | LINK.2P | 3/3→3 | D | D | 통과 (수정) | 보기 C 함정 코드 NOT_MENTIONED → WRONG_REFERENT (v2) |
| 000040 | 중간 | LINK.2P | 4/4→4 | B | B | 통과 | - |
| 000041 | 중간 | VOC.SYN | 3/3→3 | C | C | 통과 | - (아래 4장) |
| 000042 | 중간 | TF.TRUE | 3/3→3 | A | A | 통과 | - |
| 000043 | 상위 | VOC.SYN | 4/4→4 | D | D | 통과 | - (지문 수정 영향 없음) |
| 000044 | 상위 | TF.NOT | 4/3→4 | C | C | 통과 (수정) | 지문 수정에 맞춰 evidence_quote 고침 (v2) |
| 000045 | 상위 | LINK.2P | 5/4→5 | B | B | 통과 (수정) | 보기 C last spring's → last winter's, 보기 A 함정 코드 OPPOSITE_INFO → NOT_MENTIONED, 보기 C 오답 근거 보강 (v2) |
| 000046 | 상위 | LINK.2P | 4/4→4 | A | A | 통과 (수정) | 지문 수정에 맞춰 evidence_quote·해설(지난봄 → 지난겨울) 고침 (v2) |
| 000047 | 상위 | INF.IMPLY | 4/3→4 | B | B | 통과 | - (아래 4장) |
| 000048 | 상위 | TF.TRUE | 4/4→4 | D | D | 통과 | - |
| 000049 | 상위 | LINK.2P | 4/4→4 | A | A | 통과 | - |
| 000050 | 상위 | LINK.3P | 5/4→5 | C | C | 통과 | - (아래 4장) |
| 000051 | 상위 | INF.NEXT | 4/4→4 | D | D | 통과 | - |
| 000052 | 상위 | LINK.2P | 4/4→4 | C | C | 통과 (수정) | 질문 문장 수정, 보기 D 오답 근거·해설 고침 (v2) |

- 난이도 차이는 최대 1이라 5.1 규칙(평균 반올림)으로 정했습니다. 4.5와 3.5는 올림해서 작성자 값이 그대로 남았습니다.
- 모듈별 난이도 분포(확정값)
  - 기초 23~32: 1이 4개, 2가 6개 → 명세 "1~3 (주로 1~2)"에 맞습니다.
  - 중간 33~42: 2가 1개, 3이 8개, 4가 1개 → 명세 "2~4 (주로 3)"에 맞습니다.
  - 상위 43~52: 4가 8개, 5가 2개 → 명세 "3~5 (주로 4)"에 맞습니다.

## 3. 수정 내용

### 3.1 D-0003 기사 날짜가 앞뒤가 맞지 않음 (보통) → 44·45·46번
- 문제: 기사 날짜는 8월 12일이고 "began testing refill stations **last spring**", "during the **six-month** trial"이라고 했습니다. 8월에 쓴 기사에서 last spring은 보통 같은 해 봄(3~5월)입니다. 3월에 시작했어도 6개월은 9월에야 끝나므로, 8월 12일 기사가 "6개월 시범 기간에 18% 늘었다"고 과거형으로 보고할 수 없습니다. 지난해 봄으로 읽으면 맞지만, 읽는 사람에 따라 해석이 갈립니다 (7.3 날짜 일관성).
- 수정: 지문의 last spring을 **last winter**로 바꿨습니다. 2026~27년 겨울에 시작하면 6개월 시범이 8월 전에 끝납니다. Paolo Brennan이 "this summer"에 Ostley에서 전근 온 것과도 맞습니다.
- 같이 고친 곳: 44·46번 evidence_quote, 45번 보기 C("last winter's trial"), 46번 해설("지난겨울"). 43·47번은 이 문장을 쓰지 않아 영향이 없습니다.
- 지문을 바꿨으므로 9장 규정상 원어민 검수에서 이 세트를 다시 봐야 합니다.

### 3.2 52번 질문에 해석 여지 (보통)
- 문제: 원래 질문은 "How many edited photos will each Caldwell & Rook employee most likely **receive**?"였습니다. 이 회사는 단체 사진(Group photo)도 추가했습니다. 그래서 "1인당 보정 사진 3장 + 단체 사진 1장 = 4장"(보기 D)도 받는다고 주장할 수 있습니다. 단체 사진도 보정을 거친 사진이고, 직원 모두가 그 사진에 나옵니다.
- 수정: 질문을 "How many edited photos **per person are included in the package** that Caldwell & Rook was billed for?"로 바꿨습니다. 표의 열 이름(Edited photos per person)과 맞추고, 범위를 패키지로 좁혔습니다. 단체 사진은 청구서에 $120로 따로 청구된 추가 항목이라 D는 확실히 틀립니다. 정답은 C 그대로이고, 여전히 청구서(Standard로 확정)와 웹페이지 표(3장)를 함께 봐야 하므로 LINK.2P도 그대로입니다.
- 보기 D 오답 근거와 해설의 D 설명도 바꿨습니다.

### 3.3 함정 코드 (낮음)
- 45번 A "It sold more bulk goods than any other store in the chain.": 지문은 이 지점의 매출을 말하지 않습니다. 기사는 "매출로 고르지 않는다"고 했을 뿐이라 반대 정보(OPPOSITE_INFO)가 아니라 **NOT_MENTIONED**입니다.
- 39번 C "Hiring Your First Employee": 신청서에 나오는 워크숍이므로 "언급 없음"이 아닙니다. 토요일 워크숍을 목요일 워크숍과 헷갈리게 한 보기라 **WRONG_REFERENT**로 바꿨습니다.

## 4. 작성자 질문에 대한 판정

| 문항 | 질문 | 판정 |
|---|---|---|
| 38 | 중간 모듈 안의 난이도 2 | **그대로 둡니다.** 명세의 중간 모듈 범위가 2~4이고, 10문항 중 2는 이것 하나입니다. 근거가 이메일 한 문장(Would it be possible to move my registration…)에 있고, 오답 D(delivery)만 조금 매력이 있어 독립 평가도 2입니다. 세트 첫 문항으로 워밍업 역할도 합니다. |
| 47 | 난이도 4가 3처럼 풀릴 수 있음 | **4를 유지합니다.** 검수자 독립 평가는 3입니다(메모 한 문장 안에서 풀림). 차이가 1이라 평균 3.5를 올림해 4가 됩니다. 다만 "to make room for A, B will be moved from X to Y"에서 X와 Y를 바꿔 읽는 함정(보기 A)이 실제로 강해서 4도 무리가 아닙니다. 파일럿 정답률이 70%를 넘으면 3으로 내립니다. |
| 45 | 보기 C: Wrexley Road 지점이 Stokesbury 시범 지점일 수 있나 | **C는 확실히 틀립니다.** (1) 기사는 10월부터 "nine **more** stores"에 설치한다고 했으니 다음 단계 지점은 시범 지점 3곳과 다릅니다. (2) 메모는 이 지점이 "selected for the next stage"이고 10월 3일에 장비를 "will be installed"한다고 했으니 아직 스테이션이 없습니다. (3) Ostley에서 온 Paolo가 교육을 맡는 것도 이 지점에 경험자가 없다는 것과 맞습니다. 기사 dateline이 STOKESBURY라 헷갈릴 수 있어서, 보기 C 오답 근거에 (1)(2)를 넣어 보강했습니다. |
| 47 | INF.IMPLY (2번 통로 추론) | **추론 유형으로 알맞고, 정답은 하나입니다.** 지문은 스테이션이 2번 통로에 들어간다고 직접 말하지 않고 "자리를 만들려고(To make room for the station) 카드 진열대를 2번 통로에서 옮긴다"고만 합니다. 비워지는 곳이 스테이션 자리라는 추론은 한 단계이고, 질문에 most likely가 있습니다. 기사의 "scale near the store entrance"는 저울 위치라 보기에 없고, 2번 통로와 부딪치지도 않습니다. |
| 41 | VOC.SYN receive = accept, 근접 오답 welcome | **문제없습니다.** receive a delivery = accept a delivery(물건을 인수하다)는 흔한 결합입니다. welcome은 사람·소식을 반갑게 맞는 뜻이라 "I need to be there to welcome it"은 배송품에 쓰면 뜻이 달라집니다. 원어민이 쓸 만한 대체어가 아니므로 정답이 둘이 되지 않습니다. 원어민 검수 때 한 번 더 확인하면 좋습니다 (5장). |
| 50 | 청구서 "Scheduling fee"와 웹페이지 늦은 예약 수수료를 $100으로 맞추는 것이 공정한가 | **공정합니다.** 웹페이지에서 $100 요금은 14일 전보다 늦은 예약 수수료 하나뿐이고, 다른 요금은 $35·$120·$75로 모두 다릅니다. 이메일 날짜(4월 5일)와 촬영일(4월 15일)로 10일 전 예약임을 확인할 수 있어 조건도 맞습니다. 다른 보기(오후 4시 초과, 30명 초과, 단체 사진)는 각각 지문과 부딪칩니다. 항목 이름을 다르게 써서 금액·조건으로 규정을 찾게 하는 것은 상위 모듈 LINK.3P 난이도에 맞는 장치입니다. 해설과 key_point에도 이 전략이 적혀 있습니다. |

## 5. 점검 내용

### 5.1 정답 유일성·특수 유형
- 연계 문항: 39(신청서 표 + 이메일의 요일·순서), 40(이메일 환불 요청 + 신청서 회원가·환불 규정), 45·46(기사 + 메모), 49(웹페이지 규정 + 청구서), 50(웹페이지 + 이메일 + 청구서), 52(청구서 + 웹페이지 표) 모두 지문 둘 이상이 실제로 필요합니다 (3.1-8 충족).
- NOT 문항 31·44: 오답 3개의 근거 위치가 해설과 distractor_rationale에 모두 있습니다 (3.1-7 충족).
- 문장 위치 35: "This offer"가 가리킬 혜택(10% 할인)은 [4] 앞에만 있습니다. [2]는 orders of any size와 50명 이상 주문 이야기가 이어져 그럴듯하지만, offer가 가리킬 대상이 없습니다.
- 48번 A "no more than 50 employees": 추가 인원 $35 규정이 있어 틀린 보기로 확정됩니다.

### 5.2 계산
- S-0006 청구서: 120 + 210 + 120 + 85 = 535 (표의 Total due와 같음). 4월 23일 = 120 + 85 = 205.
- 34번: 14 × 20 = 280, 10% 할인 → 252.
- D-0002: 회원 절반 → (40 + 55) ÷ 2 = 47.50 (Total paid와 같음). 화요일 워크숍 환불 20.00. 3월 6일(토) 요청은 3월 9일(화) 오후 6시보다 48시간 넘게 앞서 전액 환불 조건이 맞습니다.
- T-0002 청구서: 1,050 + 120 + 100 + 75 = 1,345 (Total과 같음). 28명은 Standard 상한 30명 안이라 추가 인원 요금이 없습니다.

### 5.3 날짜·요일 (2027년 달력으로 확인)
- D-0002: 3월 6일 토요일(이메일), 3월 9일 화요일, 3월 11일 목요일, 3월 16일 화요일, 3월 20일 토요일. 모두 맞습니다. "Tuesday evening"은 이메일 다음 화요일(3월 9일)로 읽힙니다.
- T-0002: 4월 5일 월요일(이메일), 4월 15일 목요일(촬영), 4월 16일 금요일(청구서). 맞습니다.
- D-0003: 8월 12일(기사) → 9월 20일 월요일(메모, "A list is expected next month"와 맞음) → 9월 27일 신청 마감 → 10월 3일 일요일 설치(폐점 후, "Starting in October"와 맞음). 3.1의 last spring 문제는 고쳤습니다.
- S-0007: 6월 1일 화요일 (2027년과 맞음). 6월 3~4일 주차장 폐쇄.
- S-0006: 4월 9·16·23일은 모두 금요일이라 격주·주간 작업 일정과 어울립니다. 4월 30일 청구, 5월 30일 납부 기한.

### 5.4 해설·태그
- 30문항 모두 해설의 정답이 `answer`와 같고, 근거 인용, 보기별 오답 이유, key_point, 어휘가 있습니다. 해요체로 통일되어 있고 금지 표현은 없습니다.
- evidence_quote는 모두 지문 원문과 같습니다 (build_db 검증 통과, 수정 후 재확인).
- 해설 분량: 211~388자로 모두 권장 범위(200~450자) 안입니다.
- 유형 태그는 모두 문항이 실제로 묻는 것과 맞습니다.
- 정답 위치 분포: A 8 / B 7 / C 8 / D 7 (최대 26.7%). 모듈별: 기초 A3·B3·C2·D2, 중간 A3·B2·C3·D2, 상위 A2·B2·C3·D3. 한 위치가 30%를 넘지 않습니다.

### 5.5 지문 (7장)

| 세트 | 유형 | 단어 수 | 권장 범위 | 판정 |
|---|---|---|---|---|
| S-0005 | 문자 대화 | 98 | 60~150 | 통과 |
| S-0006 | 청구서 | 124 | 60~150 | 통과 |
| S-0007 | 공지 | 152 | 60~150 | 통과 (2단어 초과, 낮음, 기록만) |
| S-0008 | 웹페이지 | 163 | 짧은 지문 60~150 / 긴 지문 180~350 사이 | 통과 (3문항이라 문제없음, 기록만) |
| S-0009 | 온라인 채팅 | 109 | 60~150 | 통과 |
| D-0002 | 신청서 + 이메일 | 130 + 138 = 268 | 250~450 | 통과 |
| D-0003 | 기사 + 메모 | 221 + 159 = 380 | 250~450 | 통과 |
| T-0002 | 웹페이지 + 이메일 + 청구서 | 182 + 134 + 62 = 378 | 350~600 | 통과 |

- 문서 형식: 이메일·메모에 수신자, 발신자, 날짜, 제목, 서명이 있고, 문자·채팅 시간은 순서대로입니다. 청구서·신청서는 표 구조입니다.
- 미국식 철자로 통일되어 있습니다 (Web site, e-mail, canceled 계열 없음).
- URL과 이메일은 모두 `name.example.com` 형식입니다 (greenfold, ashdownkitchen, brightwater, ellery, lumenlane, caldwellrook). 전화번호는 555-0118, 555-0147, 555-0162로 모두 555-01xx입니다.
- 금지 주제는 없습니다. 인물 이름은 여러 문화권에서 고르게 골랐습니다.

## 6. 저작권 점검 결과 (8.3)

- 1단계 작성자 서약: 30문항 모두 `source_note`에 "자체 창작 … 참고 자료 문장 복사 없음"이 있습니다.
- 2단계 문자열 검색 (WebSearch, 큰따옴표 검색, 10건)

| 세트 | 검색 구절 | 결과 |
|---|---|---|
| S-0005 | "my train is stopped just outside" + "set up the projector and start with the sales figures" | 일치 없음 |
| S-0006 | "lawn mowing will be done every week instead of every other week" | 일치 없음 (잔디 관리 블로그 등 주제만 비슷) |
| S-0007 | "Laptops must be used inside the building and returned to the information desk" | 일치 확인 안 됨 (실제 도서관 노트북 대여 규정 PDF 등 주제가 같은 결과. 정책 문서에 흔한 표현이고 ETS·교재 출처는 없음) |
| S-0008 | "Planning food for a team meeting should not take up your whole morning" | 일치 없음 (회의 케이터링 블로그 등 주제만 비슷) |
| S-0009 | "Last year our logo came out blurry, and we had to reprint everything" | 일치 없음 |
| D-0002 | "a supplier has just scheduled a large delivery to my shop" | 일치 없음 |
| D-0003 | "lets shoppers refill their own containers with dry goods such as rice, oats, and coffee beans" | 일치 없음 (리필 매장 기사 등 주제만 비슷) |
| D-0003 | "To make room for the station, the greeting card display will be moved" | 일치 없음 |
| T-0002 | "Our photographers bring a complete portable studio to your office" | 일치 없음 (출장 촬영 업체 페이지 등 주제만 비슷) |
| T-0002 | "our managing partner would also like a photo of the entire staff to hang in the lobby" | 일치 없음 |

- 고유명사 검색: "Harlow & Pine", "Lumen & Lane", "Ashdown Kitchen", "Greenfold Grounds Care", "Caldwell & Rook Architects", "Brightwater Small Business Center"를 검색했습니다. 같은 이름의 실존 업체는 나오지 않았습니다 (Harlow 지역 식료품점, Lumen Photography, 미국 Ashdown 시 식당 등 이름 일부만 겹침).
- 한계: 검색 도구는 제목과 URL만 돌려주고 정확 일치를 보장하지 않습니다. 결과 중 ETS 또는 TOEIC 교재 출처는 없었지만, 본문 전체를 대조한 것은 아닙니다. S-0006·S-0007·S-0009는 세트당 1건만 검색했습니다.
- 3단계 내부 유사도: 도구가 아직 없습니다. batch1(S-0001~T-0001)과 비교해 보니 주제(회의실 대여, 요리 수업, 인쇄 지연 등)와 문장이 겹치지 않습니다.
- 4단계 참고 자료 대조: 작성자가 참고한 공식·경쟁사 자료가 없다고 했으므로 해당 없습니다. 보기 구성은 일반 P7 형식을 따를 뿐, 특정 기출 문항을 떠올리게 하는 조합은 찾지 못했습니다.
- 판정: 30문항 모두 **통과**. `originality_check` = {"result": "통과", "date": "2026-10-13", "method": "AI 블라인드 풀이 + 웹 구절 검색 (세트당 1~2건, 총 10건) + 고유명사 검색"}

## 7. 원어민 검수 필요 목록

30문항 모두 원어민 검수(블라인드 풀이 + 자연스러움)가 필요합니다. 특히 아래를 먼저 확인해 주세요.

| item_id | 확인할 점 |
|---|---|
| D-0003 지문 | 고친 "began testing refill stations last winter … during the six-month trial"이 8월 12일 기사로 자연스러운지 |
| RC-P7-000052 | 바꾼 질문 "How many edited photos per person are included in the package that Caldwell & Rook was billed for?"가 자연스럽고, 단체 사진을 포함하지 않는다고 분명히 읽히는지 |
| RC-P7-000041 | "receive it"(배송품)을 welcome으로 바꿔 쓸 수 없다는 데 동의하는지 |
| RC-P7-000047 | "To make room for the station, … moved from aisle 2"만으로 스테이션이 2번 통로에 놓인다고 읽히는지 |
| RC-P7-000050 | "Scheduling fee"라는 이름이 늦은 예약 수수료(14일 규정)를 가리킨다고 받아들여지는지 |
| RC-P7-000036 | "I haven't opened them"이 "확인해 줄 수 없다"로 자연스럽게 읽히는지 (A '잘못 배송'과 헷갈리지 않는지) |
| RC-P7-000048 | 보기 A "no more than 50 employees in one session"이 추가 인원 규정($35) 때문에 확실히 틀리다고 읽히는지 |

## 8. 후속 조치 요청

1. chief-of-staff: 원어민 검수자를 배정해 주세요 (7장 목록). 특히 지문을 바꾼 D-0003 세트.
2. 9장 규정: reviewer_2_id는 비어 있습니다. qa-tester 20% 무작위 재검수 대상에 이번 묶음을 넣어 주세요.
3. 파일럿 후: 47번(난이도 4, 검수자 3)과 38번(중간 모듈 안 난이도 2)의 실측 정답률을 보고 난이도를 다시 정합니다.
4. 어휘 담당: build_db의 어휘 카드 중복 11건을 정리해 주세요 (이 파일과 무관).

## 변경 파일
- `content/items/p7/p7_placementA.json`
  - 30문항: status → cross_reviewed, reviewer_1_id, originality_check, native_check_id("") 채움
  - D-0003 기사 지문: last spring → last winter
  - version 2: RC-P7-000039, 000044, 000045, 000046, 000052
