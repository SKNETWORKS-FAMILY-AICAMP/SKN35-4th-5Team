# 매출 시나리오·시장 참고 데이터

현재 Django 매출 시나리오는 `web/core/revenue_scenario.py`에서 계산하며, 배포 이미지에 포함된 `web/core/reference/penalty_schedule.json`과 `copy_effect_size_distribution.json`을 읽습니다. 이 디렉토리에는 원본 참고 자료와 AI 생성에 쓰는 제품 판매 자료를 보관합니다.

| 파일 | 용도 |
| --- | --- |
| `penalty_schedule.json` | 표시·광고 위반 유형별 처분 기준과 규정 연결 |
| `penalty_schedule_source_excerpt.txt` | 처분 기준을 정리할 때 참고한 원문 발췌 |
| `copy_effect_size_distribution.json` | 공개 제목 비교 실험의 클릭 변화 크기 분포 |
| `product_sales_observations.jsonl` | 제품군·행사·국가·기간이 명시된 공개 판매 실적 |
| `sources.json` | 수집 자료의 출처와 범위 |
| `copy_comparison/` | 성분 프로필·시장 문구 판정과 효과 크기 산출 근거 |

규정과 시나리오 파라미터를 갱신하면 웹의 `core/reference/`에도 반영해야 합니다. 광고업무정지는 판매 전면 중단을 뜻하지 않으며, 다른 분야의 클릭 변화 크기를 화장품 매출 상승률로 해석하지 않습니다. 화면의 매출·변화 범위는 사용자 가정에 따른 계산입니다.

공개 판매 자료는 과거 제품군 실적의 참고값입니다. 현재 SKU의 순매출·판매량이나 특정 광고 문구의 인과 효과를 뜻하지 않습니다. 자료별 출처·기간·제한은 JSON에 보존합니다.
