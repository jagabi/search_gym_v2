# search-o1만 맞힌 15문항 재검토

동일한 300개 문항: JEV 44, search-o1 43, 공통 정답 28. 분석 대상은 search-o1 정답 / JEV 오답인 15개다. 저장된 질문, 답변, 검색열, 트리, reader 결과를 대조했다. 기존 원문 검증을 재사용하고 검색 진입 후보와 핵심 사례를 추가 확인했다. 새 검색·모델 호출·애플리케이션 수정은 하지 않았다.

## 분류

아래는 각 문항의 대표 실패 양상에 따른 수동 분류다. 원인이 배타적이라는 의미나, 그 부분 하나를 고치면 해당 문항을 회복한다는 의미는 아니다.

|양상|문항 수|ID|
|---|---:|---|
|유효한 정답 후보 발견 실패 / 잘못된 검색 방향 지속|7|191, 326, 399, 571, 682, 1204, 1264|
|reader가 허위 근거를 생성하거나 관계를 오독|3|313, 514, 780|
|정답 또는 중간 연결고리를 접한 뒤 활용·검증 실패|4|334, 660, 1016, 1185|
|baseline의 근거 없는 추측이 적중|1|865|

## 전 문항 비교

|ID|정답|JEV에서 관찰된 실패|search-o1과 갈린 지점|
|---|---|---|---|
|191|Dr. Kang Se Hoon|Shin Hae-chul을 찾지 못하고 Chris Cornell / Robert Koblin으로 연결|의료 과실·기소 단서로 Shin 후보 발견|
|313|Spero Therapeutics|Rapport SEC 문서에 없는 직원 수·학위 보유자 수·현금 수령 조건을 reader가 만들어 최종 답에 반영|Spero 관련 문서를 확보|
|326|Baby|타워·도시 단서에 매달려 Las Vegas/St Louis 방향. 297 fetch 후 틀린 책 이름|교사·관광 가이드 경력 단서로 Fran Manushkin 발견, 3검색 30fetch|
|334|Buenos Aires|Valery Marier 발견 후 Steamship Grotesque/London으로 이탈|v-fonts.com/publishers/valery-marier에서 Montserrat·Julieta Ulanovsky 연결 확보|
|399|Ahn Byung Ik|Fantom을 발견하지 못하고 Worldcoin/Sam Altman 선택|토큰 공급량·최고가 시점 단서로 Fantom 발견|
|514|Paper and Watermark Museum|Yucatan PDF에 없는 밀랍 성인상·청동 분수 등 조건을 reader가 생성해 Mérida 선택|Fabriano와 해당 박물관 확보|
|571|Neville Gruzman|10검색 모두 1975년 컬러 TV 도입 단서에 머묾|의학을 공부하려던 건축가 단서도 사용|
|660|Ablade Glover|정답 인물의 페이지와 관련 reader 정보가 메인까지 전달됐지만 El Anatsui 선택|Glover 선택|
|682|Alexander, leukemia|질문에 없는 2023 사망·John 이름 가정 등을 삽입, 대상 인물 미발견|Ted Alexander 발견 후 부고 확인, 2검색|
|780|Raheem Sterling|맞는 경기 보고서의 경기 전체 3번째 골을 Chelsea 3번째 골로 잘못 읽음|ESPN·BBC가 Sterling을 명시. baseline의 Chelsea 요약도 오류가 있었지만 다른 자료가 정답 제공|
|865|red|저품질 페이지의 blue suitcase 문구 채택|색상 근거를 확보하지 못한 상태에서 red 추측 적중|
|1016|Fort Columbia State Park|첫 검색 스니펫에 정답 후보가 있었지만 해당 본문 점수 낮음, reader 미선정. 이후 다른 지역 건물 선택|NPS 공식 Fort Columbia 페이지 확보|
|1185|Canada|Canada 검색 및 자료 확보 시도 후 통계의 범위·분모 혼선을 해소하지 못하고 Australia 선택. 최종 제시 수치도 질문 범위 밖|Canada 선택. baseline 정답 판정이 모든 통계 근거의 정확성을 보장하지는 않음|
|1204|Islamic University of Technology|첫 9검색 ICPC, 3~9검색 Seoul 대회에 집중|2개 학부·6개 학과 단서로 IUT 연결|
|1264|Kristen Bell|대상 배우의 관련 전기 확보 실패|형제·학교 단서로 Kristen Bell을 찾고 출생 도시 확인|

## 중요한 세부 증거

### q780: 같은 reader의 오류를 다른 출처가 보완했는가

JEV 1검색, 14 fetch, reader 6개. 선정 문서:

- Chelsea 경기 보고서: direct .55 / likelihood .73.
- 여성팀 경기 일정: .03 / .18.
- Cole Palmer 소개: .03 / .18.
- 하이라이트 목록: .03 / .15.
- Chelsea 홈페이지: .02 / .15.
- 남성팀 경기 일정: .02 / .16.

경기 보고서 자체는 정답 도출에 충분했지만 reader가 골 순서를 오독했다. search-o1은 ESPN과 BBC에서 Sterling이라는 직접적인 근거를 얻었다. 특히 BBC reader에는 `R. Sterling (75'), C. Gallagher (90'+4), C. Palmer (90'+7)`가 있었다. search-o1의 Chelsea reader도 도움 선수를 James라고 표기하는 오류가 있었다. 따라서 이 사례를 단순히 JEV reader만 불안정하다고 해석하는 것은 부정확하다. baseline에는 오류를 보완할 별도 자료가 있었다.

단, JEV의 최초 검색 목록에는 baseline이 읽은 동일한 ESPN·BBC 경기 페이지가 없었다. JEV가 높은 점수로 고른 Yahoo 경기 페이지(.68)는 fetch가 실패했고, Chelsea(.34)는 성공했다. 같은 경기의 올바른 자료를 순위 때문에 버렸다고 단정할 수 없다. 검색 쿼리·시점·접근 성공률이 다른 비교다.

### q660: 트리는 성공했고, 그 뒤에 실패

검색 4의 경로: El Anatsui 소개 → 화랑 작가 목록 → Ablade Glover 소개(depth 3).

Glover는 direct .33 / likelihood .87. Ghana·UK·USA 교육과 Artists Alliance Gallery 설립 내용이 reader와 메인 입력에 전달됐다. 같은 검색의 reader 6개 중 5개는 El Anatsui 관련, 1개가 Glover였다. 그중 Clark 미술관의 같은 전시 관련 URL 3개가 포함됐다. 최종적으로 Glover를 활용하지 않았다는 사실은 확실하지만, 5:1 비중이 오답의 원인이라는 것은 가설이다.

### q313 / q514: likelihood 선정이 요약의 사실성을 보증하지 않음

- q313 Rapport SEC: direct .07 / likelihood .59. 검색 6에서 reader에 들어간 유일한 문서. 원문에 없는 질문 조건을 요약이 충족한다고 써서 즉시 Rapport로 종료.
- q514 Yucatan PDF: direct .14 / likelihood .63. 원문에 없는 wax/bronze 등의 근거를 reader가 만들어낸 뒤 검색 4에서 Mérida로 종료.

이 점수는 reader 호출 전 점수이고, reader가 이후 생성한 주장의 검증 점수가 아니다. likelihood가 높다는 이유로 reader 출력의 신뢰성이 높아지는 것은 아니다. 다만 direct가 낮은 문서를 전부 막으면 유효한 간접 단서도 잃으므로, 이 사례만으로 cutoff를 올리자는 결론은 부적절하다.

### q334: 중간 인물은 찾았지만 다른 연결을 선택

JEV 첫 검색에서 archives.design → marier.design(depth 2)로 도달. 직접 페이지에서 보인 폰트들과 woahpixels의 'Why I Love the Most Hated Font on Earth' 단서까지 reader에 전달됐다. 그러나 이후 Steamship Grotesque 방향으로 검색했다.

search-o1은 검색 3에서 v-fonts.com의 Valery Marier publisher 페이지를 읽어 Montserrat의 디자이너가 Julieta Ulanovsky임을 얻었다. 따라서 JEV가 인물을 못 찾았던 사례도, 확인된 Montserrat 링크를 낮게 평가해 잘랐던 사례도 아니다. 확인한 JEV 개인 페이지 링크 점수에는 solartype(.74), Steamship Grotesque(.52), Book Nook(.49), woahpixels(.37) 등이 있었다.

### q1016 / q1185: fetch와 스니펫 차이도 존재

q1016 첫 검색 result_6의 저품질 사이트 스니펫에는 Fort Columbia와 1896~1903이 있었다. JEV 진입 순위 2, 점수 .56으로 fetch했다. 본문은 direct .01 / likelihood .03이라 reader 미선정. 첫 검색의 reader는 0개. 스니펫은 메인 입력에 남아 있었다. 따라서 '정답 후보를 JEV가 fetch하지 않았다'는 설명은 틀리다.

q1185 Canada 관련 결과에는 공식 StatCan의 빈 본문·접근 차단도 있었고, 성공적으로 가져온 다른 자료도 있었다. 단순 fetch 실패만으로 전부 설명할 수 없으며, 마지막 답변의 수치 불일치도 별도 실패다.

## 현재 결론과 실행 가능한 후속 실험

15개 전체를 JEV 점수 또는 depth 문제로 묶을 수 없다. 정답 이름/연결고리의 검색 스니펫 수동 검색에서, 명확한 정답 자료가 JEV 진입 순위 때문에 제외된 사례는 확인되지 않았다. 이는 alias 기반 확인의 범위이며, 제외된 모든 페이지의 원문까지 조사해 부재를 증명한 것은 아니다.

사용자가 지적한 후보/가설 전환 자동 판별은 어려우므로 이번 제안에서 제외한다. reader 자체를 변경하면 baseline 비교 조건도 달라진다는 제약을 유지한다.

가장 구체적인 JEV 전용 실험 후보는 **reader에 전달하는 증거의 중복도**다. q660처럼 서로 다른 URL의 본문이 유사한 경우 reader 선정 전에 본문 유사도를 적용하면 모델 호출 추가 없이 중복 슬롯을 줄일 수 있다. 정확 일치 중복 제거는 이미 있으므로 별도 효과를 확인해야 한다. q780의 무관한 일정·홈페이지는 유사 본문 제거만으로 해결되지 않는다. 같은 domain 일괄 제한도 유효한 다단계 탐색을 자를 수 있으므로 추천하지 않는다.

더 많은 독립 자료가 생긴다는 보장은 없다. 선정 가능한 후보가 한 종류뿐이면 새 root/검색 자료가 필요하다. root 3개를 늘리고 하위 확장을 줄이는 비교는 가능하지만, 동일한 fetch 시도 예산과 reader 상한을 유지한 실험으로 효과를 확인해야 한다. 이 15개를 근거로 회복 문항 수를 예측할 수 없다.

우선 q660의 후보 6개 중 유사 문서가 실제로 몇 개인지, 저장된 전체 후보에서 어떤 문서가 대체로 들어오는지 **reader를 재호출하지 않는 선정 시뮬레이션**으로 점검할 수 있다. 이 15개만 정답 방향으로 조정하지 않도록 JEV 단독 정답 문항의 선정 변화도 함께 봐야 한다.

관련 자료: `baseline_only_entry_audit.json`, `jev_vs_search_o1_final300_diagnosis_20261007.md`.
