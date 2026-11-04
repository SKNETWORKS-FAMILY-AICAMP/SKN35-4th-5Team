from django.conf import settings
from django.db import models

# 제품을 선택하지 않은 대화에 쓰는 기본 ProductCard (AI 서버 ChatRequest 기본값과 같음)
DRAFT_PRODUCT_CARD = {"product_id": "chat_draft", "name": "나의 화장품", "category": "일반"}


class ChatSession(models.Model):
    """대화방. AI 서버가 돌려주는 대화 맥락(ChatContext)을 context에 보관해 다음 요청에 다시 보낸다."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_sessions")
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True, blank=True, related_name="chat_sessions")
    title = models.CharField(max_length=100, default="새 대화")
    context = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.title

    def product_card(self) -> dict:
        return self.product.to_product_card() if self.product else dict(DRAFT_PRODUCT_CARD)

    def history(self, limit: int = 12) -> list[dict]:
        """AI 서버에 보낼 최근 대화 (ChatTurn 목록, 오래된 순)."""
        # 한 요청에서 저장된 user/assistant 메시지는 created_at이 같을 수 있어 id로 순서를 정한다.
        recent = list(self.messages.order_by("-id")[:limit])
        return [{"role": m.role, "content": m.content[:6000]} for m in reversed(recent)]


class ChatMessage(models.Model):
    class Role(models.TextChoices):
        USER = "user", "사용자"
        ASSISTANT = "assistant", "AI"

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=Role.choices)
    content = models.TextField()
    intent = models.CharField(max_length=10, blank=True, help_text="review / generate / clarify / answer")
    # assistant 메시지의 ChatResponse 원문 (검토·생성 결과 카드 표시용)
    response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def to_dict(self) -> dict:
        return {
            "id": self.pk,
            "role": self.role,
            "content": self.content,
            "intent": self.intent,
            "response": self.response,
            "created_at": self.created_at.isoformat(),
        }
