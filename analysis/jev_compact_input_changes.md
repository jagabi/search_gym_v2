# JEV v67: 5,000토큰 본문 안의 링크만 평가

v64에서 추가했던 조건 추출 단계와 question_conditions를 제거했다.
메인 루프 진입 전과 검색 전 prepare 호출을 없앴다.
JEV와 reader 입력 모두 원 질문을 직접 사용한다. reader는 자유서술을 유지한다.

## 최종 입력

1. 기존 Jina 본문에 5,000토큰 상한을 적용한다. 5,000자가 아니다.
   기존 LLM.cap을 사용하며 토크나이저 서버가 없으면 문자 기반 근사로 동작한다.
2. 절단 경계가 Markdown 링크 또는 bare URL 중간이면 그 시작 전까지 후퇴한다.
3. 이 본문 안의 URL만 기존 방문/잡링크 필터와 최대 300개 제한으로 추출한다.
4. Markdown 링크를 원래 위치의 [앵커](link_0)로 번호 붙인다.
   bare URL에는 번호를 붙이고 URL 텍스트는 유지한다. 실제 URL 매핑은 코드에서 보관한다.
5. state에는 question, page_url, page_text만 전달한다.
6. questions는 direct_answer, answer_likelihood, link_N이다. 짧은 평가 기준을 사용한다.
   기존 100링크 분할 상한은 유지한다. 추가 묶음도 같은 짧은 본문으로 독립 평가한다.
   뒤쪽 링크 문단, 별도 조건, 링크별 URL/주변 문맥/긴 기준 복사는 보내지 않는다.

분기 3/깊이 3/reader 6은 유지한다. 절단 뒤 URL은 후보에서 빠지므로 실제 노드 수는 달라질 수 있다.
reader 본문은 줄이지 않는다. 별도 요약 모델도 호출하지 않는다.
기존 보고서의 identification/verification 필드에는 각각 direct_answer/answer_likelihood를 저장한다.
trace에는 새 의미의 필드도 명시한다.
캐시는 agent/67-jevtree-prefix-only로 분리했다. 이전 결과와 캐시는 변경하지 않았다.
새 버전 평가에는 기존 v65 폴더를 resume해서 섞지 않는다.

## 검증

로컬 JEV 테스트 18개 통과. 조건 추출 호출 0회, 조건 입력 제거, 경계 URL과 범위 밖 링크 제외,
이스케이프 URL/번호 대응, reader 원문 유지, 로그와 캐시 경로를 확인했다.
유료 JEV API와 벤치마크 실행은 하지 않았다.

기존 q40/117/516/1196의 요청을 재구성했다.
정확한 토크나이저 대신 5,000토큰을 15,000자로 근사한 오프라인 결과다.

| 항목 | 이전 | 변경 |
|---|---:|---:|
| JSON 문자 수 | 26,353,444 | 6,667,850 |
| 요청 수 | 514 | 469 |
| 링크 후보 | 13,037 | 6,873 |

문자 수는 기존의 25.3%다. 실제 과금 토큰 비율과 정답률은 아직 검증하지 않았다.
이는 기존 수집 페이지의 입력 재구성이며 새 실행에서는 링크 선택과 방문 경로가 달라질 수 있다.

재현: analysis/jev_compact_input_check.py
집계: analysis/jev_compact_input_check.json
요청 예시: analysis/jev_compact_input_example.json

이 문서는 앞서 만든 v66 문단 보존 방식의 설명을 대체한다.
