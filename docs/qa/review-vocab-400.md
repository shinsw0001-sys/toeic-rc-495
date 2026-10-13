# 어휘 카드 교차 검수 결과 — 400 레벨 (l400_a-l.json, l400_m-z.json)

- 검수: qa-tester 역할 (`ai-qa-vocab-400`, 교차 검수자이며 작성자 아님) / 보고 대상: chief-of-staff
- 검수일: 2026-10-13 / 기준: `docs/qa/vocab-standard.md` v0.1, `content/SCHEMA.md` 어휘 카드 형식(파생어 규칙, 검수 필드, `deriv_stem`)
- 대상: AI 초안 230장 (작성자 `ai-writer-vocab-4a` 115장, `ai-writer-vocab-4b` 115장)
- 빌드: `python3 -B db/build_db.py` → **OK** (어휘 카드 383개, 오류 0건)

---

## 1. 결론

**조건부 통과.** 남은 219장은 모두 `cross_reviewed`로 올렸고, 보류(draft)는 없습니다. 새로 만든 14장은 이 검수자가 직접 썼기 때문에 `self_reviewed`로 두었으며, 다른 사람의 교차 검수가 필요합니다.

| 구분 | 수 | 상태 |
|---|---|---|
| 원본 카드 | 230 | — |
| 삭제 (기초와 중복, CoS 결정) | 11 | 파일에서 제거, ID 재사용 금지 |
| 통과 (내용 수정 없음, `deriv_stem`·검수 필드만 추가) | 86 | cross_reviewed, version 2 (stem 추가) / 1 |
| 수정 후 통과 | 133 | cross_reviewed, version 2 |
| 보류 | 0 | — |
| 새 카드 (교체 11 + 다의어 분리 2 + inspect 1) | 14 | self_reviewed, version 1, `qa_note` 있음 |
| **최종 400 카드** | **233** | l400_a-l.json 110장, l400_m-z.json 123장 |

주요 결함 유형:
1. **가짜 파생어 (치명 4.2)**: 복수형(agendas, inventories, amenities 등 9건), 같은 형태 반복(attire, feedback, overview), 구동사 분해(run out, come up), 억지 연관어(ensure→sure, voucher→vouch, carry out→carrier, free of charge→freely, destination→destine, on behalf of→behalf), 뜻이 크게 달라진 어족(facility→facilitate, installment→install, considerable→consider, initial→initiative, essential→essence 등). 모두 지웠고, 어족이 없는 카드 39장은 `derivatives: []`, `no_word_family: true`로 바꾸었습니다(새 카드 포함 48장). 이 카드들 모두 confusables나 paraphrases가 1개 이상 있습니다.
2. **혼동어가 같은 어족 (VR24·5-3)**: 20건. 혼동어 칸에 들어 있던 파생어(attendee, donor, expert, inspector, permission, production 등)를 지웠습니다.
3. **다의어 미분리 (2-5)**: decline·extend는 나누었습니다(3절). 뜻이 크게 다른 보조 뜻이 있던 카드 11장은 보조 뜻과 그 뜻의 예문·콜로케이션을 지우고 대표 뜻 하나만 남겼습니다(5절 목록).
4. **콜로케이션**: 표제어가 빠진 항목(be headquartered in, expiration date), 패턴 표기(anticipate + -ing, approximately + 숫자), 다른 뜻의 항목(approve of, inquire into, media coverage)을 바꾸었습니다.
5. **패러프레이즈 충돌**: 같은 단어가 패러프레이즈이면서 혼동어였던 경우(rent, able, survey, guarantee, process, individually), 뜻이 같지 않은 경우(certificate→voucher, recipient→winner, resident→tenant 등)를 정리했습니다.

`deriv_stem`: 실제 파생어가 있는 카드 173장에 Part 5 형식 문장을 한 개씩 넣었습니다. 빈칸 자리에 맞는 품사가 정답 형태 하나뿐이 되도록 썼습니다(같은 품사 형태는 VR29에 따라 보기에서 하나만 남는다는 전제). SCHEMA에서 `deriv_stem`이 문자열이라 정답 형태는 따로 기록하지 않았습니다. 생성기에서 정답 형태가 필요하면 `answer_form` 필드를 더하자고 developer에게 제안합니다.

---

## 2. 수정 목록 (133장)

표기: 파생 = 파생어 정리, NWF = no_word_family로 전환, 혼동 = 같은 어족 혼동어 삭제, 예 = 예문, 콜 = 콜로케이션, 패 = 패러프레이즈, 뜻 = meaning_ko/sub

| ID | 표제어 | 수정 내용 |
|---|---|---|
| 0001 | admission | 파생: admissible 삭제 (뜻 변화) |
| 0003 | alternative (n) | 파생: alternate 삭제 |
| 0004 | amenity | NWF (amenities = 복수형) |
| 0005 | assembly | 파생: assembler 삭제 |
| 0006 | attendance | 파생: attendant 삭제, 혼동 attendee, 예2 교체 (같은 문형 반복, E9) |
| 0007 | attire | NWF (자기 자신 반복) |
| 0008 | benefit | 혼동 beneficial |
| 0009 | capacity | NWF (capable·capability는 뜻 변화), 혼동어 capability 유지 |
| 0010 | caterer | 혼동 catering |
| 0011 | certificate | 혼동 certification, 패 voucher 삭제 (뜻 다름) |
| 0013 | component | NWF (복수형) |
| 0014 | contractor | 혼동 contract |
| 0018 | demand | 파생: demanding 삭제, 예 교체 (0227과 5-gram 중복) |
| 0020 | destination | NWF (destined·destine 억지 연관), 혼동어 destiny 추가 |
| 0021 | district | NWF (복수형) |
| 0022 | donation | 혼동 donor |
| 0023 | entry | 파생: entrance→entrant, 보조 뜻 "입장" 삭제 (출품작과 다른 뜻) |
| 0024 | exhibition | 혼동 exhibitor, 패 exhibit(파생어와 겹침) 삭제 |
| 0025 | expertise | 혼동 expert |
| 0026 | facility | NWF (facilitate·facilitator 뜻 변화) |
| 0027 | feedback | NWF (자기 자신 반복) |
| 0028 | headquarters | 예 7단어→14단어, 콜 "be headquartered in"(표제어 없음) 교체 |
| 0030 | ingredient | NWF (복수형) |
| 0031 | installment | NWF (install·installation은 다른 어원·뜻), 혼동어 installation 유지 |
| 0032 | inventory | NWF (복수형) |
| 0033 | itinerary | NWF (복수형) |
| 0034 | landlord | NWF (landlady는 성별 짝말) |
| 0035 | coverage | 보조 뜻 "(언론) 보도"·콜 media coverage 삭제 (다른 뜻), 콜 dental coverage |
| 0037 | inspection | 혼동 inspector (inspect 카드와의 관계는 4절 참고) |
| 0038 | anniversary | NWF (복수형), 혼동어 annual 추가 |
| 0039 | banquet | NWF (banqueting 희귀) |
| 0040 | duration | NWF (durable·durability 뜻 변화), 혼동어 durability 유지 |
| 0041 | accommodate | 파생: accommodating 삭제 |
| 0044 | anticipate | 콜 "anticipate + -ing" → anticipate delays |
| 0046 | approve | 콜 "approve of"(찬성하다, 다른 뜻) → approve a request |
| 0052 | browse | 파생: browser 삭제 |
| 0055 | conduct | NWF (conduct(n) 행동·conductor 지휘자 뜻 변화) |
| 0059 | decline (v) | 분리: 대표 뜻 "거절하다, 사양하다"만 남김, 감소 뜻은 VC-4-0242로. NWF, 예2·콜·패 교체 |
| 0060 | demonstrate | 파생: demonstrator 삭제 |
| 0065 | ensure | NWF (sure 억지 연관) |
| 0066 | enroll | 파생: enrollee 삭제 (빈도 낮음) |
| 0070 | exceed | 파생: exceedingly 삭제 |
| 0071 | expand | 파생: expansive 삭제 |
| 0072 | expire | 콜 expiration date(표제어 없음) 교체 |
| 0073 | extend | 분리: "연장하다"만 남김, 초대 뜻은 VC-4-0243으로. 파생 extensive/extensively 삭제, extended(adj) 추가, 예2·콜 교체 |
| 0074 | forward | NWF (adv·adj forward는 뜻 다름) |
| 0077 | inquire | 콜 "inquire into"(조사하다) 교체 |
| 0079 | lease | 파생: leasing 삭제, 패 rent 삭제 (혼동어와 충돌) |
| 0080 | accompany | 뜻 "동반하다, 동봉되다"→"동반하다, 함께 가다", 예2(accompanying = 파생형, E4 위반) 교체, 파생 accompaniment 삭제 |
| 0081 | accessible | 예 2개 모두 7단어→12·13단어, 패 available 삭제 |
| 0086 | capable | 파생: capacity 삭제, 콜 패턴 표기 교체, 패 able(혼동어와 충돌)→competent |
| 0088 | complimentary | NWF (compliment는 '칭찬' 뜻), 보조 뜻 "칭찬하는" 삭제, 예 7단어→12단어 |
| 0089 | comprehensive | 파생: comprehend·comprehension 삭제 (이해 뜻) |
| 0091 | considerable | 파생: consider·consideration 삭제 |
| 0092 | dedicated | 보조 뜻 "전용의" 삭제, 예 교체 ("dedicated support team"은 '전용 지원팀'으로도 읽혀 E5 위반), 콜 교체 |
| 0093 | durable | 파생: duration 삭제 |
| 0096 | essential | 파생: essence·essentials 삭제 |
| 0097 | existing | 콜 "replace the existing" 미완성 → replace the existing system |
| 0099 | extensive | 파생: extend·extension 삭제 (뜻 변화) |
| 0101 | informative | 파생: informatively 삭제 (빈도 낮음) |
| 0102 | initial | 파생: initiate·initiative 삭제 |
| 0106 | alternatively | 예: 두 문장 → 한 문장(E3), 콜 대문자 정리, 패 otherwise 삭제 (뜻 다름) |
| 0107 | approximately | 콜 "approximately + 숫자" → approximately 30 minutes |
| 0109 | dramatically | 파생: drama 삭제 |
| 0110 | exclusively | 파생: exclude·exclusion 삭제 |
| 0114 | carry out | NWF (carry·carrier 구동사 분해·억지 연관) |
| 0115 | free of charge | NWF (free·freely), 예 7단어→14단어 |
| 0116 | maintenance | 파생: maintained 삭제, 혼동어 "maintainance"(없는 단어) 삭제 |
| 0117 | membership | 혼동 member |
| 0118 | merchandise | 파생: merchant 삭제 (사람, 뜻 다름) |
| 0119 | occupancy | 혼동 occupant |
| 0120 | opening | 보조 뜻 "개장, 개점"·예2·콜 grand opening 삭제, 파생 openly 삭제, 혼동 open |
| 0121 | overview | NWF (overview 동사는 사전 확인 불충분) |
| 0123 | performance | 뜻 3개→"실적, 성과" + 보조 "(기계의) 성능", 파생 performer 삭제 |
| 0124 | permit (n) | 혼동 permission |
| 0127 | priority | 예1 6단어→10단어, 파생 prior 삭제 (뜻 다름, 혼동어로 유지) |
| 0128 | procedure | 파생: process(다른 단어)·proceed 삭제, 패 process 삭제 (혼동어와 충돌) |
| 0129 | productivity | 혼동 production, 패 output 삭제, 예 교체 (0094와 5-gram 중복) |
| 0130 | promotion | 보조 뜻 "판촉"·예2·콜 삭제, 파생 promotional·promoter 삭제, 패 special offer 삭제 |
| 0131 | questionnaire | 패 survey 삭제 (혼동어와 충돌) |
| 0132 | recipient | 파생: receipt·reception 삭제, 패 winner 삭제 |
| 0133 | reference | 보조 뜻 "참고, 언급"·예2·콜 for future reference/with reference to 삭제 |
| 0134 | refreshments | NWF (refresh·refreshing 뜻 변화), 혼동어 "refreshment(단수)" 삭제 |
| 0139 | representative | 뜻 3개→"담당 직원, 대리인", 파생 representation 삭제 |
| 0142 | resident | 혼동 residence, 패 tenant 삭제 |
| 0144 | satisfaction | 혼동 satisfactory, 패 approval 삭제 |
| 0145 | shift | NWF (shift 동사는 '옮기다'), 보조 뜻 "변화"·콜 a shift in demand 삭제, 혼동어 gift 삭제 |
| 0146 | subscription | 혼동 subscriber |
| 0147 | supervisor | 혼동 supervision, 뜻 3개→2개 |
| 0149 | technician | 파생: technique·technology·technically 삭제 |
| 0150 | tenant | 패 resident 삭제 |
| 0151 | variety | 파생: variously 삭제, 혼동 various |
| 0152 | vendor | NWF (vend·vending) |
| 0153 | voucher | NWF (vouch 억지 연관), 뜻 3개→2개 |
| 0154 | warranty | NWF (warrant 뜻 변화), 패 guarantee 삭제 (혼동어와 충돌) |
| 0155 | workforce | NWF (worker·work 합성어 분해) |
| 0156 | maintain | 파생: maintained 삭제 |
| 0157 | manufacture | 혼동 manufacturer |
| 0160 | monitor | NWF (monitor(n) 화면·monitoring), 뜻 3개→2개 |
| 0163 | notify | 파생: notice 삭제 (다른 단어) |
| 0164 | obtain | 뜻 3개→2개 |
| 0165 | occupy | 파생: occupation 삭제, 보조 뜻 삭제 |
| 0166 | operate | 콜 fully operating → operate equipment, 패 work 삭제 |
| 0170 | proceed | NWF (procedure·proceeds·process 뜻 변화) |
| 0171 | process (v) | 파생: processing·processor 삭제 |
| 0172 | prohibit | 파생: prohibitive 삭제 (엄청 비싼), 예 6단어→12단어 |
| 0173 | promote | 보조 뜻 "홍보하다"·예2 삭제, 파생 promotional·promoter 삭제, 콜·패 정리 |
| 0176 | qualify | 예 7단어→13단어 |
| 0177 | recruit | 혼동 recruiter |
| 0181 | renew | 파생: renewable·renewed 삭제 |
| 0182 | reschedule | NWF (schedule·rescheduled) |
| 0188 | secure | 예 교체 (0051과 5-gram 중복) |
| 0192 | utilize | 파생: utility 삭제 (공공요금 뜻) |
| 0195 | withdraw | 보조 뜻 "철회하다"·예2·관련 콜 삭제, 패 pull out·cancel 삭제 |
| 0197 | multiple | NWF (multiply·multiplicity 뜻 변화) |
| 0198 | numerous | 파생: number(v) 삭제 |
| 0201 | outstanding | 보조 뜻 "미지불된"·예2·콜 outstanding balance/issues·패 unpaid 삭제 |
| 0202 | overdue | NWF (due·dues) |
| 0207 | qualified | 패 experienced 삭제 |
| 0208 | quarterly | 혼동 quarter |
| 0209 | reasonable | 파생: reason 삭제 |
| 0211 | reliable | 파생: reliance 삭제, 혼동어 reliant(같은 어족) 삭제 |
| 0216 | substantial | 파생: substance 삭제 |
| 0218 | upcoming | NWF (come up 구동사 분해) |
| 0219 | vacant | 파생: vacantly 삭제 |
| 0221 | originally | 파생: origin·originate 삭제, 혼동어 originality 삭제 |
| 0223 | promptly | 파생: prompt(v) 삭제 |
| 0224 | relatively | 파생: relative(n, 친척) 삭제 |
| 0225 | separately | 패 individually 삭제 (혼동어와 충돌) |
| 0226 | shortly | NWF (short·shorten·shortage 뜻 변화) |
| 0227 | steadily | 파생: steady(v) 삭제 |
| 0229 | on behalf of | NWF (behalf), 패 for 삭제 |
| 0230 | run out of | NWF (run out 구동사 분해), 패 sell out 삭제 |

나머지 86장은 내용 결함이 없어 `deriv_stem`(해당 시)과 검수 필드만 넣었습니다.

**`deriv_stem`이 없는 카드 (Q2 파생어 퀴즈 제외, 결함 아님)**: 파생어가 표제어와 철자가 같은 카드 — demand, deposit, browse, launch, lease, outline, process(v), decline(n). 파생어가 표제어와 품사가 같은 카드 — candidate(candidacy), membership(member), tenant(tenancy), merchandise(merchandising). 그리고 no_word_family 카드 48장.

---

## 3. 삭제·교체·추가 카드

### 3.1 삭제 (기초 파일과 중복, CoS 결정) — 11장
VC-4-0002 agenda (n), VC-4-0084 annual (adj), VC-4-0056 confirm (v), VC-4-0108 currently (adv), VC-4-0111 immediately (adv), VC-4-0213 responsible (adj), VC-4-0148 supplier (n), VC-4-0141 reservation (n), VC-4-0175 purchase (v), VC-4-0205 previous (adj), VC-4-0180 remind (v). ID는 재사용하지 않습니다. headquarters·launch·expand는 400에 남겼습니다.

### 3.2 교체 카드 — 11장 (모두 l400_m-z.json, 작성자 `ai-qa-vocab-400`, self_reviewed)
`content/vocab/` 아래 모든 파일에서 lemma로 겹치지 않는 것을 확인했습니다.

| ID | 표제어 | 뜻 | 파생어 |
|---|---|---|---|
| VC-4-0231 | personnel (n) | (전체) 직원, 인원 | 없음 (NWF, 혼동어 personal) |
| VC-4-0232 | premises (n) | (건물이 딸린) 부지, 구내 | 없음 (NWF, 혼동어 premise) |
| VC-4-0233 | revenue (n) | 수익, 매출 | 없음 (NWF, 혼동어 profit) |
| VC-4-0234 | venue (n) | (행사) 장소 | 없음 (NWF, 혼동어 avenue) |
| VC-4-0235 | payroll (n) | 급여 지급 (업무), 급여 대장 | 없음 (NWF, 혼동어 payment) |
| VC-4-0236 | outlet (n) | (판매) 매장, 직판점 | 없음 (NWF, 혼동어 outlook) |
| VC-4-0237 | undergo (v) | (변화·검사 등을) 겪다, 받다 | 없음 (NWF, 패 go through) |
| VC-4-0238 | compensation (n) | 보상(금), 보수 | compensate (v) |
| VC-4-0239 | incentive (n) | 장려책, 인센티브 | incentivize (v) |
| VC-4-0240 | fare (n) | (교통) 요금, 운임 | 없음 (NWF, 혼동어 fee·fair) |
| VC-4-0241 | prospective (adj) | 장래의, 예비의 | prospect (n) |

### 3.3 다의어 분리 — 2장
| ID | 표제어 | 뜻 | 비고 |
|---|---|---|---|
| VC-4-0242 | decline (n) | 감소, 하락 | VC-4-0059 decline (v)는 "거절하다"만 남김. 감소 뜻을 같은 (lemma, pos)=(decline, v) 카드로 나누면 build_db.py가 **오류**(같은 표제어·품사 중복)로 막아서 명사 카드로 나눴습니다. 파생어 decline (v)가 '감소하다' 뜻을 이어 줍니다 |
| VC-4-0243 | extend an invitation (phr) | (정식으로) 초대하다, 초청하다 | VC-4-0073 extend (v)는 "연장하다"만 남김. 같은 이유로 "(감사·초대를) 전하다" 뜻은 구(phr) 카드로 나눴습니다 |

### 3.4 추가 요청 카드 — 1장 (코디네이터 요청)
| ID | 표제어 | 뜻 | 파생어 |
|---|---|---|---|
| VC-4-0244 | inspect (v) | 점검하다, 검사하다 | inspection (n), inspector (n) |

**inspect ↔ inspection 관계**: 기초 검수자가 inspect를 기초에서 뺐고(기초 기준 ① 미충족), 지금 inspect는 어떤 파일에도 lemma로 남아 있지 않은 것을 확인했습니다. 두 카드는 **별도 카드로 두고 파생어가 서로를 가리키도록** 했습니다(VC-4-0037 inspection → inspect·inspector, VC-4-0244 inspect → inspection·inspector). 표준 8.1에 따라 서로의 뜻은 문맥 뜻 고르기 오답에서 빠지고(같은 어족), 혼동어 칸에는 서로를 넣지 않았습니다(VR24). `deriv_stem`은 서로의 형태가 정답이 되게 썼습니다(inspection 카드: 정답 inspect / inspect 카드: 정답 inspection). 어휘 체크 V1에 따라 같은 폼에 둘을 함께 내지 않을 것을 권장합니다.

---

## 4. 레벨 경계 목록 (교체하지 않고 표시만 함)

뚜렷하게 맞지 않는 카드는 없어서 레벨 때문에 교체한 카드는 없습니다. 아래는 파일럿 데이터(B4)로 다시 확인할 후보입니다.

**기초 쪽에 가까움 (B3 낮은 쪽 우선 규칙으로 400 유지)**
- feedback, benefit, complaint, attach, retire, publish, demand, membership, supervisor, variety, technician, resident, frequently, shortly, separately, gradually, temporary, temporarily, limited, accurate, efficient, multiple, portable
- 기초 카드의 파생형이라 기초에서 배운 뒤 바로 이어지는 카드: registration(기초 register), reminder(기초 remind), previously(기초 previous), inspection·inspect, expand·launch·headquarters(CoS 결정으로 400)

**450 쪽에 가까움 (B3 규칙으로 400 유지)**
- expertise, installment, precaution, occupancy, patron, utilize, renowned, punctual, comprehensive, confidential, considerable, substantial, exclusively, anticipate, mandatory, operational, vacate, complimentary, payroll, premises
- 구 카드: on behalf of, extend an invitation (B2 쓰임 기준으로 450 후보)

**뜻을 하나로 좁혀서 빠진 뜻 (다른 카드 필요, 450 후보)**: outstanding "미지불된", promote "홍보하다", promotion "판촉 (행사)", opening "개장·개점", reference "참고", shift "변화", withdraw "철회하다·불참하다", coverage "(언론) 보도", complimentary "칭찬하는", dedicated "전용의", entry "입장". 같은 (lemma, pos) 카드를 둘 두면 build_db.py가 오류로 막기 때문에 이번에는 만들지 않았습니다. 표준 13장 VR05는 이 경우를 **W(경고)**로 정의하므로, developer에게 build_db.py의 중복 검사를 (lemma, pos, meaning_ko) 기준 E와 (lemma, pos) 기준 W로 바꾸자고 제안합니다.

---

## 5. 원어민 확인 우선 목록

1. **새 카드 14장 전체** (VC-4-0231~0244): 예문·콜로케이션·`deriv_stem` 자연스러움, 그리고 교차 검수(작성자 ≠ 검수자).
2. **실존·사전 2종 확인이 필요한 파생어**: headquarter (v)·headquartered, incentivize, capably, outstandingly, knowledgeably, operationally, patronize(애용하다 뜻), resumption, obtainable, tenancy, candidacy, merchandising, entrant, precautionary, permissible, verifiable, transferable.
3. **`deriv_stem` 중 분사·명사 수식어 자리라 정답이 둘로 보일 수 있는 문장**: 0044 anticipated, 0062 enclosed, 0068 estimated, 0125 precautionary, 0143 retail, 0149 technical, 0165 occupancy, 0187 revised, 0051 award-winning, 0144 satisfied(satisfactory와 같은 adj). 4형을 직접 넣어 보고 정답이 하나인지 확인 필요 (8.2).
4. **같은 품사 형태가 둘 이상이라 생성기가 하나만 골라야 하는 카드**: 0050 authorize(authorization/authority), 0057 consult(consultation/consultant), 0061 distribute, 0087 competitive, 0124 permit(permission/permit), 0174 publish, 0186 retire(retirement/retiree), 0190 sponsor, 0215 spacious(space/spaciousness). 정답 형태가 아닌 같은 품사 형태는 보기에서 빼야 합니다(VR29).
5. **뜻 범위·번역 확인**: 0035 coverage(보장 범위), 0122 patron(이용객), 0139 representative(담당 직원), 0232 premises, 0235 payroll(급여 대장), 0243 extend an invitation.
6. **lemma 형식 예외**: refreshments, premises는 복수형만 쓰는 뜻이라 복수형을 lemma로 두었습니다. 1장 규칙(명사 단수)의 예외로 콘텐츠 리드 확인이 필요합니다.

---

## 6. 검수 방법 기록

- 230장 전체를 카드 단위로 읽고 11장 체크리스트 A~G를 적용했습니다.
- 기계 점검(자체 스크립트): 예문 표제어 1회(VR08), 8~25단어(VR09), 한 문장(VR10), 콜로케이션에 표제어 포함(VR12), 파생어와 혼동어 중복(VR24), 패러프레이즈와 혼동어 충돌, `deriv_stem` 빈칸 1개(VR30), 기초·400 전체 예문과 `deriv_stem`의 5-gram 겹침(VR23). 겹침 6건은 예문·stem을 다시 써서 해결했습니다. run out of 예문의 "ran"은 불규칙형이라 스크립트가 잡지 못했을 뿐, 확인 결과 정상입니다.
- 독창성: 모든 예문·stem은 가상 회사·인물로 자체 작성했습니다. 웹 일치 검색은 이 환경에서 하지 않았고, 기록 방법은 "AI 교차 검수, 예문 자체 작성 확인"입니다. 원어민 확인 단계(9.4-1)에서 웹 검색을 보완해야 합니다.
- 검수 필드: 통과 카드에 `reviewer_1_id: ai-qa-vocab-400`, `originality_check`(통과, 2026-10-13), `native_check_id: ""`, `status: cross_reviewed`를 넣었습니다. 내용이나 `deriv_stem`이 바뀐 카드는 `version: 2`입니다.
- 빌드: `python3 -B db/build_db.py` → OK, 오류 0건.

---

## 7. 신규 카드 14장 교차 검수

- 검수: qa-tester 역할 (`ai-qa-vocab-4b`, 작성자 `ai-qa-vocab-400`와 다른 교차 검수자) / 검수일: 2026-10-13
- 대상: VC-4-0231~0244 (l400_m-z.json, 3.2~3.4절의 교체·분리·추가 카드)
- 기준: vocab-standard 11장 체크리스트 A~G, 13장 VR01~VR33, SCHEMA 파생어 규칙(no_word_family, deriv_stem)
- 결과: **14장 모두 통과 → `cross_reviewed`** (보류 0). `reviewer_1_id: ai-qa-vocab-4b`, `qa_note` 삭제, `native_check_id`는 비워 둠. 내용을 고친 12장은 `version: 2`, 고치지 않은 2장(0237, 0242)은 `version: 1`
- 빌드: `python3 -B db/build_db.py` → **OK** (어휘 카드 383개, 오류 0건)

### 7.1 점검 결과

| ID | 표제어 | 수정 내용 | 판정 |
|---|---|---|---|
| 0231 | personnel (n) | 예1 교체: "Only authorized personnel may enter…"는 출입 안내문의 상투 문장(웹에 거의 같은 문장 다수) → 자체 문장. 예2 Harmon Clinic → Velbrook Clinic (실존 가능 이름) | 통과 |
| 0232 | premises (n) | 예1 교체 (회사 흡연 금지 규정의 상투 문장). 예2 교체 ("must show a photo ID"가 p5_placementA 문항과 5-gram 겹침, VR23) | 통과 |
| 0233 | revenue (n) | 패러프레이즈 earnings 삭제 (순이익 뜻으로도 쓰여 혼동어 profit의 구별 설명과 충돌). Pellman은 프로젝트 가상 회사라 유지 | 통과 |
| 0234 | venue (n) | Grandview Pavilion → Corlith Pavilion (같은 이름의 실제 행사장 있음) | 통과 |
| 0235 | payroll (n) | 예1 교체 ("should be sent to the"가 p6_batch1 지문과 5-gram 겹침) | 통과 |
| 0236 | outlet (n) | Barrow Coffee → Tamsford Coffee (실존 상호 "The Barrow Coffee" 확인) | 통과 |
| 0237 | undergo (v) | 수정 없음. NWF, 패러프레이즈 2개 | 통과 |
| 0238 | compensation (n) | 예1 교체 (항공 결항 보상 안내의 상투 문장). deriv_stem "will ------- customers"는 compensate만 가능, 확인 | 통과 |
| 0239 | incentive (n) | Brooke Insurance → Quenley Insurance, 패러프레이즈 reward 삭제 (사후 보상이라 뜻이 같지 않음). incentivize 실존 확인, stem 정답 하나 | 통과 |
| 0240 | fare (n) | Kenton → Dunmarsh (Kenton은 실존 지명) | 통과 |
| 0241 | prospective (adj) | deriv_stem의 Delta Foods → Ravelton Foods (실존 가능 상호). "a strong -------" 자리는 명사 prospect만 가능 | 통과 |
| 0242 | decline (n) | 수정 없음. 파생어 decline (v)는 같은 철자·다른 품사(전환)로 2절 demand·deposit과 같은 처리, deriv_stem 없음(Q2 제외, 결함 아님). VC-4-0059 decline (v)와 (lemma, pos) 중복 아님 | 통과 |
| 0243 | extend an invitation (phr) | 예2 교체: "We are pleased to extend an invitation to you for our…"는 초대장 서식 상투 문장 → 수동형 자체 문장 (예1과 문형도 다르게, E9) | 통과 |
| 0244 | inspect (v) | 예2 교체 (배송 약관 상투 문장 "Please inspect your order carefully upon delivery…"), 예1 번역 어미 통일. 파생어 inspection·inspector, VC-4-0037 inspection의 파생어에 inspect 있음(서로 가리킴), 양쪽 confusables에 서로 없음(VR24). deriv_stem은 명사 자리라 inspection 정답, inspector는 같은 품사라 VR29로 보기에서 빠짐 | 통과 |

### 7.2 공통 점검
- **중복**: content/vocab/*.json 전체에서 14장의 (lemma, pos) 중복 없음. 같은 lemma는 decline (v)/(n)뿐 (의도된 다의어 분리).
- **콜로케이션**: 56개 모두 표제어(굴절형 포함) 포함, 전치사 패턴 이상 없음.
- **뜻·품사**: 14장 모두 meaning_ko·예문·콜로케이션 품사 일치.
- **독창성**: 예문 26개와 deriv_stem 4개를 따옴표 웹 검색 — 같은 문장 일치는 찾지 못했지만, 안내문·약관에 흔한 상투 문장 5개는 예방 차원에서 바꿈. 실존 가능 고유명사 6개를 웹 검색으로 확인되지 않는 이름으로 교체. 수정 후 다른 카드(기초·400)·문항(content/items/**) 전체와 5-gram 겹침 0건 (수정 중 생긴 VC-B-0151과의 겹침도 다시 써서 해결).
- `originality_check`: 통과, 2026-10-13, 방법 "AI 교차 검수: 따옴표 웹 검색, 고유명사 교체, 5-gram 대조"를 14장에 기록.

### 7.3 남은 일
- 원어민 확인(5절 1번): 새 예문 7개(0231 예1, 0232 예1·2, 0235 예1, 0238 예1, 0243 예2, 0244 예2)와 incentivize·compensate stem의 자연스러움.
- payroll·premises·extend an invitation의 레벨(450 후보)은 4절 그대로 유지.
