from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EvidenceFormSet, ProductForm
from .models import Product


@login_required
def product_list(request):
    products = request.user.products.prefetch_related("evidences")
    return render(request, "products/product_list.html", {"products": products})


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
