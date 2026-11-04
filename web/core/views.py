from django.http import JsonResponse
from django.shortcuts import render

from core import ai_client


def home(request):
    context = {}
    if request.user.is_authenticated:
        context["products"] = request.user.products.all()[:5]
        context["recent_reviews"] = request.user.review_records.select_related("product")[:5]
    return render(request, "core/home.html", context)


def health(request):
    """배포 헬스체크용. AI 서버 연결 상태도 함께 보여준다 (Django 자체는 항상 200)."""
    try:
        ai_status = ai_client.health().get("status", "ok")
    except ai_client.AIServiceError as error:
        ai_status = f"unavailable: {error.message}"
    return JsonResponse({"status": "ok", "ai": ai_status})
