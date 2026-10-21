# p20: 기존 PDF·CSV 백엔드 파서 연결

RawTree가 browser 엔진을 지정해도 URL 경로가 `.pdf`·`.csv`로 끝나면 기존 native 파서를 먼저 사용한다. 쿼리 문자열과 대소문자는 기존 file_kind 규칙으로 처리한다. 새 MCP 도구·모델·서비스·의존성을 추가하지 않았다.

```
RawTree fetch
  PDF/CSV → 백엔드 httpx 다운로드 → pypdf / 표준 csv
  나머지 → 기존 Jina
  → Document → 기존 Docling HybridChunker → bundle/chunk d3 선별 → 원문 반환
```

파일 다운로드·파싱 실패 시 Jina로 다시 넘기던 기존 fallback은 제거했다. 원사이트 상태·콘텐츠 타입·최종 URL·오류 단계(native_transport/http/download/parse)를 로그에 남긴다. 기존 동시성 제한과 파일 크기 제한을 사용한다. 스캔 PDF OCR이나 접근 우회를 추가하지 않았다. 원사이트 503이 직접 다운로드에도 발생하면 그대로 실패한다.

PDF 페이지 구분을 Markdown heading으로 넘겨 기존 청커가 페이지 맥락을 보존한다. pypdf로 얻은 외부 링크 annotation도 원문과 함께 넘겨 depth 탐색에서 링크가 사라지지 않게 했다. 파일 전체는 텍스트로 추출하되 메인모델에 모두 보내지 않으며, 읽기·영역·bundle/chunk 한도와 d3 선별은 유지한다.

CSV 원문은 표준 csv 파서로 읽고 첫 행을 청킹 구조의 열 맥락으로 사용한다. Docling이 분할된 청크에도 이 맥락을 반복하도록 한다. 각 데이터 레코드는 literal code item으로 넣어 Markdown 변환이 셀 내부 개행·따옴표·구두점을 다시 해석하지 않게 했다. 열/행 관련성의 룰 기반 선별이나 요약은 하지 않는다.

실제 native fetch를 browser fetch로 잘못 집계하지 않도록 native_fetches를 따로 기록한다. RawTree 버전은 `/20`이다. 메인모델은 여전히 search 도구만 사용한다.

오프라인 검증: RawTree 81개, 기존 depthsearch core 18개, 새 native 연결 4개. 가짜 HTTP·가짜 d3와 메모리 PDF/CSV만 사용했다. Jina·d3·검색·메인모델·채점 서버에는 요청하지 않았다. 새 검증은 직접 다운로드에서 MCP/Jina 미호출, PDF 마지막 페이지·링크, CSV 뒤쪽 행의 열 맥락·빈 값·0·인용 개행, HTTP 503 시 재시도 없이 오류 기록을 확인한다.

서버 실행:

```cmd
conda activate search
python test.py --method jevtree --model gpt-oss --benchmark browsecomp --path data/browsecomp/test_diagnostic10.json --split test --limit 10 --tag raw_browser_p20_native --expect-raw-traversal beam --no-cache
```
