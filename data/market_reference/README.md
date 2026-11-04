# 시장 제품·광고 표현 참고 자료

공식 브랜드몰과 판매 플랫폼에서 수집한 제품·구성·가격·짧은 광고 문구·공개 지표를 보관합니다. 출처 URL과 수집 범위는 `sources.json` 및 `platform_expansion.json`에 기록되어 있습니다. 수집 시점의 자료이며 현재 가격·재고를 보장하지 않습니다.

| 파일 | 서비스에서의 사용 |
| --- | --- |
| `products.json`, `supplemental_products.json` | 제품·카테고리·성분 참고 |
| `offers.json` | 판매 구성·채널·가격 참고 |
| `copy_observations.jsonl` | 공개 광고 문구와 표현 방식 |
| `public_outcomes.json` | 제품군·브랜드의 공개 판매 지표 |
| `platform_expansion.json` | 추가 플랫폼의 제품·출처·문구·지표 |
| `sources.json` | 출처 URL·열람일·확인 범위 |

`src/cosmetic_agent/market_reference.py`가 위 자료와 `data/top_product_copies/`의 제품·문구 자료를 읽고, 생성 그래프에 유사 제품의 표현 참고를 전달합니다. 규정 검색용 Qdrant 컬렉션에는 합치지 않습니다.

시장 문구는 광고 허용 여부, 자사 제품 효능, 매출 상승의 증거가 아닙니다. 공개 시험 요약과 원보고서 보유 여부를 구분하고, 브랜드·제품군의 판매 지표를 특정 문구의 성과로 환산하지 않습니다.
