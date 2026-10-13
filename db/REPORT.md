# 문항 DB 현황

DB: `db/toeic_rc.db` (SQLite). 다시 만들기: `python3 db/build_db.py`

## Part별

| Part | 세트 | 문항 |
|---|---|---|
| 5 | - | 40 |
| 6 | 4 | 16 |
| 7 | 6 | 22 |

## 유형별

| Part | 대분류 | 유형 태그 | 문항 수 | 평균 난이도 |
|---|---|---|---|---|
| 5 | 연결어 (P5-CONN) | P5-CONN.CONJ | 1 | 4.0 |
| 5 | 연결어 (P5-CONN) | P5-CONN.CORR | 1 | 2.0 |
| 5 | 연결어 (P5-CONN) | P5-CONN.PREP | 2 | 3.0 |
| 5 | 연결어 (P5-CONN) | P5-CONN.PREPvsCONJ | 2 | 3.5 |
| 5 | 연결어 (P5-CONN) | P5-CONN.REL | 2 | 3.0 |
| 5 | 기타 문법 (P5-GRAM) | P5-GRAM.COMP | 1 | 2.0 |
| 5 | 기타 문법 (P5-GRAM) | P5-GRAM.INV | 1 | 5.0 |
| 5 | 기타 문법 (P5-GRAM) | P5-GRAM.MISC | 1 | 2.0 |
| 5 | 기타 문법 (P5-GRAM) | P5-GRAM.QUANT | 1 | 1.0 |
| 5 | 품사 (P5-POS) | P5-POS.ADJ | 2 | 2.5 |
| 5 | 품사 (P5-POS) | P5-POS.ADV | 3 | 2.7 |
| 5 | 품사 (P5-POS) | P5-POS.N | 2 | 2.0 |
| 5 | 품사 (P5-POS) | P5-POS.PRON | 2 | 1.5 |
| 5 | 품사 (P5-POS) | P5-POS.V | 1 | 1.0 |
| 5 | 동사 (P5-VERB) | P5-VERB.AGR | 1 | 3.0 |
| 5 | 동사 (P5-VERB) | P5-VERB.MOOD | 1 | 4.0 |
| 5 | 동사 (P5-VERB) | P5-VERB.NONFIN | 2 | 2.5 |
| 5 | 동사 (P5-VERB) | P5-VERB.TENSE | 2 | 3.0 |
| 5 | 동사 (P5-VERB) | P5-VERB.VOICE | 2 | 3.0 |
| 5 | 어휘 (P5-VOC) | P5-VOC.ADJ | 2 | 3.0 |
| 5 | 어휘 (P5-VOC) | P5-VOC.ADV | 1 | 3.0 |
| 5 | 어휘 (P5-VOC) | P5-VOC.COLL | 2 | 3.5 |
| 5 | 어휘 (P5-VOC) | P5-VOC.N | 2 | 3.0 |
| 5 | 어휘 (P5-VOC) | P5-VOC.PV | 1 | 2.0 |
| 5 | 어휘 (P5-VOC) | P5-VOC.V | 2 | 3.5 |
| 6 | 문맥 문법 (P6-CTX) | P6-CTX.PRON | 1 | 3.0 |
| 6 | 문맥 문법 (P6-CTX) | P6-CTX.TENSE | 1 | 3.0 |
| 6 | 문맥 문법 (P6-CTX) | P6-CTX.TRANS | 3 | 3.0 |
| 6 | 문법 (P6-GRAM) | P6-GRAM.AGR | 1 | 2.0 |
| 6 | 문법 (P6-GRAM) | P6-GRAM.REL | 1 | 4.0 |
| 6 | 문법 (P6-GRAM) | P6-GRAM.TENSE | 1 | 3.0 |
| 6 | 문법 (P6-GRAM) | P6-GRAM.V | 1 | 1.0 |
| 6 | 문장 삽입 (P6-INS) | P6-INS.SENT | 4 | 3.0 |
| 6 | 어휘 (P6-VOC) | P6-VOC.WORD | 3 | 3.0 |
| 7 | 세부 정보 (P7-DET) | P7-DET.FACT | 3 | 3.0 |
| 7 | 세부 정보 (P7-DET) | P7-DET.NUM | 1 | 2.0 |
| 7 | 추론 (P7-INF) | P7-INF.IMPLY | 2 | 3.0 |
| 7 | 추론 (P7-INF) | P7-INF.NEXT | 1 | 4.0 |
| 7 | 문장 위치 (P7-INS) | P7-INS.POS | 1 | 4.0 |
| 7 | 의도 파악 (P7-INTENT) | P7-INTENT.CHAT | 1 | 3.0 |
| 7 | 연계 (P7-LINK) | P7-LINK.2P | 3 | 4.3 |
| 7 | 연계 (P7-LINK) | P7-LINK.3P | 1 | 5.0 |
| 7 | 주제·목적 (P7-MAIN) | P7-MAIN.PURPOSE | 5 | 1.8 |
| 7 | 주제·목적 (P7-MAIN) | P7-MAIN.TOPIC | 1 | 2.0 |
| 7 | 사실 확인 (P7-TF) | P7-TF.NOT | 1 | 4.0 |
| 7 | 사실 확인 (P7-TF) | P7-TF.TRUE | 1 | 2.0 |
| 7 | 어휘 (P7-VOC) | P7-VOC.SYN | 1 | 3.0 |

아직 문항이 없는 태그: P7-INF.WHO

## 트랙별

| 트랙 | 문항 |
|---|---|
| 300-400 | 29 |
| 400-450 | 37 |
| 450-495 | 23 |

## 정답 위치 분포 (Part별)

| Part | A | B | C | D |
|---|---|---|---|---|
| 5 | 10 | 10 | 10 | 10 |
| 6 | 4 | 4 | 4 | 4 |
| 7 | 6 | 5 | 6 | 5 |

## 상태

- cross_reviewed: 78

## 어휘

- 등록 단어 242개, 문항-단어 연결 271건

## 어휘 카드 (레벨·품사별)

| 레벨 | n | v | adj | adv | 기타 | 합계 |
|---|---|---|---|---|---|---|

- 문항 은행 어휘와 연결된 카드: 0개

## 폼


## 내부 유사도 (5-gram Jaccard ≥ 0.3)

- 후보 없음
