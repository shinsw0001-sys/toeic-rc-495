"""문항 원본(content/items/**/*.json), 어휘 카드(content/vocab/*.json), 폼(content/forms/*.json)을 검증하고 SQLite DB(db/toeic_rc.db)로 적재한다.

사용법: python3 db/build_db.py
- 검증 실패 문항이 있으면 목록을 출력하고 종료 코드 1로 끝난다 (DB는 만들지 않음).
- Part별·유형별 집계는 db/REPORT.md 에 쓴다.
스키마는 docs/architecture.md 5장의 Postgres 설계를 SQLite로 옮긴 축약판이다.
"""
import collections
import glob
import json
import os
import re
import sqlite3
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "db", "toeic_rc.db")
REPORT_PATH = os.path.join(ROOT, "db", "REPORT.md")

TAGS = {
    5: {
        "P5-POS": ["N", "V", "ADJ", "ADV", "PRON"],
        "P5-VERB": ["TENSE", "VOICE", "AGR", "MOOD", "NONFIN"],
        "P5-CONN": ["PREP", "CONJ", "PREPvsCONJ", "REL", "CORR"],
        "P5-GRAM": ["COMP", "QUANT", "INV", "MISC"],
        "P5-VOC": ["N", "V", "ADJ", "ADV", "COLL", "PV"],
    },
    6: {
        "P6-GRAM": ["N", "V", "ADJ", "ADV", "PRON", "TENSE", "VOICE", "AGR", "MOOD", "NONFIN",
                    "PREP", "CONJ", "PREPvsCONJ", "REL", "CORR", "COMP", "QUANT", "INV", "MISC"],
        "P6-CTX": ["TENSE", "PRON", "TRANS"],
        "P6-VOC": ["WORD"],
        "P6-INS": ["SENT"],
    },
    7: {
        "P7-MAIN": ["TOPIC", "PURPOSE"],
        "P7-DET": ["FACT", "NUM"],
        "P7-TF": ["NOT", "TRUE"],
        "P7-INF": ["IMPLY", "WHO", "NEXT"],
        "P7-VOC": ["SYN"],
        "P7-INTENT": ["CHAT"],
        "P7-INS": ["POS"],
        "P7-LINK": ["2P", "3P"],
    },
}
CATEGORY_KO = {
    "P5-POS": "품사", "P5-VERB": "동사", "P5-CONN": "연결어", "P5-GRAM": "기타 문법", "P5-VOC": "어휘",
    "P6-GRAM": "문법", "P6-CTX": "문맥 문법", "P6-VOC": "어휘", "P6-INS": "문장 삽입",
    "P7-MAIN": "주제·목적", "P7-DET": "세부 정보", "P7-TF": "사실 확인", "P7-INF": "추론",
    "P7-VOC": "어휘", "P7-INTENT": "의도 파악", "P7-INS": "문장 위치", "P7-LINK": "연계",
}
ID_RE = {5: r"^RC-P5-\d{6}$", 6: r"^RC-P6-\d{6}$", 7: r"^RC-P7-\d{6}$"}
SET_RE = {6: r"^RC-P6-S-\d{4}$", 7: r"^RC-P7-[SDT]-\d{4}$"}
SET_SIZE = {(6, 1): (4, 4), (7, 1): (2, 4), (7, 2): (5, 5), (7, 3): (5, 5)}
REQUIRED = ["item_id", "part", "stem", "options", "answer", "type_tag", "difficulty_expert",
            "target_track", "vocab_level", "explanation_ko", "distractor_rationale", "key_point",
            "author_id", "source_note", "status", "version", "created_at"]
TRACKS = {"300-400", "400-450", "450-495"}

SCHEMA = """
CREATE TABLE tag_codes (
  code TEXT PRIMARY KEY, part INTEGER NOT NULL, category TEXT NOT NULL,
  category_ko TEXT NOT NULL, subcode TEXT NOT NULL
);
CREATE TABLE passage_sets (
  set_id TEXT PRIMARY KEY, part INTEGER NOT NULL, passage_type TEXT NOT NULL,
  passage_count INTEGER NOT NULL, business_context TEXT, fictional_entities TEXT,
  question_count INTEGER NOT NULL, source_file TEXT NOT NULL
);
CREATE TABLE passages (
  set_id TEXT NOT NULL REFERENCES passage_sets(set_id), seq INTEGER NOT NULL,
  title TEXT, passage_type TEXT, body TEXT NOT NULL, word_count INTEGER NOT NULL,
  PRIMARY KEY (set_id, seq)
);
CREATE TABLE items (
  item_id TEXT PRIMARY KEY, part INTEGER NOT NULL,
  set_id TEXT REFERENCES passage_sets(set_id), position_in_set INTEGER,
  stem TEXT NOT NULL, answer TEXT NOT NULL CHECK (answer IN ('A','B','C','D')),
  type_tag TEXT NOT NULL REFERENCES tag_codes(code), category TEXT NOT NULL,
  sub_tags TEXT, difficulty_expert INTEGER NOT NULL CHECK (difficulty_expert BETWEEN 1 AND 5),
  target_track TEXT NOT NULL, vocab_level TEXT NOT NULL,
  explanation_ko TEXT NOT NULL, evidence_quote TEXT, key_point TEXT NOT NULL,
  author_id TEXT NOT NULL, reviewer_1_id TEXT, reviewer_2_id TEXT, native_check_id TEXT,
  originality_check TEXT, source_note TEXT NOT NULL,
  status TEXT NOT NULL, version INTEGER NOT NULL, created_at TEXT NOT NULL,
  source_file TEXT NOT NULL
);
CREATE TABLE item_options (
  item_id TEXT NOT NULL REFERENCES items(item_id), label TEXT NOT NULL,
  body TEXT NOT NULL, is_answer INTEGER NOT NULL, rationale TEXT, trap_code TEXT,
  PRIMARY KEY (item_id, label)
);
CREATE TABLE item_tracks (
  item_id TEXT NOT NULL REFERENCES items(item_id), track TEXT NOT NULL,
  PRIMARY KEY (item_id, track)
);
CREATE TABLE vocab (
  word TEXT NOT NULL, pos TEXT NOT NULL, meaning_ko TEXT NOT NULL, level TEXT,
  PRIMARY KEY (word, pos)
);
CREATE TABLE item_vocab (
  item_id TEXT NOT NULL REFERENCES items(item_id), word TEXT NOT NULL, pos TEXT NOT NULL,
  PRIMARY KEY (item_id, word, pos)
);
CREATE TABLE word_cards (
  word_id TEXT PRIMARY KEY, lemma TEXT NOT NULL, pos TEXT NOT NULL, meaning_ko TEXT NOT NULL,
  meaning_ko_sub TEXT, examples TEXT NOT NULL, collocations TEXT NOT NULL, derivatives TEXT,
  confusables TEXT, paraphrases TEXT, type_tags TEXT NOT NULL, level TEXT NOT NULL,
  selection_note TEXT NOT NULL, author_id TEXT NOT NULL, reviewer_1_id TEXT,
  status TEXT NOT NULL, version INTEGER NOT NULL, created_at TEXT NOT NULL, source_file TEXT NOT NULL,
  UNIQUE (lemma, pos)
);
CREATE TABLE word_card_tags (
  word_id TEXT NOT NULL REFERENCES word_cards(word_id), type_tag TEXT NOT NULL,
  PRIMARY KEY (word_id, type_tag)
);
CREATE TABLE forms (form_id TEXT PRIMARY KEY, kind TEXT NOT NULL, routing TEXT, source_file TEXT NOT NULL);
CREATE TABLE form_slots (
  form_id TEXT NOT NULL REFERENCES forms(form_id), stage TEXT NOT NULL, seq INTEGER NOT NULL,
  item_id TEXT NOT NULL REFERENCES items(item_id), PRIMARY KEY (form_id, stage, seq)
);
CREATE TABLE vocab_check_items (
  form_id TEXT NOT NULL REFERENCES forms(form_id), seq INTEGER NOT NULL,
  word_id TEXT NOT NULL REFERENCES word_cards(word_id), level TEXT NOT NULL, phrase TEXT NOT NULL,
  options TEXT NOT NULL, answer TEXT NOT NULL, PRIMARY KEY (form_id, seq)
);
CREATE INDEX idx_cards_level ON word_cards(level, pos);
CREATE INDEX idx_items_part_tag ON items(part, type_tag);
CREATE INDEX idx_items_category ON items(part, category);
CREATE INDEX idx_tracks_track ON item_tracks(track);

CREATE VIEW v_items_by_part_type AS
  SELECT i.part, i.category, t.category_ko, i.type_tag, i.item_id, i.set_id,
         i.difficulty_expert, i.target_track, i.status, i.stem
  FROM items i JOIN tag_codes t ON t.code = i.type_tag
  ORDER BY i.part, i.category, i.type_tag, i.item_id;
CREATE VIEW v_tag_summary AS
  SELECT t.part, t.category, t.category_ko, t.code AS type_tag, COUNT(i.item_id) AS n_items,
         ROUND(AVG(i.difficulty_expert), 1) AS avg_difficulty
  FROM tag_codes t LEFT JOIN items i ON i.type_tag = t.code
  GROUP BY t.code ORDER BY t.part, t.category, t.code;
"""


def tag_rows():
    for part, cats in TAGS.items():
        for cat, subs in cats.items():
            for sub in subs:
                yield f"{cat}.{sub}", part, cat, CATEGORY_KO[cat], sub


def shingles(text, n=5):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def check_item(it, part, errors, set_ctx=None):
    iid = it.get("item_id", "?")
    for f in REQUIRED:
        if it.get(f) in (None, "", [], {}):
            errors.append(f"{iid}: 필수 필드 없음 `{f}`")
    if it.get("part") != part:
        errors.append(f"{iid}: part 불일치")
    if not re.match(ID_RE[part], iid):
        errors.append(f"{iid}: item_id 형식 오류")
    opts = it.get("options") or {}
    if sorted(opts) != ["A", "B", "C", "D"] or any(not str(v).strip() for v in opts.values()):
        errors.append(f"{iid}: 보기는 A~D 4개여야 함")
    if it.get("answer") not in ("A", "B", "C", "D"):
        errors.append(f"{iid}: answer 오류")
    if len(set(str(v).strip().lower() for v in opts.values())) < len(opts):
        errors.append(f"{iid}: 같은 보기가 중복됨")
    rat = it.get("distractor_rationale") or {}
    if sorted(rat) != ["A", "B", "C", "D"]:
        errors.append(f"{iid}: distractor_rationale는 보기 4개 모두 필요")
    tag = it.get("type_tag", "")
    cat, _, sub = tag.partition(".")
    if cat not in TAGS[part] or sub not in TAGS[part][cat]:
        errors.append(f"{iid}: 유형 태그 `{tag}`가 content-standard 4장에 없음")
    if not isinstance(it.get("difficulty_expert"), int) or not 1 <= it["difficulty_expert"] <= 5:
        errors.append(f"{iid}: difficulty_expert는 1~5 정수")
    tracks = it.get("target_track") or []
    if not tracks or not set(tracks) <= TRACKS:
        errors.append(f"{iid}: target_track 오류 {tracks}")
    if it.get("vocab_level") not in ("기초", "중급", "고급"):
        errors.append(f"{iid}: vocab_level 오류")
    if part in (6, 7):
        if not it.get("position_in_set"):
            errors.append(f"{iid}: position_in_set 없음")
        quote = (it.get("evidence_quote") or "").strip()
        if not quote:
            errors.append(f"{iid}: evidence_quote 없음 (P6·P7 필수)")
        elif set_ctx is not None and tag != "P6-INS.SENT":
            body = re.sub(r"\s+", " ", set_ctx)
            # 근거 인용은 지문에 있는 문장이어야 한다. 여러 곳 인용은 " / "로 나누고 조각마다 첫 12단어로 확인
            norm = lambda t: " ".join(re.sub(r"\[\d+\]", " ", t).replace("|", " ").split())
            hay = norm(body)
            for seg in quote.split(" / "):
                probe = " ".join(norm(seg).strip(' "“”').split()[:12])
                if probe and probe not in hay:
                    errors.append(f"{iid}: evidence_quote 조각이 지문에서 그대로 찾아지지 않음: {probe[:40]}…")


CARD_RE = {"기초": r"^VC-B-\d{4}$", "400": r"^VC-4-\d{4}$", "450": r"^VC-5-\d{4}$"}
CARD_POS = {"n", "v", "adj", "adv", "prep", "conj", "phr"}
CARD_REQUIRED = ["word_id", "lemma", "pos", "meaning_ko", "examples", "collocations", "type_tags",
                 "level", "selection_note", "author_id", "status", "version", "created_at"]


def load_cards(errors):
    cards = []
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "vocab", "*.json"))):
        rel = os.path.relpath(path, ROOT)
        try:
            data = json.load(open(path, encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: JSON 오류 {e}")
            continue
        for c in data.get("cards", []):
            wid = c.get("word_id", "?")
            for f in CARD_REQUIRED:
                if c.get(f) in (None, "", [], {}):
                    errors.append(f"{wid}: 필수 필드 없음 `{f}`")
            if c.get("level") not in CARD_RE or not re.match(CARD_RE[c.get("level")], wid):
                errors.append(f"{wid}: level과 word_id 형식 불일치")
            if c.get("pos") not in CARD_POS:
                errors.append(f"{wid}: pos `{c.get('pos')}` 오류")
            if c.get("level") in ("400", "450") and not c.get("derivatives") and not c.get("no_word_family"):
                errors.append(f"{wid}: 400 레벨부터 derivatives 필수 (어족이 없으면 no_word_family: true)")
            if not 1 <= len(c.get("examples") or []) <= 2 or any(not e.get("en") or not e.get("ko") for e in c.get("examples") or []):
                errors.append(f"{wid}: 예문은 1~2개, en·ko 모두 필요")
            if not 2 <= len(c.get("collocations") or []) <= 4:
                errors.append(f"{wid}: 콜로케이션은 2~4개")
            known = {code for code, *_ in tag_rows()}
            bad = [t for t in c.get("type_tags") or [] if t not in known]
            if bad:
                errors.append(f"{wid}: 유형 태그 오류 {bad}")
            cards.append((c, rel))
    ids = collections.Counter(c["word_id"] for c, _ in cards)
    errors += [f"{i}: word_id 중복" for i, n in ids.items() if n > 1]
    keys = collections.Counter((c.get("lemma", "").strip().lower(), c.get("pos")) for c, _ in cards)
    errors += [f"{k[0]} ({k[1]}): 같은 표제어·품사 카드 중복" for k, n in keys.items() if n > 1]
    return cards


def load_forms(errors, item_ids, card_ids):
    forms = []
    for path in sorted(glob.glob(os.path.join(ROOT, "content", "forms", "*.json"))):
        rel = os.path.relpath(path, ROOT)
        try:
            f = json.load(open(path, encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: JSON 오류 {e}")
            continue
        fid = f.get("form_id", "?")
        if "stage1" in f:
            if len(f["stage1"]) != 12:
                errors.append(f"{fid}: 1단계는 12문항이어야 함 ({len(f['stage1'])})")
            for mod in ("basic", "mid", "upper"):
                ids = (f.get("modules") or {}).get(mod, [])
                if len(ids) != 14:
                    errors.append(f"{fid}: {mod} 모듈은 14문항이어야 함 ({len(ids)})")
            used = f["stage1"] + sum(((f.get("modules") or {}).get(m, []) for m in ("basic", "mid", "upper")), [])
            errors += [f"{fid}: 없는 문항 {i}" for i in used if i not in item_ids]
            errors += [f"{fid}: 폼 안 중복 문항 {i}" for i, n in collections.Counter(used).items() if n > 1]
        for v in f.get("vocab_check", []):
            if v.get("word_id") not in card_ids:
                errors.append(f"{fid}: 어휘 체크 {v.get('seq')} 카드 없음 {v.get('word_id')}")
            if sorted(v.get("options") or {}) != ["A", "B", "C", "D"] or v.get("answer") not in "ABCD":
                errors.append(f"{fid}: 어휘 체크 {v.get('seq')} 보기/정답 오류")
        forms.append((f, rel))
    return forms


def load():
    errors, items, sets = [], [], []
    files = sorted(glob.glob(os.path.join(ROOT, "content", "items", "*", "*.json")))
    for path in files:
        rel = os.path.relpath(path, ROOT)
        try:
            data = json.load(open(path, encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{rel}: JSON 오류 {e}")
            continue
        for it in data.get("items", []):
            check_item(it, 5, errors)
            items.append((it, None, rel))
        for st in data.get("sets", []):
            sid, part = st.get("set_id", "?"), st.get("part")
            if part not in (6, 7) or not re.match(SET_RE[part], sid):
                errors.append(f"{sid}: set_id/part 오류")
                continue
            pcount = st.get("passage_count")
            if len(st.get("passages", [])) != pcount:
                errors.append(f"{sid}: passage_count와 지문 수 불일치")
            lo, hi = SET_SIZE.get((part, pcount), (0, 0))
            n = len(st.get("items", []))
            if not lo <= n <= hi:
                errors.append(f"{sid}: 문항 수 {n} (허용 {lo}~{hi})")
            if not st.get("fictional_entities"):
                errors.append(f"{sid}: fictional_entities 비어 있음")
            full = "\n".join(p.get("text", "") for p in st.get("passages", []))
            for it in st.get("items", []):
                check_item(it, part, errors, full)
                items.append((it, sid, rel))
            sets.append((st, rel))
    ids = collections.Counter(it["item_id"] for it, _, _ in items)
    errors += [f"{i}: item_id 중복" for i, c in ids.items() if c > 1]
    cards = load_cards(errors)
    forms = load_forms(errors, set(ids), {c["word_id"] for c, _ in cards})
    return files, sets, items, cards, forms, errors


def similarity_report(items, sets):
    """5-gram Jaccard로 내부 근접 중복 후보를 찾는다 (architecture.md 6장 5번)."""
    docs = {it["item_id"]: shingles(it["stem"] + " " + " ".join(it["options"].values()))
            for it, _, _ in items if it["part"] == 5}
    for st, _ in sets:
        docs[st["set_id"]] = shingles(" ".join(p["text"] for p in st["passages"]))
    keys, hits = sorted(docs), []
    for a in range(len(keys)):
        for b in range(a + 1, len(keys)):
            x, y = docs[keys[a]], docs[keys[b]]
            if x and y:
                j = len(x & y) / len(x | y)
                if j >= 0.3:
                    hits.append((keys[a], keys[b], round(j, 2)))
    return hits


def build(sets, items, cards, forms):
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA)
    con.executemany("INSERT INTO tag_codes VALUES (?,?,?,?,?)", list(tag_rows()))
    for st, rel in sets:
        con.execute("INSERT INTO passage_sets VALUES (?,?,?,?,?,?,?,?)", (
            st["set_id"], st["part"], st["passage_type"], st["passage_count"],
            st.get("business_context"), json.dumps(st.get("fictional_entities"), ensure_ascii=False),
            len(st["items"]), rel))
        for seq, p in enumerate(st["passages"], 1):
            con.execute("INSERT INTO passages VALUES (?,?,?,?,?,?)", (
                st["set_id"], seq, p.get("title"), p.get("type"), p["text"],
                len(re.findall(r"[A-Za-z0-9'’-]+", p["text"]))))
    for it, sid, rel in items:
        con.execute("INSERT INTO items VALUES (" + ",".join("?" * 25) + ")", (
            it["item_id"], it["part"], sid, it.get("position_in_set"), it["stem"], it["answer"],
            it["type_tag"], it["type_tag"].split(".")[0], json.dumps(it.get("sub_tags") or []),
            it["difficulty_expert"], ",".join(it["target_track"]), it["vocab_level"],
            it["explanation_ko"], it.get("evidence_quote") or "", it["key_point"],
            it["author_id"], it.get("reviewer_1_id"), it.get("reviewer_2_id"),
            it.get("native_check_id"), json.dumps(it.get("originality_check"), ensure_ascii=False),
            it["source_note"], it["status"], it["version"], it["created_at"], rel))
        traps = it.get("trap_code") or {}
        for lab in "ABCD":
            con.execute("INSERT INTO item_options VALUES (?,?,?,?,?,?)", (
                it["item_id"], lab, it["options"][lab], int(lab == it["answer"]),
                it["distractor_rationale"].get(lab), traps.get(lab)))
        for tr in it["target_track"]:
            con.execute("INSERT INTO item_tracks VALUES (?,?)", (it["item_id"], tr))
        for v in it.get("vocab") or []:
            if not v.get("word") or not v.get("meaning_ko"):
                continue
            key = (v["word"].strip().lower(), (v.get("pos") or "").strip())
            con.execute("INSERT OR IGNORE INTO vocab VALUES (?,?,?,?)",
                        (*key, v["meaning_ko"], v.get("level")))
            con.execute("INSERT OR IGNORE INTO item_vocab VALUES (?,?,?)", (it["item_id"], *key))
    dump = lambda v: json.dumps(v or [], ensure_ascii=False)
    for c, rel in cards:
        con.execute("INSERT INTO word_cards VALUES (" + ",".join("?" * 19) + ")", (
            c["word_id"], c["lemma"].strip(), c["pos"], c["meaning_ko"], c.get("meaning_ko_sub"),
            dump(c["examples"]), dump(c["collocations"]), dump(c.get("derivatives")),
            dump(c.get("confusables")), dump(c.get("paraphrases")), dump(c["type_tags"]), c["level"],
            c["selection_note"], c["author_id"], c.get("reviewer_1_id"), c["status"], c["version"],
            c["created_at"], rel))
        for t in c["type_tags"]:
            con.execute("INSERT OR IGNORE INTO word_card_tags VALUES (?,?)", (c["word_id"], t))
    for f, rel in forms:
        con.execute("INSERT INTO forms VALUES (?,?,?,?)", (
            f["form_id"], "placement" if "stage1" in f else "vocab_check",
            json.dumps(f.get("routing"), ensure_ascii=False), rel))
        stages = [("stage1", f.get("stage1", []))] + list((f.get("modules") or {}).items())
        for stage, ids in stages:
            for seq, iid in enumerate(ids, 1):
                con.execute("INSERT INTO form_slots VALUES (?,?,?,?)", (f["form_id"], stage, seq, iid))
        for v in f.get("vocab_check", []):
            con.execute("INSERT INTO vocab_check_items VALUES (?,?,?,?,?,?,?)", (
                f["form_id"], v["seq"], v["word_id"], v["level"], v["phrase"],
                json.dumps(v["options"], ensure_ascii=False), v["answer"]))
    con.commit()
    return con


def report(con, sim_hits):
    q = lambda sql: con.execute(sql).fetchall()
    lines = ["# 문항 DB 현황", "", f"DB: `db/toeic_rc.db` (SQLite). 다시 만들기: `python3 db/build_db.py`", ""]
    lines += ["## Part별", "", "| Part | 세트 | 문항 |", "|---|---|---|"]
    for part, n in q("SELECT part, COUNT(*) FROM items GROUP BY part"):
        ns = q(f"SELECT COUNT(*) FROM passage_sets WHERE part={part}")[0][0]
        lines.append(f"| {part} | {ns or '-'} | {n} |")
    lines += ["", "## 유형별", "", "| Part | 대분류 | 유형 태그 | 문항 수 | 평균 난이도 |", "|---|---|---|---|---|"]
    for part, cat, cat_ko, tag, n, avg in q("SELECT * FROM v_tag_summary WHERE n_items > 0"):
        lines.append(f"| {part} | {cat_ko} ({cat}) | {tag} | {n} | {avg} |")
    empty = [r[3] for r in q("SELECT * FROM v_tag_summary WHERE n_items = 0 AND type_tag NOT LIKE 'P6-GRAM.%'")]
    lines += ["", f"아직 문항이 없는 태그: {', '.join(empty) if empty else '없음'}"]
    lines += ["", "## 트랙별", "", "| 트랙 | 문항 |", "|---|---|"]
    lines += [f"| {t} | {n} |" for t, n in q("SELECT track, COUNT(*) FROM item_tracks GROUP BY track")]
    lines += ["", "## 정답 위치 분포 (Part별)", "", "| Part | A | B | C | D |", "|---|---|---|---|---|"]
    for part in (5, 6, 7):
        c = dict(q(f"SELECT answer, COUNT(*) FROM items WHERE part={part} GROUP BY answer"))
        lines.append(f"| {part} | " + " | ".join(str(c.get(k, 0)) for k in "ABCD") + " |")
    lines += ["", "## 상태", ""]
    lines += [f"- {s}: {n}" for s, n in q("SELECT status, COUNT(*) FROM items GROUP BY status")]
    lines += ["", f"## 어휘", "", f"- 등록 단어 {q('SELECT COUNT(*) FROM vocab')[0][0]}개, 문항-단어 연결 {q('SELECT COUNT(*) FROM item_vocab')[0][0]}건"]
    lines += ["", "## 어휘 카드 (레벨·품사별)", "", "| 레벨 | n | v | adj | adv | 기타 | 합계 |", "|---|---|---|---|---|---|---|"]
    for lv in ("기초", "400", "450"):
        c = dict(q(f"SELECT pos, COUNT(*) FROM word_cards WHERE level='{lv}' GROUP BY pos"))
        if c:
            etc = sum(n for p, n in c.items() if p not in ("n", "v", "adj", "adv"))
            lines.append(f"| {lv} | {c.get('n', 0)} | {c.get('v', 0)} | {c.get('adj', 0)} | {c.get('adv', 0)} | {etc} | {sum(c.values())} |")
    linked = q("SELECT COUNT(DISTINCT w.word_id) FROM word_cards w JOIN item_vocab iv ON iv.word = LOWER(w.lemma)")[0][0]
    lines += ["", f"- 문항 은행 어휘와 연결된 카드: {linked}개"]
    lines += ["", "## 폼", ""]
    for fid, kind in q("SELECT form_id, kind FROM forms"):
        parts = q(f"SELECT fs.stage, COUNT(*), GROUP_CONCAT(DISTINCT i.part) FROM form_slots fs JOIN items i ON i.item_id = fs.item_id WHERE fs.form_id='{fid}' GROUP BY fs.stage")
        nv = q(f"SELECT COUNT(*) FROM vocab_check_items WHERE form_id='{fid}'")[0][0]
        lines.append(f"- {fid} ({kind}): " + ", ".join(f"{st} {n}문항 (Part {p})" for st, n, p in parts) + (f", 어휘 체크 {nv}문항" if nv else ""))
    lines += ["", "## 내부 유사도 (5-gram Jaccard ≥ 0.3)", ""]
    lines += [f"- {a} ↔ {b}: {j}" for a, b, j in sim_hits] or ["- 후보 없음"]
    open(REPORT_PATH, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def main():
    files, sets, items, cards, forms, errors = load()
    if not files:
        print("content/items 아래에 문항 파일이 없습니다.")
        return 1
    if errors:
        print(f"검증 실패 {len(errors)}건:")
        print("\n".join("- " + e for e in errors))
        return 1
    con = build(sets, items, cards, forms)
    report(con, similarity_report(items, sets))
    print(f"OK: 파일 {len(files)}개, 세트 {len(sets)}개, 문항 {len(items)}개, 어휘 카드 {len(cards)}개, 폼 {len(forms)}개 → {os.path.relpath(DB_PATH, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
