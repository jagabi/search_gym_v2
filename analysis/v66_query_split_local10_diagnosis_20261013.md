# v66 탐색 + query split + 로컬 Jina: 진단 10문항

실행: `runs/test/20261013-1114_jevtree_gpt-oss-20b_browsecomp_v66_query_split_local10`

## 결과와 시간

| 동일 10문항 | 이번 level/query split | 직전 LDS/query split | 과거 v66 | search-o1 |
|---|---:|---:|---:|---:|
| 정답 | 3 | 5 | 8 | 7 |
| fetch 시도 | 1,890 | 2,436 | 1,725 | 435 |
| reader 호출 | 209 | 224 | 261 | 355 |
| 문항 평균 latency | 20분 2초 | 50분 2초 | 37분 57초 | 11분 37초 |
| 문항 중앙값 | 18분 35초 | 48분 56초 | 31분 10초 | 6분 37초 |

이번 문항 latency 합은 12,022.2초다. workers=4로 병렬 실행했으므로 이 합(3시간 20분)을 전체 경과 시간으로 보면 안 된다.

전체 실행 시작/종료의 절대 시각은 로그에 저장되어 있지 않고, 현재 파일 시각은 복사 시각으로 보이므로 실제 런타임의 근거로 사용하지 않았다. 데이터셋 순서와 4개 worker, 기록된 문항 latency로 실행을 재구성하면 **약 3,802.6초 = 63분 23초**다. 채점·기록·실행 준비 등의 추가 시간을 제외한 추정이며 정확한 전체 wall time은 아니다.

각 문항 `run.start.reader_status` 모두 실제 fetch 서버가 다음 설정을 확인했다:
`http://100.111.87.95:3001`, RPM=0, concurrency=50, verified_by=fetch_server.

Jina 직접 경로 1,866회: 평균 9.57초, 중앙값 6.92초. Native 경로 14회, native 실패 후 Jina fallback 10회도 있다. 전체 fetch 1,890회 평균은 9.55초, 중앙값 6.88초. 이 시간은 호출자가 관측한 요청 시간으로 재시도/대기 등을 포함하며 순수 서버 처리 시간은 아니다.

fetch 구간의 겹침을 제거해 계산하면 문항 latency의 60.8~86.9%에서 fetch가 진행 중이었다. 속도 병목이 사라진 것은 아니다. level 확장은 같은 부모의 최대 3자식을 병렬로 열지만 부모 간에는 순차 진행한다. 동시 요청 상한 50이 곧 항상 50요청 동시 처리라는 뜻은 아니다.

실행/채점 오류 0, JEV 실패 0, context exhaustion 0. fetch 실패는 records 기준 238/1,890=12.6%다. tree_fetch_failed는 239로 1건 차이가 있어 별도 계층의 집계를 섞지 않았다. 검색은 실제 성공 기준 76회다.

## 문항별 비교

| 문항 | 이번 | 직전 LDS | 과거 v66 | search-o1 | 이번 소요 시간 |
|---|---|---|---|---|---|
| 40 | O | O | O | O | 17분 55초 |
| 57 | X | O | O | O | 6분 37초 |
| 117 | X | O | O | O | 6분 42초 |
| 326 | X | X | X | O | 27분 47초 |
| 366 | X | O | O | O | 39분 24초 |
| 516 | O | X | O | X | 37분 16초 |
| 598 | X | X | O | X | 14분 30초 |
| 746 | X | X | X | X | 19분 16초 |
| 1196 | O | O | O | O | 11분 10초 |
| 1230 | X | X | O | O | 19분 48초 |

직전 LDS 대비 516을 회복하고 57/117/366을 잃었다. search-o1 대비 516 한 문제를 더 맞혔으나 57/117/326/366/1230 다섯 문제를 더 틀렸다. 이 진단 표본은 무작위 10개가 아니다. 실행 날짜·쿼리·자료·탐색·reader 등이 다르므로 변경 하나의 인과 효과를 점수 차이만으로 확정할 수 없다.

## 핵심 사례 1: 정답 페이지를 fetch했지만 메뉴 때문에 JEV가 본문을 못 봄 (366)

정답 AND1, 현재 오답 Under Armour.

메인 첫 reasoning부터 Under Armour를 가정했고, 실제 8개 검색은 모두 그 브랜드 관련이었다. 하지만 탐색 중 정답을 뒷받침하는 페이지도 도달했다:

`https://weartesters.com/and1-the-best-shoes-of-a-legendary-brand/`

원문 65,589자 중 약 33,483자 지점부터 1993년 설립, Jay Coen Gilbert/Seth Berger/Tom Austin, University of Pennsylvania 등의 정보가 있다. 약 36,756~37,267자 지점에는 1999년 AND1 Mixtape 판촉, 3주간 약 20만 개 배포, 미국 소매업 역사상 성공적 판촉이라는 내용이 있다. 질문의 핵심 여러 조건을 확인할 수 있는 자료다.

그런데 JEV 요청의 실제 `page_text`는 번호화 후 9,298자로, 끝까지 신발 분류 메뉴였다. 앞 5,000토큰 제한 때문에 위 기사 본문이 제외됐다. 당시 query는 `"Under Armour" promotion named one of the most successful U.S. retail history`였다.

JEV 점수 direct=0.09 / query=0.07, reader 미선정. **reader가 읽고 정답을 빠뜨린 사례가 아니라, JEV 평가 입력에서 핵심 본문이 잘려 reader까지 못 간 사례**다. 본문을 제대로 보여주면 반드시 정답을 맞힌다는 반사실적 결론까지 입증한 것은 아니다.

또 선택된 다른 문서의 reader 출력에는 원문에 없는 Under Armour의 'Sure Fit' 판촉과 성공적인 소매업 판촉이라는 주장이 있었다. 실제 reader 입력인 `https://www.linkedin.com/pulse/passion-purpose-kevin-plank` 본문에는 `Sure Fit`, `retail history`가 없고, reader 자신도 해당 판촉 내용이 제공된 기사에 없다고 쓰면서 외부 출처에 있다고 주장했다. 잘못된 첫 가정이 독해에서 더 강한 확신으로 바뀌는 문제도 공존한다.

## 핵심 사례 2: 후원 회사를 'award'로 바꿔 답함 (57)

정답은 Vanderbilt clinical oncology research career development award. 현재 답은 Advanced Accelerator Applications.

reader는 NETTER-1 논문의 'Funded by Advanced Accelerator Applications'라는 문장을 회사 후원이 아닌 award 이름으로 전달했다. 또 다른 reader 출력에는 논문이 2017년 NEJM 논문임이 적혀 있었는데, 최종 답은 이를 질문의 2019년 논문이라고 답했다. 첫 검색부터 정답 논문 대신 관련 임상시험/약품 승인 문서로 흘렀다. 수집 원문에서는 정답 award 명칭을 찾지 못했다.

6분 37초라는 짧은 시간은 빠르게 정답을 찾은 성과가 아니라 5검색 후 잘못된 확신으로 끝난 결과다.

## 핵심 사례 3: 다른 구조물의 임시 휴장을 정답으로 삼음 (117)

정답은 Minister's Treehouse의 소실 연도 2019. 현재 답은 Ark Encounter의 임시 휴장 연도 2020.

앞선 검색은 Noah's Ark 동물 이야기, 농장, 질문 단어가 제목에 반복되는 Instagram popular 페이지 등을 반환했다. 이후 메인이 Noah's Ark를 가정해 검색했다. reader는 한 Instagram reel의 단독 숫자 23을 결혼식 횟수일 수 있다고 추측했고, 해당 구조물을 Ark Encounter로 연결했다. 마지막에는 코로나 시기 임시 휴장 및 하루짜리 날씨 휴장 정보까지 '구조물이 사라진 연도'의 증거처럼 읽었다.

즉 정답 자료를 그대로 읽고 2019를 누락한 사례가 아니다. 다른 대상을 가정한 검색과 관계를 잘못 해석한 독해가 결합됐다. 6분 42초에 6검색으로 종료했다.

## 지속된 실패

- 326: Chicago·1972/1973·teacher/tour guide 조합을 반복했으며 답을 못 찾았다고 종료. search-o1은 정답 Baby.
- 598: Warsaw/Statistical Research Center/추정 인물에 집중. 정답 Romanian Statistical Review 대신 Journal of Economic Behavior & Organization을 답함.
- 746: Minnesota/Riverside Drive 등의 검색을 반복하고 답을 못 찾았다고 종료. 비교한 과거 JEV/search-o1도 오답.
- 1230: 정답 Regal Cinema 대신 또 Cine Theatro Brasil. reader가 극장 역사 페이지에 없는 교통 통계·주변 시설 조건까지 보완했다. 반대로 다른 reader는 2019 INRIX PDF에서 Belo Horizonte가 160시간으로 범위 밖이라고 전달했지만 최종 답은 202시간을 확정하고 극장 역사 페이지가 모든 조건을 담고 있다고 잘못 인용했다.

## 다음 개선 우선순위 (이번에는 수정하지 않음)

1. **JEV 입력을 자르기 전에 반복 메뉴를 제거하고 기사 본문을 확보.** 우선 366 원문을 고정 사례로 사용해 5,000토큰 안에 설립·판촉 문단이 보존되는지 확인한다. JEV용 발췌만 바꾸면 baseline reader 입력을 함께 바꿀 필요가 없다. 필터가 본문/표/중요 링크를 지우지 않는지도 확인해야 한다.
2. **저장된 같은 문서로 reader 프롬프트 비교.** 원 v66의 '근거 노트, 최종 답 금지' 역할과 현재 '쿼리 답 보고' 역할을 비교하되 자유서술과 query 입력은 통제한다. 57의 회사→award, 117의 휴장→소실, 366의 없는 판촉, 1230의 없는 교통 통계를 집중 검증한다. 프롬프트 문구만 바꾸면 해결된다고 전제하지 않는다.
3. **한 번에 전체를 바꾸거나 300개를 재실행하지 않는다.** 먼저 366 같은 정답 문서가 탈락하는 재현 가능한 문제를 해결하고, 동일 10문항으로 확인한다. 메인의 첫 후보 선택 오류도 있어 JEV/reader 개선만으로 모든 오답이 해결된다고 보지는 않는다.

이번에는 운영 코드나 실험 설정을 수정하지 않았고, 추가 모델/검색 요청도 실행하지 않았다.
