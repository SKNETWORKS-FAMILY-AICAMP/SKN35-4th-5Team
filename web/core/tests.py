"""웹 서비스 흐름 테스트. AI 서버는 core.ai_client 를 mock 해서 띄우지 않는다."""
import json
from unittest import mock

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from chat.models import ChatMessage, ChatSession
from core.ai_client import AIServiceError
from products.models import Evidence, Product
from reviews.models import GenerationRecord, ReviewRecord

REVIEW_RESPONSE = {
    "request_id": "r1",
    "input_text": "7일 만에 주름 개선",
    "result": {
        "status": "판정",
        "level": 2,
        "violation_type": "실증필요",
        "citations": [{"chunk_id": "c1", "source": "화장품법 시행규칙", "article": "별표5", "authority": 1}],
        "suggestion": "피부 결을 매끄럽게 가꿔줍니다",
        "next_test": None,
        "review_notes": "주름 개선 기간 표현에 대한 실증이 없습니다.",
    },
    "timing": {"retrieval_ms": 1, "llm_ms": 1, "total_ms": 2},
    "candidates": ["피부 결을 매끄럽게 가꿔줍니다"],
}

GENERATE_RESPONSE = {
    "request_id": "g1",
    "status": "생성완료",
    "product_id": "web_1",
    "candidates": [
        {"text": "촉촉함이 오래 머무는 크림", "tier": "safe", "status": "검토통과"},
        {"text": "주름이 사라지는 크림", "tier": "strong", "status": "제외"},
    ],
    "timing": {"retrieval_ms": 1, "llm_ms": 1, "total_ms": 2},
}


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", password="pw-12345678")
        self.client.force_login(self.user)
        self.product = Product.objects.create(
            owner=self.user, name="수분크림", category="기능성", functional_type="주름개선",
            key_ingredients="나이아신아마이드, 판테놀", form="크림",
        )
        Evidence.objects.create(product=self.product, test_type="인체적용시험", item="피부 보습", value="4주 후 35% 개선")


class ProductTests(BaseTestCase):
    def test_product_card_matches_ai_schema(self):
        card = self.product.to_product_card()
        self.assertEqual(card["product_id"], f"web_{self.product.pk}")
        self.assertEqual(card["key_ingredients"], ["나이아신아마이드", "판테놀"])
        self.assertEqual(card["ingredients"], [])
        self.assertEqual(card["texture"], None)
        self.assertEqual(card["owned_evidence"][0]["item"], "피부 보습")
        self.assertEqual(card["owned_evidence"][0]["institute"], None)

    def test_functional_product_requires_type(self):
        response = self.client.post(reverse("products:create"), {
            "name": "기능성 세럼", "category": "기능성", "functional_type": "",
            "evidences-TOTAL_FORMS": "0", "evidences-INITIAL_FORMS": "0",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(name="기능성 세럼").exists())

    def test_create_product_with_evidence(self):
        response = self.client.post(reverse("products:create"), {
            "name": "토너", "category": "일반",
            "evidences-TOTAL_FORMS": "1", "evidences-INITIAL_FORMS": "0",
            "evidences-0-test_type": "시험성적서", "evidences-0-item": "피부 자극", "evidences-0-value": "저자극",
        })
        product = Product.objects.get(name="토너")
        self.assertRedirects(response, reverse("products:detail", args=[product.pk]))
        self.assertEqual(product.owner, self.user)
        self.assertEqual(product.evidences.count(), 1)

    def test_other_users_product_is_hidden(self):
        other = User.objects.create_user("other", password="pw-12345678")
        self.client.force_login(other)
        self.assertEqual(self.client.get(reverse("products:detail", args=[self.product.pk])).status_code, 404)


class ReviewTests(BaseTestCase):
    @mock.patch("core.ai_client.review", return_value=REVIEW_RESPONSE)
    def test_review_saves_record(self, review):
        response = self.client.post(reverse("reviews:create"), {"product": self.product.pk, "copy_text": "7일 만에 주름 개선"})
        record = ReviewRecord.objects.get()
        self.assertRedirects(response, reverse("reviews:detail", args=[record.pk]))
        review.assert_called_once_with("7일 만에 주름 개선", self.product.to_product_card())
        self.assertEqual(record.verdict_label, "불가")
        self.assertEqual(record.violation_type, "실증필요")
        detail = self.client.get(reverse("reviews:detail", args=[record.pk]))
        self.assertContains(detail, "화장품법 시행규칙")
        self.assertContains(detail, "피부 결을 매끄럽게 가꿔줍니다")

    def test_review_without_verified_suggestion_shows_notice(self):
        response = {
            **REVIEW_RESPONSE,
            "result": {**REVIEW_RESPONSE["result"], "suggestion": None},
            "candidates": [],
            "candidate_details": [{"text": "탈락 문구", "verified": False, "verify_note": "보유 실증에 없는 수치(70%)"}],
        }
        with mock.patch("core.ai_client.review", return_value=response):
            self.client.post(reverse("reviews:create"), {"product": self.product.pk, "copy_text": "7일 만에 주름 개선"})
        detail = self.client.get(reverse("reviews:detail", args=[ReviewRecord.objects.get().pk]))
        self.assertContains(detail, "검증을 통과한 수정안이 없어")
        self.assertContains(detail, "보유 실증에 없는 수치(70%)")
        self.assertNotContains(detail, "탈락 문구")

    @mock.patch("core.ai_client.review", side_effect=AIServiceError("AI 서버에 연결하지 못했습니다."))
    def test_review_ai_error_shows_message(self, review):
        response = self.client.post(reverse("reviews:create"), {"product": self.product.pk, "copy_text": "문구"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "AI 서버에 연결하지 못했습니다.")
        self.assertFalse(ReviewRecord.objects.exists())

    def test_cannot_review_with_other_users_product(self):
        other = User.objects.create_user("other", password="pw-12345678")
        self.client.force_login(other)
        response = self.client.post(reverse("reviews:create"), {"product": self.product.pk, "copy_text": "문구"})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(ReviewRecord.objects.exists())

    @mock.patch("core.ai_client.generate", return_value=GENERATE_RESPONSE)
    def test_generate_saves_record(self, generate):
        response = self.client.post(reverse("reviews:generate"), {
            "product": self.product.pk, "instruction": "보습 강조", "channel": "SNS",
            "tone": "담백한", "length": "한 줄", "keywords": "보습, 촉촉",
        })
        record = GenerationRecord.objects.get()
        self.assertRedirects(response, reverse("reviews:generation_detail", args=[record.pk]))
        payload = generate.call_args.args[0]
        self.assertEqual(payload["keywords"], ["보습", "촉촉"])
        self.assertEqual(payload["product"]["name"], "수분크림")
        detail = self.client.get(reverse("reviews:generation_detail", args=[record.pk]))
        self.assertContains(detail, "촉촉함이 오래 머무는 크림")
        self.assertNotContains(detail, "주름이 사라지는 크림")


class ChatTests(BaseTestCase):
    def send(self, session, message):
        return self.client.post(reverse("chat:send", args=[session.pk]), json.dumps({"message": message}), content_type="application/json")

    @mock.patch("core.ai_client.chat")
    def test_send_stores_messages_and_context(self, chat):
        chat.return_value = {"intent": "answer", "message": "나이아신아마이드는 미백 원료입니다.", "context": {"tone": "담백한"}, "citations": []}
        session = ChatSession.objects.create(user=self.user, product=self.product)

        response = self.send(session, "나이아신아마이드가 뭐야?")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["assistant"]["content"], "나이아신아마이드는 미백 원료입니다.")
        chat.assert_called_with("나이아신아마이드가 뭐야?", self.product.to_product_card(), None, [])

        session.refresh_from_db()
        self.assertEqual(session.context, {"tone": "담백한"})
        self.assertEqual(session.title, "나이아신아마이드가 뭐야?")

        # 두 번째 요청에는 저장된 맥락과 이전 대화가 함께 간다.
        self.send(session, "더 알려줘")
        _, _, context, history = chat.call_args.args
        self.assertEqual(context, {"tone": "담백한"})
        self.assertEqual([turn["role"] for turn in history], ["user", "assistant"])
        self.assertEqual(ChatMessage.objects.filter(session=session).count(), 4)

    @mock.patch("core.ai_client.chat", side_effect=AIServiceError("AI 서버 응답이 늦어지고 있습니다."))
    def test_send_ai_error_does_not_store(self, chat):
        session = ChatSession.objects.create(user=self.user)
        response = self.send(session, "안녕")
        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json()["error"], "AI 서버 응답이 늦어지고 있습니다.")
        self.assertFalse(session.messages.exists())

    def test_send_rejects_empty_message(self):
        session = ChatSession.objects.create(user=self.user)
        self.assertEqual(self.send(session, "  ").status_code, 400)

    def test_draft_product_card_without_product(self):
        session = ChatSession.objects.create(user=self.user)
        self.assertEqual(session.product_card()["product_id"], "chat_draft")


class PageTests(BaseTestCase):
    def test_pages_render(self):
        session = ChatSession.objects.create(user=self.user)
        for name, args in [
            ("core:home", []), ("products:list", []), ("products:create", []),
            ("products:detail", [self.product.pk]), ("products:update", [self.product.pk]),
            ("reviews:create", []), ("reviews:list", []), ("reviews:generate", []),
            ("reviews:generation_list", []), ("chat:list", []), ("chat:room", [session.pk]),
        ]:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name, args=args)).status_code, 200)

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse("products:list"))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('products:list')}")

    def test_signup_logs_in(self):
        self.client.logout()
        response = self.client.post(reverse("accounts:signup"), {"username": "newbie", "password1": "Beaurette!2026", "password2": "Beaurette!2026"})
        self.assertRedirects(response, reverse("core:home"))
        self.assertTrue(User.objects.filter(username="newbie").exists())

    @mock.patch("core.ai_client.health", side_effect=AIServiceError("down"))
    def test_health_reports_ai_down(self, health):
        response = self.client.get(reverse("core:health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["ai"], "unavailable: down")
