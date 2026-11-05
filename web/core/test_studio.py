"""3차에서 옮겨 온 화면 세 개(상세페이지 검토 · 규정 · 가이드라인 · 예상 매출 시나리오) 테스트. AI 서버는 mock."""
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from core.ai_client import AIServiceError
from core.tests import REVIEW_RESPONSE, BaseTestCase

LAW_REVIEW = {**REVIEW_RESPONSE, "result": {**REVIEW_RESPONSE["result"], "citations": [
    {"chunk_id": "LAW_시행규칙_별표5-2가", "source": "화장품법 시행규칙", "article": "[별표 5] 제2호 가목", "authority": 1},
    {"chunk_id": "GUIDE_관리지침_별표1-39", "source": "관리지침", "article": "[별표 1]", "authority": 3},
]}}


class LoginRequiredTests(TestCase):
    def test_pages_need_login(self):
        for name in ("core:bulk", "core:library", "core:forecast"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 302, name)


class BulkTests(BaseTestCase):
    @mock.patch("core.ai_client.review_bulk", return_value=[REVIEW_RESPONSE, {**REVIEW_RESPONSE, "input_text": "촉촉한 크림",
                "result": {**REVIEW_RESPONSE["result"], "level": 0, "citations": []}, "candidates": []}])
    def test_bulk_shows_each_sentence_and_corrected_text(self, review_bulk):
        res = self.client.post(reverse("core:bulk"), {"product": self.product.pk, "full_text": "7일 만에 주름 개선\n촉촉한 크림"})
        self.assertEqual(res.status_code, 200)
        review_bulk.assert_called_once()
        self.assertEqual(len(res.context["rows"]), 2)
        self.assertEqual(res.context["counts"], {"불가": 1, "가능": 1})
        # 불가 문장은 첫 제안으로, 가능 문장은 그대로
        self.assertEqual(res.context["corrected"], "피부 결을 매끄럽게 가꿔줍니다\n촉촉한 크림")

    @mock.patch("core.ai_client.review_bulk", side_effect=AIServiceError("AI 서버에 연결하지 못했습니다."))
    def test_bulk_ai_error_shows_message(self, review_bulk):
        res = self.client.post(reverse("core:bulk"), {"product": self.product.pk, "full_text": "문장"})
        self.assertContains(res, "AI 서버에 연결하지 못했습니다.")


class LibraryTests(BaseTestCase):
    @mock.patch("core.ai_client.search", return_value=[{"content": "피부재생 금지", "metadata": {"source": "관리지침", "article": "[별표 1]", "authority": 3}}])
    def test_search_calls_ai_server(self, search):
        res = self.client.get(reverse("core:library"), {"tab": "search", "q": "피부 재생", "scope": "일반"})
        search.assert_called_once_with("피부 재생", "일반")
        self.assertContains(res, "피부재생 금지")

    def test_banned_and_cases_come_from_bundled_reference(self):
        res = self.client.get(reverse("core:library"), {"tab": "banned", "f": "아토피"})
        self.assertContains(res, "아토피")
        res = self.client.get(reverse("core:library"), {"tab": "cases"})
        self.assertEqual(len(res.context["cases"]), 6)


class ForecastTests(BaseTestCase):
    @mock.patch("core.ai_client.review", return_value=LAW_REVIEW)
    def test_forecast_uses_review_verdict_and_law_citations(self, review):
        res = self.client.post(reverse("core:forecast"), {
            "product": self.product.pk, "copy_text": "7일 만에 주름 개선", "price_krw": 32000,
            "units_low": 300, "units_mid": 600, "units_high": 1200, "offense": 1, "sanction_kind": "광고"})
        self.assertEqual(res.status_code, 200)
        before = res.context["before"]
        self.assertEqual(before["inputs"]["law_ids"], ["LAW_시행규칙_별표5-2가"])   # LAW_ 근거만 처분 기준에 쓴다
        self.assertEqual(before["monthly_revenue_krw"]["mid"], 19_200_000)
        self.assertEqual(before["revenue_at_risk_if_unchanged"]["status"], "mapped")
        self.assertEqual(res.context["after"]["revenue_at_risk_if_unchanged"]["status"], "no_violation")

    def test_units_must_be_ordered(self):
        res = self.client.post(reverse("core:forecast"), {
            "product": self.product.pk, "copy_text": "문구", "price_krw": 1000,
            "units_low": 900, "units_mid": 600, "units_high": 1200, "offense": 1, "sanction_kind": "광고"})
        self.assertContains(res, "적게 ≤ 보통 ≤ 많이")
