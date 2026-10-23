# 기존 5개 설정과 최신 p35의 동일 50문항 비교

모든 실행의 문항 ID와 질문 본문을 공백 정규화하여 대조했다. 50개 모두 일치한다.
표의 숫자는 실행 순서가 아닌 데이터셋 문항 ID다. p35 정답은8/50이다.

|기존 설정|기존 정답|공통 정답|기존만 정답|p35만 정답|둘 다 오답 수|
|---|---:|---|---|---|---:|
|DepthSearch ds_directed_v8|8/50|40, 57, 117, 127|8, 26, 74, 157|52, 53, 79, 131|38|
|JevTree v66|8/50|40, 57, 79, 117, 131|8, 74, 128|52, 53, 127|39|
|DepthSearch ds_answer_phase_v4|6/50|40, 52, 57, 79, 117|8|53, 127, 131|41|
|search-o1 baseline|5/50|40, 57, 117, 131|8|52, 53, 79, 127|41|
|ragent baseline|5/50|40, 57, 117|8, 128|52, 53, 79, 127, 131|40|

기존5개 설정 중 어느 것도 못 맞히고p35만 맞힌 문항: 53
기존 중 하나 이상이 맞혔지만p35가 틀린 문항: 8, 26, 74, 128, 157
모든6개 설정이 틀린 문항: 3, 7, 13, 15, 21, 22, 27, 32, 33, 37, 39, 44, 49, 55, 65, 69, 71, 75, 82, 86, 88, 90, 92, 93, 94, 96, 99, 106, 123, 129, 133, 135, 140, 149, 151, 154, 158

v66의 해당50문항은 전부 캐시 결과다. ds_answer_phase_v4의15번은 empty_response 실패이며 기록상0점으로 분류했다.

## 정답이 하나라도 있는 문항

|ID|정답|ds_directed_v8|v66|ds_answer_phase_v4|search-o1|ragent|최신 p35|
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
|8|White Mischief|O|O|O|O|O|X|
|26|Abdisalam Ibrahim|O|X|X|X|X|X|
|40|AUG 26 1999|O|O|O|O|O|O|
|52|Norman Naimark|X|X|O|X|X|O|
|53|China in Ten Words|X|X|X|X|X|O|
|57|Vanderbilt clinical oncology research career development award|O|O|O|O|O|O|
|74|Nicholas Constant|O|O|X|X|X|X|
|79|Johan Human|X|O|O|X|X|O|
|117|2019|O|O|O|O|O|O|
|127|Mallorca, Spain|O|X|X|X|X|O|
|128|Bacon, bubblegum, cinnamon and wasabi.|X|O|X|X|O|X|
|131|World Of The Dream Merchants|X|O|X|O|X|O|
|157|Mrs Biermann|O|X|X|X|X|X|

## 실행 경로

C:\Users\yundo\Desktop\search_gym_v2\runs\test\20261022-2100_jevtree_gpt-oss-20b_browsecomp_raw_browser_p35_unified_score_50

DepthSearch ds_directed_v8: C:\Users\yundo\Desktop\search_gym_v2\runs\test\20260924-0737_depthsearch_gpt-oss-20b_browsecomp_ds_directed_v8
JevTree v66: C:\Users\yundo\Desktop\search_gym_v2\runs\test\20261004-1329_jevtree_gpt-oss-20b_browsecomp_jevtree_v66_diagnostic10
DepthSearch ds_answer_phase_v4: C:\Users\yundo\Desktop\search_gym_v2\runs\test\20260922-0859_depthsearch_gpt-oss-20b_browsecomp_ds_answer_phase_v4
search-o1 baseline: C:\Users\yundo\Desktop\search_gym_v2\runs\test\20260919-1621_search-o1_gpt-oss-20b_browsecomp_paper_frozen_v1
ragent baseline: C:\Users\yundo\Desktop\search_gym_v2\runs\test\20260920-2130_ragent_gpt-oss-20b_browsecomp_paper_frozen_v1