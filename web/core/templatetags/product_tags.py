"""내 제품 화면의 제품 유형 묶음. 제품명 · 제형 글자로 나눈다 (DB 필드를 늘리지 않는다).

제품(Product 모델)과 예시 제품(sample_products.json 의 dict) 둘 다 받는다.
위에서부터 먼저 맞는 묶음으로 간다 — '탈모 앰플'은 스킨케어가 아니라 헤어 · 두피.
"""
from django import template

register = template.Library()

GROUPS = [
    ("hair", "헤어 · 두피", ("샴푸", "트리트먼트", "두피", "스칼프", "헤어", "탈모", "모발")),
    ("clean", "클렌징 · 바디", ("클렌저", "클렌징", "폼", "바디", "세정", "워시", "비누")),
    ("sunmake", "선케어 · 색조", ("선크림", "선스틱", "자외선", "쿠션", "립", "색조", "파운데이션", "틴트")),
    ("skin", "스킨케어", ()),   # 나머지: 크림 · 세럼 · 앰플 · 토너 · 로션 · 마스크팩
]


def _get(obj, key):
    return obj.get(key) if isinstance(obj, dict) else getattr(obj, key, "")


@register.filter
def product_group(obj) -> str:
    text = f"{_get(obj, 'name') or ''} {_get(obj, 'form') or ''} {_get(obj, 'functional_type') or ''}"
    for key, _, words in GROUPS:
        if any(w in text for w in words):
            return key
    return "skin"


DISPLAY_ORDER = ("skin", "clean", "hair", "sunmake")   # 화면에 보이는 순서 (나누는 순서와 다르다)


@register.simple_tag
def product_groups():
    labels = {k: label for k, label, _ in GROUPS}
    return [{"key": k, "label": labels[k]} for k in DISPLAY_ORDER]
