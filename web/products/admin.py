from django.contrib import admin

from .models import Evidence, Product


class EvidenceInline(admin.TabularInline):
    model = Evidence
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "functional_type", "owner", "updated_at"]
    list_filter = ["category"]
    search_fields = ["name", "owner__username"]
    inlines = [EvidenceInline]
