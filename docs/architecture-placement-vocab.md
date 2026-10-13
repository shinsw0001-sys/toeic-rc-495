# S1-14 배치고사 · 필수 학습 범위 · 어휘 추천 — 데이터 모델과 학습 로직 v0

- 작성: Developer / 보고 대상: Chief of Staff / 작성일: 2026-10-13 / 버전: v0.1 (초안)
- 입력: `docs/specs/placement-and-vocab.md`(S1-12, 이하 **명세**), `docs/architecture.md`(S1-07, 이하 **arch**: 5장 스키마, 7장 로직), `db/build_db.py`(SQLite 문항 은행 적재기), `content/SCHEMA.md`
- 산출물: 이 문서 + `db/logic_v0.py`(범위 점수·주차 배치·어휘 SRS·하루 어휘 선택의 참조 구현, 자체 테스트 포함)
- 표기: **[제안]** 승인 전 / **[가정]** 개발자가 정한 기본값 / **[확인 필요]** / **[추정]**. 명세에서 가져온 숫자는 명세 절 번호를 붙인다.
- 범위: 설계와 참조 구현만 다룬다. `architecture.md`, `build_db.py`, 콘텐츠 파일은 고치지 않았다. 패키지 설치와 커밋은 하지 않았다.

## 0. 가정

1. arch 0장 가정(1~2명 개발, TypeScript, Supabase Postgres)을 그대로 따른다. `PLAN.md`는 여전히 없다. 내용이 충돌하면 PLAN.md가 우선한다.
2. 이 문서의 DDL은 arch 5장 DDL에 **더하는 마이그레이션**이다. arch 테이블을 바꿔야 하는 곳은 `alter`로 적었다.
3. 학습 로직은 arch 7장 원칙(순수 함수 + 설정 파일, `packages/learning`)을 따른다. 숫자는 모두 설정값이고, 출처가 명세면 명세 값을 그대로 쓴다.
4. `db/logic_v0.py`는 **기준 구현**이다. 운영 코드는 TypeScript로 옮기고, 4장 테스트 표를 Vitest로 그대로 옮겨 두 구현이 같은 답을 내는지 맞춘다.

---

## 1. 결론 요약

| 항목 | 결정 [제안] |
|---|---|
| 배치고사 폼 | arch `forms`에 `kind='placement'`를 더하고, **모듈 테이블(`form_modules`)과 분기 규칙(`forms.routing` jsonb)** 을 붙인다. 응답은 기존 `attempts`(context `diagnostic`)를 그대로 쓴다. 분기 결과는 `sittings`에 고정한다 |
| 배치 결과 | `placement_results`(범위·신뢰도·모듈·어휘 레벨) + `placement_tag_strength`(대분류별 근거 수·부족분·약점/보통/강점/판단 보류). 첫 예측은 arch `predictions`에 `trigger='diagnostic'`으로 같이 넣는다 |
| 목표·범위 | `user_goals`(목표 RC) → `study_units`(학습 단위 ≈ 45) + `unit_frequency`(F표) → **`scope_snapshots` / `scope_units`** (F·C·W·P·분류·이유·주차를 계산 시점마다 덮어쓰지 않고 쌓는다). 변경 한 줄은 arch `plan_changes`에 남긴다 |
| 어휘 카드 | 문항과 같은 패턴: `word_cards`(정체성·상태) + `word_card_versions`(불변 내용). 오답에서 만든 **간이 카드**는 `kind='stub'`으로 같은 테이블에 둔다 |
| 사용자 어휘 | `user_vocab`(단계·다음 날짜·출처·아는 단어 여부), `vocab_quiz_attempts`(어휘 응답, **`attempts`와 분리** → 예측에 안 섞임), `vocab_auto_adds`(오답 자동 추가 기록, 하루 5개 상한 계산용) |
| 로직 | 분기(정답 수 컷), RC 범위(arch 7.5 그대로 + 명세 1.6 신뢰도 반폭), 대분류 강약점(부족분, 근거 < 2 = 판단 보류), 범위 점수(P = F×C×W, ≥12/6~9/≤4, 용량 강등, **중간 지점 주차 배치**), 어휘 SRS(1·3·7·14) |
| 검증 | `python3 db/logic_v0.py` → **명세 2.5 P1 예시(6주·4주) 그대로 재현, 73개 확인 통과** |
| 공수 | 로직·DB·API **약 1.4 인-스프린트**, 화면 포함 **약 2.7**. 명세 5.3 추정(+3)과 비슷하다. F11 축소판이면 **약 2.0** |

---

## 2. 스키마 추가 (Postgres DDL 초안)

### 2.1 공통 타입과 기존 테이블 변경

```sql
create type placement_module as enum ('basic','mid','upper');           -- 명세 1.3 2단계 모듈
create type tag_strength     as enum ('weak','normal','strong','hold');  -- 약점/보통/강점/판단 보류
create type scope_bucket     as enum ('must','recommended','later','done'); -- 필수/권장/나중에/완료
create type card_level       as enum ('basic','l400','l450','l495');     -- 명세 3.2 (문항 vocab_level과 다름, 2.8 참조)
create type word_pos         as enum ('n','v','adj','adv','prep','conj','phr');  -- 명세 3.3

-- arch 5.2 forms: 배치고사·어휘 체크 폼 추가
alter table forms drop constraint forms_kind_check;
alter table forms add constraint forms_kind_check
  check (kind in ('diagnostic','mock','placement','vocab_check'));
alter table forms add column form_group text check (form_group in ('A','B'));  -- 재배치는 B폼 1회 (arch 7.1)
alter table forms add column paired_form_id text references forms;            -- PLACE-A ↔ VCHK-A
alter table forms add column routing jsonb;          -- placement 전용. 아래 예시
alter table forms add column config_version text;    -- 분기 컷 버전 (파일럿 후 재조정 이력)
-- routing 예: {"from_module":"S1","rule":"stage1_correct",
--              "cuts":[{"max":5,"to":"basic"},{"max":8,"to":"mid"},{"max":12,"to":"upper"}]}

-- 폼 안의 단계·모듈. 1단계 공통 블록도 모듈 하나('S1')로 둔다
create table form_modules (
  form_id      text references forms on delete cascade,
  module_code  text not null,                    -- 'S1','basic','mid','upper'
  stage        smallint not null check (stage in (1,2)),
  level        placement_module,                 -- stage 2만
  item_count   smallint not null,                -- S1=12, 모듈=14
  rec_seconds  int,                              -- 페이스 안내용 (S1 420초). 타이머는 forms.time_limit_sec 하나
  primary key (form_id, module_code),
  check ((stage = 1 and level is null) or (stage = 2 and level is not null))
);
alter table form_slots add column module_code text;      -- placement 폼에서 필수 (가져오기 검증)
alter table form_slots add foreign key (form_id, module_code) references form_modules;

-- 어휘 체크 문항 (명세 1.4). 카드에서 만들지만 검수된 고정 문항으로 저장한다 (qa가 폼 전체를 미리 봄)
create table vocab_check_slots (
  form_id     text references forms on delete cascade,   -- kind = 'vocab_check'
  ord         smallint not null,
  level       card_level not null,                       -- 레벨 4개 × 5
  word_id     text not null,                             -- → word_cards (2.5)
  word_version int not null,
  phrase_en   text not null,                             -- 'postpone the quarterly meeting'
  options_ko  text[] not null check (cardinality(options_ko) = 4),   -- '모르겠어요'는 화면이 붙인다
  answer_idx  smallint not null check (answer_idx between 0 and 3),
  primary key (form_id, ord)
);

-- arch 5.3 sittings: 분기 결과를 고정 (명세 4.1-2, 4.1-10 "이미 분기된 모듈은 바뀌지 않는다")
alter table sittings add column parent_sitting_id uuid references sittings;  -- 어휘 체크 → 배치 RC sitting
alter table sittings add column stage smallint check (stage in (1,2));      -- 현재 단계 (이어 풀기)
alter table sittings add column stage1_submitted_at timestamptz;
alter table sittings add column stage1_correct smallint check (stage1_correct between 0 and 12);
alter table sittings add column module placement_module;                     -- 한 번 쓰면 안 바뀜 (트리거로 막음)
alter table sittings add column skipped boolean not null default false;     -- 어휘 체크 건너뛰기
```

- 응답 저장: 배치 RC 응답은 arch `attempts`에 `context='diagnostic'`로 넣는다(배치고사가 기존 F1 진단을 대체하므로 새 값을 만들지 않는다). **어휘 체크 응답은 `attempts`에 넣지 않고** `vocab_quiz_attempts`(2.6)에 넣는다 → 명세 4.1-12 "어휘 체크는 RC 예측 근거에 안 들어감"이 스키마 수준에서 보장된다.
- `sittings.module` 불변 트리거: `old.module is not null and new.module is distinct from old.module` 이면 예외. 2단계 문항 요청 API는 `stage1_submitted_at is not null`일 때만 응답한다(1단계로 돌아가기 금지).
- 마감: RC 하나의 20분 타이머 = `forms.time_limit_sec = 1200`, `sittings.deadline_at`(서버 기준). 어휘 체크는 별도 sitting(240초).

### 2.2 배치 결과

```sql
create table placement_results (
  sitting_id      uuid primary key references sittings on delete cascade,
  user_id         uuid not null references auth.users on delete cascade,
  computed_at     timestamptz not null default now(),
  model_version   text not null,                   -- 'rc-v0.1' (arch 7.5)
  logic_version   text not null,                   -- 'placement-v0.1' (분기·신뢰도·강약점 규칙)
  n_answered      smallint not null,               -- 미응답 제외 응답 수 (신뢰도 판정용)
  n_items         smallint not null,               -- 채점 문항 수 (미응답 = 오답 포함)
  -- 범위: 판정 안 함(응답 13 미만)이면 null
  rc_low smallint, rc_mid smallint, rc_high smallint,
  half_width_min  smallint,                        -- 적용한 최소 반폭 50 / 60
  confidence      text not null check (confidence in ('none','low','medium')),  -- 'high'는 배치고사에 없음 (명세 1.6)
  confidence_reasons text[] not null default '{}', -- 'few_answers','fast_answers','route_mismatch'
  module          placement_module,                -- 1단계 중 시간 초과면 null
  stage1_correct  smallint, stage2_correct smallint,
  fast_answers    smallint not null,               -- 10초 안에 답한 P5 문항 수
  timeouts        smallint not null,               -- 파트 기준 시간 1.5배 초과 문항 수
  track           track_code,                      -- arch 7.1 규칙
  track_boundary  boolean not null default false,  -- 경계 390~405 → 선택권
  vocab_level     card_level not null,
  vocab_basis     text not null check (vocab_basis in ('check','rc_estimate','track_default')),
  vocab_check     jsonb,                           -- {"basic":{"correct":5,"pass":true},"l400":{"correct":2,"pass":false},...}
  prediction_id   bigint references predictions,   -- 같은 계산을 arch predictions 스냅숏으로도 남김 (F7 첫 예측)
  check (confidence = 'none' or (rc_low is not null and rc_low <= rc_mid and rc_mid <= rc_high))
);

-- 대분류 강약점 맵 (명세 1.5). 소분류는 배치고사로 판정하지 않는다
create table placement_tag_strength (
  sitting_id  uuid references placement_results on delete cascade,
  major       text not null,            -- 'P5-VERB', 'P7-DET' (type_tags.major)
  n_items     smallint not null,
  expected    numeric(5,2) not null,    -- Σ P(정답 | 중앙값, d)
  actual      numeric(5,2) not null,    -- 정답 수
  deficit     numeric(5,2) not null,    -- expected − actual (arch 7.1 부족분)
  strength    tag_strength not null,
  primary key (sitting_id, major),
  check (n_items >= 2 or strength = 'hold')
);
```

### 2.3 목표 점수와 필수 학습 범위

```sql
-- F2 확장: 목표 RC (명세 2.1). 바뀔 때마다 새 행, 활성 1개
create table user_goals (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null references auth.users on delete cascade,
  target_rc     smallint not null check (target_rc between 5 and 495 and target_rc % 5 = 0),
  total_target  smallint check (total_target between 10 and 990),   -- 보조 계산기 입력 (선택)
  lc_score      smallint check (lc_score between 5 and 495),
  exam_date     date not null,
  daily_minutes smallint not null check (daily_minutes in (15,25,40)),
  base_prediction_id bigint references predictions,   -- 목표를 정할 때 본 현재 추정
  pts_per_week  numeric(5,1),                          -- (목표 − 중앙값) ÷ 남은 주
  challenging   boolean not null,                      -- > 15점/주 (명세 2.1) — 저장은 막지 않음
  active        boolean not null default true,
  created_at    timestamptz not null default now()
);
create unique index one_active_goal on user_goals (user_id) where active;
alter table plans add column goal_id uuid references user_goals;

-- 학습 단위 = content-standard 4장 소분류 태그 묶음 (명세 2.2). 어휘 레벨도 단위 하나
create table study_units (
  unit_id        text primary key,              -- 'U-P5-POS-NV', 'U-VOC-L400'
  kind           text not null check (kind in ('type','vocab')),
  part           part_no,                       -- vocab은 null
  label_ko       text not null,                 -- '품사 자리: 명사·동사'
  tag_codes      text[] not null default '{}',  -- {'P5-POS.N','P5-POS.V'} (type이면 1개 이상, 가져오기 검증)
  vocab_level    card_level,                    -- kind='vocab'만
  base_minutes   smallint not null,             -- P5·P6 30 / P7 45 / vocab 0 (어휘 블록 별도 용량)
  done_window    smallint not null default 10,  -- 완료 판정: 최근 10문항 첫 시도
  done_threshold numeric(3,2) not null,         -- P5·P6 0.80 / P7 0.70
  active         boolean not null default true,
  check ((kind = 'type' and cardinality(tag_codes) >= 1 and vocab_level is null)
      or (kind = 'vocab' and vocab_level is not null))
);

-- F 빈도 가중치표 (명세 2.3, 트랙 공통). 사용자에게 수치로 보이지 않음 → RLS로 학습자 직접 조회 금지
create table unit_frequency (
  unit_id        text references study_units,
  config_version text not null,                 -- 'freq-2026-10'
  f              smallint not null check (f between 1 and 3),
  note           text not null,                 -- 근거 메모 (공식 파트 문항 수 × 전문가 추정)
  approved_by    text[] not null,               -- product-planner, qa 합의 기록
  primary key (unit_id, config_version)
);
-- C를 난이도 분포 대신 사람이 정할 때만 (예시 표처럼). 없으면 계산값 사용
create table unit_contribution_override (
  unit_id text references study_units, target_band text not null,   -- '300-400','400-450','450-495'
  c smallint not null check (c between 1 and 3), note text not null,
  primary key (unit_id, target_band)
);

-- 범위 스냅숏: 재계산할 때마다 새로 쌓는다 (예측 스냅숏과 같은 원칙, 변경 이유 계산용)
create table scope_snapshots (
  id              bigint generated always as identity primary key,
  user_id         uuid not null references auth.users on delete cascade,
  goal_id         uuid not null references user_goals,
  plan_id         uuid references plans,
  computed_at     timestamptz not null default now(),
  trigger         text not null check (trigger in
                    ('placement','sessions_30','mock','goal_change','exam_date_change','user_override','regrade')),
  logic_version   text not null,                -- 'scope-v0.1'
  freq_version    text not null,                -- unit_frequency.config_version
  weeks           smallint not null,
  capacity_min    numeric(6,1) not null,        -- 신규 학습 용량
  must_min        smallint not null,
  demoted_count   smallint not null default 0,
  notes_ko        text[] not null default '{}'  -- '기간이 짧아 필수 범위 중 2개를 권장으로 옮겼어요'
);
create index on scope_snapshots (user_id, computed_at desc);

create table scope_units (
  snapshot_id  bigint references scope_snapshots on delete cascade,
  unit_id      text references study_units,
  f smallint not null, c smallint not null, w smallint not null,
  p smallint generated always as (f * c * w) stored,
  bucket       scope_bucket not null,
  flags        text[] not null default '{}',    -- maintain, demoted, overflow, user_added, vocab
  w_source     text not null check (w_source in ('placement','unit_sessions','default')),
  minutes      smallint not null,
  week_no      smallint,                        -- null = 배치 안 함 ('시간 남으면' 또는 나중에)
  rank         smallint not null,               -- 화면 정렬 순서
  reason_ko    text not null,                   -- '약점 · 목표 400에서 맞혀야 하는 유형 · 자주 나옴'
  primary key (snapshot_id, unit_id)
);

-- 사용자가 '나중에' 단위를 직접 플랜에 넣은 기록 (명세 4.2-5). 재계산해도 유지
create table user_unit_overrides (
  user_id uuid references auth.users on delete cascade,
  unit_id text references study_units,
  action  text not null check (action in ('add_to_plan','remove_from_plan')),
  created_at timestamptz not null default now(),
  primary key (user_id, unit_id)
);

-- 단위 진척 (대시보드 '필수 범위 진척 4 / 9'). attempts에서 계산해 캐시
create table user_unit_progress (
  user_id   uuid references auth.users on delete cascade,
  unit_id   text references study_units,
  n_first   int not null default 0,             -- 첫 시도 응답 수 (W를 단위 자체 값으로 바꾸는 6문항 기준)
  last10_acc numeric(4,3),
  deficit_per_item numeric(5,3),                -- (예상 − 실제) / n, W 판정용
  status    text not null default 'not_started' check (status in ('not_started','in_progress','completed')),
  completed_at timestamptz,
  primary key (user_id, unit_id)
);
```

- 범위 분류가 바뀌면 arch `plan_changes`에 `reason='scope_recalc'`, `summary_ko='시제 정답률 85% → 시제 완료, 필수에서 뺐어요'`처럼 한 줄을 남긴다(명세 2.3-3). 이전 스냅숏과 `scope_units`를 비교해 만든다.
- 세션 구성(arch 7.3 4단계)은 `plan_sessions.composition`에 `{"vocab_minutes":5,"unit_ids":[...],"review_share":0.25}`를 더 적는다. 별도 테이블은 만들지 않는다.

### 2.4 어휘 카드 (명세 3.3)

```sql
create table word_cards (
  word_id      text primary key check (word_id ~ '^W-[0-9]{5}$'),
  kind         text not null check (kind in ('master','stub')),   -- stub = 오답에서 만든 간이 카드
  lemma        text not null,                  -- 소문자 정규화
  pos          word_pos not null,
  sense_key    text not null default '1',      -- 다의어 분리: address#speech / address#deal_with
  status       item_status not null default 'draft',  -- 문항과 같은 상태 규칙. published만 노출 (명세 4.3-9)
  published_version int,
  created_at   timestamptz not null default now(),
  updated_at   timestamptz not null default now(),
  unique (lemma, pos, sense_key)
);

create table word_card_versions (
  word_id        text references word_cards,
  version        int not null,
  level          card_level not null,
  meaning_ko     text not null,
  meaning_ko_alt text,                          -- 보조 뜻 1개까지
  examples       jsonb not null,                -- [{"en":"...","ko":"..."}] 1~2개, 가상 회사·인물만
  collocations   text[] not null default '{}',  -- master: 2~4개
  derivatives    jsonb not null default '[]',   -- [{"pos":"n","form":"competition"},...] l400 이상 master 필수
  confusables    jsonb not null default '[]',   -- [{"word":"adopt","note_ko":"..."}]
  paraphrases    text[] not null default '{}',
  family_key     text,                          -- 같은 어족 묶음 키 (퀴즈 오답 보기 제외용, 명세 4.3-8)
  type_tags      text[] not null,               -- content-standard 4장 코드 (가져오기에서 type_tags 존재 검증)
  corpus_freq    int not null default 0,        -- 자체 코퍼스 표제어 빈도 (선정 순서)
  selection_note jsonb not null,                -- {"corpus_freq":12,"public_list":"대조만","expert":"..."} (저작권 점검)
  source_item_id text, source_item_version int, -- stub: 예문을 가져온 우리 문항
  author_id uuid references staff, reviewer_1_id uuid references staff,
  reviewer_2_id uuid references staff, native_check_id uuid references staff,
  originality_check jsonb,
  change_kind    text not null check (change_kind in ('initial','typo','meaning_or_example')),
  created_at     timestamptz not null default now(),
  primary key (word_id, version),
  check (jsonb_array_length(examples) between 1 and 2),
  -- master 카드만 검수·콜로케이션·파생어 필수. stub은 공개 문항에서 파생되므로 자동 생성
  check (source_item_id is not null or (author_id is not null and reviewer_2_id is not null
         and cardinality(collocations) between 2 and 4
         and (level = 'basic' or jsonb_array_length(derivatives) >= 1)))
);

-- arch 5.2 item_vocab에 카드 연결과 보기 연결을 더한다
alter table item_vocab add column word_id text references word_cards;   -- 가져오기 때 (lemma, pos)로 해석
alter table item_vocab add column option_label option_label;             -- 이 단어가 정답/오답 보기 단어면 그 보기
alter table item_vocab add column level card_level;                      -- 2.8 매핑값

-- 학습자에게 보이는 카드 (servable_items와 같은 원칙)
create view servable_word_cards as
select w.word_id, w.kind, w.lemma, w.pos, w.published_version as version
from word_cards w where w.status = 'published' and w.published_version is not null;

-- "이 단어가 나온 문제 보기" = 연결 문항 (명세 3.3 linked_items: 저장하지 않고 조회)
create view word_card_items as
select iv.word_id, iv.item_id, iv.version as item_version, iv.option_label
from item_vocab iv join servable_items s on s.item_id = iv.item_id and s.version = iv.version
where iv.word_id is not null;
```

- 간이 카드(stub): 마스터 카드가 없는 `item_vocab` 단어가 오답 자동 추가 대상이 되면 서버가 즉시 만든다. `meaning_ko`·`pos`는 `item_vocab`에서, 예문은 **그 문항 문장**(P5 stem 정답 채움 / P6·P7 근거 문장)에서 가져온다. 번역은 문항 해설에 문장 번역이 없을 수 있으므로 `ko`는 빈 문자열 허용 → **[확인 필요, Q-D5]**. 상태는 출처 문항이 `published`일 때만 `published`.
- 마스터 카드가 나중에 생기면 같은 (lemma, pos, sense_key)라 unique에 걸린다. 그때는 stub 행의 `kind`를 `master`로 바꾸고 새 버전을 쌓는다(사용자 진척 유지).

### 2.5 사용자 어휘 상태 · 퀴즈 응답 · 오답 자동 추가

```sql
create table user_vocab_profile (
  user_id       uuid primary key references auth.users on delete cascade,
  current_level card_level not null,
  level_basis   text not null check (level_basis in ('check','rc_estimate','track_default','recheck')),
  placement_sitting_id uuid references sittings,
  updated_at    timestamptz not null default now()
);

-- SRS 상태 (명세 3.5: 1·3·7·14일, 틀리면 1일). 카드 1장당 1행
create table user_vocab (
  user_id     uuid references auth.users on delete cascade,
  word_id     text references word_cards,
  status      text not null check (status in ('queued','learning','known_check','mastered','suspended')),
              -- queued = 내 단어에 들어왔지만 아직 신규 학습 전 (오답·수동 추가, 하루 상한 넘침)
              -- known_check = '알아요' + 퀴즈 정답 → 14일 뒤 1회 확인
  step        smallint not null default 0 check (step between 0 and 3),  -- 다음 간격 인덱스 (1,3,7,14)
  due_on      date,                         -- queued면 신규로 꺼낼 수 있는 날
  source      text not null check (source in ('placement','plan','wrong_answer','manual')),
  source_attempt_id bigint references attempts,
  is_known    boolean not null default false,   -- 첫 노출 '아는 단어'
  lapses      smallint not null default 0,
  first_learned_on date,
  mastered_on date,
  retention_check_on date,                  -- mastered + 30일 무작위 표본 (명세 3.5 유지율 측정)
  updated_at  timestamptz not null default now(),
  primary key (user_id, word_id),
  check (status <> 'mastered' or due_on is null)
);
create index on user_vocab (user_id, due_on) where status in ('learning','known_check','queued');

-- 어휘 응답. attempts와 분리 (예측·문항 약점 계산에 섞이지 않게, 명세 5.4 developer 항목)
create table vocab_quiz_attempts (
  id          bigint generated always as identity primary key,
  user_id     uuid not null references auth.users on delete cascade,
  word_id     text not null references word_cards,
  word_version int not null,
  context     text not null check (context in ('placement_check','first_exposure','review','retention')),
  quiz_type   text not null check (quiz_type in
               ('check_meaning','meaning_in_context','derivative_blank',      -- MVP (명세 3.5)
                'collocation','paraphrase','confusable')),                     -- Next
  self_report text check (self_report in ('know','unsure','unknown')),  -- 첫 노출 거르기 답
  prompt      jsonb not null,               -- 생성된 퀴즈 스냅숏 {sentence, options[], answer_idx, template_version}
  chosen      smallint,                     -- null = 미응답 / '모르겠어요'
  dont_know   boolean not null default false,  -- '모르겠어요' = 오답 (명세 1.4)
  is_correct  boolean not null,
  step_before smallint, step_after smallint,
  sitting_id  uuid references sittings,     -- placement_check만
  plan_session_id uuid references plan_sessions,
  time_ms     int,
  answered_at timestamptz not null default now(),
  foreign key (word_id, word_version) references word_card_versions
);
create index on vocab_quiz_attempts (user_id, answered_at desc);

-- 오답 원인 '② 어휘' → 내 단어 자동 추가 기록 (명세 3.4-3, 4.3-4, 4.4 F5)
create table vocab_auto_adds (
  id          bigint generated always as identity primary key,
  user_id     uuid not null references auth.users on delete cascade,
  word_id     text not null references word_cards,
  reason      text not null check (reason in ('cause_vocab','explanation_button')),
  attempt_id  bigint references attempts,
  action      text not null check (action in ('created','reset','deferred','already_queued')),
  effective_on date not null,               -- 신규로 나올 수 있는 날 (deferred면 다음 날 이후)
  created_at  timestamptz not null default now()
);
create index on vocab_auto_adds (user_id, created_at);
```

- 하루 5개 상한은 `vocab_auto_adds`에서 `reason='cause_vocab' and action='created' and created_at::date = 오늘(KST)`을 세서 판정한다. "단어장에 넣기" 버튼(`explanation_button`)은 상한 밖이고 다음 날 신규 맨 앞에 들어간다(명세 4.3-5).
- 같은 단어가 다시 오답 원인이 되면 새 카드·새 행을 만들지 않고 `user_vocab.step=0, due_on=내일, status='learning'`으로 되돌린다(명세 4.4 F5, `action='reset'`).

### 2.6 RLS (arch 5.6에 추가)

| 테이블 | 학습자 | 서버 |
|---|---|---|
| `placement_results`, `placement_tag_strength`, `user_goals`, `scope_snapshots`, `scope_units`, `user_unit_progress`, `user_vocab_profile` | 본인 행 **읽기** (`user_goals`는 쓰기도) | 전체 |
| `user_vocab`, `vocab_quiz_attempts`, `vocab_auto_adds` | 본인 행 읽기. 쓰기는 채점·SRS API만 (단계 조작 방지) | 전체 |
| `user_unit_overrides` | 본인 행 읽기·쓰기 | 전체 |
| `word_cards`, `word_card_versions`, `vocab_check_slots`, `form_modules` | 직접 접근 금지. API가 `servable_word_cards` 기준으로 준다. 어휘 체크는 채점 전 `answer_idx`를 빼고 준다 | 전체 |
| `study_units` | 읽기 (이름·분량만 노출하는 뷰) | 전체 |
| `unit_frequency`, `unit_contribution_override` | **금지** (F 수치 비노출, 명세 가정 5) | 전체 |

### 2.7 개인정보

- 비회원 배치고사(arch `profiles.is_anonymous`)의 `placement_results`·`user_vocab_profile`은 가입 시 같은 `user_id`로 이어진다(Supabase 익명 사용자 → 연결). 새 개인정보 항목은 없다. `user_goals.lc_score`는 사용자가 입력한 점수뿐이다.

### 2.8 기존 SQLite 테이블(`db/build_db.py`)과의 대응

| SQLite (`build_db.py`) | Postgres (arch 5.2 + 이 문서) | 옮길 때 처리 |
|---|---|---|
| `vocab(word, pos, meaning_ko, level)`, PK (word, pos) | **`word_cards` + `word_card_versions`의 출발 데이터(후보 목록)**. 그대로 카드가 되지는 않는다 | 1) 문항 은행에서 나온 단어 = **자체 코퍼스 후보**(명세 3.1-2). 콘텐츠팀이 카드 작성 대상을 고르는 입력으로 쓴다. 2) 마스터 카드가 없는 단어는 오답 자동 추가 때 stub 카드가 된다 |
| `vocab.word` (소문자 정규화) | `word_cards.lemma` | 같음. 단, `out of service`처럼 구도 들어 있다 → `pos='phr'` |
| `vocab.pos` (`'n.'`, `'v.'`, `'adj.'`, `'adv.'`, `'prep.'`, `'phr.'` 자유 텍스트) | `word_pos` enum | 끝의 마침표를 떼어 매핑 (`'n.'→'n'`). `conj.`는 현재 데이터에 없음. 매핑 실패는 가져오기 에러 |
| `vocab.level` (`기초`/`중급`/`고급` = 문항 `vocab_level`) | `card_level` (`basic`/`l400`/`l450`/`l495`) | **눈금이 다르다.** stub 카드 기본 매핑 [가정]: 기초→basic, 중급→l400, 고급→l450. 마스터 카드는 명세 3.1-4 규칙(코퍼스 난이도·공개 목록·전문가)으로 다시 정한다 → Q-D4 |
| PK (word, pos) + `INSERT OR IGNORE` → **같은 품사의 두 번째 뜻은 버려진다** | `unique (lemma, pos, sense_key)` | 명세 3.1-5 다의어 카드 분리와 맞지 않는다. Postgres 쪽은 `item_vocab.meaning_ko`를 문항별로 보존하므로 문제없음. SQLite는 현황 집계용이라 그대로 둬도 되지만, 카드 후보를 뽑을 때는 SQLite `vocab`이 아니라 원본 JSON에서 (word, pos, meaning_ko) 전체를 읽어야 한다 |
| `item_vocab(item_id, word, pos)` | arch `item_vocab(item_id, version, ord, word, pos, meaning_ko, collocation)` + 이 문서의 `word_id`, `option_label`, `level` | SQLite에는 문항 버전·순서·뜻이 없다. Postgres 가져오기는 원본 JSON에서 직접 채운다. `option_label`은 원본에 필드가 없으므로 가져오기 때 **보기 텍스트와 표제어를 비교해 추정**한다(소문자·완전 일치 → 그 보기, 아니면 null) → Q-D6 |
| (없음) 정답 단어·오답 보기 단어 구분 | `item_vocab.option_label` | 예: P6 `install` 문항은 보기가 `install / installed / installing / installation`이라 `install`만 일치한다. 파생형 보기는 표제어와 다르므로 원본 JSON에 `vocab[].option` 필드를 추가하는 것이 정확하다(콘텐츠 형식 변경이라 qa·content 합의 필요) |
| `items.type_tag` | `word_card_versions.type_tags` 기본값 | stub 카드는 출처 문항의 `type_tag`를 물려받는다 |

현재 데이터(`content/items/p6/p6_batch1.json`, 세트 4개) 기준 단어 61건: 품사 n 22 · phr 13 · v 12 · adj 8 · adv 5 · prep 1, 레벨 중급 42 · 기초 13 · 고급 6. 어휘 카드 1,000개 목표(명세 3.6)에 비해 문항 은행 코퍼스는 아직 작아서, 당분간 카드 선정은 전문가 판단 비중이 크다 [추정].

---

## 3. 학습 로직 v0 (순수 함수)

`packages/learning/placement.ts`, `scope.ts`, `vocab.ts`로 나눈다. 아래 TypeScript는 시그니처와 핵심 규칙이다. **범위 점수·주차 배치·SRS·하루 어휘 선택은 `db/logic_v0.py`에 실행 가능한 기준 구현이 있다.**

### 3.1 1단계 → 2단계 모듈 분기 (명세 1.3)

```ts
type Module = 'basic' | 'mid' | 'upper';
const ROUTING = { cuts: [{ max: 5, to: 'basic' }, { max: 8, to: 'mid' }, { max: 12, to: 'upper' }] }; // forms.routing

function routeStage1(stage1Correct: number, routing = ROUTING): Module {
  if (!Number.isInteger(stage1Correct) || stage1Correct < 0 || stage1Correct > 12) throw new RangeError();
  return routing.cuts.find(c => stage1Correct <= c.max)!.to;   // 미응답 = 오답으로 센 정답 수
}
```

- 컷 근거 재확인: arch 7.5.2 모델에 1단계 난이도 구성(d2 3 · d3 6 · d4 3)을 넣으면 예상 정답 수가 RC 300 → 4.1, 350 → 5.7, 400 → 7.8, 450 → 9.6 (logic_v0 자체 테스트로 확인). 명세 값과 같다.
- "정답 수 대신 1단계 사후 중앙값" 대안(명세 1.3)은 구현하지 않는다. 1단계 12문항의 난이도 구성이 고정이라 정답 수와 사후 중앙값은 단조 관계다. 폼마다 구성이 달라지면(B폼) 컷을 `forms.routing`에 폼별로 둔다.
- 분기는 서버가 1단계 제출 API에서 한 번 계산해 `sittings.module`에 쓰고, 이후 재계산하지 않는다(재채점으로 1단계 정답이 바뀌어도 모듈은 유지하고 점수만 다시 계산).

### 3.2 RC 범위 추정과 신뢰도 (arch 7.5 재사용 + 명세 1.6)

```ts
interface PlacementResponse { itemId: string; difficulty: 1|2|3|4|5; part: 5|6|7; major: string;
  stage: 1|2; answered: boolean; correct: boolean; timeMs: number | null; }

function estimatePlacement(rs: PlacementResponse[], module: Module | null): {
  confidence: 'none' | 'low' | 'medium'; reasons: string[];
  range?: { low: number; mid: number; high: number }; halfWidthMin?: 50 | 60;
} {
  const nAnswered = rs.filter(r => r.answered).length;
  if (nAnswered < 13) return { confidence: 'none', reasons: ['few_answers'] };       // 범위 대신 이어 풀기
  const post = posteriorGrid(rs.map(r => ({ d: r.difficulty, correct: r.answered && r.correct, w: 1.0 })));
  // ↑ arch 7.5.2 그대로: 격자 5..495, 사전 N(330,100), P = 0.2 + 0.8·σ((s−400)/50 − b_d), 가중치 1.0(진단)
  const reasons: string[] = [];
  if (nAnswered <= 19) reasons.push('few_answers');
  if (rs.filter(r => r.part === 5 && r.answered && r.timeMs !== null && r.timeMs < 10_000).length >= 5)
    reasons.push('fast_answers');
  const s2 = rs.filter(r => r.stage === 2);
  const acc2 = s2.length ? s2.filter(r => r.correct).length / s2.length : null;
  if (acc2 !== null && (acc2 < 0.30 || acc2 > 0.90)) reasons.push('route_mismatch');     // 14문항: ≤4 또는 ≥13
  const halfWidthMin = reasons.length ? 60 : 50;
  return { confidence: reasons.length ? 'low' : 'medium', reasons,
           range: widen(post.q10, post.median, post.q90, halfWidthMin), halfWidthMin };
}
// widen: arch 7.5 6번 — 사후 80% 구간이 최소 반폭보다 좁으면 중앙값 ± 반폭으로 넓히고, 5점 단위·5~495로 자름
```

- 명세 4.1-8에 따라 "낮음" 조건이면 **어느 이유든 반폭 ±60**으로 넓힌다(명세 1.6 표의 fast_answers 행에는 반폭이 없지만 수용 기준을 따름).
- 트랙 배정은 arch 7.1 규칙 그대로(`assignTrack(range, part5Accuracy)`). 배치고사의 Part 5는 12문항이다.
- 같은 결과를 `predictions`에 `trigger='diagnostic'`, `n_items=26`(또는 응답한 만큼)으로 넣는다. 어휘 체크는 넣지 않는다.

### 3.3 대분류 강약점 (명세 1.5, arch 7.1 부족분)

```ts
type Strength = 'weak' | 'normal' | 'strong' | 'hold';
function tagStrength(rs: PlacementResponse[], mid: number): Record<string, { n: number; deficit: number; strength: Strength }> {
  const by = groupBy(rs, r => r.major);                       // 'P5-VERB', 'P6-CTX', 'P7-DET' ...
  const rows = Object.entries(by).map(([major, xs]) => {
    const expected = sum(xs.map(r => pCorrect(mid, r.difficulty)));
    const actual = xs.filter(r => r.answered && r.correct).length;
    return { major, n: xs.length, deficit: round2(expected - actual) };
  });
  const eligible = rows.filter(r => r.n >= 2);
  const top3 = new Set(eligible.filter(r => r.deficit > 0).sort((a, b) => b.deficit - a.deficit).slice(0, 3).map(r => r.major));
  return Object.fromEntries(rows.map(r => [r.major, { ...r, strength:
      r.n < 2 ? 'hold'
    : (r.deficit >= 0.8 || top3.has(r.major)) ? 'weak'
    : r.deficit <= -0.5 ? 'strong' : 'normal' }]));
}
```

- 판정 순서: **근거 < 2 → 판단 보류**가 먼저다(명세 4.1-7). 그다음 약점, 강점, 보통.
- "상위 3개" 규칙은 **부족분이 0보다 큰 것만** 센다 [가정]. 모두 잘 본 사람에게 약점 3개를 억지로 붙이지 않기 위해서다 → Q-D2.
- `mid`는 26문항 사후 중앙값이다. 예측 화면의 "끌어내리는 요인"(arch 7.5, 근거 4개 미만 제외)과 같은 계산·같은 시점 데이터를 쓴다(명세 4.4 F7).
- 배치고사 폼은 고정이라 근거 수도 고정이다: P5-GRAM은 1문항이라 **항상 판단 보류**(명세 1.5).

### 3.4 어휘 레벨 (명세 1.4, 3.4-1)

```ts
const LEVELS = ['basic', 'l400', 'l450', 'l495'] as const;
function vocabLevel(byLevel: Record<Level, { correct: number; n: number }> | null,
                    track: Track, rcVocab?: { correct: number; n: number }): { level: Level; basis: string } {
  if (byLevel) {
    let i = 0;
    while (i < LEVELS.length && byLevel[LEVELS[i]].correct >= 4) i++;   // 아래부터 연속 통과 ('모르겠어요' = 오답)
    return { level: LEVELS[Math.min(i, 2)], basis: 'check' };            // MVP 카드는 l450까지 → 상한 l450
  }
  const base = track === '300-400' ? 'l400' : 'l450';                     // 명세 3.4-1 트랙 기본
  if (rcVocab && rcVocab.n >= 3 && rcVocab.correct <= 1) return { level: LEVELS[LEVELS.indexOf(base) - 1], basis: 'rc_estimate' };
  return { level: base, basis: rcVocab ? 'rc_estimate' : 'track_default' };
}
```

- 전부 통과(495 레벨 통과)해도 MVP 카드가 없으므로 l450에서 시작한다 [가정]. 건너뛰기 처리는 명세 안에서 두 군데(1.3 "P5-VOC 3개로 간이 추정" vs 3.4-1 "트랙 기본 레벨")가 달라서 **둘을 합친 규칙을 임시로 썼다** → Q-D3.

### 3.5 필수 학습 범위 점수 (명세 2.3~2.5) — `logic_v0.py: score_scope`

**입력**: 단위 목록(F, C, W, 분량, 어휘 여부, 완료 여부), 목표 RC, 남은 주 `W`(arch 7.3 `floor((시험일 − 3 − 오늘)/7)`), 하루 시간, 학습 요일 수, 모의고사 여부.

```ts
// C: 단위 문항의 난이도 분포 × 목표 점수 정답 확률 (명세 2.3). override 표가 있으면 그 값
function contributionC(difficulties: number[], targetRc: number): 1 | 2 | 3 {
  const m = mean(difficulties.map(d => pCorrect(targetRc, d)));   // 단위의 servable 문항 전체
  return m >= 0.70 ? 3 : m < 0.50 ? 1 : 2;
}
// W: 배치 대분류 값을 물려받고, 단위 첫 시도 6문항 이상이면 단위 자체 값 (명세 2.3)
function weaknessW(placement: Strength, unit?: { nFirst: number; expectedAcc: number; actualAcc: number }): 1 | 2 | 3 {
  if (unit && unit.nFirst >= 6) {
    const gap = unit.expectedAcc - unit.actualAcc;
    return gap >= 0.20 ? 3 : gap <= -0.10 ? 1 : 2;               // 강점 문턱 −0.10은 [가정] → Q-D2
  }
  return { weak: 3, normal: 2, hold: 2, strong: 1 }[placement];
}
const bucketOf = (p: number) => p >= 12 ? 'must' : p <= 4 ? 'later' : 'recommended';
// P = F·C·W 가능한 값은 1,2,3,4,6,8,9,12,18,27뿐이라 세 구간이 빈틈없이 나뉜다

function newLearningCapacity(weeks: number, daily: 15|25|40, days = 5, hasMock = true): number {
  const rcMinutes = weeks * days * (daily - VOCAB_MIN[daily]);    // VOCAB_MIN = {15:3, 25:5, 40:7}
  return Math.max(0, (rcMinutes - (hasMock ? 100 : 0)) * (1 - 0.25));
}
```

**절차** (`score_scope`)

1. 단위마다 P = F × C × W, `bucketOf(P)`. 완료 단위는 `done`(간격 복습만), 어휘 단위는 용량을 쓰지 않는다(어휘 블록 별도).
2. **유지 규칙**: F = 3, C = 3, W = 1 → `recommended` + `maintain`, 신규 용량을 쓰지 않는다.
3. **정렬**: 분류 → P 내림차순 → 동점이면 **W → C → F 내림차순** → 입력(콘텐츠 표) 순서. W를 먼저 보는 이유: 같은 P면 지금 약한 것을 먼저 배치한다. 이 순서여야 명세 2.5 예시의 주차 배치(5·6·7 → 2주, 8·9·10 → 3주)가 나온다.
4. **용량 강등**: 필수 분량 합 > 용량이면 정렬의 끝(P가 가장 낮은 필수)부터 `recommended` + `demoted`로 옮기며 합 ≤ 용량이 될 때까지 반복. 안내 문구 `기간이 짧아 필수 범위 중 N개를 권장으로 옮겼어요`.
5. **배치**: 필수 → 권장(강등 단위는 권장의 끝) 순서로 용량 안에서 쌓는다. 권장이 남은 용량을 넘으면 그 단위는 건너뛰고(`overflow` = "시간 남으면") 다음 단위를 본다(first-fit).
6. **주차**: 기초+확장 주 수 `fe = floor(0.4W) + floor(0.4W)`(각 최소 1, 나머지가 실전), 주당 몫 = 용량 ÷ fe. 단위는 **누적 분량에서 그 단위의 중간 지점이 들어가는 주**에 둔다: `week = ceil((누적끝 − 분량/2) / 주당몫)`. 끝 지점 기준이면 P1 예시의 10번(누적 285분)이 4주로 밀려 명세와 어긋나서 중간 지점 기준을 골랐다.
7. **이유 한 줄**: `약점 · 목표 400에서 맞혀야 하는 유형 · 자주 나옴` 형식. 점수(+N점)는 쓰지 않는다(명세 2.3-4).
8. 사용자 추가(`user_unit_overrides.add_to_plan`)는 권장 끝에 넣고, 용량을 넘으면 밀리는 권장 단위 목록을 미리보기로 돌려준다(명세 4.2-5).
9. **도전 목표**: `(목표 − 현재 중앙값) ÷ 남은 주 > 15` → `challenging = true`. 저장은 막지 않는다.

**재계산 트리거**: 세션 첫 시도 응답 30개마다, 모의고사 완료, 목표·시험일 변경, 재채점. 매번 새 `scope_snapshots` 행 + 바뀐 단위만 `plan_changes` 한 줄. 이미 지난 주차의 배치는 바꾸지 않고 이번 주 이후만 다시 배치한다 [가정].

**완료 판정**: 단위 태그 문항의 최근 10개 첫 시도 정답률 ≥ `done_threshold`(P5·P6 0.80, P7 0.70) → `done`. 10문항이 안 되면 완료가 아니다.

### 3.6 하루 어휘 선택과 SRS (명세 3.4~3.5) — `logic_v0.py: select_daily_vocab, review, first_exposure`

**상태 전이**

| 현재 | 사건 | 다음 |
|---|---|---|
| (없음) | 신규 카드 첫 노출 "몰라요/헷갈려요" | `learning`, step 0, due +1일 |
| (없음) | "알아요" + 문맥 퀴즈 정답 | `known_check`, step 3, due +14일 (`is_known`) |
| (없음) | "알아요" + 퀴즈 오답 | `learning`, step 0, due +1일 |
| `learning` step k (k < 3) | 복습 정답 | step k+1, due = **복습한 날** + [1,3,7,14][k+1] |
| `learning` step 3 / `known_check` | 복습 정답 | `mastered` (due 없음, 30일 뒤 유지율 표본 대상) |
| `learning` / `known_check` | 복습 오답 | `learning`, step 0, due +1일, lapses +1 |
| 아무 상태 (queued 제외) | 같은 단어가 다시 오답 원인 ② | `learning`, step 0, due +1일 (새 카드 없음) |

- 간격은 **실제 복습한 날 기준**으로 계산한다(밀린 복습은 밀린 만큼 뒤로). arch 7.4 문항 Leitner와 같은 간격 배열을 설정에서 공유한다.
- 하루 한 카드는 한 번만 복습 결과를 반영한다(같은 날 재시도는 기록만, 단계 변화 없음) [가정].

**하루 선택** (`select_daily_vocab`)

```ts
function selectDailyVocab(states: VocabState[], candidates: Candidate[], daily: 15|25|40, today: Date) {
  const due = states.filter(s => (s.status === 'learning' || s.status === 'known_check') && s.dueOn <= today)
                    .sort(by(s => s.dueOn, s => s.step));            // 많이 밀린 것, 낮은 단계 먼저
  let quota = { 15: 8, 25: 12, 40: 15 }[daily];
  if (due.length > 40) quota = Math.max(0, quota - (due.length - 40));  // 초과 1개당 신규 1개 감소 [가정]
  const queued = states.filter(s => s.status === 'queued' && s.dueOn <= today)
                       .sort(by(s => ({ manual: 0, wrong_answer: 1 }[s.source] ?? 2), s => s.dueOn));
  const fresh = candidates.filter(notIn(states))                       // 현재 레벨의 servable 카드
                          .sort(by(c => !c.requiredTag, c => -c.corpusFreq)); // 필수 단위 태그와 겹치는 단어 먼저
  let news = [...queued.map(id), ...fresh.map(id)].slice(0, quota);
  // 시간 가드: 어휘 블록(3/5/7분) 안에 들어가게 신규 → 복습 순으로 줄임. 초당 비용은 [가정, 파일럿 실측]
  return fitToBudget(news, due, VOCAB_MIN[daily] * 60, { secPerNew: 12, secPerReview: 3 });
}
```

- 신규 순서: **수동 "단어장에 넣기" → 오답 자동 추가 → 필수 단위 태그와 겹치는 카드 → 현재 레벨 나머지(코퍼스 빈도순)**. 명세 3.4-5는 오답을 맨 앞에 두지만 4.3-5는 수동 추가를 "맨 앞"이라 해서 수동을 먼저 뒀다 → Q-D3.
- 퀴즈 유형 비중(명세 3.4-4): 범위에서 P5-POS 단위가 필수면 `derivative_blank` 비중 50%, 아니면 30% [가정]. 파생어가 없는 카드(basic)는 항상 `meaning_in_context`.
- 퀴즈 오답 보기: 같은 `pos`·같은 `level`의 다른 카드에서 고르되 **같은 `family_key`, 정답 카드의 `paraphrases`·`confusables`에 있는 단어는 제외**(명세 4.3-8). 후보가 3개 미만이면 그 퀴즈를 만들지 않고 다른 유형으로 바꾼다.
- 레벨 진행: 현재 레벨의 servable 카드를 다 꺼냈으면(남은 후보 0) 다음 레벨로 올린다. `user_vocab_profile.current_level` 갱신.

### 3.7 오답에서 자동 추가 (명세 3.4-3) — `logic_v0.py: auto_add_from_wrong`

```ts
function wordsFromWrongAttempt(attempt: { chosen: Label; answer: Label }, itemVocab: ItemVocab[]): string[] {
  const byOption = itemVocab.filter(v => v.optionLabel === attempt.answer || v.optionLabel === attempt.chosen);
  return (byOption.length ? byOption : itemVocab.slice(0, 2)).map(v => v.wordId ?? createStub(v));
  // option_label을 못 찾은 문항(파생형 보기 등)은 item_vocab 앞 2개로 대신 [가정] → Q-D6
}
```

- 트리거: arch 7.4 원인 추정이 `vocab`(② 어휘)이고 사용자가 원인을 바꾸지 않은 상태로 해설을 닫을 때. "찍음(⑤)"으로 바꾼 오답은 추가하지 않는다.
- 하루 5개 상한(신규 생성만 셈). 넘치면 `queued`로 넣고 `due_on = 내일`(다음 날 신규 후보), `vocab_auto_adds.action='deferred'`.
- 응답 문구 "단어 N개를 단어장에 넣었어요"의 N = 오늘 반영한 수(`created + reset`).

---

## 4. 단위 테스트 케이스

`db/logic_v0.py`의 `_selftest()`가 아래 표의 ✔ 행을 실행한다. TypeScript 이전 때 Vitest로 같은 표를 옮긴다.

### 4.1 분기 (`routeStage1`)

| # | 입력: 1단계 정답 수 | 기대 | 비고 | py |
|---|---|---|---|---|
| R1 | 0 | basic | 하한 | ✔ |
| R2 | 5 | basic | 경계 | ✔ |
| R3 | 6 | mid | 경계 | ✔ |
| R4 | 8 | mid | 경계 | ✔ |
| R5 | 9 | upper | 경계 | ✔ |
| R6 | 12 | upper | 상한 | ✔ |
| R7 | −1, 13, 5.5 | 에러 | 입력 검증 | (TS) |
| R8 | 1단계 12문항 중 3개 미응답, 정답 6 | mid | 미응답 = 오답, 정답 수만 봄 | (TS) |
| R9 | 모듈 기록 후 재요청 | 같은 모듈 | `sittings.module` 불변 | (DB) |
| R10 | 모델 기대 정답 수 RC 300/350/400/450 | 4.1/5.7/7.8/9.6 (±0.05) | 컷 근거 회귀 | ✔ |

### 4.2 배치 신뢰도·강약점 (`estimatePlacement`, `tagStrength`) — TS로 작성

| # | 입력 | 기대 |
|---|---|---|
| C1 | 응답 12 (1단계 중 시간 초과) | `confidence='none'`, 범위 없음 |
| C2 | 응답 15, 나머지 정상 | low, 반폭 ≥ 60, reasons=[few_answers] |
| C3 | 응답 26, P5 10초 안 응답 5개 | low, ±60, [fast_answers] |
| C4 | 응답 26, 2단계 14문항 중 4개 정답 (28.6%) | low, [route_mismatch] |
| C5 | 응답 26, 2단계 13/14 (92.9%) | low, [route_mismatch] |
| C6 | 응답 26, 2단계 9/14, 빠른 응답 2 | medium, 반폭 ≥ 50 |
| C7 | 모든 경우 | confidence ≠ 'high'; low ≤ mid ≤ high, 5점 단위, 5~495 |
| T1 | P5-GRAM 1문항 (오답) | hold (부족분이 커도) |
| T2 | 대분류 부족분 +0.9 | weak |
| T3 | 부족분 +0.3, 부족분 양수 대분류 중 상위 3위 | weak |
| T4 | 부족분 −0.6 | strong |
| T5 | 모든 대분류 부족분 ≤ 0 | weak 없음 (상위 3개 규칙은 양수만) |
| V1 | 어휘 basic 5/5, 400 2/5 | l400, basis=check |
| V2 | basic 3/5 | basic |
| V3 | 전부 5/5 | l450 (MVP 상한) |
| V4 | 건너뜀, 300→400 트랙, RC P5-VOC 1/3 | basic, rc_estimate |

### 4.3 범위 점수 (`score_scope`) — 명세 2.5 P1 예시

입력: 명세 2.5 표 19개 단위(F·C·W·분량 그대로), 목표 400, 하루 25분, 주 5회, 모의고사 있음.

| # | 입력 | 기대 | py |
|---|---|---|---|
| S1 | P = 27, 18, 12 / 9, 8, 6 / 4, 3, 2, 1 | must / recommended / later | ✔ |
| S2 | 용량 (6주) | 30×25 − 150 − 100 = 500 × 0.75 = **375분** | ✔ |
| S3 | 6주 단계 | 기초 2 · 확장 2 · 실전 2 | ✔ |
| S4 | 6주 분류·주차 | 1·2·3·4(어휘) → 1주, 5·6·7 → 2주, 8·9·10 → 3주 (필수 285분 = 용량의 76%), 11·12 → 4주(권장), 13·14·15 → 권장 "시간 남으면", 16~19 → 나중에 | ✔ |
| S5 | 4주 용량 | 20×20 − 100 = 300 × 0.75 = **225분** | ✔ |
| S6 | 4주 강등 | 9·10(P 12) → 권장(demoted), 필수 합 225분, 문구 "기간이 짧아 필수 범위 중 2개를 권장으로 옮겼어요", 권장 전부 "시간 남으면" | ✔ |
| S7 | 단위 하나 F3·C3·W1 | P 9, recommended + maintain, 주차 없음 | ✔ |
| S8 | C: 난이도 [1,2,3] / [3,3] / [4,5] @ 목표 400 | 3 / 2 / 1 | ✔ |
| S9 | C: [2,3,4] / [5] @ 목표 450 | 3 / 1 | ✔ |
| S10 | 현재 320 → 목표 400, 6주 / 목표 450 | 도전 아님(13.3점/주) / 도전(21.7점/주) | ✔ |
| S11 | 완료 단위 | bucket done, 용량 안 씀 | (TS) |
| S12 | F/C/W에 0 또는 4 | 에러 | (TS) |
| S13 | 남은 주 0 | 용량 0 → 필수 전부 강등, challenging = true | (TS) |

### 4.4 SRS·어휘 선택

| # | 입력 | 기대 | py |
|---|---|---|---|
| Q1 | 10/13 신규 학습 | step 0, due 10/14 | ✔ |
| Q2 | 10/14 정답 → 10/17 정답 → 10/24 정답 | due 10/17 → 10/24 → 11/07 (1·3·7·14) | ✔ |
| Q3 | 11/07 (step 3) 오답 | learning, step 0, due 11/08, lapses 1 | ✔ |
| Q4 | 11/07 (step 3) 정답 | mastered, due 없음 | ✔ |
| Q5 | 10/13 신규, 10/20(6일 밀림) 정답 | due 10/23 (복습한 날 + 3) | ✔ |
| Q6 | "알아요" + 퀴즈 정답 (10/13) | known_check, due 10/27; 그날 정답 → mastered | ✔ |
| Q7 | "알아요" + 퀴즈 오답 | learning, due 10/14 | ✔ |
| Q8 | 오답 자동 추가 7단어 (1개는 이미 학습 중), 오늘 추가 0 | 기존 1개 step 0 리셋 + 신규 5개, 1개 내일로 | ✔ |
| Q9 | 25분 플랜, 복습 0, 후보 60 | 신규 12, 필수 태그 겹치는 단어 먼저 | ✔ |
| Q10 | 25분, 복습 41 | 신규 11, 복습 41, 300초 안 | ✔ |
| Q11 | 15분, queued 수동 1·오답 1 | 신규 순서 수동 → 오답 | ✔ |
| Q12 | 15분, 복습 60 | 신규 0, 복습은 180초 안에 들어가는 만큼(60개), 넘친 복습은 내일 | (TS) |
| Q13 | mastered 카드 복습 시도 | 에러 | (TS) |

### 4.5 DB·API (pgTAP / Vitest + 로컬 Supabase)

- 어휘 체크 응답이 `attempts`에 생기지 않는다 / `predictions.n_items`에 포함되지 않는다.
- 1단계 제출 전 2단계 문항 요청 → 403. 1단계 제출 후 1단계 응답 수정 → 거부.
- 학습자가 `unit_frequency`, `word_card_versions` 직접 조회 → 0행.
- `user_vocab` 직접 update → 거부(서버 API만).
- 같은 날 `cause_vocab` 6번째 단어 → `deferred`.

---

## 5. 참조 구현 실행

```
python3 db/logic_v0.py
```

- 표준 라이브러리만 쓴다. 출력 첫 줄 `self-test OK: 73 checks passed`, 그 아래 P1 6주 배치표와 4주 강등 문구.
- 포함 함수: `p_correct`, `route_stage1`, `contribution_c`, `weakness_w`, `bucket_of`, `new_learning_capacity`, `phase_weeks`, `is_challenging`, `score_scope`, `start_learning`, `first_exposure`, `review`, `auto_add_from_wrong`, `select_daily_vocab`. 설정은 맨 위 `CONFIG` 하나에 모았다.
- 포함하지 않은 것: 사후 분포 격자 계산(3.2), 대분류 강약점(3.3), 어휘 레벨(3.4). arch 7.5 구현(S3)과 같이 TS로 바로 쓴다.

---

## 6. 공수 추정 [추정]

1 인-스프린트 = 2주 · 개발자 1명(약 10일). 콘텐츠 제작·검수 시간은 뺐다.

| 묶음 | 내용 | 일 |
|---|---|---|
| DB | 2장 마이그레이션, RLS, 불변 트리거, 뷰, pgTAP | 3 |
| 콘텐츠 가져오기 | 배치 폼·모듈·어휘 체크 폼, 카드 JSON 검증·가져오기, `item_vocab` 카드 연결·`option_label` 추정, 단위·F표 | 3 |
| 배치고사 API·로직 | 2단계 분기, 이어 풀기(모듈 고정), 채점·신뢰도·강약점·어휘 레벨, 첫 예측 | 3 |
| 범위 엔진 | F·C·W·P, 용량 강등, 주차 배치, 재계산 트리거, 변경 한 줄, 사용자 추가, 플랜·세션 구성 연결 | 4 |
| 어휘 엔진 | SRS, 첫 노출 거르기, 하루 선택, 퀴즈 2종 템플릿·오답 보기 규칙, 오답 자동 추가·간이 카드 | 4 |
| 테스트 | 4장 표 Vitest 이전, 성질 테스트, API 테스트 | 2 |
| **로직·DB·API 소계** | | **19일 ≈ 1.4 인-스프린트** |
| 화면 (S1-13 설계 기준) | 배치 1→2단계 전환, 어휘 체크, 결과(범위·신뢰도·강약점·판단 보류), 목표 입력, 범위 3묶음, 대시보드 어휘·진척, 카드·퀴즈 화면 | 13 |
| **합계** | | **약 32일 ≈ 2.7 인-스프린트** (명세 5.3 추정 +3과 비슷) |
| F11 축소판 (명세 Q-P7 (a)) | 퀴즈 Next 3종·어휘 대시보드 상세·유형 카드 화면 제외 | **약 24일 ≈ 2.0** |

- 일정 위험: 가장 큰 변수는 개발이 아니라 **배치 폼 108문항 + 어휘 체크 40 + 카드 380(1차)** 콘텐츠다(명세 5.2). 개발은 S3에 배치·범위 로직, S4에 어휘 엔진 순서가 자연스럽다. 카드 가져오기 형식은 S2 파일럿(카드 50개) 전에 확정해야 한다.

---

## 7. 열린 질문

| # | 질문 | 누가 | 개발 권장 |
|---|---|---|---|
| Q-D1 | **1단계 중 시간 초과**: 응답이 최대 12개라 명세 1.6 규칙상 항상 "판정 안 함"이다. 명세 4.1-3("1단계 응답만으로 채점")과 충돌 | product-planner | 그대로 "판정 안 함 + 이어 풀기"로 둔다(20분에 12문항을 못 끝낸 경우는 드묾 [추정]) |
| Q-D2 | 강약점 세부 문턱: 대분류 "상위 3개"를 부족분 > 0인 것만 셀지, 소분류 W = 1(강점) 문턱(예상보다 10%p 이상 높음) | product-planner·qa | 둘 다 위 [가정]대로 시작, 파일럿 응답으로 조정 |
| Q-D3 | 명세 안 불일치 두 가지: ① 어휘 체크 건너뛰기 = P5-VOC 간이 추정(1.3) vs 트랙 기본 레벨(3.4-1) ② 신규 카드 맨 앞 = 오답 단어(3.4-5) vs 수동 추가(4.3-5) | product-planner | ① 트랙 기본, P5-VOC 0~1/3이면 한 단계 낮춤 ② 수동 → 오답 |
| Q-D4 | 문항 `vocab_level`(기초/중급/고급)과 카드 레벨(기초/400/450/495) 눈금 통일 여부 | qa-tester·content | 문항 필드는 그대로 두고 매핑표(2.8)로 시작. 카드 레벨이 확정되면 문항 필드를 카드 눈금으로 바꾸는 것을 검토 |
| Q-D5 | 간이 카드 예문 번역: 문항 해설에 문장 번역이 없을 수 있음 | qa-tester | 번역 없이 원문만 보이고 "간이 카드" 표시. 노출이 많은 간이 카드는 콘텐츠팀 마스터 카드 작성 대기열로 |
| Q-D6 | 정답·오답 보기 단어 구분: 원본 JSON `vocab[]`에 보기 연결 필드가 없어 텍스트 일치로 추정(파생형 보기는 못 찾음) | qa-tester·content (content/SCHEMA.md) | `vocab[].option: "A"~"D" \| null` 필드 추가 제안. 추가 전에는 앞 2개 단어로 대신 |
| Q-D7 | 하루 어휘 분량과 시간: 25분 플랜 5분에 신규 12 + 복습 최대 40은 카드당 약 6초라 빠듯하다. 시간 가드(신규 12초·복습 3초 [가정])가 실제로는 신규를 자주 줄일 수 있다 | product-planner | 파일럿에서 카드당 시간을 재고 `daily_new`·`sec_per_*`를 같이 조정 |
| Q-D8 | 주차 배치 규칙: 기초·확장 주 수 내림(6주 → 2·2·2)과 "중간 지점이 들어가는 주" 규칙 | product-planner | 명세 예시를 재현하는 이 규칙으로 시작 |
| Q-D9 | C 계산: "대부분이 예상 정답률 ≥ 70%"를 **단위 평균 예상 정답률**로 해석함. 단위 문항 수가 적으면(5개) 난이도 1~2개로 C가 흔들린다 | product-planner·qa | 평균으로 시작, 단위 문항 10개 미만이면 `unit_contribution_override` 표의 사람 값 사용 |
| Q-D10 | 재계산 시 이미 지난 주차 배치를 바꿀지 | product-planner | 바꾸지 않음(이번 주 이후만) |
