"""3차 화면이 쓰던 참고 자료를 web/core/reference/ 로 옮겨 둔다.

Django 이미지(docker/Dockerfile.web)는 web/ 만 담는다 → 저장소의 app/ · data/ 를 서버에서 읽을 수 없다.
그래서 규정 · 가이드라인과 예상 매출 시나리오가 쓰는 '바뀌지 않는 자료'만 여기서 JSON 으로 떠 둔다.
(조항 검색 · 문구 판정은 AI 서버 API 를 그대로 부른다.)

실행: 저장소 루트에서 python web/scripts/export_reference.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "web" / "core" / "reference"
sys.path.insert(0, str(REPO))

from app.services import data_sources as ds  # noqa: E402


def dump(name: str, data) -> None:
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print("wrote", name)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dump("guide_rows.json", ds.guide_rows())              # 관리지침 [별표 1] 금지 표현
    dump("cases.json", ds.enforcement_trends())           # 식약처 부당광고 적발 사례
    dump("kb_stats.json", ds.kb_stats())
    ref = REPO / "data" / "sales_forecast_reference"
    for name in ("penalty_schedule.json", "copy_effect_size_distribution.json"):   # 예상 매출 시나리오
        shutil.copyfile(ref / name, OUT / name)
        print("copied", name)


if __name__ == "__main__":
    main()
