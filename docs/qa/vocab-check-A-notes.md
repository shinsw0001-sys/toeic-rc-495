# 배치고사 A폼 어휘 체크 메모 (S2-08)

- 작성: ai-writer-vocab-5 / 작성일: 2026-10-13 / 상태: draft
- 대상 파일: `content/forms/placement_A.json`의 `vocab_check`(20문항), `content/vocab/l450_batch1.json`(신규 450 카드 10개, VC-5-0001~0010)
- 기준: `docs/specs/placement-and-vocab.md` v0.2 1.4·3.2, `docs/qa/vocab-standard.md` 7장(V1~V12)
- 빌드: `python3 -B db/build_db.py` 오류 0

## 1. 설계

- 구성: 레벨 4개 × 5문항. 순서는 쉬운 레벨부터 기초(1~5) → 400(6~10) → 450(11~15) → 495(16~20). 판정이 "아래부터 연속 통과"라 이 순서가 채점 흐름과 같다.
- 형식: 짧은 비즈니스 구(2~6단어) 속 **굵은 표제어**의 한국어 뜻 고르기 A~D. ⑤ "모르겠어요"는 UI 고정 보기(오답 처리)라 파일에 넣지 않았다(빌드는 보기 A~D만 허용).
- 정답 위치: A·B·C·D 각 5개 (V10 35% 이하 충족). 레벨 안에서도 한 위치에 몰리지 않게 섞었다.
- 품사(V11): 기초 n2·v1·adj1·adv1 / 400 v2·adj1·n1·adv1 / 450 adj1·n1·v2·adv1 / 495 adj2·v2·n1. 한 품사 4개 이상 없음.
- 오답 보기(V5·V6): 정답과 같은 품사인 기존 카드의 대표 뜻에서 골랐다. 동의어·paraphrase 뜻·같은 어족·상위/하위어·반대말 한 쌍은 뺐다. 예: tentative에 "임시의"(temporary), mandatory에 "선택적인"(optional, 반대말), rectify에 "처리하다"(상위어), deposit의 "보증금"을 warranty 문항에 쓰지 않음("보증" 겹침).
- 구(V2·V3): 카드 예문을 그대로 쓰지 않았고, 가능하면 다른 보기를 넣어도 말이 되는 구로 만들었다(예: "**expedite** the approval process" → outline/oversee/restrict도 자연스러움).
- 단어 선택: 기초·400은 cross_reviewed 카드만 사용. VC-4-0231~0244(검수 중)는 쓰지 않았고, inspect·inspection은 둘 다 넣지 않았다. 표제어 20개 모두 서로 다름.

| seq | 레벨 | 단어 (word_id) | 정답 |
|---|---|---|---|
| 1 | 기초 | deadline (VC-B-0034) | B 마감일 |
| 2 | 기초 | hire (VC-B-0078) | D 고용하다 |
| 3 | 기초 | convenient (VC-B-0114) | A 편리한 |
| 4 | 기초 | carefully (VC-B-0144) | C 주의 깊게 |
| 5 | 기초 | refund (VC-B-0011) | A 환불 |
| 6 | 400 | relocate (VC-4-0179) | C 이전하다 |
| 7 | 400 | mandatory (VC-4-0196) | B 의무적인 |
| 8 | 400 | warranty (VC-4-0154) | D 품질 보증 |
| 9 | 400 | promptly (VC-4-0223) | A 신속하게 |
| 10 | 400 | secure (VC-4-0188) | B 확보하다 |
| 11 | 450 | tentative (VC-5-0010) | D 잠정적인 |
| 12 | 450 | discrepancy (VC-5-0005) | C 불일치 |
| 13 | 450 | comply (VC-5-0003) | A 준수하다 |
| 14 | 450 | expedite (VC-5-0006) | B 신속히 처리하다 |
| 15 | 450 | accordingly (VC-5-0001) | D 그에 맞게 |
| 16 | 495* | contingent (VC-5-0004) | C 조건부인 |
| 17 | 495* | commensurate (VC-5-0002) | A 상응하는 |
| 18 | 495* | rectify (VC-5-0008) | D 바로잡다 |
| 19 | 495* | stipulate (VC-5-0009) | B 규정하다 |
| 20 | 495* | provision (VC-5-0007) | C 조항 |

## 2. 495 대리(proxy)

- 495 카드가 없고 카드 `level`은 기초/400/450만 허용된다(빌드 CARD_RE, vocab-standard VR04). 그래서 495 구간은 **450 카드 중 더 어려운 단어 5개**로 채웠다.
- 문항 `level`은 `"495"`로 표시했다. 명세 1.3 표와 3.3 필드가 어휘 체크 레벨로 495를 두고 있고, 빌드는 문항 `level` 값을 검사하지 않는다. 카드 자체는 450이며, 폼 파일 `vocab_check_note`와 카드 `selection_note`에 대리 사용을 적었다.
- 고른 기준: 미세한 의미 차이·고난도 콜로케이션(명세 3.2의 495 성격). commensurate with, contingent on, stipulate, rectify, (계약) provision.
- 495 카드가 만들어지면 16~20번을 495 카드로 바꾸고, 이 5개 카드는 450 학습 카드로 그대로 둔다.
- 오답 보기 레벨: 495 문항의 오답은 400 카드 뜻(카드 기준 한 단계 아래)이다. 450 카드 10개가 모두 이 폼 정답이라 450 뜻을 오답으로 쓰면 다른 문항 정답을 알려 주게 되어 피했다.

## 3. 다시 볼 항목

1. **V1 미충족**: 450·495 문항 10개의 카드는 `draft`. V1은 published 카드만 쓰라고 한다. 교차 검수·원어민 확인 뒤 공개 전까지 이 폼은 출시 불가.
2. **기초·400 카드도 아직 cross_reviewed**: published 아님. 같은 이유로 공개 시점 확인 필요.
3. **discrepant (VC-5-0005 파생어)**: 사전에 있으나 드문 형태. 사전 2종 확인 필요, 아니면 빼고 `no_word_family`로 바꿀 것.
4. **provision (VC-5-0007)**: provide·provisional은 뜻이 크게 달라(4.2-6) 파생어로 넣지 않고 `no_word_family: true` + paraphrase "clause"로 두었다. CoS 규칙("어족 없는 핵심어")에 맞는 해석인지 확인 필요.
5. **accordingly (VC-5-0001) 파생어 accordance**: 같은 어족(accord)이지만 품사 빈칸 퀴즈에 쓸 만한지 확인. "따라서, 그러므로" 뜻은 카드에 넣지 않았다(다의어 분리 대상).
6. **17번 commensurate**: 오답 "상당한"이 "상응하는"과 한글 모양이 비슷하다. 의도한 함정이지만 파일럿 정답률이 지나치게 낮으면 교체.
7. **16번 contingent**: "조건부인"은 형용사 어미 경고(VR20) 대상일 수 있다. 뜻은 정확.
8. **1번 deadline**: "a tight budget"도 자연스러운 조합이라 "예산"이 강한 오답이다. 뜻을 묻는 문항이라 정답은 하나.
9. **오답 뜻 반복**: "따로"(9·15번), "감독하다"(6·14번), "협상하다"(13·19번)가 두 번씩 나온다. 정답 노출은 아니지만 B폼 설계 때 줄일 것.
10. **블라인드 재풀이**: 작성자가 정답을 가리고 20문항을 다시 풀어 모두 일치. 규칙상 교차 검수자·원어민(또는 동급)의 블라인드 풀이와 qa-tester 전수 재풀이가 남아 있다.

---

## 450 카드 10장 교차 검수

- 검수: qa-tester 역할 (`ai-qa-vocab-5b`, 작성자 `ai-writer-vocab-5`와 다른 교차 검수자) / 검수일: 2026-10-13
- 대상: `content/vocab/l450_batch1.json` VC-5-0001~0010
- 기준: vocab-standard 11장 체크리스트 A~G, 13장 VR01~VR33, 7장 V1~V12(폼 정답 일치), SCHEMA 파생어 규칙(no_word_family, deriv_stem)
- 결과: **10장 모두 통과 → `cross_reviewed`** (보류 0). `reviewer_1_id: ai-qa-vocab-5b`, `native_check_id`는 비워 둠. 내용을 고친 4장은 `version: 2`, 나머지 6장은 `version: 1`
- 빌드: `python3 -B db/build_db.py` → **OK** (어휘 카드 393개, 오류 0건, VC-5 경고 없음)

### 1. 카드별 결과

| ID | 표제어 | 수정 내용 | 판정 |
|---|---|---|---|
| 0001 | accordingly (adv) | 수정 없음. 파생어 accordance 유지(아래 2-3) | 통과 |
| 0002 | commensurate (adj) | 콜 "a salary commensurate with"(끝이 잘린 구) → "a salary commensurate with qualifications". 파생 commensurately 실존 확인 | 통과 |
| 0003 | comply (v) | 수정 없음. deriv_stem "tested for ------- with"는 전치사 뒤 명사 자리라 compliance만 가능(comply·compliant 불가), 3형이라 Q2 대상 | 통과 |
| 0004 | contingent (adj) | 수정 없음. 뜻 표현 유지(아래 2-4). 파생 contingency 유지: 계약의 "조건(contingency clause)" 뜻으로 같은 의미 축 | 통과 |
| 0005 | discrepancy (n) | 파생어 discrepant 삭제 → `derivatives: []`, `no_word_family: true` (아래 2-1). confusables(discretion)·paraphrases 2개 있음 | 통과 |
| 0006 | expedite (v) | 수정 없음. expeditious·expeditiously 실존·같은 뜻 축 확인. deriv_stem "handling the request so -------"는 부사 자리라 expeditiously만 가능 | 통과 |
| 0007 | provision (n) | 수정 없음. `no_word_family: true` 확인(아래 2-2) | 통과 |
| 0008 | rectify (v) | 수정 없음 | 통과 |
| 0009 | stipulate (v) | 예문 교체: "...must be paid within thirty days"가 VC-B 카드(basic_batch1, Marlow Office Supplies 예문)와 5-gram 2개 겹침(VR23) → "Our contract with Quellmont Cleaning stipulates that the lobby windows must be washed twice a month." | 통과 |
| 0010 | tentative (adj) | 예문 고유명사 Kessler → Dornvale (Kessler는 실존 기업명 다수) | 통과 |

### 2. 작성자 질문에 대한 판정

1. **discrepant**: Merriam-Webster 등 일반 사전에는 형용사로 있으나 학습자 사전(Oxford Learner's)에는 discrepancy만 있고 discrepant는 없다. 실제 쓰임도 통계·과학 문서("discrepant results")에 치우친 희귀어라 4.2-1 "희귀어는 쓰지 않는다"에 해당. 400 검수의 enrollee·banqueting 처리와 같게 삭제하고 `no_word_family: true`로 바꿈. 기존 confusable discretion, paraphrases inconsistency·mismatch로 SCHEMA 조건 충족.
2. **provision `no_word_family: true`**: 확인. provide와 어원은 같지만 "조항" 뜻에서는 연결이 끊기고, provisional(임시의)은 뜻이 크게 달라 4.2-6에 해당. paraphrase clause로 조건 충족. 참고: 기초 카드 VC-B-0083 provide는 파생어로 provision을 두는데, 이는 "제공" 뜻이라 이 카드(조항)와 충돌하지 않음. 다만 Q2 생성 시 provide 카드 보기의 provision을 이 카드 뜻으로 해설하지 않도록 developer에 공유 필요.
3. **accordingly → accordance**: 같은 어족(accord)이고 "~에 맞춤, 일치"라는 같은 뜻 축(in accordance with = ~에 따라)이라 허용. 형태가 2개뿐이라 Q2 대상은 아니며 결함 아님. "따라서, 그러므로" 뜻은 카드에 넣지 않은 작성자 판단 유지(다의어 분리, 필요하면 별도 카드).
4. **contingent "조건부인"**: "조건부(條件附)+인"으로 맞는 형용사형이며 VR20 어미 규칙("인")도 통과(빌드 경고 없음). "~에 달려 있는"과 함께 써서 contingent on 구조의 뜻이 분명하다. 폼 16번 정답 "조건부인"과 일치하므로 유지.

### 3. 공통 점검

- **뜻·품사**: 10장 모두 meaning_ko·예문·콜로케이션 품사 일치, type_tags VOC 소분류도 품사와 맞음.
- **콜로케이션**: 31개 모두 표제어 포함, 전치사 패턴(comply with, commensurate with, contingent on/upon, a discrepancy between/in) 정확.
- **레벨**: 10장 모두 450 타당(450-①②③: 전치사 패턴·형식어·Part 7 패러프레이즈). commensurate·contingent·stipulate·rectify·provision은 체감상 그 이상이지만 카드 레벨 상한이 450이라 450 유지, 폼의 495 대리 사용은 메모 2절대로.
- **독창성**: 예문 10개와 deriv_stem 2개를 따옴표 웹 검색 — 일치 없음. 고유명사(Ferrin Bay, Pendrick Logistics, Corlett Printing, Brightwell Hotel, Marlow Street, Quellmont Cleaning, Dornvale) 검색, Kessler만 실존 기업과 겹쳐 교체. 수정 후 content/items/**, 다른 카드(기초·400·450), 폼 파일 전체와 5-gram 겹침 0건.
- **중복**: 다른 카드와 (lemma, pos) 중복 없음.
- `originality_check`: 통과, 2026-10-13, 방법 "AI 교차 검수(ai-qa-vocab-5b): 예문·deriv_stem 따옴표 웹 검색 일치 없음, 실존 가능 고유명사 교체, 카드·문항·폼 5-gram 대조"를 10장에 기록.

### 4. 폼(placement_A 11~20번)과의 일치

- 10장의 meaning_ko는 이번 검수에서 바꾸지 않았고, 각 문항 정답과 일치한다(V4): 11 잠정적인, 12 불일치, 13 준수하다, 14 신속히 처리하다, 15 그에 맞게, 16 조건부인, 17 상응하는, 18 바로잡다, 19 규정하다, 20 조항. **불일치 0건, 폼 수정 없음.**
- 교차 검수자 블라인드 풀이: 11~20번 정답을 가리고 풀어 10문항 모두 파일 정답과 일치. 오답 보기에 정답 카드의 paraphrase·파생어 뜻 없음(V6). 바뀐 예문(0009·0010)은 폼 구와 겹치지 않음(V2).
- 남은 V1 문제: 카드가 `cross_reviewed`가 되었을 뿐 published가 아니므로, 메모 3절 1번대로 원어민 확인·공개 전까지 폼 출시 불가는 그대로.

### 5. 남은 일

- 원어민 확인: 새 예문 0009(stipulate), 0010 고유명사 교체, expeditiously·compliance stem의 자연스러움.
- discrepancy 카드 변경(파생어 삭제)에 맞춰 이 카드가 들어간 퀴즈가 있으면 재생성(8.3-3). 현재 Q2 대상 아님.

### 판정

**조건부 가능.** 10장 모두 교차 검수 통과(치명·높음 없음). 조건: 원어민(또는 MVP 예외의 영어 전문가) 확인 후 published 전환 전까지 placement_A 어휘 체크 450·495 구간은 출시 불가(V1).
