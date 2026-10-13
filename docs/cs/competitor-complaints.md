# 경쟁사 리뷰 불만 유형 분류 (S1-10)

- 작성: CS Manager · 기준일: **2026-10-13**
- 대상: 산타토익(Santa, Socra AI/구 뤼이드), 해커스토익(앱·해커스인강/해커스 ONE·빅플), YBM(YBM인강·픽토), 영단기(에스티유니타스, 단기PLAYER·기출보카)
- 조사 방법: WebSearch/WebFetch로 Google Play 상세 페이지(노출 리뷰 + 평점·리뷰 수), App Store 페이지, 커뮤니티(클리앙·블라인드·어미새·개인 블로그), 언론 보도, 한국소비자원·공정위 자료를 확인했다.
- **표기 규칙**
  - **[사실]**: 기준일에 출처 페이지에서 직접 확인한 내용
  - **[추정]**: 표본이 작아 CS Manager가 판단한 내용 (빈도 등급 포함)
  - **[미검증]**: 기억에 기반한 대략적인 내용. 웹에서 재확인하지 못했다.
- **한계**
  - Google Play 상세 페이지는 앱당 2~3건의 "대표 리뷰"만 노출한다. 전체 리뷰를 크롤링하지 못했으므로 빈도는 정량 집계가 아니라 **등급(●●● 높음 / ●● 중간 / ● 낮음 / – 확인 안 됨)으로 추정**했다.
  - App Store(한국) 산타 페이지, 디시 토익갤러리 본문, 정부 보도자료 원문(korea.kr, consumer.go.kr)은 접근이 차단되거나 오류가 나서 읽지 못했다.

---

## 핵심 결론 3줄

1. **업계 최대 분쟁원은 "환급(리워드)형 상품"이다.** 소비자원 집계 기준 20·30대 인강 피해 중 외국어가 32.5%로 1위다. 리워드형 피해의 유형은 위약금 과다 34.0%, 페이백 미지급 24.6%, 연장·갱신 미이행 16.9% 순이다. 해커스·영단기 환급반 후기에서도 "서류·출석 조건이 까다롭다"는 불만이 반복된다. [사실]
2. **인강 플레이어 앱의 품질이 처참하다.** 앱의 평점은 단기PLAYER 1.3점(리뷰 약 6.7천 건), 해커스 ONE 1.7점(약 1.4천 건), YBM인강 3.5점이다. 주요 불만은 튕김·재생 실패·로딩 지연, 그리고 기기 등록·로그인 반복이다. [사실]
3. **산타는 결제보다 "문제 품질·반복, 실전과의 괴리, AI·점수 신뢰도"에서 불만이 나온다.** 산타의 평점은 4.4(Play)로 가장 높다. 그러나 "문제가 실제 토익과 다르고 같은 문제가 반복된다", "예상 점수가 후하다", "AI 질문 기능이 응답하지 않는다", "점수 산정 방식을 이해하기 어렵다"는 불만이 있다. 우리의 차별 지점 후보는 **문항 품질 + 투명한 점수 예측 + 단순하고 정직한 가격·환불**이다. [추정]

---

## 1. 앱 평점 스냅샷 (2026-10-13 확인) [사실]

| 경쟁사 | 앱 | 평점 | 리뷰 수 | 다운로드 | 출처 |
|---|---|---|---|---|---|
| 산타 | 산타 - AI 토익&토플 (Play) | 4.4 | 약 3.05만 | 100만+ | [Play](https://play.google.com/store/apps/details?id=co.riiid.vida&hl=ko) |
| 산타 | 산타 - AI 토익/토플 (App Store US) | 4.6 | 130 | – | [App Store](https://apps.apple.com/us/app/%EC%82%B0%ED%83%80-ai-%ED%86%A0%EC%9D%B5-%ED%86%A0%ED%94%8C/id1148006701?l=ko) |
| 해커스 | 해커스 토익 (Play) | 3.7~3.8 | 약 2.7천 | 100만+ | [Play](https://play.google.com/store/apps/details?id=com.hackers.app&hl=ko) |
| 해커스 | 해커스 ONE 스마트클래스 (인강 플레이어, Play) | **1.7** | 약 1.4천 | 50만+ | [Play](https://play.google.com/store/apps/details?id=com.hackers.HackersOne&hl=ko) |
| 해커스 | 해커스토익 빅플 (AI 튜터, Play) | 4.1 | 781 | 10만+ | [Play](https://play.google.com/store/apps/details?id=com.hackers.app.bigple&hl=ko) |
| 해커스 | 해커스토익 (App Store KR) | 4.4 | 497 | – | [App Store](https://apps.apple.com/KR/app/id430260350) |
| YBM | YBM인강 수강전용 앱 (Play) | 3.5 | 139 | 5만+ | [Play](https://play.google.com/store/apps/details?id=com.ybmnet.app.onlinelecture&hl=ko) |
| YBM | YBM 픽토 (AI 토익, Play) | 4.2 | 152 | 1만+ | [Play](https://play.google.com/store/apps/details?id=com.ybmnet.caet&hl=ko) |
| 영단기 | 단기PLAYER (인강 플레이어, Play) | **1.3** | 약 6.7천 | 100만+ | [Play](https://play.google.com/store/apps/details?id=com.stn.mobile_player&hl=ko) |
| 영단기 | [영단기] 토익 기출 보카 (Play) | 1.9 | 56 | 1만+ | [Play](https://play.google.com/store/apps/details?id=com.stn.toeicvocaplus&hl=ko) |

> 해석 [추정]: AI 문제풀이형 앱(산타·빅플·픽토)은 4점대이고, 인강 플레이어형 앱(해커스 ONE·단기PLAYER)은 1점대다. 기존 인강 강자의 디지털 경험이 약점이라는 신호다.

---

## 2. 불만 유형표

빈도 등급은 노출 리뷰, 커뮤니티, 기사를 종합한 **[추정]**이다.

| # | 불만 유형 | 산타 | 해커스 | YBM | 영단기 | 대표 사례 (요약·짧은 인용) | 출처 |
|---|---|---|---|---|---|---|---|
| 1 | **환급(리워드)형 조건·지급 분쟁** | ● | ●●● | ● | ●●● | 해커스 환급반 리뷰: 성적 증빙이 까다롭고, "올린 서류가 잘못 돼도 직접 확인 안 하면 따로 연락도 없다". 30일 기한을 놓칠 우려가 있다(2021-06). 업계 공통: 출석 미인정, 조건 일방 변경, 제세공과금 22%·교재비 공제로 실수령액이 적다. 산타: 출석률 80% + 앱 예상 815점이 조건이며, 카드 취소로 전액을 약 2주 만에 받았다는 긍정 후기가 있다(2022). | [해커스 Play](https://play.google.com/store/apps/details?id=com.hackers.app&hl=ko), [서울신문 2017](https://www.seoul.co.kr/news/2017/10/21/20171021020008), [투데이신문 2021](https://www.ntoday.co.kr/news/articleView.html?idxno=79806), [산타 후기 블로그](https://holeman4110.github.io/certificate/santa-toeic/) |
| 2 | **중도해지 위약금·환불 계산** | ● | ●● | ● | ●● | 업계 공통: 위약금 과다 청구가 리워드형 피해의 34.0%다. 할인 전 정가를 기준으로 공제해 환불액이 줄어든다. "의무사용기간"을 이유로 환불을 거부한다. (업체별 건수 공개 없음) | [파이낸셜뉴스 2026-07](https://www.fnnews.com/news/202607101200426847), [포인트경제 2023](https://www.pointe.co.kr/news/articleView.html?idxno=6866), [비즈한국](https://bizhankook.com/articles/20434.html) |
| 3 | **가격·요금제 구조 복잡** | ●● | ● | – | ● | 산타: "뭘 골라도 뭔가 손해보는 듯한 요금구성", 30일 약 9만 원은 부담된다, 무료체험이 3일로 짧다. 60일/100일 패키지를 잘못 골라 시험 후에도 출석을 이어가야 했다는 후기도 있다. | [클리앙 2022](https://www.clien.net/service/board/use/17086659), [어미새 2022](https://eomisae.co.kr/fe/92103712), [산타 후기 블로그](https://holeman4110.github.io/certificate/santa-toeic/) |
| 4 | **콘텐츠 오류·실전 괴리·문제 반복** | ●●● | ● | ● | ● | 산타: "문제가 실제 토익 문제와 느낌이 많이 다르고 오류가 많다", 같은 문제가 반복된다(2026-08). 리스닝이 실제보다 쉽다(2022). 영단기 보카: 오타와 잘못된 이미지, "발음이 나왔다 안 나왔다"(2023). | [산타 Play](https://play.google.com/store/apps/details?id=co.riiid.vida&hl=ko), [산타 후기 블로그](https://holeman4110.github.io/certificate/santa-toeic/), [영단기 보카 Play](https://play.google.com/store/apps/details?id=com.stn.toeicvocaplus&hl=ko) |
| 5 | **해설 접근성·해설 부족** | ● | ●● | – | – | 해커스: 리스닝 해설을 보려면 웹사이트 방문, 교재 코드 입력, 로그인, 시리즈 검색을 거쳐야 한다. "그냥 문제집 뒤에다가 해설집도 좀 껴 놓으면 안됩니까??"(2022). 빅플: Part 6·7 해설에 정답 근거 위치가 없다(2021). | [해커스 Play](https://play.google.com/store/apps/details?id=com.hackers.app&hl=ko), [빅플 Play](https://play.google.com/store/apps/details?id=com.hackers.app.bigple&hl=ko) |
| 6 | **점수 예측·채점 방식 불신** | ●● | – | – | – | 산타: AI 예상 점수가 실제보다 후하다(클리앙 댓글). "세트를 다 맞혀도 점수가 떨어진다". 너무 빨리 풀면 경고와 함께 점수에 반영되지 않는다. 반대로 예측 935점 → 실제 940점, 920 → 915로 잘 맞았다는 사례도 있다. **불신과 신뢰가 공존한다.** | [클리앙](https://www.clien.net/service/board/use/17086659), [산타 후기 블로그](https://holeman4110.github.io/certificate/santa-toeic/), [블라인드 2023](https://www.teamblind.com/kr/post/%EC%82%B0%ED%83%80%ED%86%A0%EC%9D%B5-%EC%98%88%EC%B8%A1%EC%A0%90%EC%88%98-%EB%AF%BF%EC%9D%84%EB%A7%8C%ED%95%9C%EA%B0%80%EC%9A%A9-gY5sscLK) |
| 7 | **앱 버그·재생 실패·속도** | ●● | ●●● | ●●● | ●●● | 해커스 ONE: "앱 키면 한 3초뒤에 튕깁니다"(2026-07), 와이파이가 정상인데 "네트워크 연결을 확인하라고 뜨면서 재생불가", 태블릿에서는 재생이 안 된다(2026-06). YBM인강: "강의 불러오는데만 5분이 걸리고"(2024), "버튼을 눌러도 잘 인식을 못합니다"(2025). 산타: AI 질문에 대기 문구만 나온다, 듣기 음성 앞부분이 끊긴다("k you", 2026-08, 개발사가 수정 완료라고 답변). 빅플: 진단고사 중 다음 문제가 뜨지 않는다(2020). | [해커스 ONE Play](https://play.google.com/store/apps/details?id=com.hackers.HackersOne&hl=ko), [YBM인강 Play](https://play.google.com/store/apps/details?id=com.ybmnet.app.onlinelecture&hl=ko), [산타 Play](https://play.google.com/store/apps/details?id=co.riiid.vida&hl=ko), [빅플 Play](https://play.google.com/store/apps/details?id=com.hackers.app.bigple&hl=ko) |
| 8 | **기기 등록·로그인·계정·지역 문제** | ●● | ● | – | ●●● | 단기PLAYER: 등록 기기에서도 "동영상강의 볼때마다 로그인해야해요"(2026-09), 서류를 내도 기기 삭제를 거부당했다(2026-07). 산타: 오랜만에 접속하니 앱이 전부 영어로 바뀌었고 "계정을 삭제하라"는 안내를 받았다(2026-08). 해외에서 한국 계정 로그인이 안 되고 해설이 영어로만 나온다(2023). 영단기 보카: 교재 쿠폰 PIN이 "존재하지 않는 PIN"으로 뜬다(2022). | [단기PLAYER Play](https://play.google.com/store/apps/details?id=com.stn.mobile_player&hl=ko), [산타 Play](https://play.google.com/store/apps/details?id=co.riiid.vida&hl=ko), [산타 App Store](https://apps.apple.com/us/app/%EC%82%B0%ED%83%80-ai-%ED%86%A0%EC%9D%B5-%ED%86%A0%ED%94%8C/id1148006701?l=ko), [영단기 보카 Play](https://play.google.com/store/apps/details?id=com.stn.toeicvocaplus&hl=ko) |
| 9 | **UX 복잡·학습 자율성 부족·모바일 가독성** | ●● | ●● | ●● | ● | 산타: 긴 지문(Part 7) "화면 구성이 답이 없다", 8인치 이상 태블릿을 권한다(2022). 모바일에서 Part 3·4·6·7 풀이가 어렵다(2026-08). YBM 픽토: "학습 자율성이 너무 떨어집니다", 글자 크기를 조절할 수 없다(2026-07). 채점·다음 버튼을 혼동하고 이전 문제로 돌아갈 수 없다(2023, 2026). 해커스: 메뉴와 웹사이트가 복잡하다(2021). 단기PLAYER: 최저 밝기가 너무 밝다, 진입 때마다 알람 설정을 요구한다(2026-05). | [클리앙](https://www.clien.net/service/board/use/17086659), [산타 Play](https://play.google.com/store/apps/details?id=co.riiid.vida&hl=ko), [픽토 Play](https://play.google.com/store/apps/details?id=com.ybmnet.caet&hl=ko), [해커스 Play](https://play.google.com/store/apps/details?id=com.hackers.app&hl=ko), [단기PLAYER Play](https://play.google.com/store/apps/details?id=com.stn.mobile_player&hl=ko) |
| 10 | **고객센터 응대** | ● | ●● | ● | ●● | 산타: 문의 채널이 카카오톡뿐이다(2022). 해커스: 앱 리뷰에 정형화된 답변("해커스에 바란다"로 영상·오류 정보 제출 요청)을 단다. 단기PLAYER: "상담원 불친절", 표시된 리뷰에 개발사 답변이 없다. YBM: "많은 이슈가 남아 있다"는 사과만 하고 재설치를 안내한다. | [클리앙](https://www.clien.net/service/board/use/17086659), [해커스 ONE Play](https://play.google.com/store/apps/details?id=com.hackers.HackersOne&hl=ko), [단기PLAYER Play](https://play.google.com/store/apps/details?id=com.stn.mobile_player&hl=ko), [YBM인강 Play](https://play.google.com/store/apps/details?id=com.ybmnet.app.onlinelecture&hl=ko) |
| 11 | **광고 과장·후기 조작** | – | ●●● (제재 이력) | – | ● [미검증] | 해커스: 2023-10 공정위 제재. 직원을 수험생으로 위장해 토익캠프 등 네이버 카페 16개에서 홍보 댓글을 달고 투표를 조작했다. 해커스어학원·챔프스터디·교암에 과징금 총 약 7.8억 원(잠정). 2023-06에는 "공무원 1위" 등 기만 광고로 챔프스터디에 2.86억 원(공무원·공인중개사 분야). 업계 공통: "100% 환급"·"0원" 광고가 조건을 작게 표기한다. 영단기 "300% 환급" 광고 조건에 대한 커뮤니티 불만은 기억에 기반한 내용이다 [미검증]. | [데일리안 2023-10](https://www.dailian.co.kr/news/view/1282171/), [한국일보 2023-06](https://www.hankookilbo.com/news/article/A2023062710270001869), [투데이신문](https://www.ntoday.co.kr/news/articleView.html?idxno=79806) |
| 12 | **강의 품질(강사·노후 강의)** | – | ● [미검증] | ●● [미검증] | ● [미검증] | 이번 조사에서는 직접 인용할 근거를 확보하지 못했다. 업계 통념상 YBM 강의가 오래되고 사이트가 구형이라는 불만, 영단기의 스타강사 이탈(2021 메가스터디 소송 보도)로 인한 라인업 변동이 거론된다. | [한국경제 2021 (강사 이적 소송)](https://www.hankyung.com/article/202103309351Y) — 불만 근거는 [미검증] |

### 경쟁사별 한 줄 요약 [추정]
- **산타**: 결제·환불 불만은 적은 편이다(환급 후기도 긍정적). 대신 **문항 품질·반복, 실전 난이도 괴리, 점수 산정 투명성, 계정·언어 버그, 모바일 장지문 UX**가 약점이다.
- **해커스**: **환급반 행정(서류·기한), 인강 플레이어(해커스 ONE 1.7점), 해설 접근 동선**이 약점이다. 공정위 후기 조작 제재 이력이 있어 신뢰 리스크가 있다.
- **YBM**: 노출 리뷰가 적어 불만 볼륨은 작다. 대신 **앱 반응 속도·로딩, AI 앱의 학습 자율성·글자 크기**가 약점이다.
- **영단기**: **단기PLAYER 1.3점(리뷰 약 6.7천)**으로 플레이어 불만 볼륨이 가장 크다. 기기 등록·로그인 반복, 상담 응대, 교재 쿠폰 연동 문제가 있다.

---

## 3. 업계 공통 통계 (한국소비자원·지자체) [사실]

| 항목 | 수치 | 출처 |
|---|---|---|
| 인터넷교육서비스 피해구제 신청 (2021~2025) | 4,202건, 그중 20·30대 48.2%(2,024건) | [파이낸셜뉴스 2026-07-10](https://www.fnnews.com/news/202607101200426847) |
| 20·30대 피해의 분야별 비중 | **외국어 32.5%(629건)**, 직무·취업 24.0%, 공무원 12.1%, 자격증 10.5% | 〃 |
| 20·30대 피해 중 리워드형 비중 | 32.3%(623건) | 〃 |
| 리워드형 피해 유형 | 위약금 과다 34.0%, 페이백 미지급 24.6%, 연장·갱신 미이행 16.9%, 허위·과장광고 9.1%, 정보제공 미흡 5.6% | 〃 |
| 인터넷교육 피해구제 추이 | 2019년 486건 → 2023년(8월까지) 614건. 계약 관련이 84% | [더퍼블릭 2023-10](https://www.thepublic.kr/news/articleView.html?idxno=204094) |
| 12월 집중 | 11월 222건 → 12월 367건(+65%), 계약해지 분쟁 약 52% (2019~2022) | [포인트경제 2023-11](https://www.pointe.co.kr/news/articleView.html?idxno=6866) |
| 환급형 인강 피해 유형 (2014~2016) | 위약금 33.3%, 출석 미인정 31.9%, 조건 일방 변경 18.1%, 지연·거부 7.0% | [서울신문 2017](https://www.seoul.co.kr/news/2017/10/21/20171021020008) |

> 업체별 소비자원 접수 건수는 공개 자료에서 확인하지 못했다.

---

## 4. 우리가 피해야 할 것 / 기회로 삼을 것

### 4-1. 제품 관점
| 피해야 할 것 | 기회로 삼을 것 |
|---|---|
| 같은 문항의 반복 노출, 실전과 다른 난이도, 문항 오류 방치 (산타) | **문항 품질을 공개 지표로 운영한다**: 오류 신고 → 72시간 내 수정 → 신고자 회신. 문항별 "실전 유사도" 검수 절차는 qa-tester와 함께 만든다 |
| 이유를 알 수 없는 점수 변동, 속도 경고로 점수를 미반영하는 식의 블랙박스 처리 (산타) | **설명 가능한 점수 예측**: 예측 범위(±점수), 근거 문항 수, 신뢰도를 표시한다. "예측 vs 실제" 사용자 데이터를 공개한다 |
| 해설을 보려면 웹 방문·코드 입력·로그인을 거치게 하는 동선 (해커스), 정답 근거 위치 미표시 | **풀이 직후 같은 화면에서 해설**을 보여주고, Part 6·7은 근거 문장을 하이라이트한다 |
| 무거운 인강 플레이어: 튕김·로딩 5분·태블릿 재생 불가 (해커스 ONE·YBM·단기PLAYER) | **웹 우선·가벼운 재생**: 짧은 클립, 오프라인 저장, 배속, 다크/저밝기 모드. 크래시율을 QA 출시 기준에 넣는다 |
| 모바일 장지문(Part 7) 가독성 문제, 글자 크기 고정, 이전 문제로 복귀 불가 | **분할 화면·글자 크기 조절·자유 이동**을 MVP 수용 기준에 넣는다 |
| 기기 등록 제한 + 매번 재로그인·휴대폰 인증 (영단기) | 합리적인 기기 정책(셀프 기기 해제, 월 n회)을 두고 세션을 유지한다 |

### 4-2. 정책 관점
| 피해야 할 것 | 기회로 삼을 것 |
|---|---|
| 조건이 복잡한 환급형(출석 6개 조건, 서류 반려를 통지하지 않음, 30일 기한, 제세공과금·교재비 공제) | 환급형을 넣는다면 **조건 3개 이하, 자동 출석 판정, 진행률 대시보드, 서류 반려 시 즉시 알림**. 아예 환급형 없이 **"낮은 정가 + 간단한 환불"**로 차별화하는 안도 검토한다 (product-planner 결정 필요) |
| 정가 기준 공제, 의무사용기간을 이유로 한 환불 거부 | **실결제가 기준 일할 환불**, 7일 내 무조건 청약철회. 전자상거래법·콘텐츠이용자보호지침 준수 여부는 **법률 검토 필요** |
| "뭘 골라도 손해 보는" 다층 패키지, 3일 무료체험 | 요금제 2~3개, 기간 변경·업그레이드 차액 정산, 체험 7일(제안) |
| 자동결제 해지 동선 은닉 | 해지 2탭 이내, 갱신 3일 전 알림 (업계 일반 이슈. 이번 조사에서 경쟁사별 직접 사례는 확보하지 못함 [추정]) |
| "1위" 광고, 직원 위장 후기 (해커스 제재 사례) | **검증 가능한 주장만** 한다(근거·기간 표기). 후기에 인센티브가 있으면 표시한다(해커스 ONE 리뷰에도 "쿠폰 받고 작성" 사례가 있음) |

### 4-3. CS 관점
| 피해야 할 것 | 기회로 삼을 것 |
|---|---|
| 카톡 단일 채널 (산타), 정형화된 "재설치하세요" 답변 (YBM·해커스), 리뷰 무응답 (단기PLAYER) | 앱 내 문의 + 이메일 + 카톡 3채널. **스토어 리뷰 48시간 내 개별 응답**, 원인과 조치 일정을 명시한다 |
| 오류 재현을 고객에게 떠넘김("영상 첨부해 해커스에 바란다로") | 앱 내 "문제 신고" 버튼으로 기기·버전·로그를 자동 첨부한다 |
| 계정 문제에 "삭제하라" 안내 (산타) | 계정·지역·언어 문제를 위한 복구 매뉴얼과 에스컬레이션 기준을 만든다 |
| 12월·시험 직후 분쟁 급증에 대응하지 못함 | 시즌 대비(12월, 정기시험 성적 발표 직후) FAQ와 환불 응대 템플릿을 미리 준비한다 |

---

## 5. 후속 작업 제안
- [ ] Google Play 전체 리뷰를 정량 수집한다(최근 12개월, 앱별 n≥200, 별점 1~2점 분류). 크롤러나 데이터 서비스가 필요해 이번 범위 밖이었다.
- [ ] App Store KR 리뷰와 디시 토익갤러리·네이버 카페 본문은 이번에 접근하지 못했다. 수동 표본 조사(각 30건)가 필요하다.
- [ ] 위 결론을 product-planner(차별 지점 3개, MVP 범위)와 qa-tester(크래시율·문항 오류 SLA)에 전달한다.
- [ ] 환불 정책 초안을 작성한다(`docs/cs/refund-policy-draft.md`, 법률 검토 표시 포함). 사용자 승인 후 확정한다.

---

## 출처 (접속일 2026-10-13)

**앱 스토어**
- 산타 Play: https://play.google.com/store/apps/details?id=co.riiid.vida&hl=ko
- 산타 App Store(US): https://apps.apple.com/us/app/%EC%82%B0%ED%83%80-ai-%ED%86%A0%EC%9D%B5-%ED%86%A0%ED%94%8C/id1148006701?l=ko
- 해커스 토익 Play: https://play.google.com/store/apps/details?id=com.hackers.app&hl=ko
- 해커스 ONE Play: https://play.google.com/store/apps/details?id=com.hackers.HackersOne&hl=ko
- 해커스 ONE App Store: https://apps.apple.com/us/app/%ED%95%B4%EC%BB%A4%EC%8A%A4-one-%EC%8A%A4%EB%A7%88%ED%8A%B8-%ED%81%B4%EB%9E%98%EC%8A%A4/id1538534916?l=ko
- 해커스토익 빅플 Play: https://play.google.com/store/apps/details?id=com.hackers.app.bigple&hl=ko
- 해커스토익 App Store KR: https://apps.apple.com/KR/app/id430260350
- YBM인강 Play: https://play.google.com/store/apps/details?id=com.ybmnet.app.onlinelecture&hl=ko
- YBM 픽토 Play: https://play.google.com/store/apps/details?id=com.ybmnet.caet&hl=ko
- 단기PLAYER Play: https://play.google.com/store/apps/details?id=com.stn.mobile_player&hl=ko
- 영단기 토익 기출보카 Play: https://play.google.com/store/apps/details?id=com.stn.toeicvocaplus&hl=ko

**커뮤니티·블로그**
- 클리앙 산타토익 후기(2022-03): https://www.clien.net/service/board/use/17086659
- 어미새 산타토익 질문(2022-08): https://eomisae.co.kr/fe/92103712
- 블라인드 산타 예측점수(2023-03): https://www.teamblind.com/kr/post/%EC%82%B0%ED%83%80%ED%86%A0%EC%9D%B5-%EC%98%88%EC%B8%A1%EC%A0%90%EC%88%98-%EB%AF%BF%EC%9D%84%EB%A7%8C%ED%95%9C%EA%B0%80%EC%9A%A9-gY5sscLK
- 개인 블로그 산타토익 후기(2022-03): https://holeman4110.github.io/certificate/santa-toeic/

**언론·공공**
- 파이낸셜뉴스(2026-07-10) 소비자원 인터넷교육 피해: https://www.fnnews.com/news/202607101200426847
- 더퍼블릭(2023-10-05) 인터넷교육 피해 급증: https://www.thepublic.kr/news/articleView.html?idxno=204094
- 포인트경제(2023-11-29) 인강 피해주의보: https://www.pointe.co.kr/news/articleView.html?idxno=6866
- 서울신문(2017-10-21) '100% 환불' 꼼수: https://www.seoul.co.kr/news/2017/10/21/20171021020008
- 투데이신문(2021-07-28) 수강료 100% 환급 광고: https://www.ntoday.co.kr/news/articleView.html?idxno=79806
- 비즈한국(2020-08) 인강 환불 계산(클래스101, 해커스·파고다 비교): https://bizhankook.com/articles/20434.html
- 데일리안(2023-10-12) 공정위 해커스 후기 조작 제재: https://www.dailian.co.kr/news/view/1282171/
- 한국일보(2023-06-27) 해커스 '1위' 광고 제재: https://www.hankookilbo.com/news/article/A2023062710270001869
- 한국경제(2021-03-30) 에스티유니타스 강사 이적 소송: https://www.hankyung.com/article/202103309351Y

**접근 실패(미반영)**: consumer.go.kr 리워드형 피해 원문(robots 차단), korea.kr 공정위 보도자료(robots 차단), 디시 토익갤러리 게시글(본문 미추출), App Store KR 산타 페이지(오류)
