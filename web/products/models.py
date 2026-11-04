from django.conf import settings
from django.db import models


def split_items(text: str) -> list[str]:
    """쉼표·줄바꿈으로 구분된 입력을 목록으로 바꾼다."""
    return [item.strip() for item in text.replace("\n", ",").split(",") if item.strip()]


class Product(models.Model):
    """사용자가 등록한 제품. AI 서버의 ProductCard로 변환해서 검토·생성에 전달한다."""

    class Category(models.TextChoices):
        GENERAL = "일반", "일반 화장품"
        FUNCTIONAL = "기능성", "기능성 화장품"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    name = models.CharField("제품명", max_length=100)
    category = models.CharField("분류", max_length=10, choices=Category.choices, default=Category.GENERAL)
    functional_type = models.CharField("기능성 유형", max_length=50, blank=True, help_text="예: 미백, 주름개선")
    key_ingredients = models.TextField("주요 성분", blank=True, help_text="쉼표로 구분. 예: 나이아신아마이드, 판테놀")
    ingredients = models.TextField("전성분", blank=True, help_text="쉼표로 구분")
    form = models.CharField("제형", max_length=50, blank=True, help_text="예: 세럼, 크림")
    texture = models.CharField("질감", max_length=200, blank=True)
    scent = models.CharField("향", max_length=100, blank=True)
    package = models.CharField("용량·용기", max_length=100, blank=True)
    usage_step = models.CharField("사용 방법", max_length=200, blank=True)
    skin_type = models.CharField("추천 피부 타입", max_length=100, blank=True)
    highlight = models.CharField("한 줄 특징", max_length=200, blank=True)
    # 3차 예시 제품(products/sample_products.json)에서 불러온 경우 그 product_id. 직접 등록하면 빈 값.
    sample_id = models.CharField("예시 제품 ID", max_length=50, blank=True, editable=False)
    source_note = models.TextField("자료 출처 안내", blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name

    def to_product_card(self) -> dict:
        """AI 서버 ProductCard 형식 (src/cosmetic_agent/domain/schemas.py)."""
        optional = {
            field: getattr(self, field) or None
            for field in ("form", "texture", "scent", "package", "usage_step", "skin_type", "highlight")
        }
        return {
            "product_id": f"web_{self.pk}",
            "name": self.name,
            "category": self.category,
            "functional_type": self.functional_type or None,
            "key_ingredients": split_items(self.key_ingredients),
            "ingredients": split_items(self.ingredients),
            "owned_evidence": [evidence.to_owned_evidence() for evidence in self.evidences.all()],
            **optional,
        }


class Evidence(models.Model):
    """제품이 보유한 실증 자료(시험 결과). 판정 시 표현 가능한 상한을 정한다."""

    class SourceKind(models.TextChoices):
        PROVIDED_REPORT = "provided_report", "보유 시험 보고서"
        PUBLIC_BRAND_SUMMARY = "public_brand_summary", "공식몰 공개 요약 (원보고서 미확보)"

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="evidences")
    test_type = models.CharField("시험 종류", max_length=100, help_text="예: 인체적용시험")
    item = models.CharField("시험 항목", max_length=200, help_text="예: 피부 겉보습 개선")
    value = models.CharField("결과 수치", max_length=100, blank=True, help_text="예: 4주 후 42% 개선")
    institute = models.CharField("시험 기관", max_length=100, blank=True)
    conditions = models.CharField("시험 조건", max_length=200, blank=True)
    # AI 서버는 공개 요약 근거면 "원보고서 미확보" 안내를 판정 결과에 덧붙인다.
    source_kind = models.CharField("자료 종류", max_length=30, choices=SourceKind.choices, default=SourceKind.PROVIDED_REPORT)
    source_url = models.URLField("출처 URL", max_length=500, blank=True)

    def __str__(self):
        return f"{self.test_type} - {self.item}"

    def to_owned_evidence(self) -> dict:
        return {
            "test_type": self.test_type,
            "item": self.item,
            "value": self.value or None,
            "institute": self.institute or None,
            "conditions": self.conditions or None,
            "source_kind": self.source_kind,
            "source_url": self.source_url or None,
        }
