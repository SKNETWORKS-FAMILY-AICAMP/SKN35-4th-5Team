"""상세페이지 검토 · 규정·가이드라인 · 예상 매출 시나리오 화면.

- 판정 · 검색은 AI 서버 API 를 그대로 부른다 (ai_client.review_bulk · search · review).
- 바뀌지 않는 참고 자료(관리지침 금지 표현 · 적발 사례 · 처분 기준표)는 core/reference/ 에 떠 둔 JSON 을 읽는다.
  Django 이미지에는 web/ 아래의 자료만 포함한다.
- 요청 결과를 화면에 표시하며 별도 이력 모델은 없다.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core import ai_client
from core import revenue_scenario
from reviews.forms import ProductChoiceMixin

REFERENCE = Path(__file__).resolve().parent / "reference"
LEVEL_LABEL = {0: "가능", 1: "조건부", 2: "불가"}
AUTHORITY = {1: "법령", 2: "고시", 3: "지침", 4: "사례"}

# 상세페이지 검토 입력 예시
BULK_SAMPLE = """건조한 피부에 촉촉함을 채워 주는 데일리 수분 크림입니다.
4주 사용 후 피부 보습력 42% 개선 (인체적용시험, 한국피부과학연구원).
바르는 순간부터 24시간 촉촉함이 지속됩니다.
손상된 피부를 완벽하게 재생시켜 줍니다!
피부 고민 1위 국민 수분 크림.
타사 수분 크림 대비 2배 촉촉합니다.
엑소좀 성분이 피부 속 깊이 전달됩니다.
민감한 피부도 편안하게 사용할 수 있습니다."""
# 규정 검색 바로가기
LIBRARY_QUICK = ["피부 재생", "실증자료 요건", "탈모 표현", "최고 1위 표현", "기능성화장품 오인"]


@lru_cache(maxsize=8)
def _reference(name: str):
    return json.loads((REFERENCE / name).read_text(encoding="utf-8"))


def _verdict(result: dict) -> tuple[int | None, str]:
    if result.get("status") != "판정":
        return None, result.get("status") or "판단보류"
    return result.get("level"), LEVEL_LABEL.get(result.get("level"), "판정")


# ── 상세페이지 검토 ──────────────────────────────────────────────
class BulkForm(ProductChoiceMixin, forms.Form):
    product = forms.ModelChoiceField(queryset=None, label="제품")
    full_text = forms.CharField(label="상세페이지 문구", max_length=50000, initial=BULK_SAMPLE,
                                widget=forms.Textarea(attrs={"rows": 10}),
                                help_text="줄바꿈 · 문장부호로 문장을 나눠 순서대로 검토합니다 (최대 100문장).")


@login_required
def bulk(request):
    form = BulkForm(request.POST or None, user=request.user)
    rows, counts, corrected = [], {}, ""
    if request.method == "POST" and form.is_valid():
        product = form.cleaned_data["product"]
        try:
            responses = ai_client.review_bulk(form.cleaned_data["full_text"], product.to_product_card())
        except ai_client.AIServiceError as error:
            messages.error(request, error.message)
        else:
            fixed = []
            for r in responses:
                result = r.get("result") or {}
                level, label = _verdict(result)
                candidates = r.get("candidates") or ([result["suggestion"]] if result.get("suggestion") else [])
                rows.append({"text": r.get("input_text", ""), "level": level, "label": label,
                             "violation": result.get("violation_type"), "notes": result.get("review_notes"),
                             "candidates": candidates, "citations": (result.get("citations") or [])[:3]})
                counts[label] = counts.get(label, 0) + 1
                fixed.append(candidates[0] if level in (1, 2) and candidates else r.get("input_text", ""))
            corrected = "\n".join(fixed)
    return render(request, "core/bulk.html", {"form": form, "rows": rows, "counts": counts, "corrected": corrected})


# ── 규정 · 가이드라인 ─────────────────────────────────────────────
@login_required
def library(request):
    tab = request.GET.get("tab", "search")
    q = request.GET.get("q", "").strip()
    scope = request.GET.get("scope", "공통")
    context = {"tab": tab, "q": q, "scope": scope, "quick": LIBRARY_QUICK, "scopes": ["공통", "일반", "기능성"],
               "stats": _reference("kb_stats.json")}
    if tab == "search" and q:
        try:
            hits = ai_client.search(q, scope)
        except ai_client.AIServiceError as error:
            messages.error(request, error.message)
            hits = []
        context["hits"] = [{"content": h.get("content", ""), **(h.get("metadata") or {}),
                            "authority_label": AUTHORITY.get((h.get("metadata") or {}).get("authority"))
                            or (h.get("metadata") or {}).get("doc_type") or "근거"} for h in hits[:10]]
    elif tab == "banned":
        f = request.GET.get("f", "").strip()
        rows = _reference("guide_rows.json")
        if f:
            rows = [r for r in rows if f in (r.get("text") or "") or f in (r.get("category") or "") or f in (r.get("note") or "")]
        context.update(f=f, rows=rows)
    elif tab == "cases":
        cases = _reference("cases.json")
        top = max((c.get("cosmetics_count") or c.get("count") or 0) for c in cases) or 1
        context["cases"] = [dict(c, n=c.get("cosmetics_count") or c.get("count") or 0,
                                 pct=round((c.get("cosmetics_count") or c.get("count") or 0) / top * 100)) for c in cases]
    return render(request, "core/library.html", context)


# ── 예상 매출 시나리오 ────────────────────────────────────────────
class ForecastForm(ProductChoiceMixin, forms.Form):
    product = forms.ModelChoiceField(queryset=None, label="제품")
    copy_text = forms.CharField(label="지금 쓰는 광고 문구", max_length=5000, widget=forms.Textarea(attrs={"rows": 3}),
                                initial="바르는 순간 주름이 사라지는 비타민A 브라이트닝 앰플")
    price_krw = forms.IntegerField(label="판매가 (원)", min_value=0, initial=32000)
    units_low = forms.IntegerField(label="월 판매량 · 적게", min_value=0, initial=300)
    units_mid = forms.IntegerField(label="월 판매량 · 보통", min_value=0, initial=600)
    units_high = forms.IntegerField(label="월 판매량 · 많이", min_value=0, initial=1200)
    offense = forms.ChoiceField(label="위반 차수", choices=[(1, "1차"), (2, "2차"), (3, "3차"), (4, "4차 이상")], initial=1)
    sanction_kind = forms.ChoiceField(label="위반 대상", choices=[("광고", "광고 (광고업무정지)"), ("표시", "표시 (판매업무정지)")])
    ad_share = forms.IntegerField(label="광고에서 나오는 매출 비중 (%)", min_value=0, max_value=100, required=False,
                                  help_text="모르면 비워 두세요. 최대 금액으로 보여 줍니다.")

    def clean(self):
        data = super().clean()
        if all(k in data for k in ("units_low", "units_mid", "units_high")) and not data["units_low"] <= data["units_mid"] <= data["units_high"]:
            raise forms.ValidationError("월 판매량은 적게 ≤ 보통 ≤ 많이 순서로 입력해 주세요.")
        return data


@login_required
def forecast(request):
    form = ForecastForm(request.POST or None, user=request.user)
    context = {"form": form, "label": revenue_scenario.DISPLAY_LABEL}
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        try:
            review = ai_client.review(d["copy_text"], d["product"].to_product_card())
        except ai_client.AIServiceError as error:
            messages.error(request, error.message)
            return render(request, "core/forecast.html", context)
        result = review.get("result") or {}
        level = result.get("level") if result.get("status") == "판정" else None
        law_ids = list(dict.fromkeys(c["chunk_id"] for c in result.get("citations") or [] if str(c.get("chunk_id", "")).startswith("LAW_")))
        common = dict(price_krw=d["price_krw"], monthly_units={"low": d["units_low"], "mid": d["units_mid"], "high": d["units_high"]},
                      offense=int(d["offense"]), sanction_kind=d["sanction_kind"],
                      ad_dependent_share=(d["ad_share"] / 100) if d["ad_share"] is not None else None)
        before = revenue_scenario.build_scenario(level=level or 0, law_ids=law_ids, **common)
        best = (review.get("candidates") or [None])[0] or result.get("suggestion")
        after = revenue_scenario.build_scenario(level=0, law_ids=[], **common) if best else None   # 역검증을 통과한 제안 문구
        _, verdict_label = _verdict(result)
        risk = before["revenue_at_risk_if_unchanged"]
        risk_amount = (risk.get("estimate_krw") or risk.get("upper_bound_krw") or risk.get("amount_krw") or {}).get("high")
        band = before["copy_change_band"]
        context.update(review=review, level=level, verdict_label=verdict_label, law_ids=law_ids,
                       before=before, after=after, best=best, copy_text=d["copy_text"],
                       risk=risk, risk_amount=risk_amount, band=band,
                       # 대시보드 차트용 (forecast-dash.js) — 화면 숫자와 같은 값
                       fc_data={"revenue": before["monthly_revenue_krw"], "risk_status": risk["status"],
                                "risk_amount": risk_amount, "risk_is_estimate": bool(risk.get("estimate_krw")),
                                "months": risk.get("months"), "band": band["typical_range_krw"],
                                "band_pct": band["change_magnitude_pct"]["p75"], "has_best": bool(best)})
    return render(request, "core/forecast.html", context)
