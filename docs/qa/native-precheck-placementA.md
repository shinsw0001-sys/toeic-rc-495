# 배치고사 A폼 원어민 사전 검수 (AI): Part 5·6·7

- 검수자: `ai-native-pre-1` (native-reviewer 역할, AI 사전 검수)
- 검수일: 2026-10-13
- 대상: 54문항, 모두 `cross_reviewed`
  - `content/items/p5/p5_placementA.json` (RC-P5-000041~060)
  - `content/items/p6/p6_placementA.json` (세트 RC-P6-S-0005, RC-P6-000017~020)
  - `content/items/p7/p7_placementA.json` (세트 S-0005~0009, D-0002, D-0003, T-0002, RC-P7-000023~052)
- 이 검수는 사람 원어민 검수를 대신하지 않습니다. `native_check_id`는 비워 두었고, 결과는 문항의 `native_precheck_id`(`ai-native-pre-1`), `native_precheck_note`와 이 보고서에만 남겼습니다.

---

## 1. 요약

| 판정 | 문항 수 |
|---|---|
| 통과 | 35 |
| 수정 후 통과 | 5 (P7-038, 039, 040, 042, 047) |
| 사람 원어민 확인 필요 | 14 |
| 합계 | 54 |

- 블라인드 풀이: 정답 키를 보기 전에 54문항을 모두 풀었고, 54문항 모두 키와 같았습니다.
- 정답 기호는 하나도 바꾸지 않았습니다.
- 지문을 고친 곳은 2곳입니다 (D-0002 이메일 1문장, D-0003 기사 1문장). 직접 영향을 받는 040, 047은 `version`을 올리고 `updated_at: "2026-10-13"`을 넣었습니다. 038·039·042는 같은 지문을 쓰지만 문항 텍스트, 근거 인용, 해설이 바뀌지 않아 version은 그대로 두고 메모에만 남겼습니다.
- "사람 원어민 확인 필요" 14건 중 대부분은 결함을 찾은 것이 아닙니다. QA가 지정했거나 지문이 바뀐 세트라서, 추측으로 통과시키지 않고 올린 것입니다. 실제로 원어민 판단이 갈릴 수 있는 것은 P5-060, P7-050, D-0003 세트입니다.
- 빌드: `python3 -B db/build_db.py` → `OK: 파일 6개, 세트 19개, 문항 132개, 어휘 카드 383개, 폼 1개`. 새 필드 때문에 깨지지 않았습니다.

### 표기·이름 일관성 (4. 문화·표기)
- 철자: 미국식으로 통일되어 있습니다 (canceled, center, color 계열). 영국식 철자는 없습니다.
- 날짜: 모두 "April 30, 2027"처럼 월 일, 연도 순서입니다. 요일과 날짜는 2027년 달력과 맞습니다 (3월 6일 토, 3월 9일 화, 9월 20일 월, 10월 3일 일, 4월 15일 목, 6월 1일 화).
- 시각: 한 세트 안에서는 형식이 같습니다 (P6 세트는 "7 A.M.", P7은 "9:00 P.M."). 세트끼리 다른 것은 문제되지 않습니다.
- "Web site", "E-mail", "Internet"(대문자): 지금의 미국 언론 표기(website, email, internet)보다 옛날식이지만 TOEIC 문체와 맞고 세트 안에서 일관됩니다. 고치지 않았습니다.
- 가상 이름: Halcrest Logistics, Brightholm Lodge, Quarrington Workspace, Pexley Engineering, Skelbrook Paper를 웹 검색했습니다. 같은 이름의 실존 업체는 없었습니다 (Hillcrest, Brighton Lodge처럼 비슷한 이름만 나옴). QA가 검색한 나머지 이름(Harlow & Pine, Lumen & Lane 등)도 그대로 인정합니다. 이상한 뜻을 가진 이름은 없습니다.
- 원문 유사성: ETS 기출이나 시판 교재와 지나치게 닮았다고 느낀 문장은 없습니다.

---

## 2. 수정한 문항 (수정 전후)

### 2.1 RC-P7-D-0002 이메일: "the Tuesday workshop" (보통) → 040 (v2), 038·039·042 메모
- 문제: Mr. Ellery가 신청한 두 워크숍(Bookkeeping Basics 3월 9일, Pricing Your Products 3월 16일)이 **모두 화요일**입니다. 그래서 "the Tuesday workshop"이 어느 쪽인지 문장만으로는 정해지지 않습니다. 앞의 "the first workshop", "that same week"으로 풀리기는 하지만, 3월 16일로 읽으면 55달러의 절반인 $27.50이 되어 040 보기 D와 정확히 맞습니다. 원어민 편집자라면 바로 고칠 문장입니다.
- 수정 전: "If the Thursday session is already full, please cancel my registration for the Tuesday workshop and refund what I paid for it."
- 수정 후: "If the Thursday session is already full, please cancel my registration for the **March 9** workshop and refund what I paid for it."
- 040에서 같이 고친 곳: evidence_quote(지문과 글자 그대로 같게), 해설("3월 9일 워크숍"), 오답 근거 B·D(D는 "3월 16일 Pricing Your Products의 회원가, 그대로 듣겠다고 함"). 금액은 여전히 신청서의 정가·회원 할인과 합쳐야 나오므로 LINK.2P 성격과 난이도는 그대로입니다.

### 2.2 RC-P7-D-0003 기사: 저울 위치 문장 (보통) → 047 (v2)
- 문제: "Each station will have a scale near the store entrance"는 '스테이션마다 입구 근처에 저울이 있다'라서, 스테이션 자체가 입구 쪽에 놓인다고 읽힐 수 있습니다. 047의 정답 근거(카드 진열대를 2번 통로에서 빼서 스테이션 자리를 만든다)와 부딪치는 인상을 줍니다. 보기에 '입구'가 없어 정답이 둘이 되지는 않지만, 상위 모듈 수강생을 헷갈리게 만드는 불필요한 잡음입니다.
- 수정 전: "Each station will have a scale near the store entrance so that shoppers can weigh their empty containers before filling them."
- 수정 후: "Each **participating store will also** have a scale near **its** entrance so that shoppers can weigh their empty containers before filling them."
- 047 해설에 "기사의 저울(scale)은 매장 입구 근처에 따로 두는 것이라 스테이션 위치와는 관계없어요."를 덧붙였습니다. 이 문장을 인용하는 evidence_quote는 없어서 인용은 그대로입니다.
- 이 세트는 QA 단계에서도 지문을 고쳤으므로(last winter), 사람 원어민이 세트 전체를 다시 읽어야 합니다.

---

## 3. 문항별 판정

### 3.1 Part 5

| ID | 판정 | 근거 문장 / 메모 |
|---|---|---|
| RC-P5-000041 | 통과 | "received enthusiastic comments from guests" 자연스러운 결합 |
| RC-P5-000042 | 통과 | "Every member of ~ must show a photo ID". membership은 주어로 의미가 맞지 않음 |
| RC-P5-000043 | 통과 | "Since it opened in 2019, ~ has welcomed more than two million visitors" |
| RC-P5-000044 | 통과 | "will be conducted by an outside firm next Tuesday" |
| RC-P5-000045 | 통과 | because + 절. "due to + 절"은 원어민도 비격식으로만 가끔 써서 정답 경쟁이 되지 않음 |
| RC-P5-000046 | 통과 | "most of whom have experience in airport design" |
| RC-P5-000047 | 통과 | "accommodate up to 400 guests" 고빈도 연어 |
| RC-P5-000048 | 사람 원어민 확인 필요 (낮음) | "fully compatible with ~ so no additional setup is required". compatible이 강한 연어라 정답은 분명함. comparable은 결과절 so로만 배제되므로 QA 지정대로 확인 |
| RC-P5-000049 | 통과 | "much larger than the old one" |
| RC-P5-000050 | 통과 | "Each of the training rooms ~ has" |
| RC-P5-000051 | 통과 | "closed on Sundays and national holidays". 미국식으로는 holidays, federal holidays도 흔하지만 고칠 정도 아님 |
| RC-P5-000052 | 통과 | "keep your receipt after paying" |
| RC-P5-000053 | 통과 | "Further information"만 불가산 명사와 결합 |
| RC-P5-000054 | 통과 | "Employees wishing to attend" |
| RC-P5-000055 | 사람 원어민 확인 필요 (낮음) | "whether they work full-time or part-time" 정답 분명. "either they work ~ or ~"를 구어로 받아들이는 원어민이 있는지만 확인 |
| RC-P5-000056 | 사람 원어민 확인 필요 (낮음) | "go through the customer feedback forms" 자연스러움. v2 오답 turn down은 확실히 틀림. put off는 '미루다'라 summarize와 이어지지 않음. QA 지정 항목 |
| RC-P5-000057 | 통과 | "Should you need further assistance" 도치 자연스러움 |
| RC-P5-000058 | 통과 | 혼합 가정법 "would be managing ~ now" |
| RC-P5-000059 | 사람 원어민 확인 필요 (낮음) | "Now that ~ is finished, ~ can finally display". Even if는 finally와 논리가 맞지 않음. QA 지정 항목 |
| RC-P5-000060 | 사람 원어민 확인 필요 (보통) | "at the discretion of the front desk manager" 고정 표현. v2 오답 opinion은 확실히 비문. 다만 "at the approval of", "at the permission of"는 드물지만 실제 문서에서 아주 없지는 않아 원어민 판단 필요 |

### 3.2 Part 6 (RC-P6-S-0005)

| ID | 판정 | 근거 문장 / 메모 |
|---|---|---|
| RC-P6-000017 | 통과 | "The same desk is reserved for you every day" |
| RC-P6-000018 | 통과 | "They come furnished with desks, chairs, and a large whiteboard" |
| RC-P6-000019 | 통과 | "Each is equipped with a video screen and can seat up to ten people". B는 "open ~ every day of the year"와 충돌 |
| RC-P6-000020 | 사람 원어민 확인 필요 (낮음) | "By contrast, annual plans cannot be canceled ~". Similarly·As a result는 논리상 불가. QA 지정 항목 |

- 지문 메모: "Our private offices hold teams of two to six people."의 hold는 accommodate보다 가볍지만 자연스럽습니다. 수정하지 않았습니다.

### 3.3 Part 7

| ID | 판정 | 근거 문장 / 메모 |
|---|---|---|
| RC-P7-000023 | 통과 | "my train is stopped just outside Linwood Station" 자연스러운 구어 |
| RC-P7-000024 | 통과 | "No problem. I have all the slides on my laptop." 의도가 하나로 정해짐 |
| RC-P7-000025 | 통과 | "I'll handle the new product samples when I get there." |
| RC-P7-000026 | 통과 | 청구서 표기 자연스러움 (120 + 85 = 205) |
| RC-P7-000027 | 통과 | "Bill to: ~ Facilities Office / Attention: Ravi Castellanos" |
| RC-P7-000028 | 통과 | "every week instead of every other week". "Your new monthly rate"는 회당 청구 방식과 조금 어긋나지만 정답에 영향 없음 (참고) |
| RC-P7-000029 | 통과 | 공지 제목·본문 자연스러움 |
| RC-P7-000030 | 통과 | "Laptops must be used inside the building" |
| RC-P7-000031 | 통과 | "can be booked by groups of two to six people" |
| RC-P7-000032 | 통과 | booked = reserved |
| RC-P7-000033 | 통과 | "come back for all the containers afterward" |
| RC-P7-000034 | 통과 | "10 percent off their first order" |
| RC-P7-000035 | 통과 | "This offer applies to orders of any size." |
| RC-P7-000036 | 사람 원어민 확인 필요 (낮음) | "I haven't opened them"은 '확인 못 했다'로 자연스럽게 읽힘. QA 지정 항목 |
| RC-P7-000037 | 통과 | "I'm going down there ~ I'll have a look." |
| RC-P7-000038 | 수정 후 통과 | 같은 세트 이메일 수정(2.1). 정답 근거 "Would it be possible to move my registration ~"는 그대로 |
| RC-P7-000039 | 수정 후 통과 | 같은 세트 이메일 수정(2.1). 정답 영향 없음 |
| RC-P7-000040 | 수정 후 통과 (v2) | 2.1 참고. "the Tuesday workshop" → "the March 9 workshop" |
| RC-P7-000041 | 사람 원어민 확인 필요 (낮음) | "I need to be there to receive it" = accept. welcome은 배송품에 쓰지 않음. QA 지정 항목 |
| RC-P7-000042 | 수정 후 통과 | 같은 세트 이메일 수정(2.1). 정답 근거 "All workshops are held at 15 Quarry Lane, Room 204."는 그대로 |
| RC-P7-000043 | 통과 | "To address this" = deal with |
| RC-P7-000044 | 사람 원어민 확인 필요 (보통) | 지문 수정 세트. "began testing refill stations last winter ~ during the six-month trial"이 8월 12일 기사로 자연스러운지 (AI 판단으로는 자연스러움) |
| RC-P7-000045 | 사람 원어민 확인 필요 (보통) | 정답 분명. 지문 수정 세트이고 보기 C "last winter's trial"도 바뀐 표현 |
| RC-P7-000046 | 사람 원어민 확인 필요 (보통) | "who transferred to our store from Ostley this summer" 자연스러움. 지문 수정 세트 |
| RC-P7-000047 | 수정 후 통과 (v2) | 2.2 참고. 사람 원어민이 세트와 함께 재확인 권장 |
| RC-P7-000048 | 사람 원어민 확인 필요 (낮음) | "Each additional employee beyond the package limit: $35"로 A 배제. QA 지정 항목 |
| RC-P7-000049 | 통과 | "Locations more than 30 miles from our Halverton studio are charged a $75 travel fee."는 조금 딱딱하지만('A $75 travel fee applies to ~'가 더 매끄러움) 고칠 정도 아님 |
| RC-P7-000050 | 사람 원어민 확인 필요 (보통) | 청구서 "Scheduling fee"를 웹페이지의 14일 규정 $100으로 연결하는 것이 원어민에게 자연스러운지. 실제 업계에서는 "Late booking fee"나 "Rush fee"가 더 흔함 |
| RC-P7-000051 | 통과 | "so that no one is kept waiting" |
| RC-P7-000052 | 사람 원어민 확인 필요 (낮음) | v2 질문 "included in the package that Caldwell & Rook was billed for"는 자연스러움. 단체 사진 제외로 읽히는지 QA 지정 항목 |

---

## 4. 사람 원어민 검수자가 먼저 볼 목록

우선순위 순입니다. 1~4는 판단이 실제로 갈릴 수 있는 것, 5 이후는 확인만 하면 되는 것입니다.

1. **RC-P7-D-0003 세트 전체 (043~047)**: 지문이 두 번 바뀌었습니다 (QA: last spring → last winter, AI 사전 검수: 저울 문장). "began testing refill stations last winter ~ six-month trial"(8월 12일 기사)과 "Each participating store will also have a scale near its entrance"가 자연스러운지, 047(2번 통로)이 하나로 풀리는지.
2. **RC-P7-000050**: "Scheduling fee"가 14일 전보다 늦은 예약 수수료로 읽히는지. 아니라면 "Late booking fee"로 바꾸면 정답이 너무 쉬워지는지도 함께 판단.
3. **RC-P5-000060**: "at the approval of", "at the permission of"를 원어민이 비문으로 느끼는지.
4. **RC-P7-D-0002 이메일 (040)**: 바꾼 "please cancel my registration for the March 9 workshop"이 자연스러운지, 040이 $20 하나로 풀리는지.
5. RC-P5-000048 (comparable with ~, so no additional setup is required)
6. RC-P5-000055 (either they work full-time or part-time)
7. RC-P5-000056 (put off, come across)
8. RC-P5-000059 (Even if)
9. RC-P6-000020 (Similarly, As a result)
10. RC-P7-000041 (welcome vs accept), RC-P7-000036, RC-P7-000048, RC-P7-000052
