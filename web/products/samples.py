"""
서비스에 포함된 예시 제품을 사용자 제품으로 복사한다.

sample_products.json 은 저장소 루트 data/assets/ 의 mock_products.json(시연 시나리오 제품) +
sample_products.json(제형·기능성 유형별 예시) + public_analysis_products.json(공개 분석 샘플)을
3차 화면과 같은 순서로 합친 사본이다. web 컨테이너에는 web/ 폴더만 들어가므로 사본을 둔다.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from django.db import transaction

from .models import Evidence, Product

SAMPLES_PATH = Path(__file__).with_name("sample_products.json")
# 제품 선택지 값: 내 제품은 pk("12"), 아직 불러오지 않은 예시 제품은 "sample:SAMPLE_01"
SAMPLE_CHOICE_PREFIX = "sample:"

PRODUCT_FIELDS = ("form", "texture", "scent", "package", "usage_step", "skin_type", "highlight")
EVIDENCE_FIELDS = ("test_type", "item", "value", "institute", "conditions", "source_url")


@lru_cache(maxsize=1)
def load_samples() -> tuple[dict, ...]:
    return tuple(json.loads(SAMPLES_PATH.read_text(encoding="utf-8")))


def get_sample(sample_id: str) -> dict | None:
    return next((s for s in load_samples() if s["product_id"] == sample_id), None)


@transaction.atomic
def create_from_sample(user, sample: dict) -> Product:
    product = Product.objects.create(
        owner=user,
        name=sample["name"],
        category=sample.get("category") or Product.Category.GENERAL,
        functional_type=sample.get("functional_type") or "",
        key_ingredients=", ".join(sample.get("key_ingredients") or []),
        ingredients=", ".join(sample.get("ingredients") or []),
        sample_id=sample["product_id"],
        source_note=sample.get("source_note") or "",
        **{field: sample.get(field) or "" for field in PRODUCT_FIELDS},
    )
    Evidence.objects.bulk_create([
        Evidence(
            product=product,
            source_kind=evidence.get("source_kind") or Evidence.SourceKind.PROVIDED_REPORT,
            **{field: evidence.get(field) or "" for field in EVIDENCE_FIELDS},
        )
        for evidence in sample.get("owned_evidence") or []
    ])
    return product


def product_choices(user) -> list:
    """<select> 선택지. 이미 불러온 예시는 '내 제품' 쪽에만 보인다."""
    mine = list(user.products.only("pk", "name", "sample_id"))
    imported = {p.sample_id for p in mine if p.sample_id}
    choices: list = [("", "제품을 선택하세요")]
    if mine:
        choices.append(("내 제품", [(str(p.pk), p.name) for p in mine]))
    samples = [(SAMPLE_CHOICE_PREFIX + s["product_id"], s["name"]) for s in load_samples() if s["product_id"] not in imported]
    if samples:
        choices.append(("예시 제품 (3차 시연 제품)", samples))
    return choices


def resolve_product_choice(user, value: str) -> Product | None:
    """선택지 값 → 사용자의 Product. 예시 제품이면 내 제품으로 복사한다 (이미 불러왔으면 그 제품)."""
    value = (value or "").strip()
    if value.startswith(SAMPLE_CHOICE_PREFIX):
        sample_id = value[len(SAMPLE_CHOICE_PREFIX):]
        existing = user.products.filter(sample_id=sample_id).first()
        if existing:
            return existing
        sample = get_sample(sample_id)
        return create_from_sample(user, sample) if sample else None
    if value.isdigit():
        return user.products.filter(pk=int(value)).first()
    return None
