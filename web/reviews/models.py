from django.conf import settings
from django.db import models

LEVEL_LABELS = {0: "가능", 1: "조건부", 2: "불가"}


class ReviewRecord(models.Model):
    """광고 문구 검토 이력. AI 응답 원문(ReviewResponse)은 response에 그대로 보관한다."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review_records")
    # 제품을 지워도 이력은 남긴다. 제품명은 product_name에 따로 보관.
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="review_records")
    product_name = models.CharField(max_length=100)
    copy_text = models.TextField()
    status = models.CharField(max_length=10, help_text="판정 / 판단보류")
    level = models.PositiveSmallIntegerField(null=True, blank=True, help_text="0 가능 · 1 조건부 · 2 불가")
    violation_type = models.CharField(max_length=20, blank=True)
    suggestion = models.TextField(blank=True)
    response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.verdict_label}] {self.copy_text[:30]}"

    @property
    def verdict_label(self) -> str:
        if self.status != "판정":
            return self.status or "판단보류"
        return LEVEL_LABELS.get(self.level, "판정")

    @classmethod
    def from_response(cls, *, user, product, copy_text: str, response: dict) -> "ReviewRecord":
        result = response.get("result") or {}
        return cls(
            user=user,
            product=product,
            product_name=product.name,
            copy_text=copy_text,
            status=result.get("status", ""),
            level=result.get("level"),
            violation_type=result.get("violation_type", ""),
            suggestion=result.get("suggestion") or "",
            response=response,
        )


class GenerationRecord(models.Model):
    """광고문 생성 이력. AI 응답 원문(GenerateResponse)은 response에 그대로 보관한다."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="generation_records")
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="generation_records")
    product_name = models.CharField(max_length=100)
    instruction = models.TextField()
    channel = models.CharField(max_length=20)
    tone = models.CharField(max_length=100)
    length = models.CharField(max_length=20)
    status = models.CharField(max_length=10, help_text="생성완료 / 생성보류")
    response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.status}] {self.instruction[:30]}"

    @property
    def candidates(self) -> list[dict]:
        return self.response.get("candidates", [])
