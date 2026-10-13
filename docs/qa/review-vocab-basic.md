# 기초 어휘 카드 교차 검수 — basic_batch1.json

- 검수: qa-tester (`ai-qa-vocab`, 교차 검수자 · 작성자 아님) / 보고 대상: chief-of-staff
- 검수일: 2026-10-13 / 기준: `docs/qa/vocab-standard.md` v0.1, `content/SCHEMA.md` 어휘 카드 형식·파생어 규칙
- 대상: `content/vocab/basic_batch1.json` (AI 초안 150카드, 작성자 `ai-writer-vocab-b`)

## 1. 결론

**조건부 통과.** 검수 후 파일은 150카드다.

| 구분 | 수 | 상태 |
|---|---|---|
| 통과 (수정 없음) | 95 | `cross_reviewed`, version 1 |
| 수정 후 통과 | 51 | `cross_reviewed`, version 2 |
| 보류 (새 카드, 다른 검수자 필요) | 4 | `draft` + `qa_note` |
| 삭제 | 4 | headquarters·launch·expand (400 소유, CoS 결정), inspect (400으로 레벨 조정) |

- 통과 카드 146장에 `reviewer_1_id: "ai-qa-vocab"`, `originality_check: 통과 / 2026-10-13 / AI 교차 검수, 예문 자체 작성 확인`, `native_check_id: ""`를 채웠다. **원어민 확인(10장 4단계)은 아직 남아 있다.**
- 치명 결함(없는 파생어, 다른 어족, 예문 복사, 실존 기업)은 **없었다**. 높음 결함 6건(예문의 뜻·품사가 카드와 다름, 콜로케이션이 다른 뜻·다른 품사)과 보통·낮음 결함은 모두 고쳤다.
- `python3 -B db/build_db.py` 결과: 오류 11건이 남았고, 모두 CoS가 기초에 남기기로 한 단어(agenda, annual, confirm, currently, immediately, responsible, supplier, reservation, purchase, previous, remind)의 400 파일 쪽 중복이다. 400 검수자가 그쪽 카드를 지우면 없어진다. 이 파일에서 생긴 다른 오류는 없다.
- 이번에 고친 예문은 다른 카드·문항과 5-gram 겹침을 다시 검사했고, 겹침이 0건이다.

## 2. 수정 목록 (version 2, 51장)

**높음 — 예문·콜로케이션의 뜻이나 품사가 카드와 다름**
| ID | 표제어 | 결함 → 조치 |
|---|---|---|
| VC-B-0049 | sale (n) | 예문이 보조 뜻 *sales*(매출)로 쓰여 대표 뜻(판매, 할인 판매)과 다름 → 할인 판매 예문으로 바꿈 |
| VC-B-0089 | introduce (v) | 예문은 "출시하다"인데 대표 뜻은 "소개하다" → 대표 뜻을 "도입하다, (신제품을) 출시하다"로 바꾸고 *introduce A to B*를 교체 |
| VC-B-0133 | public (adj) | 예문 *open to the public*은 명사 용법이라 품사가 다름 → 형용사 예문(*public transportation*)으로 바꾸고 명사 콜로케이션을 교체 |
| VC-B-0101 | increase (v) | 콜로케이션 *increase in*은 명사 용법 → *increase production*으로 교체. 어색한 예문(*increased its opening hours*)도 교체, 뜻은 3개에서 2개로 줄임 |
| VC-B-0098 | manage (v) | *manage to do*(간신히 해내다)는 다른 뜻 → *manage a project*로 교체 |
| VC-B-0070 | record (v) | *record sales*가 형용사 record(기록적인)로 읽힘 → *record expenses*로 교체, 보조 뜻 삭제 |

**보통 — 다의어 보조 뜻, 콜로케이션, 파생어**
- 보조 뜻이 다른 뜻(카드를 나눠야 하는 다의어)이어서 지움: application(응용 프로그램), stock(주식), appointment(임명), position(위치), unit(한 세대), deliver(연설을 하다), present(상을 주다, 해당 콜로케이션도 교체), arrange(정리하다), reach(연락이 닿다, *can be reached at*도 교체), apply(적용하다), return(돌아오다, *return a call*·*return to the office*도 교체), free(한가한), finally(마지막으로). 이 뜻이 필요하면 별도 카드로 만든다.
- 콜로케이션에 표제어(굴절형)가 없거나 조합이 아님: convenient(*conveniently located* → *a convenient time*), usually(*than usual* → *usually arrive*), include(*including* 한 단어 → *include shipping costs*), organize(*organize files*는 다른 뜻 → *organize a conference*).
- 파생어(SCHEMA 파생어 규칙, 기준 4.2): director → *direction* 삭제(뜻이 크게 다름), ready → *readily*를 *readiness*로(뜻이 다름), pleased → *pleasant*를 *pleasure*로(뜻이 다름), hire → *hiring* 삭제, update → *updated* 삭제(분사형 형용사가 사전 2종에 표제로 실렸는지 확인하기 어려움).
- 예문 겹침(9.4-2): request(P5 문항의 정답 *in advance*와 같은 구절이라 정답이 드러날 위험), construction(P5 문항 문장과 겹침), participant·position(400 카드 예문과 겹침), stock(P6 지문과 겹침), recent(P5 문항과 겹침), annual(VC-B-0015와 같은 문장 틀, E9) → 예문 7개를 새로 씀.
- E2 지명 가상: 실존 도시명 Riverside·Toronto·Boston·Seattle·Portland → Kensford·Halverton·Carvale·Norbridge·Westmoor (branch, client, book, attend, manage).
- VR06: *according to*, *instead of*는 공백이 있는 표제어라서 pos를 `prep`에서 `phr`로 바꿈. type_tags `P5-VOC.COLL`·`P5-CONN.PREP`는 그대로 둠.

**낮음 — 뜻 표기**
- 대표 뜻 3개 나열을 2개로 줄임(2-4): director, payment, location, item, policy, regular, organize, increase.
- 그 밖: shipment("발송(물)" 괄호 정리), salary("월급"은 범위가 좁음 → "봉급"), unit("(제품의) 한 개, 단위"), daily("일일" → "일일의"), reserve(20자 초과 → "예약하다, (자리를) 잡아 두다"), complete·document(번역을 meaning_ko와 맞추고 어색한 표현을 고침).

**지시 사항**
- VC-B-0008: lemma `résumé`를 `resume`으로 바꿈. meaning_ko는 "이력서(résumé)"로 적어 400 카드 resume(v) "재개하다"와 구별되게 함. 예문·콜로케이션 철자도 같이 바꿈. (lemma, pos) 키가 (resume, n)과 (resume, v)로 달라서 중복 오류는 나지 않는다.

## 3. 레벨 조정

| 조치 | 내용 |
|---|---|
| 삭제 (CoS 결정) | VC-B-0050 headquarters (n), VC-B-0096 launch (v), VC-B-0097 expand (v). 400 파일에 그대로 둔다. ID는 다시 쓰지 않는다. |
| 400으로 이동 | VC-B-0059 **inspect (v)**. 6.1 기초 기준 ①(중학~고1 일반어)에 맞지 않는다. 같은 어족 *inspection*이 이미 400에 있어 레벨이 갈라진다. 경계 규칙 B3에 따라 400으로 올린다. **400 담당자가 l400 파일에 inspect (v) 카드를 추가해야 한다**(지금은 어느 파일에도 없음). |
| 대체 추가 (`draft`) | VC-B-0151 visitor (n) 방문객 · VC-B-0152 invite (v) 초대하다 · VC-B-0153 price (n) 가격 → 중복 3장 대체 / VC-B-0154 prepare (v) 준비하다 → inspect 대체. 네 단어 모두 `content/vocab/` 어느 파일에도 없음을 확인했다. |
| 기초 유지 | agenda, annual, confirm, currently, immediately, responsible, supplier, reservation, purchase, previous, remind (CoS 결정). 400 검수자가 400 쪽 카드를 지운다. |

- 대체 카드 4장은 교차 검수자가 직접 썼으므로 작성자 ≠ 검수자 규칙(10장, VR26)에 따라 `draft`로 두었다(`author_id: ai-qa-vocab`, `qa_note`에 사유를 적음). **다른 검수자가 교차 검수를 해야 한다.**
- organize의 뜻을 "(행사를) 기획하다, 조직하다"로 바꿔 새 카드 prepare("준비하다")와 뜻이 겹치지 않게 했다. 겹치면 퀴즈 오답에 동의어가 들어갈 수 있다(V6).
- 참고: `selection_note`는 SCHEMA 예시 형식("선정 근거: … 복사 없음")을 따르고 있다. 기준 9.3의 세미콜론 형식(근거; 레벨 근거; 복사 없음)과는 다르다. "복사 없음"은 들어 있어 VR21을 통과하므로 결함으로 세지 않았다. **두 문서의 형식 통일은 콘텐츠 담당이 정해야 한다.**

## 4. 원어민 확인 우선 목록

10장 4단계에서 먼저 볼 카드다. 교차 검수자가 새로 쓰거나 크게 바꾼 문장과, 사전 표기를 확인하기 애매한 형태를 앞에 두었다.

1. **새 카드 4장**: VC-B-0151~0154. 예문·콜로케이션 전체를 확인한다. 특히 *sign in at the front desk*, *a visitor badge*, *at a low price*.
2. **새로 쓴 예문**: sale(0049), public(0133), increase(0101), request(0023), construction(0025), participant(0017), stock(0022), position(0045), recent(0116), annual(0118).
3. **바꾼 콜로케이션**: *record expenses*, *reach the office*, *present the results*, *return a product for a refund*, *include shipping costs*, *organize a conference*, *usually arrive*, *a convenient time*, *public parking*.
4. **분사형 형용사·드문 파생어의 실존 여부(사전 2종)**: discounted(0033), located(0043), scheduled(0001·0104), reduced(0102), preferred(0068), required(0084), expensively(0107), helpfully(0124), offering(0075), readiness(0121), increasingly(0101).
5. **자연스러움이 애매한 초안 표현**: *upgraded its Internet service*(0071), *assist in*(0094), *has recently been*(0137), *already been shipped*(0141), *work full-time*(0109), *a registered member*(0062), *The staff … were very helpful*(0124).
6. **뜻 경계**: complete(0063, "완료하다"와 "(양식을) 작성하다"를 한 카드에 둔 것이 다의어 분리 기준에 맞는지), introduce(0089, 대표 뜻을 바꿈), resume(0008).

## 5. 후속 조치

- 400 검수자: 위 11개 단어의 400 카드를 삭제하고, **inspect (v)를 400 카드로 추가**한다.
- 다른 교차 검수자: VC-B-0151~0154를 검수한 뒤 `cross_reviewed`로 올린다.
- 원어민(또는 MVP 예외 기준의 영어 전문가): 4장 목록부터 확인하고 `native_check_id`를 채운다.
- 웹 검색 기반 독창성 점검(9.4-1, 7단어 이상 구절)은 이번 검수에서 하지 않았다. 표본 20% 재검수 때 같이 한다.
