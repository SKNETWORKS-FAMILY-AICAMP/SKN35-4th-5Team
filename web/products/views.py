from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import EvidenceFormSet, ProductForm
from .models import Product
from .samples import create_from_sample, get_sample, load_samples


@login_required
def product_list(request):
    products = request.user.products.prefetch_related("evidences")
    added = set(products.exclude(sample_id="").values_list("sample_id", flat=True))
    samples = [
        {**sample, "evidence_count": len(sample.get("owned_evidence") or []), "added": sample["product_id"] in added}
        for sample in load_samples()
    ]
    return render(request, "products/product_list.html", {"products": products, "samples": samples})


@login_required
@require_POST
def sample_add(request, sample_id):
    """3차 예시 제품을 내 제품으로 복사한다. 이미 불러온 예시는 그 제품으로 이동한다."""
    sample = get_sample(sample_id)
    if sample is None:
        raise Http404("예시 제품이 없습니다.")
    existing = request.user.products.filter(sample_id=sample_id).first()
    if existing:
        messages.info(request, f"'{existing.name}'은(는) 이미 불러온 예시 제품입니다.")
        return redirect("products:detail", pk=existing.pk)
    product = create_from_sample(request.user, sample)
    messages.success(request, f"예시 제품 '{product.name}'을(를) 내 제품에 추가했습니다.")
    return redirect("products:detail", pk=product.pk)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    return render(request, "products/product_detail.html", {"product": product})


def _save_product_form(request, product=None):
    form = ProductForm(request.POST or None, instance=product)
    formset = EvidenceFormSet(request.POST or None, instance=product or Product())
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        with transaction.atomic():
            saved = form.save(commit=False)
            saved.owner = request.user
            saved.save()
            formset.instance = saved
            formset.save()
        messages.success(request, f"'{saved.name}' 제품을 저장했습니다.")
        return redirect("products:detail", pk=saved.pk)
    return render(request, "products/product_form.html", {"form": form, "formset": formset, "product": product})


@login_required
def product_create(request):
    return _save_product_form(request)


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    return _save_product_form(request, product)


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, owner=request.user)
    if request.method == "POST":
        product.delete()
        messages.success(request, f"'{product.name}' 제품을 삭제했습니다.")
        return redirect("products:list")
    return render(request, "products/product_confirm_delete.html", {"product": product})
