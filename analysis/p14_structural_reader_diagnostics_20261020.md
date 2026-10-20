# p14: 접근 실패 진단과 관계 중심 트리 선택

2026-10-20. `jevtree / raw / beam`을 수정했다. 메인 reasoning 전달, 새로운 메인 도구, BM25/임베딩, 대체 fetch 엔진, PDF 우회 처리, 추가 HTTP probe는 도입하지 않았다.

## Reader 접근 실패 진단

기존 `_fetch_engine()`은 `raise_for_status()`에서 발생한 예외만 남겨 reader 응답 본문을 잃었다. 같은 HTTP 요청의 응답에서 아래 정보를 보존한다.

- `reader_http_status`: 로컬 Jina의 HTTP 상태. 이것을 원문 사이트 상태로 해석하면 안 된다.
- `reader_response_headers`: Content-Type/Length, server, retry-after, x-request-id의 허용 목록만 기록. Authorization/Cookie 등은 수집하지 않는다.
- `reader_code`, `reader_name`, `reader_message`: reader JSON 응답에 해당 필드가 있을 때 기록.
- `source_reported`: reader의 data에 명시된 원문 URL/상태/contentType/mimeType/메시지 등. 제공되지 않은 원문 상태나 MIME은 추정하지 않는다.
- `reader_response_excerpt`: HTTP/JSON/payload 오류 시 reader 응답 본문 앞 4,096자. 원문 근거로 메인에 넣지 않고 trace metadata에 기록한다.
- `failure_stage`: reader_transport / reader_http / reader_json / reader_payload / reader_content 구분.
- `exception_type`, `error_message`, queue/http/elapsed 시간, engine, asserted_source_status.
- `url_type_hint`: URL 경로가 .pdf로 끝나면 pdf, 그 외 unknown. 실제 MIME 검출 결과가 아니다.

정보는 문항의 `trace.jsonl` 내 `fetch.raw.reader_metadata`와 `rawtree.fetch_failed.reader_metadata`에 남는다. reader가 상위 원인 메시지를 주면 PDF 다운로드/변환 오류, 원문 상태 오류, 네트워크/timeout 등을 구분할 수 있다. reader 자체가 일반적인 오류만 반환하면 원인 확정은 여전히 불가능하다.

현재 raw 경로는 PDF URL도 `engine=browser`로 요청하며, 기존 baseline fetch에 있는 native PDF 분기로 우회하지 않는다. 따라서 PDF 다운로드/변환 문제가 원인일 가능성은 있지만 확정한 것은 아니다. 이 전송 동작은 바꾸지 않았다. 재시도·우회·추가 요청 없이 로그만 보강했다.

## 트리 확장

1. 페이지 prefix 평가에서 기존 direct_answer/query_answer와 함께 `follow_links`를 판정한다. 현재 쿼리의 미확인 관계와 구체적인 후속 경로가 있는지 묻는다.
2. 알려진 follow_links 점수가 0.5 미만이면 링크별 판정을 생략한다. 판정 실패로 점수가 없는 경우에는 낮은 관련성으로 바꾸지 않는다.
3. beam에서는 링크별 평가 전에 원질문/쿼리 페이지 점수로 부모를 좁힌다. 기존 `jev_frontier_width=2`를 사용해 깊이 전체 최대 두 부모만 링크 평가한다. 루트 여섯 개의 fetch/페이지 평가는 유지된다.
4. 선택한 부모에 대해서만 개별 링크를 d3로 평가하고 기존 부모당 후보 2개·링크 하한 0.10·다음 깊이 전체 2개를 적용한다.

이 변경은 '링크 수백 개를 모두 평가한 다음 두 개만 고르는' 작업을 줄이려는 구조 변경이다. 새 점수 하한과 부모 축소가 유용한 가지를 놓칠 위험은 있다. 비용 감소나 정확도 상승은 서버에서 확인해야 한다. best_first는 기존 rolling 순서를 유지하고 같은 follow_links 조건만 적용한다. progressive 도구를 활성화하지 않았다.

새 로그: `rawtree.expansion_selection`에 부모 후보/선택과 생략 이유, `rawtree.links`에 실제 평가한 링크, reader_stats에 `link_parent_skips`가 기록된다.

## 순차 독해와 보완 선택

1. 첫 페이지를 기존 문서 구간→번들→청크 파이프라인으로 실제 독해한다.
2. 선별한 원문 청크에서 원질문/현재 쿼리 각각의 core를 먼저 보존해 비교 문맥을 만든다. 기본 상한은 max(2×chunk_tokens, 2×region_tokens)=1,200토큰이다. 앞부분 600토큰이나 생성 요약으로 대체하지 않는다.
3. 다음 독해 후보는 기존 d3 페이지 점수로 같은 beam 폭 안에 좁힌다. 두 목적의 할당을 사용해 기본 최대 두 후보만 보완 판정한다.
4. 후보의 최초 평가 prefix는 그대로 유지한다. 이미 읽은 페이지는 원문 전체 prefix 대신 실제 선별 근거로 비교한다.
5. 선택 점수는 기존 관련도×보완성으로 계산한다. 보완성만 높고 관련성이 낮은 후보가 쉽게 올라오지 않게 한다. 보완 판정 실패 시 관련도만 사용하고 실패 로그를 유지한다.
6. 선택된 페이지의 청크/점수는 검색 내부에서 재사용한다. 최종 렌더링에서 다시 모델을 호출하거나 읽기 슬롯을 중복 차감하지 않는다. 최종 청크 4+8개 및 전체 출력 예산은 두 페이지 전체에 공동 적용한다.

새 로그: `rawtree.read_context`의 실제 core ID/토큰/read_duration_s, `rawtree.read_selection`의 후보 pool/관련도/보완성/선택 점수. 단계가 순차 독해로 바뀌었으므로 과거처럼 traversal_end→pages_selected 전체를 순수 보완 선택 시간으로 집계하면 안 된다. 그 구간에는 실제 독해도 포함된다. read_context와 jev.request의 phase를 함께 봐야 한다.

## 메인과 통제값

메인 프롬프트를 짧은 관계 확인·후보 구별·출처별 역할·종료 지시로 정리했다. 기억으로 인명/수치를 제한 조건에 넣지 않고, 근거가 요청한 답을 식별하면 주변 단서 확인만 계속하지 않도록 했다. 예산 소진 뒤에는 web_search 도구도 노출하지 않는다. 별도 답변 검토 모델은 추가하지 않았다.

검색 10회, 검색 결과 10개, 루트 6개, 깊이 3, 검색당 방문 최대 10개, 본격 독해 1+1페이지, 출력 16,000토큰, HTTP당 판정 1개와 strict wave 4개는 유지한다. 코드 버전은 `raw-browser-d3-navigation-docling/14`이며 기존 runner fingerprint로 p13 응답 캐시와 구분된다. baseline 설정/프롬프트 및 기본 fetch 동작은 수정하지 않았다.

## 확인 상태

변경한 Python의 AST 문법과 diff 공백 오류를 검사했다. 설정의 기존 scalar 예산은 유지했음을 텍스트로 확인했다. YAML parser 검사는 수행하지 않았다. reader의 실패 응답 보존/무재시도, 실제 선별 근거 재사용, 낮은 관련성의 보완 점수 과대평가, 링크 판정 전 부모 beam 및 불필요 확장 생략에 대한 회귀 테스트를 추가·갱신했다.

로컬 단위 테스트·모델 호출·replay·benchmark는 실행하지 않았다. 서버에서 검증하기 전에는 10/10, 속도 또는 정확도 개선을 주장하지 않는다.

## 서버 실행

변경 파일을 서버에 반영한 뒤 프로젝트 루트에서:

```bash
python test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --limit 10 --raw-traversal beam --expect-raw-traversal beam --tag raw_browser_p14_structural10
```

중단 후 같은 명령 끝에 `--resume`을 붙인다. p13 폴더를 지정해 이어 돌리지 않는다. 새 실행에는 접근 실패 진단도 자동 기록된다.

서버에서 별도로 회귀 테스트를 확인할 때:

```bash
python -m unittest discover -s tests -p "test_raw*.py" -q
```
