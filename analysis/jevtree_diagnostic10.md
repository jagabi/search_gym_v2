# JEV 비교 진단용 10문항

300문항 완료 실행 7개 기준. 기존 JEV 10개 제외. 전원 정답 5개 + 일부 정답 5개.
고정 난수 seed=20261003. 일부 정답은 RA만/o1만/두 baseline 모두/DS만으로 나눠 1/1/1/2개 추출.
RA만/o1만은 두 베이스라인 사이의 구분이며 DS 정답 여부는 제한하지 않는다.
전체 성능 추정용이 아니다. 짧은 실행의 미실행 문항은 오답으로 취급하지 않는다.

| ID | 그룹 | search-o1 | RAgent | DS frozen | DS v3 | DS v4 | DS v6 | DS v8 |
|---|---|---|---|---|---|---|---|---|
| 40 | all_correct | O | O | O | O | O | O | O |
| 57 | all_correct | O | O | O | O | O | O | O |
| 117 | all_correct | O | O | O | O | O | O | O |
| 326 | both_baselines_yes_some_ds_no | O | O | X | X | O | O | O |
| 366 | all_correct | O | O | O | O | O | O | O |
| 516 | only_ds_versions_yes | X | X | X | X | O | X | O |
| 598 | ragent_yes_search_o1_no | X | O | X | X | X | O | X |
| 746 | only_ds_versions_yes | X | X | O | X | X | X | X |
| 1196 | all_correct | O | O | O | O | O | O | O |
| 1230 | search_o1_yes_ragent_no | O | X | X | X | X | X | X |

실행별 정확한 경로와 짧은 실행의 추가 결과는 `jevtree_diagnostic10_manifest.json` 참조.
실행 코드/프롬프트/reader/트리 설정은 변경하지 않았다.
