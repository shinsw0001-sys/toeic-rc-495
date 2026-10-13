"""배치고사 · 필수 학습 범위 · 어휘 SRS 학습 로직 v0 참조 구현 (S1-14).

설계 문서: docs/architecture-placement-vocab.md (명세: docs/specs/placement-and-vocab.md)
- 운영 코드는 TypeScript(packages/learning)로 옮긴다. 이 파일은 계산 규칙을 고정하는 기준 구현이다.
- 모든 함수는 순수 함수다 (DB·시계·난수 없음. 오늘 날짜는 인자로 받는다).
- 숫자는 전부 [가정]이며 CONFIG로 모았다. 파일럿·베타 데이터로 바꾼다.

실행: python3 db/logic_v0.py   (표준 라이브러리만 사용, 자체 테스트 실행)
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# 설정 [가정]
# ---------------------------------------------------------------------------
CONFIG = {
    "version": "scope-v0.1",
    # architecture 7.5.2 예측 모델
    "guess_c": 0.20,
    "b": {1: -2.5, 2: -1.5, 3: -0.2, 4: 0.8, 5: 1.8},
    "prior_mean": 330, "prior_sd": 100,
    # 명세 1.3 2단계 분기 (1단계 12문항 정답 수 기준)
    "routing_cuts": [(5, "basic"), (8, "mid"), (12, "upper")],
    # 명세 2.3 분류 문턱
    "must_min_p": 12, "later_max_p": 4,
    # 명세 2.3 C 기준: 단위 문항의 목표 점수 예상 정답률 평균
    "c_high": 0.70, "c_low": 0.50,
    # 명세 2.3 보정 규칙 2: 용량
    "vocab_minutes": {15: 3, 25: 5, 40: 7},
    "mock_minutes": 100,            # 풀이 75 + 리뷰 25
    "review_share": 0.25,
    "challenge_pts_per_week": 15,   # 명세 2.1
    # 명세 3.5 어휘
    "srs_intervals": [1, 3, 7, 14],
    "known_check_days": 14,
    "daily_new": {15: 8, 25: 12, 40: 15},
    "review_soft_cap": 40,
    "auto_add_daily_cap": 5,
    "sec_per_new": 12, "sec_per_review": 3,   # 시간 가드용 [가정, 파일럿 실측]
}

LEVELS = ["basic", "400", "450", "495"]


# ---------------------------------------------------------------------------
# 예측 모델 (architecture 7.5.2 재사용)
# ---------------------------------------------------------------------------
def p_correct(score: float, difficulty: int, cfg=CONFIG) -> float:
    theta = (score - 400) / 50
    z = theta - cfg["b"][difficulty]
    return cfg["guess_c"] + (1 - cfg["guess_c"]) / (1 + math.exp(-z))


def route_stage1(correct: int, cfg=CONFIG) -> str:
    """1단계 정답 수(0~12) → 2단계 모듈. 미응답은 오답으로 센다."""
    if not 0 <= correct <= 12:
        raise ValueError("stage-1 correct must be 0..12")
    for upper, module in cfg["routing_cuts"]:
        if correct <= upper:
            return module
    raise AssertionError


# ---------------------------------------------------------------------------
# 필수 학습 범위 (명세 2장)
# ---------------------------------------------------------------------------
def contribution_c(difficulties: list[int], target_rc: int, cfg=CONFIG) -> int:
    """단위 문항 난이도 분포 → C(1~3). 목표 점수에서 예상 정답률 평균으로 판정."""
    if not difficulties:
        return 2
    mean_p = sum(p_correct(target_rc, d, cfg) for d in difficulties) / len(difficulties)
    if mean_p >= cfg["c_high"]:
        return 3
    if mean_p < cfg["c_low"]:
        return 1
    return 2


def weakness_w(strength: str) -> int:
    """강약점 → W. 판단 보류는 모르므로 2 (명세 2.3)."""
    return {"weak": 3, "normal": 2, "hold": 2, "strong": 1}[strength]


def bucket_of(p: int, cfg=CONFIG) -> str:
    if p >= cfg["must_min_p"]:
        return "must"
    if p <= cfg["later_max_p"]:
        return "later"
    return "recommended"


def new_learning_capacity(weeks: int, daily_minutes: int, study_days: int = 5,
                          has_mock: bool = True, cfg=CONFIG) -> float:
    """신규 학습 용량(분) = (총 − 어휘 − 모의고사) × (1 − 복습 몫)."""
    sessions = weeks * study_days
    rc = sessions * (daily_minutes - cfg["vocab_minutes"][daily_minutes])
    rc -= cfg["mock_minutes"] if has_mock else 0
    return max(0.0, rc * (1 - cfg["review_share"]))


def phase_weeks(weeks: int) -> tuple[int, int, int]:
    """architecture 7.3 기초 40 · 확장 40 · 실전 20 → 주 수 (내림, 각 1주 이상 가능할 때)."""
    if weeks <= 2:
        return (1, 0, weeks - 1) if weeks == 2 else (1, 0, 0)
    f = max(1, math.floor(weeks * 0.4))
    e = max(1, math.floor(weeks * 0.4))
    return f, e, weeks - f - e


def is_challenging(current_mid: int, target_rc: int, weeks: int, cfg=CONFIG) -> bool:
    return weeks <= 0 or (target_rc - current_mid) / weeks > cfg["challenge_pts_per_week"]


@dataclass
class Unit:
    unit_id: str
    label_ko: str
    F: int
    C: int
    W: int
    minutes: int              # 기본 분량. 어휘 단위는 0 (별도 용량)
    is_vocab: bool = False
    completed: bool = False


@dataclass
class ScopeRow:
    unit_id: str
    label_ko: str
    F: int
    C: int
    W: int
    P: int
    bucket: str               # must / recommended / later / done
    minutes: int
    week: int | None          # None = 배치 안 함 ("시간 남으면" 또는 나중에)
    flags: list[str] = field(default_factory=list)   # maintain, demoted, overflow, vocab
    reason_ko: str = ""


def _reason(u: Unit, target_rc: int) -> str:
    w = {3: "약점", 2: "보통·판단 보류", 1: "강점"}[u.W]
    c = {3: f"목표 {target_rc}에서 맞혀야 하는 유형", 2: f"목표 {target_rc}에서 일부 필요",
         1: f"목표 {target_rc}에서는 고난도"}[u.C]
    f = {3: "자주 나옴", 2: "보통 빈도", 1: "드묾"}[u.F]
    return f"{w} · {c} · {f}"


def score_scope(units: list[Unit], target_rc: int, weeks: int, daily_minutes: int,
                study_days: int = 5, has_mock: bool = True, cfg=CONFIG) -> dict:
    """P = F × C × W → 분류 → 용량 강등 → 주차 배치. 반환: rows(순위순), 요약."""
    cap = new_learning_capacity(weeks, daily_minutes, study_days, has_mock, cfg)
    f_w, e_w, _ = phase_weeks(weeks)
    fe_weeks = max(1, f_w + e_w)
    weekly = cap / fe_weeks if cap > 0 else 0

    rows: list[ScopeRow] = []
    for u in units:
        for v in (u.F, u.C, u.W):
            if v not in (1, 2, 3):
                raise ValueError(f"{u.unit_id}: F/C/W must be 1..3")
        p = u.F * u.C * u.W
        r = ScopeRow(u.unit_id, u.label_ko, u.F, u.C, u.W, p, bucket_of(p, cfg),
                     u.minutes, None, [], _reason(u, target_rc))
        if u.completed:
            r.bucket, r.reason_ko = "done", "완료 · 간격 복습으로만 나와요"
        elif u.is_vocab:
            r.flags.append("vocab")          # 어휘 블록 별도 용량
        elif u.F == 3 and u.C == 3 and u.W == 1:
            r.bucket = "recommended"          # 보정 1: 유지 (P=9)
            r.flags.append("maintain")
            r.reason_ko = "강점 유지 · 간격 복습만 해요"
        rows.append(r)

    # 정렬: P 내림차순, 동점이면 W(지금 약한 것 먼저) → C → F 내림차순, 마지막은 입력 순서 (안정 정렬)
    order = {"must": 0, "recommended": 1, "later": 2, "done": 3}
    rows.sort(key=lambda r: (order[r.bucket], -r.P, -r.W, -r.C, -r.F))

    def needs_capacity(r: ScopeRow) -> bool:
        return "vocab" not in r.flags and "maintain" not in r.flags

    # 보정 2: 필수 합이 용량 초과 → P 낮은 필수부터 권장으로
    musts = [r for r in rows if r.bucket == "must" and needs_capacity(r)]
    total = sum(r.minutes for r in musts)
    demoted = 0
    for r in reversed(musts):
        if total <= cap + 1e-9:
            break
        r.bucket = "recommended"
        r.flags.append("demoted")
        r.reason_ko = "기간이 짧아 필수에서 권장으로 옮겼어요 · " + r.reason_ko
        total -= r.minutes
        demoted += 1
    rows.sort(key=lambda r: (order[r.bucket], "demoted" in r.flags, -r.P, -r.W, -r.C, -r.F))

    # 주차 배치: 필수 → 권장 순서로 쌓고, 단위 분량의 중간 지점이 들어가는 주에 둔다 (기초·확장 주에만)
    used = 0.0
    for r in rows:
        if "vocab" in r.flags:
            r.week = 1 if r.bucket != "later" else None
            continue
        if r.bucket not in ("must", "recommended") or not needs_capacity(r):
            continue
        if used + r.minutes <= cap + 1e-9:
            used += r.minutes
            r.week = min(fe_weeks, max(1, math.ceil((used - r.minutes / 2) / weekly - 1e-9)))
        else:
            r.flags.append("overflow")       # 권장 중 용량 초과 → "시간 남으면"
    must_minutes = sum(r.minutes for r in rows if r.bucket == "must" and needs_capacity(r))
    notes = []
    if demoted:
        notes.append(f"기간이 짧아 필수 범위 중 {demoted}개를 권장으로 옮겼어요")
    return {"capacity": cap, "must_minutes": must_minutes, "used_minutes": used,
            "demoted": demoted, "fe_weeks": fe_weeks, "rows": rows, "notes": notes,
            "config_version": cfg["version"]}


# ---------------------------------------------------------------------------
# 어휘 SRS (명세 3.4~3.5)
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class VocabState:
    word_id: str
    status: str               # queued / learning / known_check / mastered
    step: int                 # learning: 0..3 = 다음 간격 인덱스 (1·3·7·14일)
    due_on: date | None
    source: str = "plan"      # placement / plan / wrong_answer / manual
    lapses: int = 0


def start_learning(word_id: str, today: date, source: str = "plan") -> VocabState:
    """신규 학습(또는 '헷갈려요/몰라요') → 1일 뒤 첫 복습."""
    return VocabState(word_id, "learning", 0, today + timedelta(days=1), source)


def first_exposure(word_id: str, answer: str, quiz_correct: bool | None, today: date,
                   source: str = "plan", cfg=CONFIG) -> VocabState:
    """첫 노출 거르기. answer ∈ {'know','unsure','unknown'}."""
    if answer == "know":
        if quiz_correct:
            return VocabState(word_id, "known_check", 3, today + timedelta(days=cfg["known_check_days"]), source)
        return start_learning(word_id, today, source)
    return start_learning(word_id, today, source)


def review(state: VocabState, correct: bool, today: date, cfg=CONFIG) -> VocabState:
    """복습 결과 반영. 맞히면 다음 간격, 틀리면 1일로. 14일 단계 통과 → mastered."""
    iv = cfg["srs_intervals"]
    if state.status not in ("learning", "known_check"):
        raise ValueError(f"cannot review state {state.status}")
    if not correct:
        return replace(state, status="learning", step=0, due_on=today + timedelta(days=iv[0]),
                       lapses=state.lapses + 1)
    if state.step >= len(iv) - 1:
        return replace(state, status="mastered", step=len(iv) - 1, due_on=None)
    nxt = state.step + 1
    return replace(state, status="learning", step=nxt, due_on=today + timedelta(days=iv[nxt]))


def auto_add_from_wrong(existing: dict[str, VocabState], words: list[str], today: date,
                        added_today: int, cfg=CONFIG) -> tuple[dict[str, VocabState], list[str], list[str]]:
    """오답 원인 '② 어휘' → 내 단어 추가. 이미 있으면 새로 만들지 않고 1일 단계로 되돌린다.
    반환: (새 상태 dict, 오늘 추가·리셋한 단어, 내일로 넘긴 단어). 하루 cap은 신규 추가에만 적용."""
    out = dict(existing)
    done, deferred = [], []
    for w in dict.fromkeys(words):            # 같은 호출 안 중복 제거, 순서 유지
        if w in out and out[w].status != "queued":
            out[w] = replace(out[w], status="learning", step=0, due_on=today + timedelta(days=1))
            done.append(w)
        elif added_today < cfg["auto_add_daily_cap"]:
            out[w] = VocabState(w, "queued", 0, today, "wrong_answer")   # 오늘 신규 카드 맨 앞 후보
            added_today += 1
            done.append(w)
        else:
            out[w] = VocabState(w, "queued", 0, today + timedelta(days=1), "wrong_answer")
            deferred.append(w)
    return out, done, deferred


def select_daily_vocab(states: list[VocabState], candidates: list[dict], daily_minutes: int,
                       today: date, cfg=CONFIG) -> dict:
    """그날 어휘 블록. states = 사용자 단어 상태, candidates = 아직 안 배운 레벨 카드
    [{'word_id','required_tag':bool,'freq':int}] (빈도순 정렬 불필요).
    순서: 복습(밀린 순) → 신규(수동 → 오답 → 필수 태그 겹침 → 빈도순)."""
    due = sorted((s for s in states if s.status in ("learning", "known_check")
                  and s.due_on is not None and s.due_on <= today),
                 key=lambda s: (s.due_on, s.step, s.word_id))
    quota = cfg["daily_new"][daily_minutes]
    if len(due) > cfg["review_soft_cap"]:
        quota = max(0, quota - (len(due) - cfg["review_soft_cap"]))
    src_rank = {"manual": 0, "wrong_answer": 1}
    queued = sorted((s for s in states if s.status == "queued" and s.due_on is not None and s.due_on <= today),
                    key=lambda s: (src_rank.get(s.source, 2), s.due_on, s.word_id))
    have = {s.word_id for s in states}
    fresh = sorted((c for c in candidates if c["word_id"] not in have),
                   key=lambda c: (not c.get("required_tag", False), -c.get("freq", 0), c["word_id"]))
    new = [s.word_id for s in queued] + [c["word_id"] for c in fresh]
    new = new[:quota]
    # 시간 가드: 어휘 블록 시간 안에 들어가게 신규 → 복습 순으로 줄인다
    budget = cfg["vocab_minutes"][daily_minutes] * 60
    reviews = [s.word_id for s in due]
    cost = lambda n, r: n * cfg["sec_per_new"] + r * cfg["sec_per_review"]
    while new and cost(len(new), len(reviews)) > budget:
        new.pop()
    while reviews and cost(len(new), len(reviews)) > budget:
        reviews.pop()
    return {"reviews": reviews, "new": new, "carried_reviews": len(due) - len(reviews),
            "seconds": cost(len(new), len(reviews))}


# ---------------------------------------------------------------------------
# 자체 테스트
# ---------------------------------------------------------------------------
def _p1_units() -> list[Unit]:
    """명세 2.5 P1 김민지 예시 표 (F·C·W는 명세의 예시값)."""
    t = [
        (1, "품사 자리: 명사·동사", 3, 3, 3, 30), (2, "품사 자리: 형용사·부사", 3, 3, 3, 30),
        (3, "시제", 3, 3, 3, 30), (4, "어휘 400 레벨", 3, 3, 3, 0),
        (5, "수 일치", 2, 3, 3, 30), (6, "능동·수동", 2, 3, 3, 30),
        (7, "전치사 vs 접속사", 3, 3, 2, 30), (8, "Part 7 세부 사항·수치", 3, 3, 2, 45),
        (9, "to부정사·동명사·분사", 2, 2, 3, 30), (10, "Part 6 문맥 시제·접속부사", 2, 3, 2, 30),
        (11, "관계사", 2, 2, 2, 30), (12, "Part 7 추론", 2, 2, 2, 45),
        (13, "비교·최상급", 2, 2, 2, 30), (14, "Part 7 NOT·TRUE", 2, 2, 2, 45),
        (15, "Part 7 주제·목적", 2, 3, 1, 45), (16, "Part 6 문장 삽입", 2, 1, 2, 45),
        (17, "Part 7 이중·삼중 연계", 2, 1, 2, 45), (18, "문자·채팅 의도 파악", 1, 2, 2, 45),
        (19, "도치·가정법", 1, 1, 2, 30),
    ]
    return [Unit(f"U{n}", l, f, c, w, m, is_vocab=(n == 4)) for n, l, f, c, w, m in t]


def _selftest() -> None:
    checks = 0

    def eq(a, b, msg):
        nonlocal checks
        assert a == b, f"{msg}: expected {b!r}, got {a!r}"
        checks += 1

    # 1) 분기
    for n, m in [(0, "basic"), (5, "basic"), (6, "mid"), (8, "mid"), (9, "upper"), (12, "upper")]:
        eq(route_stage1(n), m, f"route {n}")
    exp = lambda s: 3 * p_correct(s, 2) + 6 * p_correct(s, 3) + 3 * p_correct(s, 4)
    eq(all(abs(exp(s) - v) < 0.06 for s, v in [(300, 4.1), (350, 5.7), (400, 7.8), (450, 9.6)]), True,
       "명세 1.3 예상 정답 수 (300≈4.1, 350≈5.7, 400≈7.8, 450≈9.6)")

    # 2) C 기여도 (명세 2.4)
    eq(contribution_c([1, 2, 3], 400), 3, "C 400 d1-3")
    eq(contribution_c([3, 3], 400), 2, "C 400 d3")
    eq(contribution_c([4, 5], 400), 1, "C 400 d4-5")
    eq(contribution_c([2, 3, 4], 450), 3, "C 450 d2-4")
    eq(contribution_c([5], 450), 1, "C 450 d5")

    # 3) 분류 문턱: P 가능한 값 전부
    for p, b in [(27, "must"), (18, "must"), (12, "must"), (9, "recommended"), (8, "recommended"),
                 (6, "recommended"), (4, "later"), (3, "later"), (2, "later"), (1, "later")]:
        eq(bucket_of(p), b, f"bucket {p}")

    # 4) P1 예시: 현재 320, 목표 400, 6주, 하루 25분
    eq(is_challenging(320, 400, 6), False, "P1 도전 목표 아님 (13.3점/주)")
    eq(is_challenging(320, 450, 6), True, "목표 450이면 도전적 (21.7점/주)")
    eq(new_learning_capacity(6, 25), 375.0, "P1 용량")
    eq(phase_weeks(6), (2, 2, 2), "6주 단계")
    res = score_scope(_p1_units(), 400, 6, 25)
    by = {r.unit_id: r for r in res["rows"]}
    expect = {  # unit: (P, bucket, week)
        "U1": (27, "must", 1), "U2": (27, "must", 1), "U3": (27, "must", 1), "U4": (27, "must", 1),
        "U5": (18, "must", 2), "U6": (18, "must", 2), "U7": (18, "must", 2),
        "U8": (18, "must", 3), "U9": (12, "must", 3), "U10": (12, "must", 3),
        "U11": (8, "recommended", 4), "U12": (8, "recommended", 4),
        "U13": (8, "recommended", None), "U14": (8, "recommended", None),
        "U15": (6, "recommended", None),
        "U16": (4, "later", None), "U17": (4, "later", None), "U18": (4, "later", None),
        "U19": (2, "later", None),
    }
    for uid, (p, b, w) in expect.items():
        eq((by[uid].P, by[uid].bucket, by[uid].week), (p, b, w), f"P1 {uid}")
    eq(res["must_minutes"], 285, "P1 필수 소계 285분")
    eq(round(res["must_minutes"] / res["capacity"], 2), 0.76, "필수 = 용량의 76%")
    eq(sorted(u for u in by if "overflow" in by[u].flags), ["U13", "U14", "U15"], "P1 시간 남으면")
    eq(res["demoted"], 0, "P1 강등 없음")

    # 5) 같은 사람 4주: 용량 225, 필수 9·10 강등
    res4 = score_scope(_p1_units(), 400, 4, 25)
    by4 = {r.unit_id: r for r in res4["rows"]}
    eq(res4["capacity"], 225.0, "4주 용량")
    eq(res4["demoted"], 2, "4주 강등 수")
    eq(sorted(u for u in by4 if "demoted" in by4[u].flags), ["U10", "U9"], "4주 강등 단위")
    eq(res4["must_minutes"], 225, "4주 필수 합")
    eq(res4["notes"], ["기간이 짧아 필수 범위 중 2개를 권장으로 옮겼어요"], "4주 안내 문구")
    eq(all(by4[u].week is None for u in ["U9", "U10", "U11", "U12", "U13", "U14", "U15"]), True,
       "4주 권장 전부 시간 남으면")

    # 6) 유지 규칙: F3 C3 W1 → 권장(유지), 용량 안 씀
    r = score_scope([Unit("M", "강점 유형", 3, 3, 1, 30)], 400, 6, 25)["rows"][0]
    eq((r.P, r.bucket, "maintain" in r.flags, r.week), (9, "recommended", True, None), "유지 규칙")

    # 7) SRS 1·3·7·14
    d0 = date(2026, 10, 13)
    s = start_learning("postpone", d0)
    eq((s.step, s.due_on), (0, date(2026, 10, 14)), "신규 → 1일")
    s = review(s, True, date(2026, 10, 14)); eq((s.step, s.due_on), (1, date(2026, 10, 17)), "→ 3일")
    s = review(s, True, date(2026, 10, 17)); eq((s.step, s.due_on), (2, date(2026, 10, 24)), "→ 7일")
    s = review(s, True, date(2026, 10, 24)); eq((s.step, s.due_on), (3, date(2026, 11, 7)), "→ 14일")
    s2 = review(s, False, date(2026, 11, 7)); eq((s2.status, s2.step, s2.due_on, s2.lapses),
                                                ("learning", 0, date(2026, 11, 8), 1), "틀리면 1일로")
    s = review(s, True, date(2026, 11, 7)); eq((s.status, s.due_on), ("mastered", None), "14일 통과 → 익힌 단어")
    late = review(start_learning("x", d0), True, date(2026, 10, 20))
    eq(late.due_on, date(2026, 10, 23), "밀린 복습은 실제 복습일 기준")
    k = first_exposure("eligible", "know", True, d0)
    eq((k.status, k.due_on), ("known_check", date(2026, 10, 27)), "아는 단어 → 14일 뒤 1회")
    eq(review(k, True, date(2026, 10, 27)).status, "mastered", "아는 단어 확인 통과")
    eq(first_exposure("eligible", "know", False, d0).due_on, date(2026, 10, 14), "알아요+퀴즈 오답 → 신규 학습")

    # 8) 오답 자동 추가: 하루 5개, 기존 단어는 리셋
    existing = {"install": review(start_learning("install", d0), True, date(2026, 10, 14))}
    out, done, deferred = auto_add_from_wrong(existing, ["install", "a", "b", "c", "d", "e", "f"], d0, 0)
    eq(out["install"].step, 0, "기존 단어 1일로 리셋")
    eq((len(done), deferred), (6, ["f"]), "하루 5개 + 리셋 1개, 1개 이월")

    # 9) 하루 선택: 25분 → 신규 12, 복습 41개면 신규 11
    cands = [{"word_id": f"w{i:03d}", "required_tag": i % 10 == 0, "freq": 100 - i} for i in range(60)]
    sel = select_daily_vocab([], cands, 25, d0)
    eq(len(sel["new"]), 12, "25분 신규 12")
    eq(sel["new"][:3], ["w000", "w010", "w020"], "필수 태그 겹치는 단어 먼저")
    dues = [VocabState(f"r{i}", "learning", 1, d0 - timedelta(days=i % 3)) for i in range(41)]
    sel = select_daily_vocab(dues, cands, 25, d0)
    eq((len(sel["new"]), len(sel["reviews"])), (11, 41), "복습 41 → 신규 11")
    eq(sel["seconds"] <= 300, True, "25분 플랜 어휘 5분 안")
    man = [VocabState("m1", "queued", 0, d0, "manual"), VocabState("e1", "queued", 0, d0, "wrong_answer")]
    eq(select_daily_vocab(man, cands, 15, d0)["new"][:2], ["m1", "e1"], "수동 → 오답 순서")

    print(f"self-test OK: {checks} checks passed")
    print(f"P1 (RC 320 → 400, 6주, 하루 25분): 용량 {res['capacity']:.0f}분, 필수 {res['must_minutes']}분")
    for r in res["rows"]:
        wk = f"{r.week}주" if r.week else ("시간 남으면" if "overflow" in r.flags else "–")
        print(f"  {r.unit_id:>4} P={r.P:>2} {r.bucket:<11} {wk:<6} {r.label_ko}")
    print(f"P1 4주: {res4['notes'][0]}")


if __name__ == "__main__":
    _selftest()
