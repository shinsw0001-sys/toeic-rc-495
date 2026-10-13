# 배치고사 A폼 교차 검수 결과: Part 5·6 (S2-09)

- 검수자: ai-qa-pl-p56 (qa-tester 역할, 작성자 ai-writer와 다른 검수자)
- 검수일: 2026-10-13
- 대상: `content/items/p5/p5_placementA.json` (RC-P5-000041~060, 20문항), `content/items/p6/p6_placementA.json` (세트 RC-P6-S-0005, RC-P6-000017~020, 4문항)
- 기준: `docs/qa/content-standard.md` 3장(정답 유일성·오답), 5장(난이도), 6장(해설), 7장(지문), 8장(저작권), 10장(체크리스트), `content/SCHEMA.md`, 폼 구성 `content/forms/placement_A.json`

---

## 1. 결론

**판정: 조건부 가능.** 24문항 모두 `cross_reviewed`로 올렸습니다. 공개(published)는 원어민 검수 뒤에 할 수 있습니다.

| 구분 | 문항 수 | 내용 |
|---|---|---|
| 그대로 통과 | 22 | 정답 일치, 결함 없음 또는 '낮음'만 있음 |
| 수정 후 통과 (version 2) | 2 | RC-P5-000056, RC-P5-000060 |
| 보류 (draft 유지) | 0 | 없음 |
| 합계 | 24 | 모두 `status: cross_reviewed`, `reviewer_1_id: ai-qa-pl-p56` |

- 블라인드 풀이: 정답 키를 보기 전에 24문항을 모두 풀었고, 24문항 모두 키와 일치했습니다.
- 다른 보기도 답이 될 수 있는 문항(3.1-2 위반 위험): 2건(P5-056, P5-060). 둘 다 오답 보기 1개를 바꿔 해결했고, 정답 글자는 그대로 뒀습니다.
- 난이도는 바꾸지 않았습니다. stage1 난이도 구성 d2×3, d3×6, d4×3이 그대로 유지됩니다.
- 정답 위치 분포는 모듈마다 고르게 유지됩니다(4장).
- `reviewer_2_id`, `native_check_id`는 빈 값으로 두었습니다(원어민 검수 대기).
- 검증: `python3 -B db/build_db.py` 결과, 검증 실패 11건은 모두 `content/vocab`의 어휘 카드 중복("같은 표제어·품사 카드 중복")입니다. 이 파일들은 다른 담당자가 고치는 중입니다. 이번 검수 대상 문항이나 세트와 관련된 오류는 0건입니다.

---

## 2. 문항별 판정 표

난이도는 '작성자 / 검수자 독립 평가'입니다. 차이가 1이면 5.1 규칙(평균 반올림)을 따랐습니다.

### 2.1 Part 5

| item_id | 모듈 | 블라인드 답 | 정답 키 | 판정 | 난이도 | 메모 |
|---|---|---|---|---|---|---|
| RC-P5-000041 | stage1 | A | A | 통과 | 2/2 | |
| RC-P5-000042 | stage1 | C | C | 통과 | 3/3 | 작성자 불확실 표시 → 5장 판정 참고 |
| RC-P5-000043 | stage1 | B | B | 통과 | 3/2 | 작성자 불확실 표시. 평균 2.5를 반올림하면 3이라 그대로 뒀습니다(5장) |
| RC-P5-000044 | stage1 | D | D | 통과 | 3/3 | |
| RC-P5-000045 | stage1 | C | C | 통과 | 2/2 | |
| RC-P5-000046 | stage1 | A | A | 통과 | 4/4 | (B) 함정 코드 VERB_PATTERN은 '격 혼동'에 더 가깝습니다(낮음) |
| RC-P5-000047 | stage1 | D | D | 통과 | 3/3 | (B) occur는 버리는 보기에 가깝지만, 대상 트랙에 300-400이 있어 허용 범위입니다 |
| RC-P5-000048 | stage1 | B | B | 통과 | 4/4 | 작성자 불확실 표시 → 5장 판정 참고 |
| RC-P5-000049 | basic | B | B | 통과 | 1/1 | |
| RC-P5-000050 | basic | D | D | 통과 | 2/2 | |
| RC-P5-000051 | basic | A | A | 통과 | 1/1 | |
| RC-P5-000052 | basic | C | C | 통과 | 2/2 | |
| RC-P5-000053 | mid | D | D | 통과 | 3/3 | |
| RC-P5-000054 | mid | A | A | 통과 | 3/3 | |
| RC-P5-000055 | mid | B | B | 통과 | 3/3 | (A) 함정 코드 PREP_CONJ_CONFUSION은 다소 느슨합니다(낮음) |
| RC-P5-000056 | mid | C | C | **수정** | 3/3 | (B) take over를 **turn down**으로 바꿨습니다. "asked the interns to take over the customer feedback forms and summarize ~"는 '의견서 처리 업무를 넘겨받아 요약하라'로 읽힐 수 있어 원어민이 답으로 받아들일 수 있습니다(3.1-2 위반 위험, 결함 등급: 높음). turn down(거절하다)은 의견서와 의미가 맞지 않아 확실히 틀립니다. 해설, 오답 이유, key_point를 함께 고쳤습니다 |
| RC-P5-000057 | upper | C | C | 통과 | 4/4 | |
| RC-P5-000058 | upper | A | A | 통과 | 5/5 | |
| RC-P5-000059 | upper | D | D | 통과 | 4/4 | 작성자 불확실 표시 → 5장 판정 참고 |
| RC-P5-000060 | upper | B | B | **수정** | 4/4 | 작성자 불확실 표시. (D) judgment를 **opinion**으로 바꿨습니다(5장). 해설, 오답 이유, key_point를 함께 고쳤습니다 |

### 2.2 Part 6 (RC-P6-S-0005, web_page, stage1)

| item_id | 블라인드 답 | 정답 키 | 판정 | 난이도 | 메모 |
|---|---|---|---|---|---|
| RC-P6-000017 | B | B | 통과 | 3/3 | 근거 문장(Flex Desk "Use any open desk")이 빈칸 문장 밖에 있어 3.1-4를 지킵니다 |
| RC-P6-000018 | D | D | 통과 | 2/1 | 작성자 불확실 표시. 평균 1.5를 반올림하면 2라서 그대로 뒀습니다(5장) |
| RC-P6-000019 | C | C | 통과 | 4/4 | 오답 3개 모두 지문과 확실히 충돌합니다: (A) 회의실 단락에 책상 없음, (B) "every day of the year"와 충돌, (D) 요금제가 아닌 회의실 단락 |
| RC-P6-000020 | A | A | 통과 | 3/3 | |

지문 점검(F 항목):
- 단어 수: 177단어로 100~180 범위 안입니다(상한에 가까움).
- 회사·지명은 가상(Quarrington Workspace, Dunleigh, Brackmoor Avenue), URL `quarringtonworkspace.example.com`, 전화 `555-0148`로 규칙을 지킵니다.
- 날짜·요일 표기가 없어 요일 검산은 해당 없습니다. 금액·시간은 서로 모순이 없습니다.
- 금지 주제가 없습니다.

### 2.3 공통 점검 결과

- 해설 분량: P5는 169~294자로 150~350자 기준 안입니다. P6는 324~390자로 200~400자 기준 안입니다.
- 해요체 통일, 금지 표현 없음, 해설의 정답과 `answer` 필드가 모두 일치합니다.
- `distractor_rationale`, `trap_code`가 보기 4개 모두에 있고 정답의 trap_code는 null입니다.
- P6 `evidence_quote`는 모두 지문 원문과 글자 그대로 같고, 빈칸 표기가 들어 있지 않습니다.
- 유형 태그는 문항이 실제로 묻는 것과 맞습니다.

### 2.4 등급 '낮음·보통' 지적 (수정하지 않고 기록만 함)

| 항목 | 내용 | 등급 |
|---|---|---|
| 함정 코드 | P5-046 (B)·(D), P5-055 (A)의 코드가 오답 이유와 정확히 맞지 않습니다 | 낮음 |
| P6 지문 번역 | Batch 1과 같이 '지문 전체 번역 1회'를 넣을 필드가 아직 없습니다 | 보통 (기존 열린 이슈) |
| 지명 겹침 | Yarrowfield가 P5-044(공장)와 P5-051(도서관)에 함께 나옵니다. 같은 폼 안이라 이름이 겹치지만 문제 풀이에는 영향이 없습니다 | 낮음 |
| 실재 도로명 | P5-049 "Mill Road"는 흔한 도로명으로 실재 지명과 겹칩니다. 특정 업체를 가리키지 않아 그대로 뒀습니다 | 낮음 |

---

## 3. 저작권 점검 결과 (8.3 2단계)

- 방법: WebSearch로 특징 구절(대부분 문제 문장 전체 또는 7단어 이상)을 큰따옴표로 묶어 검색했습니다.
  - P5: 20문항 전체에서 22건 (P5-048은 2건, P5-060은 '재량' 오답 확인용 포함 3건)
  - P6: 세트 S-0005에서 3건 (Fixed Desk 문장, 회의실 삽입 문장, 해지 규정 문장)
  - 가상 회사명 확인: 2건 (9개 회사·시설명 묶음 검색)
- 결과: **같은 문장이 나온 경우는 없었습니다.** 결과 목록에 ETS 문항 페이지나 국내 경쟁사(해커스, YBM, 산타, 영단기) 도메인은 나오지 않았습니다.
- 시험 대비 사이트가 걸린 경우는 1건이었고, WebFetch로 직접 열어 대조했습니다.

| 검색 구절 (문항) | 걸린 페이지 | 대조 결과 |
|---|---|---|
| P5-052 "Please keep your receipt after paying, because it is required for all returns and exchanges" | bestmytest.com (TOEIC 어휘 e북, 반품·교환 단원) | 같은 문장은 없습니다. 페이지 문장은 "Keep your receipt in case you need to return the product." 등입니다. '영수증 보관'이라는 일반 소재만 같습니다. 통과 |

- 가상 회사명: Quarrington Workspace, Brightholm Lodge, Pexley Engineering, Skelbrook Paper, Kellridge Museum, Ferrisgate Plaza, Benlowe Fitness, Drensby Catering, Orvelle Hotel을 검색했고, 같은 이름의 실존 업체는 결과에 나오지 않았습니다.
- **한계**: Batch 1과 같이 이번 WebSearch도 결과의 제목과 URL만 주고 본문 스니펫은 주지 않았습니다. 유료 문제집 PDF와 한국어 교재 사이트는 검색으로 잡히지 않을 수 있습니다.
- 내부 유사도(8.3 3단계): 이번 빌드는 어휘 카드 중복 오류로 끝나서 `db/REPORT.md`의 근접 중복 결과를 새로 받지 못했습니다. 어휘 오류가 고쳐진 뒤 빌드를 다시 돌려 확인해야 합니다.
- 기록: 24문항 모두 `originality_check = {result: "통과", date: "2026-10-13", method: "AI 블라인드 풀이 + 웹 구절 검색 N건 (일치 없음, 검색 도구가 제목·URL만 제공)"}`으로 적었습니다.

---

## 4. 정답 위치 분포 (모듈별)

P7 문항(`p7_placementA.json`)은 이번 범위가 아니라 읽기만 했습니다. 정답 글자를 바꾼 문항은 없습니다.

| 모듈 | 문항 수 | A | B | C | D | 최대 비율 |
|---|---|---|---|---|---|---|
| stage1 (P5 8 + P6 4) | 12 | 3 | 3 | 3 | 3 | 25% |
| basic (P5 4 + P7 10) | 14 | 4 | 4 | 3 | 3 | 29% |
| mid (P5 4 + P7 10) | 14 | 4 | 3 | 4 | 3 | 29% |
| upper (P5 4 + P7 10) | 14 | 3 | 3 | 4 | 4 | 29% |

모든 모듈이 3.2-4 기준(한 위치 35% 이하)을 지킵니다.

---

## 5. 작성자가 불확실하다고 표시한 문항 판정

| 문항 | 판정 | 근거 |
|---|---|---|
| P5-048 compatible vs comparable | **통과 (수정 없음)** | comparable with는 문법적으로 맞지만, '비슷하다'는 사실은 'so no additional setup is required(그래서 추가 설정이 필요 없다)'의 이유가 되지 못합니다. so 결과절이 뜻을 하나로 정해 주므로 comparable은 확실히 틀립니다. 다만 의미로만 배제되므로 원어민 검수 목록에 넣었습니다. 난이도 4 적정 |
| P5-060 at the discretion of | **수정** | approval, permission은 at the ~ of와 결합하지 않고(with/subject to the approval of) 그대로 둡니다. judgment는 discretion과 사전적 의미가 겹치고(3.1-3 동의어 금지), "at the judgment of the instructor"처럼 실제 쓰이는 예도 있어 답으로 받아들여질 위험이 있었습니다. **opinion**으로 바꿨습니다. "at the opinion of"는 비문이고(in the opinion of), 함정 코드 COLLOCATION_MISMATCH가 그대로 맞습니다 |
| P5-042 member vs membership | **통과 (수정 없음)** | Every 뒤 단수라 (B)·(D)는 문법으로 빠집니다. membership(회원 자격)은 'must show a photo ID when entering'의 주어가 될 수 없어 확실히 틀립니다. 난이도 3 유지(두 단서 조합, 5.1의 3등급 예시와 일치) |
| P5-059 Now that vs Even if | **통과 (수정 없음)** | Even if는 양보라서 finally(마침내)와 결과 흐름이 맞지 않습니다. "Even if ~ is finished, the museum can finally display ~"는 원어민에게 논리가 깨진 문장입니다. 정답은 하나입니다 |
| P6-018 It/We/Them/They, d2 vs d1 | **통과, 난이도 2 유지** | 검수자 독립 평가는 1입니다. 평균 1.5를 반올림하면 2라서 그대로 뒀습니다. We는 버리는 보기에 가깝지만, 대상 트랙이 300-400뿐이라 3.2-3에서 허용합니다(문항당 1개). It(수 일치)과 Them(격)은 하위권 수강생에게 매력이 있습니다. 배치고사 stage1의 쉬운 기준 문항 역할에 맞습니다 |
| P5-043 d2 vs d3 | **난이도 3 유지** | 검수자 독립 평가는 2입니다(since + 현재완료는 기본 규칙). 평균 2.5를 반올림하면 3이라 기존 값을 유지했습니다(Batch 1 P5-038과 같은 처리). 그래서 stage1 구성 d2×3, d3×6, d4×3을 다시 맞출 필요가 없습니다. 파일럿 정답률이 70%를 넘으면 5.3 절차로 2로 내리고, 그때 다른 d2 문항 1개를 d3으로 올려 구성을 맞추는 것을 권합니다 |

---

## 6. 원어민 검수 필요 목록

24문항 모두 `native_check_id`가 비어 있습니다. 특히 아래 문항은 정답 유일성을 꼭 확인해 주세요.

| item_id | 확인할 점 |
|---|---|
| RC-P5-000056 (v2) | 새 오답 turn down이 확실히 틀리는지, put off·come across도 답으로 받아들여지지 않는지 |
| RC-P5-000060 (v2) | 새 오답 opinion과 approval이 at the ~ of에서 확실히 비문으로 느껴지는지 |
| RC-P5-000048 | "fully comparable with ~, so no additional setup is required"를 답으로 받아들이지 않는지 |
| RC-P5-000059 | Even if를 답으로 받아들이지 않는지 |
| RC-P5-000055 | either they work full-time or part-time이 확실히 비문인지 |
| RC-P6-000020 | By contrast 외에 Similarly·As a result를 받아들일 여지가 없는지 |

---

## 7. 출시 판정

**조건부 가능 (교차 검수 단계까지).** 배치고사 A폼 P5·P6 24문항은 정답, 해설, 메타데이터 기준으로 `cross_reviewed`에 올릴 수 있습니다.

`published`로 넘기려면 아래 조건이 모두 필요합니다.
1. 원어민 검수에서 정답 일치. 특히 6장 목록
2. 2차 검수자(`reviewer_2_id`) 지정
3. 어휘 카드 중복 오류가 고쳐진 뒤 `build_db.py`를 다시 돌려 내부 유사도 결과 확인
4. 스니펫을 주는 검색 환경이나 사람이 하는 수작업으로 독창성 검색 보완
