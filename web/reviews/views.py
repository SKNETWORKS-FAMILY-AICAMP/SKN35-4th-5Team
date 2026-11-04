from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from core import ai_client

from .forms import GenerateForm, ReviewForm
from .models import GenerationRecord, ReviewRecord


def _initial_product(request):
    product_id = request.GET.get("product")
    return {"product": product_id} if product_id else None


@login_required
def review_create(request):
    form = ReviewForm(request.POST or None, user=request.user, initial=_initial_product(request))
    if request.method == "POST" and form.is_valid():
        product = form.cleaned_data["product"]
        copy_text = form.cleaned_data["copy_text"]
        try:
            response = ai_client.review(copy_text, product.to_product_card())
        except ai_client.AIServiceError as error:
            messages.error(request, error.message)
        else:
            record = ReviewRecord.from_response(user=request.user, product=product, copy_text=copy_text, response=response)
            record.save()
            return redirect("reviews:detail", pk=record.pk)
    return render(request, "reviews/review_form.html", {"form": form})


@login_required
def review_detail(request, pk):
    record = get_object_or_404(ReviewRecord, pk=pk, user=request.user)
    # AI 서버는 검증 탈락 후보를 candidates 에서 빼고 candidate_details 에만 사유와 함께 남긴다.
    rejected = [d.get("verify_note") for d in record.response.get("candidate_details", []) if not d.get("verified") and d.get("verify_note")]
    return render(request, "reviews/review_detail.html", {
        "record": record,
        "result": record.response.get("result", {}),
        "rejected": list(dict.fromkeys(rejected)),
    })


@login_required
def review_list(request):
    records = request.user.review_records.all()
    product_id = request.GET.get("product")
    if product_id:
        records = records.filter(product_id=product_id)
    return render(request, "reviews/review_list.html", {"records": records})


@login_required
def generate_create(request):
    form = GenerateForm(request.POST or None, user=request.user, initial=_initial_product(request))
    if request.method == "POST" and form.is_valid():
        data = form.cleaned_data
        product = data["product"]
        payload = {
            "instruction": data["instruction"],
            "product": product.to_product_card(),
            "channel": data["channel"],
            "tone": data["tone"],
            "length": data["length"],
            "keywords": data["keywords"],
        }
        try:
            response = ai_client.generate(payload)
        except ai_client.AIServiceError as error:
            messages.error(request, error.message)
        else:
            record = GenerationRecord.objects.create(
                user=request.user,
                product=product,
                product_name=product.name,
                instruction=data["instruction"],
                channel=data["channel"],
                tone=data["tone"],
                length=data["length"],
                status=response.get("status", ""),
                response=response,
            )
            return redirect("reviews:generation_detail", pk=record.pk)
    return render(request, "reviews/generate_form.html", {"form": form})


@login_required
def generation_detail(request, pk):
    record = get_object_or_404(GenerationRecord, pk=pk, user=request.user)
    return render(request, "reviews/generation_detail.html", {"record": record})


@login_required
def generation_list(request):
    return render(request, "reviews/generation_list.html", {"records": request.user.generation_records.all()})
