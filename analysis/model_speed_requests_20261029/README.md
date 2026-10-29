# 모델 속도 테스트 인계: d3-mini / d3-flash / pplx decider

이 폴더는 2026-10-29 대화에서 실제 사용한 요청 코드를 모델별로 모은 것이다.
세 파일 모두 Python 표준 라이브러리만 사용하며 독립 실행할 수 있다.
파일 정리 과정에서 서버에 새 성능 테스트를 보내지는 않았다.

## 먼저 알아야 할 차이

**세 모델을 동일한 요청 코드로 측정한 것이 아니다.**
d3-mini와 d3-flash는 모델 ID를 제외하면 같은 코드다.
decider는 서버 인터페이스가 달라 입력 구성, 작업 종류, 동시성 단위, 워밍업이 다르다.
기존 결과만으로 순수 모델 속도의 공정한 비교라고 결론 내리면 안 된다.

| 항목 | benchmark_d3_mini.py | benchmark_d3_flash.py | benchmark_pplx_decider.py |
|---|---|---|---|
| 서버 | http://172.16.3.192:8101 | 동일 | 동일 주소에 서버를 교체 |
| 모델 ID | vllm-sr/d3-mini | vllm-sr/d3-flash | 사용자가 pplx decider라고 알림; 모델 목록 API로 검증 못 함 |
| 추론 경로 | POST /pooling | POST /pooling | POST / |
| 작업 | task=classify, 입력당 분류 벡터 반환 | 동일 | state와 choice 질문을 주고 답/확률 반환 |
| 입력 | /tokenize로 확보한 유효 토큰 ID의 작은 집합에서 무작위 추출 | 동일 | 공백으로 구분한 무작위 대문자 문자열 + 고정 질문/선택지 |
| 4096 길이 기준 | 토큰 ID 배열의 원소 4096개 | 동일 | 템플릿과 질문 포함 usage.input_tokens=4096 |
| 배치 실험 | HTTP 요청 하나에 독립 입력 배열 1·2·4·8·16·32개 | 동일 | 이 형태의 배열 API가 확인되지 않음 |
| 동시 요청 실험 | HTTP 요청 10개 동시 전송, 각 요청에 입력 32개: 총 320개 입력 | 동일 | HTTP 요청 1·2·4·8·16·32개 동시 전송, 각 요청에 입력 1개 |
| 워밍업 | 32토큰 입력 1개 | 동일 | 길이 보정 요청 후 4096토큰 입력 1개 |
| 입력 중복 회피 | 매번 새 난수, 첫 16 토큰 조합 중복 검사 | 동일 | 매번 새 난수, 첫 16문자 조합 검사, SHA256/공통 접두부 감사 |
| 캐시 옵션 | 배치 요청마다 새 cache_salt | 동일 | 독립 요청마다 새 cache_salt를 전송 |

cache_salt를 보냈다는 사실과 서버가 실제로 캐시를 비활성화했다는 것은 다르다.
decider API는 cache_salt 필드가 적용되는지 알려주지 않았다.
HTTP 상태 200만으로 필드 적용 여부를 증명할 수 없다.
각 입력의 state는 다르지만 decider의 질문, 선택지 및 서버 템플릿은 고정이다.
프롬프트 캐시와 별개로 서버의 컴파일 결과/초기화 결과는 재사용될 수 있다.
첫 실행 지연 원인은 서버 로그나 지표로 확인하지 못했다.

## 실제 요청 모양

d3-mini / d3-flash:

```python
POST /pooling
{
    "model": "vllm-sr/d3-mini",  # flash에서는 vllm-sr/d3-flash
    "input": [[...4096개의 토큰 ID...], [...다른 4096개...]],
    "task": "classify",
    "add_special_tokens": False,
    "cache_salt": "요청마다 새 UUID"
}
```

decider:

```python
POST /
{
    "state": "요청마다 새로 생성한 무작위 영문 문자열",
    "questions": {
        "strategy": {
            "type": "choice",
            "instructions": "Which retrieval strategy best satisfies the stated requirements?",
            "criteria": {
                "A": "Always retrieve ten documents without additional searches",
                "B": "Use iterative retrieval when evidence is insufficient",
                "C": "Retrieve twenty documents and select the top three"
            }
        }
    },
    "cache_salt": "요청마다 새 UUID"
}
```

decider의 state 배열은 테스트에서 HTTP 200이어도 sequences=1이었다.
여러 questions를 넣은 테스트도 sequences=1이었다.
이를 여러 독립 입력의 서버 배치로 계산하지 않았다.
요청 전체를 배열로 넣거나 requests 배열로 감싼 형태는 HTTP 500이었다.

## 실행 방법

서버에 해당 모델이 올라와 있을 때 하나씩 실행한다.
다른 모델용 스크립트를 동시에 실행하면 성능 측정에 간섭한다.

```powershell
cd C:\Users\yundo\Desktop\search_gym_v2\analysis\model_speed_requests_20261029

# d3: 입력 배열 크기 1, 2, 4, 8, 16, 32를 순차 측정
python benchmark_d3_mini.py --test batch
python benchmark_d3_flash.py --test batch

# d3: 배치 32 요청을 10개 동시 전송
python benchmark_d3_mini.py --test concurrent
python benchmark_d3_flash.py --test concurrent

# d3: 위 두 실험을 순서대로 실행
python benchmark_d3_mini.py --test both
python benchmark_d3_flash.py --test both

# decider: 단일 입력 요청을 1, 2, 4, 8, 16, 32개씩 동시 전송
python benchmark_pplx_decider.py --test concurrent
```

결과는 스크립트 옆에 모델명·실험명·UTC 실행 시각을 포함한 JSON으로 저장한다.
동일 파일을 재실행해도 이전 실행 결과를 덮어쓰지 않는다.

## 원본 코드와 수정 범위

이 폴더의 d3 파일은 아래 배치/동시 요청 원본을 각각 함수로 감싸 한 파일로 묶었다.
명령행에서 실험 선택 가능하도록 하고 결과 파일명에 실행 시각을 붙였다.
새 파일의 배치 크기는 사용자의 최신 요청에 맞춰 32까지로 제한했다.
원본 배치 실험은 64까지였으며 원본 코드와 결과는 수정하지 않았다.
요청 본문, 난수 생성 방식 및 핵심 측정 방식은 원본을 유지했다.

저장소 루트 기준 원본 경로:

| 모델/실험 | 원본 코드 | 실제 측정 결과 |
|---|---|---|
| mini 배치 | analysis/batch_probe_20261029.py | analysis/batch_probe_20261029.json |
| mini 32×10 동시 요청 | analysis/concurrent_batch_probe_20261029.py | analysis/concurrent_batch_probe_20261029.json |
| flash 배치 | analysis/batch_probe_d3_flash_20261029.py | analysis/batch_probe_d3_flash_20261029.json |
| flash 32×10 동시 요청 | analysis/concurrent_batch_probe_d3_flash_20261029.py | analysis/concurrent_batch_probe_d3_flash_20261029.json |
| decider 최초 숫자 입력 | analysis/decider_concurrency_probe_20261029.py | analysis/decider_concurrency_probe_20261029.json |
| decider 숫자 입력 재측정 | analysis/decider_concurrency_probe_repeat_20261029.py | analysis/decider_concurrency_probe_repeat_20261029.json |
| decider 새 영문 입력(최신, 이 폴더에 수록) | analysis/decider_fresh_letters_20261029.py | analysis/decider_fresh_letters_20261029.json |

decider 최신 코드는 첫 두 실험과 달리 영문 입력을 쓰고 해시/접두부 감사를 추가했다.
코드의 digits 변수명/일부 메타데이터 키는 원본 흔적이며 최신 버전의 실제 입력은 영문자다.
calibration의 valid=false는 16/32문자 길이 보정용 입력이 4096토큰이 아니기 때문으로,
HTTP 오류라는 뜻은 아니다. 본 실험에서는 4096토큰과 sequences=1, 답 1개를 검사한다.

## 결과를 읽을 때

- 시간은 네트워크, 서버 대기, 서버 추론, 응답 파싱 등을 포함한 클라이언트 측 시간이다.
- d3 배열 배치의 시간 측정은 JSON 직렬화를 포함한다. 동시 요청 실험들은 본문을 미리 직렬화한다.
- decider 최신 코드는 요청 시간 안에 입력 해시 계산도 포함한다.
- throughput은 성공 검증된 입력 토큰 총수 / 전체 완료 시간이다.
- d3 batch의 elapsed/입력 수는 분담 비용이며 개별 입력의 실제 응답 지연이 아니다.
- 무작위 토큰/영문 입력은 합성 부하 테스트다. 자연어 업무의 정확도나 속도를 대표하지 않는다.
- mini/flash는 한 실행, decider는 서로 다른 입력으로 여러 실행을 했으며 서버 설정/다른 부하는 기록하지 못했다.

다른 세션에 넘길 핵심 요청:

> 이 폴더의 README와 세 benchmark_*.py를 읽고 기존 결과의 비교 가능성을 검토해 주세요.
> d3의 서버 배열 배치와 decider의 독립 HTTP 동시 요청이 다릅니다.
> 공정 비교를 새로 설계할 때는 요청 단위, 입력/질문 형식, 토큰 집계 범위, 워밍업,
> 동시 요청 수 및 시간 측정 경계를 먼저 맞춰야 합니다.
> 서버 초기화/컴파일이나 KV 캐시 사용 여부는 현재 결과만으로 확정하지 마세요.
