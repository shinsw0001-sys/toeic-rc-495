# 문항 원본 파일 형식 (Batch 1)

기준: docs/qa/content-standard.md 2장(필드), 3장(정답 유일성·오답), 4장(유형 태그), 5장(난이도), 6장(해설), 7장(지문), 8장(저작권).
파일 하나 = JSON 하나. 경로: `content/items/<파트>/<파일>.json` (UTF-8).

## Part 5 파일: `{ "items": [ ITEM, ... ] }`
## Part 6·7 파일: `{ "sets": [ SET, ... ] }`

SET = {
  "set_id": "RC-P6-S-0001" | "RC-P7-S-0001"(단일) | "RC-P7-D-0001"(이중) | "RC-P7-T-0001"(삼중),
  "part": 6 | 7,
  "passage_type": "email" | "letter" | "memo" | "notice" | "advertisement" | "article" | "form" | "invoice" | "schedule" | "text_message_chain" | "online_chat" | "web_page" | "review",
  "passage_count": 1 | 2 | 3,
  "business_context": "주문·배송" 등,
  "fictional_entities": ["Pellman Office Supply", ...],   // 모두 가상, 실존 회사·인물 금지
  "passages": [ { "title": "...", "type": "email", "text": "문단은 \n\n 로 구분. Part 6 빈칸은 [131], [132]처럼 표기, 문장 삽입 위치는 [134]. Part 7 문장 위치 문제는 [1] [2] [3] [4] 표기" } ],
  "items": [ ITEM, ... ]   // P6=4, P7 단일 2~4, 이중 5, 삼중 5
}

ITEM = {
  "item_id": "RC-P5-000001" (P5) | "RC-P6-000001" | "RC-P7-000001",
  "part": 5 | 6 | 7,
  "position_in_set": 1~5 (P6·P7만),
  "stem": "문제 문장(P5, 빈칸은 -------) 또는 질문(P7). P6는 \"[131]\"처럼 빈칸 번호",
  "options": { "A": "...", "B": "...", "C": "...", "D": "..." },
  "answer": "A" | "B" | "C" | "D",
  "type_tag": "P5-POS.ADV" 등 content-standard 4장 코드 1개,
  "sub_tags": [],
  "difficulty_expert": 1~5,
  "target_track": ["300-400"] 등,
  "vocab_level": "기초" | "중급" | "고급",
  "explanation_ko": "해설 (정답 근거 → 핵심 규칙, 해요체)",
  "evidence_quote": "P6·P7: 정답 근거가 되는 지문 문장 그대로 인용 (P5는 빈 문자열)",
  "distractor_rationale": { "A": "...", "B": "...", "C": "...", "D": "..." },   // 정답 보기에는 "정답: 이유"
  "trap_code": { "A": "POS_CONFUSION" 등 오답이 노린 함정 영어 대문자 코드, 정답은 null },
  "key_point": "1~2문장 핵심 규칙",
  "vocab": [ { "word": "postpone", "pos": "v.", "meaning_ko": "연기하다", "level": "중급", "option": "B" } ],   // 어휘 추천용 핵심 단어 2~5개. option(선택): 그 단어가 나온 보기 A~D, 문제 문장·지문 단어면 null
  "author_id": "ai-writer-p5" 등,
  "source_note": "자체 창작. 착상: <일반 비즈니스 주제>. 참고 자료 문장 복사 없음",
  "status": "draft",
  "version": 1,
  "created_at": "2026-10-13"
}

함정 코드 예: POS_CONFUSION, NUMBER_AGREEMENT, TENSE_MISMATCH, VOICE_CONFUSION, SIMILAR_FORM, MEANING_NEAR_MISS, COLLOCATION_MISMATCH, PREP_CONJ_CONFUSION, WORD_REPEAT_TRAP, PARTIAL_INFO, OVERGENERALIZATION, WRONG_REFERENT, NOT_MENTIONED, OPPOSITE_INFO, VERB_PATTERN(동사 뒤 구조 오류), STATED_IN_PASSAGE(NOT 문항에서 지문에 실제로 나온 오답).

가상 URL은 `name.example.com` 형식을 쓴다 (실제 등록 가능한 도메인 금지).

---

# 어휘 카드 파일 형식 (content/vocab/<레벨>_<묶음>.json)

`{ "cards": [ CARD, ... ] }` — 기준: docs/specs/placement-and-vocab.md 3.2~3.3

CARD = {
  "word_id": "VC-B-0001" (기초) | "VC-4-0001" (400) | "VC-5-0001" (450),
  "lemma": "reimburse",
  "pos": "n" | "v" | "adj" | "adv" | "prep" | "conj" | "phr",
  "meaning_ko": "(비용을) 상환하다, 환급하다",
  "meaning_ko_sub": "" (선택, 보조 뜻 1개),
  "examples": [ { "en": "자체 작성 비즈니스 예문 (가상 회사·인물만)", "ko": "정확한 번역" } ],   // 1~2개
  "collocations": ["reimburse employees for travel expenses", "be reimbursed for"],   // 2~4개
  "derivatives": [ { "pos": "n", "form": "reimbursement" } ],   // 400 레벨부터 필수, 기초는 있으면
  "confusables": [ { "word": "...", "note_ko": "구별 한 줄" } ],   // 선택
  "paraphrases": ["pay back"],   // 선택
  "type_tags": ["P5-VOC.V"],   // content-standard 4장 코드, 1개 이상
  "level": "기초" | "400" | "450",
  "selection_note": "선정 근거: 전문가 판단(토익 비즈니스 맥락 고빈도) / 자체 문항 은행 등장 여부. 공개·상업 단어장 목록·예문 복사 없음",
  "author_id": "...", "status": "draft", "version": 1, "created_at": "2026-10-13",
  // 검수 단계에서 채우는 선택 필드 (CoS 결정 2026-10-13, docs/qa/vocab-standard.md)
  "reviewer_1_id": "", "native_check_id": "", "originality_check": { "result": "", "date": "", "method": "" },
  "deriv_stem": "파생어 빈칸 퀴즈용 Part 5 형식 문장, 빈칸은 ------- (400 레벨부터 권장)"
}

파생어 규칙 (CoS 결정 2026-10-13): 진짜 어족만 적는다. 복수형, 구동사 분해("run out"), 억지 연관어("ensure → sure")는 파생어가 아니다. 어족이 없는 핵심어(personnel, premises, revenue, venue 등)는 `"derivatives": []`, `"no_word_family": true`로 두고 confusables나 paraphrases를 1개 이상 채운다.

문항 `vocab_level`과 카드 `level` 대응: 기초 = 기초, 중급 = 400, 고급 = 450.

# 배치고사 폼 구성 파일 (content/forms/placement_A.json)

{ "form_id": "PL-A", "stage1": [item_id...], "modules": { "basic": [...], "mid": [...], "upper": [...] }, "routing": { "basic": [0,5], "mid": [6,8], "upper": [9,12] } }
