# 성분·시장 문구와 시나리오 산출 근거

| 파일 | 용도 |
| --- | --- |
| `ingredient_profiles.json` | 공식 제품 성분·출처·수집일과 내부 예시 제품의 연결 |
| `market_copy_judgements.jsonl` | 수집된 시장 문구의 규칙 판정·사유. 생성 표현을 고를 때 참고 |
| `headline_comparisons.jsonl` | 효과 크기 분포를 계산한 공개 제목 비교 자료 |
| `manifest.json` | 제목 비교 원자료의 URL·해시·추출 기준·라이선스 |

성분 프로필과 시장 문구는 `src/cosmetic_agent/domain/` 및 `market_reference.py`에서 읽습니다. 시장 문구 판정은 수집 당시 자료이며, 현재 사용자의 제품·문구에 대한 실시간 검토를 대신하지 않습니다.

공식몰 공개 시험 요약은 원보고서 보유나 독립 검증을 의미하지 않습니다. 예시 제품의 `source_kind`, `source_url`과 원본 출처를 함께 유지합니다. 공개 제목 실험은 클릭 변화의 참고 범위이며 화장품 광고의 매출 상승 효과가 아닙니다.
