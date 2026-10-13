# S1-07 아키텍처·데이터 모델·학습 로직 v0 (설계 초안)

- 작성: Developer / 보고 대상: Chief of Staff / 작성일: 2026-10-13 / 버전: v0.1
- 입력: `docs/roadmap.md` (F1~F10 수용 기준), `docs/specs/vision.md` (W1~W3), `docs/qa/content-standard.md` (문항 메타데이터·난이도·태그·결함 처리)
- 표기: **[제안]** 사용자 승인 전 / **[가정]** 개발자가 정한 기본값 / **[확인 필요]** 사실 확인이 아직 안 된 것 / **[추정]** 해석
- 범위: 설계 문서만 쓴다. 앱 코드·패키지 설치·커밋은 하지 않았다.

## 0. 가정

1. `PLAN.md`를 읽지 못했다(저장소 접근 대기). 기술 방향이 PLAN.md와 다르면 PLAN.md가 우선하고 이 문서를 다시 맞춘다.
2. 개발 인력은 **1~2명**이고, 언어는 TypeScript 하나로 맞춘다 [가정]. 콘텐츠 인력(작성·검수)은 별도이며 개발자가 아니다.
3. 첫 해 사용자 규모는 **월 활성 1만 명 이하**로 본다 [가정]. 이 규모에서는 대규모 분산 설계가 필요 없다. 단순한 모놀리식 + 관리형 DB로 충분하다.
4. 결제는 **단일 상품 1회 결제(트랙권)** 를 기준으로 설계한다 (roadmap Q1 권장안). 월 구독으로 바뀌면 7.3의 결제 모델만 바꾼다.
5. 가격·요금 수치는 작성자가 알고 있는 공개 요금 기준이며 바뀌었을 수 있다 **[확인 필요]**. 결정 전 각 서비스 요금 페이지에서 다시 확인한다.

---

## 1. 결론 요약

| 항목 | 결정 [제안] |
|---|---|
| 기술 스택 | **Next.js(App Router, TypeScript) + Supabase(Postgres·Auth·RLS, 서울 리전) + Vercel + 토스페이먼츠 결제위젯** |
| 문항 데이터 | Postgres. 문항은 **불변 버전 행**(`item_versions`)으로 저장하고, 응답은 항상 (문항, 버전)을 가리킨다. 근거 하이라이트는 **문장 ID** 기준 |
| 콘텐츠 입력 (MVP) | 관리자 CMS를 만들지 않는다. **구조화 파일(YAML) + 스키마 검증 + 가져오기 스크립트**로 시작 (콘텐츠 인력 결정 Q4에 따라 재검토) |
| 학습 로직 | 전부 **순수 함수 + 설정 파일**로 두고 단위 테스트한다. 점수 예측은 "전문가 난이도를 로지스틱 곡선에 얹은 규칙 기반 모델 + 데이터 양에 따른 범위 하한" |
| 예측의 정직성 | 실제 성적 데이터가 없는 동안 예측은 **가설**이다. 범위를 좁게 보이지 않게 최소 폭(±25~±50)을 강제하고, F8 데이터 30건부터 보정, 100건 + 목표 달성 전에는 정확도를 대외에 쓰지 않는다 |

---

## 2. 기술 스택 후보 비교 [제안, 사용자 승인 필요]

### 2.1 후보

| 안 | 구성 | 한 줄 설명 |
|---|---|---|
| **A** | Next.js + Supabase(Postgres, Auth, Storage) + Vercel | 프론트·서버를 한 TypeScript 앱으로. DB·인증·권한(RLS)은 관리형으로 맡긴다 |
| **B** | Next.js + 관리형 Postgres(Neon 등) + ORM(Drizzle) + Auth.js, Vercel 또는 AWS 서울 | A와 같은 앱 구조, 인증·DB를 직접 조합. 벤더 의존이 작다 |
| **C** | Django(Python) + Postgres + 서버 렌더링(+htmx), Render/Fly 또는 국내 클라우드(NCP) | 전통적 모놀리식. **Django admin으로 콘텐츠 관리 화면을 거의 공짜로** 얻는다 |

### 2.2 비교 (5점 척도, 높을수록 좋음)

| 기준 | A. Next.js + Supabase | B. Next.js + Neon + Auth.js | C. Django + htmx |
|---|---|---|---|
| **개발 속도** | 5 — 인증(이메일·카카오 OAuth·익명 로그인), RLS, 마이그레이션, 로컬 개발 환경이 한 번에 | 4 — 인증·권한을 직접 짜야 함(1~2주 추가 [추정]) | 4 — CRUD·관리 화면은 가장 빠름. 단 F3 분할 화면·타이머·하이라이트 같은 상호작용 UI는 JS를 따로 써야 해서 느려짐 |
| **비용 (초기~월 1만 MAU)** | 4 — 무료 등급으로 개발, 운영은 Supabase Pro 약 $25/월 + Vercel Pro 약 $20/월/인 수준 [확인 필요] | 4 — 비슷하거나 조금 쌈 | 4 — 서버 1대 + DB로 비슷 |
| **1인~소규모 운영** | 5 — 서버 관리 없음, 백업·패치는 관리형 | 4 — 구성 요소가 하나 더 많음 | 3 — 서버·워커·정적 파일 운영을 직접 (관리형 PaaS를 쓰면 4) |
| **한국 결제 연동** | 5 — 토스페이먼츠·포트원 모두 JS SDK + 서버 승인 API. Next.js Route Handler에서 처리 | 5 — 동일 | 4 — 서버 SDK는 문제없음. 결제위젯은 JS로 별도 삽입 |
| **SEO** | 5 — 랜딩·진단 소개·학습 가이드 페이지를 정적 생성(SSG)/서버 렌더링 | 5 — 동일 | 4 — 서버 렌더링이라 SEO는 좋음. 프론트 생태계는 약함 |
| **데이터·리전 (개인정보)** | 4 — DB를 서울 리전(AWS ap-northeast-2)에 둘 수 있음 [확인 필요]. Vercel은 국외 사업자라 처리위탁·국외이전 고지 필요 | 4 — 비슷 | 5 — 국내 클라우드를 고르면 국외 이전 고지가 줄어듦 |
| **벤더 종속 위험** | 3 — Supabase Auth·RLS에 기대는 부분이 생김. 다만 DB 자체는 표준 Postgres라 덤프·이전 가능 | 5 | 5 |
| **콘텐츠 관리 화면** | 2 — 직접 만들거나 파일 기반 + Supabase Studio로 버팀 | 2 | 5 — Django admin |
| **합계** | **33** | 33 | 33 |

합계는 같다. 가중치를 이 프로젝트 상황에 맞춰 주면 갈린다:
- 개발 인력 1~2명, 인터랙션이 많은 학습 화면(F3·F4·F6)이 제품의 핵심(W2) → **개발 속도·상호작용 UI 비중이 크다.**
- 콘텐츠 관리 화면은 MVP에서 "파일 + 검증 스크립트"로 대신할 수 있다 (6장). 콘텐츠 인력이 비개발자 다수로 정해지면 그때 관리 화면을 만든다.

### 2.3 추천: A안 (Next.js + Supabase + Vercel + 토스페이먼츠)

이유:
1. **가장 빨리 F1~F10을 만든다.** F1의 "회원가입 없이 진단 → 가입하면 결과가 계정에 연결"은 Supabase 익명 로그인 + 계정 연결(link identity)로 거의 그대로 된다. 카카오 로그인도 기본 제공 제공자다.
2. **권한을 DB에서 막는다.** 사용자 기록 테이블은 RLS로 "본인 행만" 보이게 한다. 1~2명 팀이 API마다 권한 검사를 빠뜨리는 실수를 구조적으로 줄인다.
3. **한 언어(TypeScript)** 로 화면·서버·학습 로직·테스트를 다 쓴다. 학습 로직(채점·플랜·예측)을 순수 함수로 두면 서버와 브라우저가 같은 코드를 쓴다.
4. **SEO가 필요한 페이지**(랜딩, 무료 진단 소개, 응시료 지원 안내 S2)는 Next.js 정적 생성으로 해결된다.
5. **나가는 길이 있다.** DB는 표준 Postgres이고 학습 로직은 프레임워크와 분리한다. Supabase를 떠나야 하면 B안(Auth.js + 다른 Postgres)으로 옮길 수 있다.

A안의 약점과 대응:
- 콘텐츠 관리 화면이 없다 → 6장 파일 기반 파이프라인. Q4 결정 후 필요하면 Next.js 안에 `/admin` 최소 화면(검수 상태 변경, 신고 처리)만 만든다.
- 국외 사업자(Vercel·Supabase) 사용 → 개인정보처리방침에 처리위탁·국외이전 항목을 넣는다(8장). 법률 검토 필요.
- Vercel 서버리스 함수 실행 시간 제한 → 재채점(F9) 같은 무거운 일은 Supabase의 DB 함수 + 예약 작업(pg_cron) 또는 큐 테이블로 나눠 처리한다.

**C안이 나은 경우**: 개발자가 Python에 익숙하고, 콘텐츠 작성자가 5명 이상 비개발자로 정해져 관리 화면이 첫날부터 필요하면 C안이 낫다. 이 판단은 Q4(콘텐츠 인력) 결정 뒤 다시 한다.

### 2.4 결제: 토스페이먼츠 직접 연동 vs 포트원 [제안]

| | 토스페이먼츠 결제위젯 직접 | 포트원 V2 (PG 통합) |
|---|---|---|
| 장점 | 연동 층이 하나. 카드·간편결제(토스페이·카카오페이·네이버페이 등)를 위젯 하나로 [확인 필요]. 문서 한국어 | PG를 바꾸거나 여러 개 붙이기 쉬움. 결제 이력 관리 콘솔 |
| 단점 | PG를 바꾸면 결제 코드 재작성 | 한 층이 더 생김. 요금·정산 구조 확인 필요 |
| MVP 판단 | **추천**: 단일 상품·단일 PG면 충분 | 정기결제·다중 PG가 필요해지면 전환 |

어느 쪽이든 코드에서는 `PaymentProvider` 인터페이스(결제 요청 생성, 승인, 취소·부분취소, 웹훅 검증) 뒤에 숨겨서 교체 비용을 줄인다. 사업자 등록·PG 계약·통신판매업 신고는 개발 전 선행 조건이다 (사용자 할 일).

---

## 3. 시스템 구성

```
[브라우저 (반응형 웹)]
   │  Next.js 페이지: 정적(랜딩·SEO) / 서버 렌더링(대시보드) / 클라이언트(풀이 화면)
   ▼
[Next.js on Vercel (서울 함수 리전)]
   ├─ Route Handlers / Server Actions
   │    ├─ 채점 API (정답은 서버에만 있음)
   │    ├─ 세션 생성·플랜 재배분
   │    ├─ 예측 계산
   │    └─ 결제 승인·웹훅
   └─ packages/learning (순수 TS: 채점, 트랙 배정, 플랜, 복습, 예측)  ← 단위 테스트 대상
   ▼
[Supabase (서울 리전)]
   ├─ Postgres: 콘텐츠 · 학습 기록 · 예측 · 결제 (RLS)
   ├─ Auth: 이메일 매직링크 + 카카오, 익명 로그인
   ├─ pg_cron: 문항 통계 재계산(월 1회), 재채점 큐 처리, 성적 입력 요청 대상 선정
   └─ Storage: (MVP에서는 거의 안 씀. 성적표 이미지는 받지 않음 — F8)
[토스페이먼츠]  결제위젯 + 승인 API + 웹훅
[이메일 발송 (Resend 등)]  F9 접수 알림, 매직링크, S1 리마인더
```

저장소 구조 [제안]:
```
apps/web/              Next.js 앱
packages/learning/     채점·트랙·플랜·복습·예측 (프레임워크 무관, 순수 함수)
packages/content-schema/  문항 YAML 스키마(zod) + 검증기 + 가져오기 스크립트
supabase/migrations/   SQL 마이그레이션 (이 문서 5장 DDL이 출발점)
content/               (별도 저장소 권장) 문항 YAML 원본
```

핵심 원칙:
- **정답·해설은 채점 전에 브라우저로 보내지 않는다.** 문항 조회 API는 `answer`, `distractor`, `evidence`를 빼고 준다. 채점 요청이 들어오면 서버가 채점하고 그때 해설을 준다. (답 유출·콘텐츠 긁어가기 방지)
- **모의고사·진단 타이머는 서버 시각 기준**(`deadline_at`)으로 마감한다. 브라우저 시계는 표시용이다.
- **학습 로직 파라미터는 코드가 아니라 설정**(`learning_config` 테이블 또는 버전 붙은 JSON)에 둔다. 예측에는 `model_version`을 같이 저장해 나중에 비교할 수 있게 한다.

---

## 4. 데이터 모델 개요

### 4.1 엔터티 관계

```
type_tags ─┐          trap_types ─┐
           ▼                      ▼
passage_sets ─< passages    items ─< item_versions ─< item_options (보기·오답 함정)
     │                               │      ├─< item_evidence (근거 문장 하이라이트)
     └─< set_versions ───────────────┘      ├─< item_vocab
                                            └── item_stats (실측 난이도)
forms (진단 A·B / 모의고사) ─< form_slots ─> items

users(auth) ─ profiles
   ├─< sittings (진단·모의고사 1회 응시) ─< attempts
   ├─< plans ─< plan_weeks ─< plan_sessions ─< attempts
   ├─< attempts ─< attempt_causes (오답 원인)
   ├─< review_queue
   ├─< predictions (예측 스냅숏)
   ├─< actual_scores (실제 성적)
   ├─< error_reports ─> defects
   ├─< explanation_feedback
   └─< orders ─< payments / refunds → entitlements
```

### 4.2 설계 결정

| 결정 | 이유 |
|---|---|
| **문항 = `items`(정체성·상태) + `item_versions`(불변 내용)** | content-standard 2.1 `version`: "수정할 때마다 +1, 이전 버전 보관". 응답이 어느 버전을 풀었는지 알아야 F9·11.3 재채점과 F4 피드백(`item_id`·버전)이 된다 |
| **상태(`status`)는 `items`에** | 공개 중단(suspended)은 문항 전체에 즉시 걸려야 한다. 공개 중인 버전은 `items.published_version`이 가리킨다 |
| **지문은 문장 단위로 분할 저장, 문장마다 안정 ID(`s1`, `s2`…)** | F4 "근거 문장 하이라이트·스크롤". 글자 위치(offset)는 오탈자 하나에도 깨지지만 문장 ID는 유지된다. 문장 안 일부만 강조할 필요가 있으면 선택적으로 offset을 함께 둔다 |
| **보기(`item_options`)에 오답 함정 코드(`trap_code`)** | F4 "고른 오답의 함정 이름을 맨 위에", F5 "같은 함정 태그의 다른 문항". `distractor_rationale`을 보기별 행으로 쪼갠 것 |
| **태그·함정은 코드 테이블** | content-standard 4장 태그 체계는 바뀔 수 있다(product-planner 합의 필요). 코드 테이블이면 마이그레이션 없이 추가 |
| **`attempts` 한 테이블에 모든 풀이** (진단·세션·복습·모의고사) | 예측·약점·오답노트가 한 곳에서 계산된다. `context` 열로 구분 |
| **예측은 덮어쓰지 않고 스냅숏으로 쌓음** | F7 "직전 예측 대비 변경 이유", F8 "마지막 예측과 비교" |
| **파일럿 문항은 점수에 반영 안 함** | content-standard 9장 4단계. `attempts.counts_for_score`로 표시 |

### 4.3 content-standard 2장 필드 대응표

| content-standard 필드 | 저장 위치 |
|---|---|
| `item_id` | `items.item_id` (예 `RC-P5-000123`, 형식 CHECK) |
| `part` | `items.part` |
| `set_id`, `position_in_set` | `items.set_id`, `items.position_in_set` (P6·P7 필수: CHECK) |
| `stem` | `item_versions.stem` |
| `options` | `item_options` (A~D 4행, CHECK로 4개 강제는 가져오기 검증에서) |
| `answer` | `item_versions.answer` |
| `type_tag`, `sub_tags` | `item_versions.type_tag` → `type_tags`, `item_versions.sub_tags text[]` (최대 2) |
| `difficulty_expert` | `item_versions.difficulty_expert` (1~5) + 작성자·검수자 각자 값 `difficulty_votes` |
| `difficulty_empirical` | `item_stats` (정답률, 변별도, 보기별 선택률, 풀이 시간) + `items.difficulty_empirical_grade` |
| `target_track` | `item_versions.target_tracks text[]` |
| `vocab_level` | `item_versions.vocab_level` |
| `explanation_ko` | `item_versions.explanation_ko` (마크다운) |
| `distractor_rationale` | `item_options.rationale_ko` + `item_options.trap_code` |
| `key_point` | `item_versions.key_point` |
| 어휘 (6.1-5) | `item_vocab` |
| 근거 문장 위치 (6.1-2, 3.1-6·7) | `item_evidence` |
| `author_id`, `reviewer_1_id`, `reviewer_2_id`, `native_check_id` | `item_versions` 동명 열 + CHECK(작성자 ≠ 검수자) |
| `originality_check` | `item_versions.originality_check jsonb` ({result, date, method, checker_id}) |
| `source_note` | `item_versions.source_note` |
| `status` | `items.status` (enum 7개) |
| `version` | `item_versions.version` |
| `created_at`, `updated_at` | 각 테이블 |
| `defect_history` | `defects` 테이블 (item_id로 조회) |
| 세트: `set_id`, `passage_type`, `passage_count`, `passages`, `word_count`, `business_context`, `fictional_entities`, `question_count` | `passage_sets` + `set_versions` + `passages` (단어 수는 가져오기 때 자동 계산) |

---

## 5. 스키마 (Postgres DDL 초안)

> 출발점용 초안이다. 인덱스·RLS 정책은 핵심만 적었다. 읽기 쉽게 주제별로 묶어서 외래 키 대상 테이블이 뒤에 나오는 곳이 있다(`staff`, `plan_sessions`, `defects`). 실제 마이그레이션에서 생성 순서를 정리한다. 본문에서 언급만 한 보조 테이블(`regrade_jobs`, `events`, `notifications`, `learning_config`)도 구현 때 추가한다.

### 5.1 코드 테이블

```sql
create type part_no        as enum ('5','6','7');
create type track_code     as enum ('300-400','400-450','450-495');
create type item_status    as enum ('draft','self_reviewed','cross_reviewed','pilot','published','suspended','retired');
create type vocab_level    as enum ('basic','intermediate','advanced');   -- 기초/중급/고급
create type option_label   as enum ('A','B','C','D');

-- content-standard 4장 유형 태그. 예: P5-VERB.TENSE
create table type_tags (
  code        text primary key check (code ~ '^P[567]-[A-Z]+\.[A-Za-z0-9]+$'),
  part        part_no not null,
  major       text not null,          -- 'P5-VERB'
  major_label_ko text not null,       -- '동사'
  minor_label_ko text not null,       -- '시제'
  cause_family text not null check (cause_family in ('grammar','vocab','reading')),  -- F5 원인 ①② 판정용
  active      boolean not null default true
);

-- 오답 함정 이름. content-standard 3.2-1 예시에서 출발 [제안, qa-tester와 확정]
-- 예: TRAP.POS(품사 혼동), TRAP.AGR(수 일치), TRAP.TENSE(시제), TRAP.LOOKALIKE(형태 유사 어휘),
--     TRAP.ECHO(지문 단어 반복), TRAP.PARTIAL(부분만 맞는 정보), TRAP.OVERREACH(범위 과장),
--     TRAP.COLLOC(콜로케이션 불일치), TRAP.CONTEXT(문맥 불일치), TRAP.WRONGREF(다른 대상·지문 정보)
create table trap_types (
  code      text primary key,
  name_ko   text not null,            -- 화면에 보이는 함정 이름: '지문 단어 반복 함정'
  desc_ko   text not null,
  active    boolean not null default true
);

create table tracks (
  code          track_code primary key,
  name_ko       text not null,
  open          boolean not null,     -- 450-495 = false (MVP 대기 등록)
  recommended_weeks int not null,     -- 6 [제안]
  graduation    jsonb not null        -- 졸업 조건 (7.2 참조)
);
```

### 5.2 콘텐츠

```sql
create table passage_sets (
  set_id        text primary key check (set_id ~ '^RC-P[67]-[SDT]?-?[0-9]{4}$'),  -- 형식은 qa와 확정
  part          part_no not null check (part in ('6','7')),
  status        item_status not null default 'draft',
  published_version int,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

create table set_versions (
  set_id            text references passage_sets,
  version           int not null,
  passage_count     smallint not null check (passage_count between 1 and 3),
  question_count    smallint not null,
  business_context  text not null,
  fictional_entities text[] not null,
  translation_ko    text not null,          -- 6.1: 지문 전체 번역 1회
  created_at        timestamptz not null default now(),
  primary key (set_id, version),
  check ((passage_count = 1 and question_count between 2 and 4) or question_count in (4,5))
);

create table passages (
  set_id        text,
  set_version   int,
  idx           smallint not null,          -- 1~3 (이중·삼중 지문 순서)
  passage_type  text not null,              -- email, memo, online_chat ...
  -- 문장 단위 블록. 표·양식·채팅도 블록으로 표현:
  -- [{"id":"s1","kind":"header","text":"To: ..."},{"id":"s2","kind":"para_sentence","para":1,"text":"..."},
  --  {"id":"t1","kind":"table","rows":[[...]]},{"id":"c3","kind":"chat","speaker":"...","time":"10:02","text":"..."}]
  blocks        jsonb not null,
  word_count    int not null,               -- 가져오기 때 계산
  primary key (set_id, set_version, idx),
  foreign key (set_id, set_version) references set_versions
);

create table items (
  item_id        text primary key check (item_id ~ '^RC-P[567]-[0-9]{6}$'),
  part           part_no not null,
  set_id         text references passage_sets,
  position_in_set smallint,
  status         item_status not null default 'draft',
  published_version int,                    -- 학습자에게 보이는 버전
  difficulty_empirical_grade smallint check (difficulty_empirical_grade between 1 and 5),
  created_at     timestamptz not null default now(),
  updated_at     timestamptz not null default now(),
  check ((part = '5' and set_id is null and position_in_set is null)
      or (part in ('6','7') and set_id is not null and position_in_set between 1 and 5)),
  unique (set_id, position_in_set)
);

create table item_versions (
  item_id          text references items,
  version          int not null,
  set_version      int,                     -- P6·P7: 이 문항 버전이 짝지어진 지문 버전
  stem             text not null,           -- P6 빈칸 문항은 '빈칸 번호' 등 짧은 텍스트 허용
  answer           option_label not null,
  type_tag         text not null references type_tags,
  sub_tags         text[] not null default '{}' check (cardinality(sub_tags) <= 2),
  difficulty_expert smallint not null check (difficulty_expert between 1 and 5),
  difficulty_votes jsonb not null,          -- [{"by":"author","v":3},{"by":"reviewer_2","v":4},{"by":"tiebreak","v":4}]
  target_tracks    track_code[] not null check (cardinality(target_tracks) >= 1),
  vocab_level      vocab_level not null,
  explanation_ko   text not null,
  key_point        text not null,
  author_id        uuid not null references staff,
  reviewer_1_id    uuid not null references staff,
  reviewer_2_id    uuid not null references staff,
  native_check_id  uuid not null references staff,
  originality_check jsonb not null,         -- {"result":"pass|hold","date":"2026-..","method":["web_search","ngram"],"by":"..."}
  source_note      text not null,
  change_kind      text not null check (change_kind in ('initial','typo','explanation','answer_or_passage')),
  created_at       timestamptz not null default now(),
  primary key (item_id, version),
  check (reviewer_2_id <> author_id)        -- 9장: 작성자와 2차 검수자는 다른 사람
);

create table item_options (
  item_id      text,
  version      int,
  label        option_label,
  text         text not null,
  rationale_ko text not null,               -- 오답: 왜 틀렸나 / 정답: 한 줄 근거
  trap_code    text references trap_types,  -- 정답 보기는 null
  primary key (item_id, version, label),
  foreign key (item_id, version) references item_versions
);

-- 정답 근거 하이라이트. P7 NOT/TRUE는 오답 3개 근거도 (3.1-7) → option_label로 구분
create table item_evidence (
  item_id      text,
  version      int,
  passage_idx  smallint not null,
  block_id     text not null,               -- 's7'
  char_start   int, char_end int,           -- 선택: 문장 일부만 강조할 때
  for_option   option_label,                -- null = 정답 근거
  location_ko  text not null,               -- '이메일 2문단 첫 문장'
  foreign key (item_id, version) references item_versions
);

create table item_vocab (
  item_id text, version int, ord smallint,
  word text not null, pos text not null, meaning_ko text not null, collocation text,
  primary key (item_id, version, ord),
  foreign key (item_id, version) references item_versions
);

-- 5.3 실측 난이도. 월 1회 + 파일럿 50건 도달 시 재계산
create table item_stats (
  item_id        text, version int,
  computed_at    timestamptz not null,
  n_first        int not null,              -- 첫 응답 수
  p_correct      numeric(4,3),
  p_by_track     jsonb,                     -- {"300-400":0.71,...}
  point_biserial numeric(4,3),
  option_rates   jsonb,                     -- {"A":0.12,...}
  median_time_ms int,
  primary key (item_id, version, computed_at)
);

-- 진단 A·B, 모의고사. 연습 세션에서는 이 문항들을 쓰지 않는다 (측정용으로 깨끗하게 유지)
create table forms (
  form_id     text primary key,             -- 'DIAG-A', 'DIAG-B', 'MOCK-01'
  kind        text not null check (kind in ('diagnostic','mock')),
  time_limit_sec int not null,              -- 1500 / 4500
  active      boolean not null default true
);
create table form_slots (
  form_id  text references forms,
  ord      smallint not null,
  item_id  text not null references items,
  primary key (form_id, ord)
);

create table staff (
  id uuid primary key, name text not null,
  roles text[] not null                     -- author, reviewer, native, qa, admin, cs
);

-- 학습자에게 보여도 되는 문항만. 모든 학습 화면 조회는 이 뷰(또는 같은 조건의 함수)를 거친다 (F4)
create view servable_items as
select i.item_id, i.part, i.set_id, i.position_in_set, i.status,
       i.published_version as version, (i.status = 'pilot') as is_pilot
from items i
where i.status in ('published','pilot') and i.published_version is not null;
```

### 5.3 사용자·학습 기록

```sql
create table profiles (
  user_id       uuid primary key references auth.users on delete cascade,
  nickname      text,
  purpose       text check (purpose in ('civil_service','promotion','job_application','graduation','other')),
  font_scale    smallint not null default 1 check (font_scale between 0 and 2),  -- F3 글자 크기 3단계
  is_anonymous  boolean not null default false,   -- F1 비회원 진단
  marketing_opt_in boolean not null default false,
  created_at    timestamptz not null default now()
);

-- 진단 1회, 모의고사 1회
create table sittings (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null references auth.users on delete cascade,
  form_id     text not null references forms,
  started_at  timestamptz not null default now(),
  deadline_at timestamptz not null,            -- 서버 기준 마감
  submitted_at timestamptz,
  submit_reason text check (submit_reason in ('user','timeout')),
  last_ord    smallint,                        -- F1 이어 풀기 (24시간)
  result      jsonb,                           -- 파트별 정답률, 시간, 미응답 수, 약점 상위 3
  regraded_at timestamptz
);

create type attempt_context as enum ('diagnostic','mock','session','review');

create table attempts (
  id            bigint generated always as identity primary key,
  user_id       uuid not null references auth.users on delete cascade,
  item_id       text not null references items,
  item_version  int not null,
  context       attempt_context not null,
  sitting_id    uuid references sittings,
  plan_session_id uuid references plan_sessions,
  chosen        option_label,                  -- null = 미응답
  is_correct    boolean not null,
  is_first_try  boolean not null,              -- 이 사용자가 이 문항을 처음 푼 것인지 (통계·예측용)
  counts_for_score boolean not null,           -- 파일럿 문항이면 false
  time_ms       int,                           -- 문항별 풀이 시간 (F3)
  set_time_ms   int,                           -- P7 세트 단위 시간
  flagged       boolean not null default false,-- 모의고사 '표시'
  answered_at   timestamptz not null default now(),
  -- F9·11.3 재채점: 원래 값은 보존하고 재채점 결과를 따로 둔다
  regraded_is_correct boolean,
  regraded_at   timestamptz,
  foreign key (item_id, item_version) references item_versions
);
create index on attempts (user_id, answered_at desc);
create index on attempts (item_id, item_version) where is_first_try;

-- F5 오답 원인. 시스템 추정 1~2개 + 사용자 수정
create type error_cause as enum ('grammar','vocab','trap','time','guess');
create table attempt_causes (
  attempt_id  bigint references attempts on delete cascade,
  cause       error_cause not null,
  source      text not null check (source in ('system','user')),
  type_tag    text references type_tags,      -- grammar/vocab 원인일 때 묶음 키
  trap_code   text references trap_types,     -- trap 원인일 때 묶음 키
  active      boolean not null default true,  -- 사용자가 바꾸면 system 행은 false
  created_at  timestamptz not null default now(),
  primary key (attempt_id, cause, source)
);

-- F2 플랜
create table plans (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null references auth.users on delete cascade,
  track         track_code not null,
  exam_date     date not null,
  daily_minutes smallint not null check (daily_minutes in (15,25,40)),
  study_days    smallint[] not null default '{1,2,3,4,5}', -- 요일 (1=월)
  status        text not null check (status in ('active','completed','abandoned','replaced')),
  compressed    boolean not null default false,
  diagnostic_sitting_id uuid references sittings,
  config_version text not null,               -- 플랜 생성 규칙 버전
  created_at    timestamptz not null default now()
);
create unique index one_active_plan on plans (user_id) where status = 'active';

create table plan_weeks (
  plan_id   uuid references plans on delete cascade,
  week_no   smallint not null,
  starts_on date not null,
  phase     text not null check (phase in ('foundation','expand','exam')),
  part_mix  jsonb not null,                   -- {"5":0.5,"6":0.2,"7":0.3}
  session_count smallint not null,
  has_mock  boolean not null default false,
  primary key (plan_id, week_no)
);

create table plan_sessions (
  id          uuid primary key default gen_random_uuid(),
  plan_id     uuid not null references plans on delete cascade,
  week_no     smallint not null,
  scheduled_on date not null,
  planned_minutes smallint not null,
  status      text not null check (status in ('pending','in_progress','done','skipped')),
  composition jsonb,                          -- 생성 시 결정: 문항 목록, 복습 비율, 선정 이유
  started_at  timestamptz, completed_at timestamptz
);

-- 재배분 기록 (F2: 무엇이 바뀌었는지 한 줄)
create table plan_changes (
  id bigint generated always as identity primary key,
  plan_id uuid references plans on delete cascade,
  changed_at timestamptz not null default now(),
  reason text not null,                      -- 'skipped_2_sessions'
  summary_ko text not null                   -- '빠진 2회분을 남은 4주에 나눠 넣었어요 (주 5회 → 5~6회)'
);

-- F5 복습 큐: 문항 단위 간격 복습
create table review_queue (
  user_id     uuid references auth.users on delete cascade,
  item_id     text references items,
  step        smallint not null default 0,   -- 간격 단계 (7.4)
  due_on      date not null,
  understood  boolean not null default false,-- 사용자 '이해함'
  last_attempt_id bigint references attempts,
  primary key (user_id, item_id)
);
```

### 5.4 예측·실제 성적·피드백·신고

```sql
-- F7 예측 스냅숏. 덮어쓰지 않는다
create table predictions (
  id            bigint generated always as identity primary key,
  user_id       uuid not null references auth.users on delete cascade,
  computed_at   timestamptz not null default now(),
  model_version text not null,               -- 'rc-v0.1'
  trigger       text not null check (trigger in ('diagnostic','mock','sessions','regrade','recalibration')),
  rc_low        smallint not null, rc_mid smallint not null, rc_high smallint not null,
  n_items       int not null,                -- 근거 문항 수
  evidence      jsonb not null,              -- 파트별 정답률, 끌어내리는 요인 상위 2, 범위를 좁히는 데 필요한 문항 수
  change_reason_ko text,                     -- 직전 대비 |Δmid| >= 10일 때
  check (rc_low between 5 and 495 and rc_high between 5 and 495
         and rc_low <= rc_mid and rc_mid <= rc_high
         and rc_low % 5 = 0 and rc_mid % 5 = 0 and rc_high % 5 = 0)
);
create index on predictions (user_id, computed_at desc);

-- F8 실제 성적 (자기 보고만. 성적표 이미지 받지 않음)
create table actual_scores (
  id           bigint generated always as identity primary key,
  user_id      uuid not null references auth.users on delete cascade,
  exam_date    date not null,
  rc_score     smallint not null check (rc_score between 5 and 495 and rc_score % 5 = 0),
  entered_at   timestamptz not null default now(),
  compared_prediction_id bigint references predictions,  -- 시험일 이전 마지막 예측
  outcome      text check (outcome in ('in_range','above','below')),
  unique (user_id, exam_date)
);

-- F4 해설 피드백
create table explanation_feedback (
  user_id uuid references auth.users on delete cascade,
  item_id text, item_version int,
  helpful boolean not null,
  created_at timestamptz not null default now(),
  primary key (user_id, item_id, item_version)
);

-- F9 사용자 신고
create table error_reports (
  id           bigint generated always as identity primary key,
  user_id      uuid references auth.users on delete set null,
  item_id      text not null references items,
  item_version int not null,
  category     text not null check (category in ('answer','explanation','typo','other')),
  body         text check (length(body) <= 2000),
  chosen       option_label,
  user_agent   text,
  status       text not null default 'received' check (status in ('received','acknowledged','triaged','fixed','rejected')),
  acknowledged_at timestamptz,               -- 1영업일 안 접수 알림
  triaged_at   timestamptz,                  -- 2영업일 안 분류
  defect_id    bigint references defects,
  created_at   timestamptz not null default now()
);

-- content-standard 10~11장 결함 (내부·외부 출처 공통) = defect_history
create table defects (
  id          bigint generated always as identity primary key,
  item_id     text not null references items,
  item_version int not null,
  severity    text not null check (severity in ('critical','high','medium','low')),
  root_cause  text check (root_cause in ('authoring','review_miss','standard_gap')),
  summary     text not null,
  opened_at   timestamptz not null default now(),
  resolved_at timestamptz,
  resolved_version int
);

-- 상태 변경 감사 기록 (자동 중단 포함)
create table item_status_log (
  id bigint generated always as identity primary key,
  item_id text not null, from_status item_status, to_status item_status not null,
  actor text not null,                       -- staff id 또는 'system:auto_suspend'
  reason text not null, at timestamptz not null default now()
);
```

**F9 자동 중단 규칙 (DB 트리거)**: 같은 문항(현재 공개 버전)에 `category = 'answer'` 신고가 **서로 다른 사용자 3명** 이상이면 `items.status = 'suspended'`로 바꾸고 `item_status_log`에 `system:auto_suspend`를 남긴다. 한 사람이 여러 번 신고해 문항을 내리는 일을 막으려고 "서로 다른 사용자"로 센다 [제안 — 수용 기준은 "3건"이므로 product-planner·qa 확인 필요]. 공개 중단된 문항은 `servable_items`에서 빠지므로 새 세션에 나오지 않는다. 이미 생성된 세션 구성에 들어 있으면 세션을 열 때 다시 걸러낸다.

**F9 재채점 (11.3)**: `change_kind = 'answer_or_passage'`인 새 버전이 공개되면 `regrade_jobs` 큐에 넣고, 예약 작업이 (1) 이전 버전 응답의 `regraded_is_correct` 계산 (2) 관련 `sittings.result` 재계산 (3) 오답노트·복습 큐 갱신 (4) `predictions`에 `trigger='regrade'` 스냅숏 추가 (5) 앱 안 알림을 만든다. 원래 채점 값은 지우지 않는다.

### 5.5 결제 (F10)

```sql
create table products (id text primary key, name_ko text, price_krw int not null, duration_days int, active boolean);
create table orders (
  id uuid primary key default gen_random_uuid(),   -- PG orderId로 사용
  user_id uuid not null references auth.users,
  product_id text not null references products,
  amount_krw int not null,                         -- 서버가 상품에서 계산. 클라이언트 값 신뢰 안 함
  status text not null check (status in ('created','paid','canceled','partially_refunded','refunded','failed')),
  created_at timestamptz not null default now()
);
create table payments (
  id bigint generated always as identity primary key,
  order_id uuid not null references orders,
  provider text not null,                          -- 'tosspayments'
  payment_key text not null unique,                -- PG 거래 키 (멱등성)
  method text, approved_at timestamptz, raw jsonb not null  -- 카드번호 등 민감정보는 PG가 마스킹한 값만
);
create table refunds (
  id bigint generated always as identity primary key,
  order_id uuid not null references orders,
  amount_krw int not null, reason text not null,
  requested_at timestamptz not null default now(), processed_at timestamptz
);
create table entitlements (
  user_id uuid references auth.users, product_id text references products,
  starts_at timestamptz not null, ends_at timestamptz,
  source_order_id uuid references orders,
  primary key (user_id, product_id, starts_at)
);
```

결제 기록은 탈퇴해도 전자상거래법상 보관 기간(대금결제·공급 기록 5년) 동안 남긴다 [확인 필요, 법률 검토]. 그래서 결제 테이블은 `on delete cascade`를 걸지 않고 탈퇴 시 사용자 식별 정보만 분리·가명화한다.

### 5.6 RLS 기본 정책

| 테이블 | 학습자 | 서버(서비스 키) |
|---|---|---|
| `profiles`, `plans*`, `review_queue`, `predictions`, `actual_scores`, `explanation_feedback` | 본인 행 읽기·쓰기 | 전체 |
| `attempts`, `attempt_causes` | 본인 행 **읽기만**. 쓰기는 채점 API(서버)만 | 전체 |
| `sittings` | 본인 행 읽기 | 생성·마감·채점 |
| `error_reports` | 본인 행 쓰기·읽기 | 전체 |
| `items`, `item_versions`, `item_options`, `item_evidence`, `passages` | **직접 접근 금지**. 서버 API가 `servable_items` 기준으로, 채점 전에는 정답·해설을 뺀 형태로 준다 | 전체 |
| `orders`, `payments`, `refunds`, `entitlements` | 본인 행 읽기 | 전체 |
| `staff`, `defects`, `item_status_log` | 금지 | 전체 (관리 화면은 staff 역할 확인) |

---

## 6. 콘텐츠 파이프라인 (MVP) [제안]

관리자 CMS 대신 다음을 쓴다. Q4(콘텐츠 인력) 결정 후 다시 본다.

1. **원본**: 문항·세트를 YAML 파일로 작성(세트 1개 = 파일 1개). 문장 분할은 작성자가 하지 않고, 지문을 문단 단위로 쓰면 가져오기 스크립트가 문장 ID를 붙인다. 근거는 문장 텍스트 일부를 인용해 지정하면 스크립트가 ID로 바꾼다(못 찾으면 에러).
2. **검증 (CI)**: zod 스키마로 content-standard 2장 필수 필드, 형식(item_id 정규식, 보기 4개, 세트 문항 수, 단어 수 범위 7.1 — 벗어나면 사유 필드 필수), 작성자 ≠ 2차 검수자, 정답 위치 분포(3.2-4: 한 위치 35% 이하, 묶음 단위)를 검사한다. 실패하면 병합 불가.
3. **상태 전이**: `draft → … → published`는 파일의 `status`와 검수자 필드로 표현하고, 가져오기 스크립트가 허용되지 않은 전이(예: 정답이 바뀌었는데 `cross_reviewed`를 건너뜀)를 거부한다.
4. **가져오기**: 내용이 바뀐 문항만 새 `item_versions` 행을 만든다. 같은 내용이면 버전을 올리지 않는다.
5. **내부 유사도 검사 (content-standard 13장 4번)**: 가져오기 단계에서 영어 지문·문장의 5-gram shingle Jaccard 유사도로 기존 문항 은행과 비교해 상위 후보를 보고서로 낸다. 기준값은 파일럿 30문항으로 정한다(예: 0.3 이상이면 수동 확인 [가정]). 임베딩 유사도는 Next에서 검토.
6. **검수 체크리스트(10장)**: 검수 PR 템플릿의 체크박스로 둔다.

콘텐츠 작성자가 git을 쓰기 어렵다면 대안은 "Google Sheets 양식 → 내보내기 → 같은 검증·가져오기"다. 검증·가져오기 코드는 그대로 쓴다.

---

## 7. 학습 로직 v0

모든 로직은 `packages/learning`의 순수 함수다. 입력은 응답 목록·문항 메타데이터·설정, 출력은 결과 객체다. 아래 숫자는 전부 **[가정]** 이며 설정값으로 둔다.

### 7.1 진단 채점 → 구간 판정 → 트랙 배정 (F1)

**채점**
1. 30문항 응답(미응답 = 오답)을 채점한다. 파일럿 문항은 진단 폼에 넣지 않는다.
2. 7.5의 예측 모델로 RC 추정값(중앙값)과 범위를 낸다. 진단 단독이면 근거 문항이 30개라 범위 하한 폭이 **±50**이다.
3. 파트별(5·6·7) 정답률, 유형 대분류별 정답률, 시간 초과 문항 수(파트 기준 시간의 1.5배 초과)를 계산한다.
4. **약점 상위 3개 유형**: 대분류마다 `부족분 = Σ(모델이 예측한 정답 확률 − 실제 정답 여부)`를 구해 큰 순서로 3개. 근거 문항이 2개 미만인 대분류는 빼고, 남는 게 3개보다 적으면 있는 만큼만 보여 준다. (단순 정답률이 아니라 "이 실력이면 맞혔어야 할 문제를 틀린 양"이라 난이도 차이를 보정한다.)

**트랙 배정 규칙**

| 조건 | 배정 | 화면 안내 |
|---|---|---|
| 하한 ≥ 450 | 450→495 **대기 등록** + 400→450 고난도 세션 대안 | F1 수용 기준 그대로 |
| 중앙값 ≥ 400 (하한 < 450) | 400→450 | |
| 중앙값 < 400 | 300→400 | 중앙값 < 280이면 "권장 기간 8주 이상" 안내 [가정] |
| 경계: 중앙값 390~405 | 기본은 위 규칙. **Part 5 정답률 < 70%면 300→400**, 아니면 사용자에게 두 트랙 중 선택권 | "두 트랙 경계예요" 문구 |

경계 구간에서 Part 5를 보는 이유: 300→400 트랙은 Part 5·6 비중이 크게 설계되어 있다(roadmap 3.2). 문법 기초가 약하면 400→450에서 따라가기 어렵다 [추정].

**재진단**: B폼으로 1회. A를 푼 사람에게는 B만 준다. 같은 폼 재응시는 예측 근거에서 뺀다.

### 7.2 졸업 조건 (F2 대시보드)

`tracks.graduation` 예시 (roadmap F2 제안값 그대로):
```json
{"300-400": [
   {"metric":"part_accuracy","part":"5","window_items":40,"target":0.85},
   {"metric":"part7_single_accuracy","window_items":30,"target":0.70},
   {"metric":"prediction_low","target":400}],
 "400-450": [
   {"metric":"part_accuracy","part":"5","window_items":40,"target":0.90},
   {"metric":"part_accuracy","part":"6","window_items":24,"target":0.80},
   {"metric":"p7_seconds_per_item","window_sets":8,"target":"<= 60"},
   {"metric":"prediction_low","target":450}]}
```
정답률은 **최근 N문항 이동창**(첫 시도만, 복습 재풀이 제외)으로 잰다. 누적 정답률은 초반 실수를 오래 끌고 가서 진척이 안 보이기 때문이다. Part 7 시간 기준값(60초/문항)은 파일럿 풀이 시간으로 다시 정한다.

### 7.3 플랜 생성 (F2)

**입력**: 트랙, 시험일, 평일 하루 학습 시간(15/25/40분), 학습 요일(기본 월~금), 오늘 날짜, 진단 결과.

**1단계 — 필요량과 가능량**
- 트랙 필요량 `R = 권장 주수(6) × 주 5회 × 25분 = 750분` [가정].
- 가용 주수 `W = floor((시험일 − 3일 − 오늘) / 7)`. 시험 직전 3일은 가벼운 복습만 두므로 뺀다 [가정].
- 가능량 `A = W × 학습 요일 수 × 하루 시간`.

**2단계 — 판정**
| 경우 | 처리 |
|---|---|
| A ≥ R | 정상 플랜. W > 권장 주수면 앞쪽 주를 "기초 다지기 + 복습 확대"로 늘린다 |
| 0.6R ≤ A < R | 경고: "기간이 짧아 하루 N분이 필요합니다" (N = R ÷ (W × 학습 요일 수)를 15/25/40 중 바로 위 값으로). 선택지: ① 하루 시간 올리기 ② **압축 플랜**(기초 단계 축소, 약점 유형 집중) ③ 다음 시험일 고르기 |
| A < 0.6R 또는 W < 2 | 압축 플랜만 가능 + 다음 시험일 권장. "목표 점수에 닿기 어려울 수 있어요"를 숨기지 않는다 |

**3단계 — 주차 구조**

| 단계 | 비율 | 300→400 파트 비중 (5/6/7) | 400→450 파트 비중 (5/6/7) |
|---|---|---|---|
| 기초 (foundation) | 앞 40% | 0.55 / 0.25 / 0.20 | 0.35 / 0.25 / 0.40 |
| 확장 (expand) | 중간 40% | 0.40 / 0.20 / 0.40 | 0.25 / 0.20 / 0.55 (이중·삼중 포함) |
| 실전 (exam) | 뒤 20% | 0.30 / 0.20 / 0.50 + 모의고사 | 0.20 / 0.15 / 0.65 + 모의고사 |

- 모의고사(F6)는 `max(3주차, 실전 단계 첫 주)`에 1회 넣는다. MVP에 폼이 1개뿐이라 두 번째 모의고사는 없다.
- 기초 단계 안에서는 약점 상위 3개 유형의 비중을 1.5배로 올린다.

**4단계 — 세션 구성 (그날 세션을 열 때 생성)**
- 시간 → 문항 수 환산(학습 모드, 해설 읽는 시간 포함) [가정, 파일럿으로 실측]: Part 5 문항당 1.5분, Part 6 세트당 6분, Part 7 단일 세트당 6~8분(문항 수 비례), 이중·삼중 세트당 12분. 25분이면 대략 Part 5 8문항 + Part 7 단일 1세트.
- 구성: 신규 70~80% + 복습 20~30% (7.4). 복습 거리가 없으면 전부 신규.
- 문항 고르기: `servable_items`에서 (1) 트랙 일치 (2) 진단·모의고사 폼 문항 제외 (3) 이미 푼 문항 제외(복습 큐 문항은 예외) (4) 트랙 난이도 분포(content-standard 5.2)에 맞게 (5) 약점 유형 가중 (6) 최근 3세션에 나온 세트와 같은 `business_context`는 피한다.
- 파일럿 문항은 세션당 최대 2개, "새 문항(점수 미반영)" 표시.
- 하루 분량이 끝나면 "오늘 분량 완료" + 추가 학습은 선택.

**5단계 — 재배분 (F2: 이틀 이상 건너뜀)**
- 대시보드를 열 때 `skipped` 세션이 2개 이상 쌓였으면 남은 세션 수를 다시 계산한다: 빠진 분량을 남은 주에 고르게 나누되 **한 주 세션 수 증가는 +1까지**, 하루 시간은 바꾸지 않는다.
- 다 못 넣으면 기초 단계 분량을 줄이고(약점 유형은 유지), 그래도 안 되면 2단계 경고를 다시 띄운다.
- 무엇이 바뀌었는지 `plan_changes.summary_ko`에 한 줄로 남겨 보여 준다.

### 7.4 오답 원인 태깅과 복습 주기 (F5)

**원인 추정 (틀린 문항마다, 최대 2개 표시)**

| 순서 | 규칙 | 원인 |
|---|---|---|
| 1 | 고른 오답 보기에 `trap_code`가 있고, 그 함정이 문법형(TRAP.POS·AGR·TENSE)이 아닐 때 | ③ 함정 (묶음 키 = trap_code) |
| 2 | `type_tags.cause_family = 'vocab'` (P5-VOC, P6-VOC, P7-VOC) 이거나 함정이 TRAP.LOOKALIKE·COLLOC | ② 어휘 (묶음 키 = type_tag) |
| 3 | `cause_family = 'grammar'` | ① 문법 개념 (묶음 키 = type_tag) |
| 4 | 풀이 시간 > 기준 시간 × 1.5 (기준 = 그 문항 실측 중앙값, 표본 30건 미만이면 파트 기본값 P5 30초·P6 40초·P7 60초 [가정]) | ④ 시간 — 위 1~3과 함께 붙는다 |
| - | Part 7 독해형(MAIN·DET·INF 등)에서 함정 코드가 없으면 | ③ 대신 "근거 위치 놓침"으로 표시하고 묶음 키는 type_tag [제안] |
| 사용자 | 한 번 클릭으로 원인 변경 또는 ⑤ 찍음 | 시스템 행은 `active=false` |

"찍음"으로 표시된 오답은 약점 집계에서는 빼고, 복습 큐에는 넣는다.

**문항 단위 간격 복습** (같은 문항 다시 풀기)
- 틀리면 `review_queue`에 step 0, 다음 날 이후 세션에 넣는다.
- 간격: step 0 → 1일, 1 → 3일, 2 → 7일, 3 → 14일, 다시 맞히면 step +1, 틀리면 0으로. step 4에서 맞히면 큐에서 뺀다 [가정, Leitner 방식].
- 오답노트에서 "이해함"을 누르면 step 1(3일 뒤)로 옮긴다. roadmap F5의 "3일·7일" 제안과 맞춘 것이다.
- **맞힌 문항은 7일 안에 다시 나오지 않는다** (F5 수용 기준). 복습에서 맞힌 경우도 다음 간격이 최소 7일이 되도록 step 2 이상으로 둔다.

**원인 묶음 복습** (같은 이유로 틀릴 **다른** 문항)
- 묶음 = (원인, 묶음 키). 최근 21일 안에 활성 오답이 **3개 이상**이면 "열린 묶음"이다.
- 세션 생성 때 열린 묶음에서 같은 `type_tag` 또는 같은 `trap_code`를 가진 **아직 안 푼 문항**을 세션의 20~30%로 넣는다. 열린 묶음이 여럿이면 부족분(7.1과 같은 방식)이 큰 순서.
- 묶음 닫기: 그 묶음 키 문항의 최근 5회 첫 시도 정답률 ≥ 80%.
- 같은 함정 코드 문항이 은행에 부족하면(5개 미만) 같은 type_tag로 대신하고, 콘텐츠 팀에 "함정 X 문항 부족" 리포트를 남긴다. → F5가 돌아가려면 **함정 코드별 문항 수**가 콘텐츠 제작 목표에 들어가야 한다 (roadmap 3.2 커버리지 조건에 추가 제안).

### 7.5 RC 점수 예측 v0 (F7)

#### 7.5.1 무엇을 믿을 수 있고 무엇은 못 믿나 (먼저 읽기)

- 출시 시점에는 **실제 TOEIC 점수와 연결된 데이터가 0건**이다. 아래 모델의 "점수 눈금"(어느 실력이면 어느 난이도를 몇 % 맞히나)은 content-standard 5.1의 예상 정답률 표를 옮긴 **전문가 가설**이다. 문항 난이도도 처음엔 전문가 추정이다.
- 그래서 v0이 실제로 할 수 있는 것은 **같은 사람의 상대적 변화**(지난주보다 나아졌나)와 **약점 위치**를 보여 주는 것이고, 절대 점수는 **방향이 맞는 대략치**다. 실제 점수와 체계적으로 수십 점 어긋날 수 있다.
- 실제 TOEIC 자체도 같은 사람이 다시 보면 점수가 흔들린다. ETS가 공개한 섹션 점수의 측정 표준오차는 약 25점으로 알려져 있다 **[확인 필요: ETS 공식 자료로 재확인]**. 이게 맞다면 **±25보다 좁은 범위는 어떤 모델로도 의미가 없다.** roadmap F7의 최소 폭 ±25는 이 수준과 맞는다.
- 화면에는 항상 "베타 예측", 범위, 근거 문항 수를 같이 보이고, 환급·보장 조건에 쓰지 않는다(F7).

#### 7.5.2 모델

난이도를 로지스틱 곡선에 얹은 단순 모델(Rasch 계열, 추측 확률 고정)을 쓰고, 파라미터는 전문가 가설로 둔다. 응답이 쌓이면 같은 틀에서 파라미터만 데이터로 바꿔 IRT로 넘어간다(content-standard 5.3-4). 처음부터 이 틀을 쓰는 이유는 "근거 문항 수가 적을수록 범위가 넓다"가 계산에서 자연스럽게 나오고, 나중에 교체가 쉽기 때문이다.

```
점수 후보 s ∈ {5, 10, …, 495}
실력 θ(s) = (s − 400) / 50
문항 정답 확률 P(정답 | s, 난이도 d) = c + (1 − c) · σ(θ(s) − b_d)
   c = 0.20  (보기 4개 찍기 확률을 조금 낮춰 잡음)
   b = { d1: −2.5, d2: −1.5, d3: −0.2, d4: 0.8, d5: 1.8 }   [가정]
```

이 값으로 계산한 예상 정답률(추측 보정 전 σ 값 기준 대략치) — content-standard 5.1 표와 비교하는 점검표:

| RC 점수 | d1 | d2 | d3 | d4 | d5 |
|---|---|---|---|---|---|
| 300 | 0.62 | 0.38 | 0.14 | 0.06 | 0.02 |
| 350 | 0.82 | 0.62 | 0.31 | 0.14 | 0.06 |
| 425 | 0.95 | 0.88 | 0.67 | 0.43 | 0.21 |
| 470 | 0.98 | 0.95 | 0.83 | 0.65 | 0.40 |

(300→400 트랙 수강생이 d1 85%·d2 70~85%, 400→450 수강생이 d3 50~70%·d4 30~50%라는 5.1 기대와 대체로 맞도록 잡았다. qa-tester·product-planner 검토 대상이다.)

**계산 절차**
1. **근거 응답**: 점수 반영 대상(`counts_for_score`) 문항의 **첫 시도**만. 진단·모의고사·세션 모두 포함, 복습 재풀이는 제외. 난이도는 `difficulty_empirical_grade`가 있으면 그것, 없으면 `difficulty_expert`.
2. **최신성 가중**: 28일보다 오래된 응답은 가중치 0.5 [가정] (실력이 변하므로).
3. **세션 응답 할인**: 세션 풀이는 시간 압박이 없고 약점 문항 위주라 모의고사와 성격이 다르다. 세션 응답 가중치 0.7, 진단·모의고사 1.0 [가정].
4. **사후 분포**: 사전 분포 정규(평균 330, 표준편차 100) [가정 — 한국 평균 RC 303(personas.md)보다 조금 위, 넓게] × 가중 우도. 점수 격자에서 직접 계산(495개 이하라 바로 됨).
5. **중앙값** = 사후 중앙값, 5점 단위 반올림.
6. **범위** = 사후 80% 구간을 구한 뒤, 근거 문항 수에 따른 **최소 반폭**보다 좁으면 넓힌다:

| 근거 문항 수 (가중 전) | 최소 반폭 |
|---|---|
| < 60 (진단만) | ±50 |
| 60~149 | ±35 |
| ≥ 150 이고 모의고사 포함 | ±25 |
| ≥ 150, 모의고사 없음 | ±35 (실전 형식 측정이 없으므로) |

   사후 구간은 "표본이 적어서 생기는 흔들림"만 반영하고 "모델이 틀렸을 가능성"은 반영하지 못한다. 최소 반폭은 그 몫을 사람이 정해 덮어씌우는 것이다. 범위는 5~495로 자른다.
7. **"범위를 좁히려면 문항 N개 더"**: 다음 단계 최소 반폭 문턱까지 남은 문항 수(모의고사 미응시면 "모의고사 1회")를 보여 준다.

**근거 보기 (F7)**
- 근거 문항 수, 파트별 정답률.
- **끌어내리는 요인 상위 2개**: (파트 × 유형 대분류) 묶음마다 `부족분 = Σ 가중치 × (P(정답 | 현재 중앙값, d) − 실제)`를 구해 큰 순서 2개. 근거 문항 4개 미만인 묶음은 뺀다. 모의고사가 있으면 "미응답·시간 초과 N문항"도 후보로 넣는다(미응답은 오답으로 채점되어 점수에 이미 반영되어 있고, 원인을 설명하는 용도).
- 문구 예: "Part 7 이중 지문 정답률 40% (이 실력대 예상 62%)".

**변경 이유 (F7: |Δ중앙값| ≥ 10)**
- 직전 예측과 이번 예측 사이에 새로 들어온 응답을 트리거(진단/모의고사/세션/재채점)와 파트별로 나눠, 우도 변화가 가장 큰 묶음을 한 줄로: "모의고사 Part 7 결과 반영", "Part 5 세션 40문항 반영", "문항 RC-P5-000123 정답 수정으로 재계산".

**예측 갱신 시점**: 진단 완료, 모의고사 완료, 세션 응답 누적 30문항마다, 재채점, 모델 재보정. 매 문항마다 바꾸지 않는다(숫자가 출렁여 불신을 키우는 것을 피함 — 산타 "점수가 왜 떨어지는지 모름" 불만).

#### 7.5.3 실제 성적(F8)으로 보정하는 방법

**모을 것**: 실제 RC 점수, 시험일, 시험일 **이전 마지막 예측**(`compared_prediction_id`), 그 예측과 시험일 사이 간격, 근거 문항 수, 모의고사 여부, 트랙.

**단계**

| 표본 수 (실제 성적 입력) | 할 일 |
|---|---|
| 0~29 | 내부 모니터링만: 적중률(범위 안 비율), 평균 오차(실제 − 중앙값, 부호 있음 = 편향), 평균 절대 오차(MAE). 모델은 바꾸지 않는다. 표본이 이 정도면 숫자 자체가 크게 흔들린다 |
| 30~99 | **1차 보정**: ① 편향 보정: 실제 = α + β·중앙값을 맞추되, 표본이 적으므로 α=0·β=1 쪽으로 강하게 당긴다(축소 추정). 결과는 θ(s) 눈금 조정으로 반영. ② 범위 폭 보정: 잔차(실제 − 중앙값)의 절대값 80% 분위수를 근거 문항 수 구간별로 구해 최소 반폭 표를 바꾼다(적중률 80% 목표, vision.md 8장). 좁히는 쪽 변경은 표본 50건 이상일 때만 |
| ≥ 100 + 문항당 응답 300건 문항이 충분 | 문항 난이도를 실측 IRT(1PL→2PL) 값으로 바꾸고 점수 눈금을 실제 성적에 맞춰 다시 추정. 적중률 ≥ 80%·MAE ≤ 25 달성 시 정확도 공개 페이지 검토(Next, vision.md W3) |

**보정 전후 비교**: 모델이 바뀌면 `model_version`을 올리고, 과거 (예측, 실제) 쌍에 새 모델을 다시 돌려 적중률·MAE가 실제로 좋아졌는지 확인한 뒤에만 배포한다(과거 데이터 재검증).

**이 데이터의 한계 (정직하게)**
- **자기 보고 편향**: 점수가 잘 나온 사람이 더 많이 입력할 가능성이 크다 [추정]. 그러면 모델이 실제보다 낙관적으로 보정된다. 입력률(목표 30%)과 함께 입력한 사람·안 한 사람의 마지막 예측 분포를 비교해 편향 크기를 본다.
- **시간 간격**: 마지막 예측 뒤에도 공부하거나 쉰다. 간격 14일 초과 표본은 따로 본다.
- **허위 입력**: 확인 수단이 없다(성적표 이미지 안 받음 — F8). 5~495 범위 밖이나 마지막 예측과 200점 이상 차이 나는 값은 보정 계산에서 빼고 따로 검토한다 [가정].
- **표본 100건은 적다**: 80% 적중률을 100건으로 재면 신뢰구간이 대략 ±8%p 정도 된다 [추정]. 공개할 때 표본 수와 이 불확실성을 같이 적는다.
- **트랙 쏠림**: MVP 사용자는 300~450 구간이 대부분이라 450 이상 예측은 보정되지 않는다. 450 이상 범위에는 별도 표시를 둔다.

---

## 8. 보안·개인정보 기본

**수집 최소화** (개인정보보호법 기준 검토 필요 — 법률 자문 대상)
- 필수: 이메일(또는 카카오 계정 식별자), 닉네임(선택), 시험 예정일, 학습 목적, 학습 기록, 결제 기록, 자기 보고 RC 점수.
- 받지 않음: 이름·전화번호(결제 PG가 요구하면 PG 화면에서만 처리), 성적표 이미지, 수험번호, 생년월일. 만 14세 미만은 가입 제한(법정대리인 동의 절차를 만들지 않기 위해) [제안].
- 비회원 진단: 익명 사용자로 저장, 가입하지 않으면 30일 후 삭제 [가정].
- 개인정보처리방침에 **처리위탁·국외이전**(Vercel, Supabase, 이메일 발송 서비스, PG) 항목을 넣는다.
- 탈퇴: 학습 기록·예측·실제 성적 즉시 삭제(통계용으로는 가명 집계만 남김), 결제 기록은 법정 보관 기간 동안 분리 보관.

**접근 통제**
- RLS(5.6) 전 테이블 기본 거부, 필요한 정책만 연다. RLS 정책은 자동 테스트로 검증(10장).
- Supabase 서비스 키는 서버에만. 브라우저 번들에 들어가면 CI가 실패하도록 검사.
- 관리 기능(신고 처리·문항 상태 변경)은 `staff.roles` 확인 + 감사 기록(`item_status_log`).

**콘텐츠 보호**
- 정답·해설은 채점 후에만 전송(3장). 문항 조회 API에 사용자별 속도 제한(예: 분당 60회 [가정]), 대량 조회 엔드포인트 없음.
- 콘텐츠는 회사 자산이라 긁어가기를 완전히 막을 수는 없다. 비정상 패턴(짧은 시간에 수백 문항 조회) 로그·알림 정도만.

**결제**
- 카드 정보는 우리 서버를 거치지 않는다(PG 위젯).
- 금액은 서버가 `products`에서 계산해 주문을 만들고, 승인 시 PG가 돌려준 금액과 주문 금액이 같은지 확인한 뒤 승인한다.
- 웹훅은 PG 문서의 검증 방식(서명·조회 재확인)으로 확인하고 `payment_key`로 멱등 처리.

**기타**
- 비밀값은 Vercel·Supabase 환경변수에만. 저장소에 `.env` 커밋 금지(CI 비밀값 스캔).
- 로그에 이메일·자유 입력 신고 본문을 남기지 않는다.
- 백업: Supabase 일일 백업 확인, 유료 사용자 생기기 전 시점 복구(PITR) 추가 여부 결정 [비용 확인 필요].
- 의존성 취약점 자동 알림(GitHub Dependabot).

---

## 9. 배포·환경

| 환경 | 구성 | 용도 |
|---|---|---|
| local | Supabase CLI(로컬 Docker Postgres) + Next.js dev | 개발, 마이그레이션 작성 |
| preview | PR마다 Vercel 미리보기 + **staging Supabase 프로젝트**(공유) | 리뷰, QA 확인, E2E |
| production | Vercel production + production Supabase (서울 리전) | 실제 서비스 |

- 마이그레이션은 `supabase/migrations`에 SQL로, 코드와 같은 PR에서 리뷰. production 적용은 수동 승인 단계를 둔다.
- 콘텐츠 가져오기는 staging에 먼저 → QA 확인 → production. 콘텐츠 배포와 코드 배포를 분리한다.
- 브랜치 전략: 기능 브랜치 → PR → main. **main 병합·production 배포·비밀값 변경은 사용자 승인 후**(developer 역할 규칙).
- 결제는 staging에서 PG 테스트 키, production에서 실 키.
- 모니터링: Vercel 기본 로그 + 오류 추적(Sentry 등 [제안]) + 주요 지표 이벤트(진단 시작·완료, 세션 완료, 해설 열람, 신고, 성적 입력)를 `events` 테이블에 적재. 외부 분석 도구는 개인정보 검토 뒤.
- 예약 작업(pg_cron): 문항 통계 월 1회 재계산(content-standard 5.3-5), 재채점 큐, 신고 처리 기한 알림(1·2영업일), 성적 입력 요청 대상 선정(시험일 + 약 10일 [확인 필요]), 비회원 익명 데이터 30일 삭제.

---

## 10. 테스트 전략 개요

| 층 | 도구 [제안] | 무엇을 |
|---|---|---|
| 학습 로직 단위 | Vitest | 채점, 트랙 배정 경계(390·400·405·450), 플랜 판정(A ≥ R, 0.6R, W < 2), 재배분 상한(+1회/주), 복습 간격, "맞힌 문항 7일 안 미출제", 원인 추정 규칙, 예측의 성질 테스트(아래) |
| 예측 성질 테스트 | Vitest + 속성 기반(fast-check) | ① 응답을 더 맞히면 중앙값이 내려가지 않는다 ② 범위 반폭 ≥ 최소 반폭 ③ low ≤ mid ≤ high, 5점 단위, 5~495 ④ 근거 문항이 늘면 최소 반폭이 커지지 않는다 |
| 예측 시뮬레이션 | 스크립트 | 모델에서 가상 학습자를 만들어 범위 적중률이 약 80% 이상인지 확인. **모델 자기 일관성 점검일 뿐 실제 정확도 검증이 아니다** (실제 검증은 F8 데이터로만) |
| 콘텐츠 검증 | zod + CI | content-standard 2장 필수 필드, 형식, 정답 위치 분포, 근거 인용 매칭, 작성자 ≠ 검수자 |
| DB | pgTAP 또는 Supabase 테스트 | RLS: 다른 사용자 행 접근 불가, 학습자가 `item_versions` 직접 조회 불가, F9 자동 중단 트리거(서로 다른 3명), 재채점이 원래 채점값을 보존 |
| API | Vitest + 로컬 Supabase | 채점 전 응답에 정답·해설이 없음, 마감 후 제출 거부, 결제 금액 불일치 거부, 웹훅 멱등성 |
| E2E | Playwright | F1~F10 수용 기준의 주요 흐름 (비회원 진단 → 24시간 내 이어 풀기 → 가입 후 결과 연결, 분할 화면 1024px 경계, 근거 하이라이트 스크롤, 모의고사 자동 제출, 해지 2클릭) |
| 성능 | Lighthouse CI | F3 "3초 안 상호작용" (qa-tester가 기준·측정 환경 확정) |
| 브라우저 | Playwright (Chromium·WebKit) + 수동(Edge) | Chrome·Edge·Safari 최신 2개 버전 (F3) |

qa-tester에게 넘길 때 "변경 사항·실행 방법·테스트 방법" 요약을 PR마다 붙인다.

---

## 11. 구현 순서 (roadmap Now-2와 맞춤) [제안]

| 스프린트 | 범위 | 비고 |
|---|---|---|
| S2 | 저장소 셋업, 스키마 마이그레이션 1차(콘텐츠), 콘텐츠 YAML 스키마·검증·가져오기, 파일럿 30문항 넣기 | S2 문항 파일럿 제작과 같이 가야 처리량 실측이 됨 |
| S3 | F1 진단(비회원·이어 풀기·결과), F3 분할 화면, F4 해설·근거 하이라이트 | 예측 v0 계산 함수(진단용) 포함 |
| S4 | F2 플랜·세션 생성·재배분, F5 원인 태깅·복습, F9 신고·자동 중단 | |
| S5 | F6 모의고사, F7 예측 근거·변경 이유, F8 성적 입력, F10 결제(테스트 키) | 재채점 작업 |

---

## 12. 열린 질문 (결정 필요)

| # | 질문 | 누가 | 개발 권장 |
|---|---|---|---|
| D1 | **기술 스택 A안 승인** | 사용자 | A안 (2.3) |
| D2 | 결제: 토스페이먼츠 직접 vs 포트원 | 사용자 | 토스페이먼츠 직접 (단일 상품·단일 PG 전제) |
| D3 | 로그인 수단: 이메일 매직링크 + 카카오 / 이메일만 | 사용자·product-planner | 이메일 + 카카오 (F10 "소셜 1종") |
| D4 | 콘텐츠 입력: YAML 파일 / 구글 시트 / 관리 화면 | Chief of Staff (Q4와 함께) | 작성자가 개발 친화적이면 YAML, 아니면 시트 |
| D5 | 함정 코드 목록(`trap_types`) 확정 | qa-tester·product-planner | 5.1의 10개로 시작 |
| D6 | F9 자동 중단: "3건" vs "서로 다른 사용자 3명" | product-planner·qa-tester | 서로 다른 사용자 3명 |
| D7 | 예측 모델 파라미터(7.5.2 b값, 최소 반폭, 사전 분포) 검토 | qa-tester·product-planner | 파일럿 응답으로 S4에 1차 조정 |
| D8 | ETS 섹션 점수 측정 표준오차 확인 | market-researcher 또는 qa-tester | 공식 자료 확인 후 7.5.1 문구 확정 |
| D9 | 개인정보처리방침·국외이전·결제 기록 보관 기간 법률 검토 | Chief of Staff (외부 자문) | 유료 출시 전 필수 |
| D10 | PLAN.md 반영 | 사용자 (저장소 권한) | 권한이 생기면 이 문서 재검토 |
