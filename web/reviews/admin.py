from django.contrib import admin

from .models import GenerationRecord, ReviewRecord


@admin.register(ReviewRecord)
class ReviewRecordAdmin(admin.ModelAdmin):
    list_display = ["copy_text", "verdict_label", "violation_type", "product_name", "user", "created_at"]
    list_filter = ["status", "level", "violation_type"]
    search_fields = ["copy_text", "product_name", "user__username"]


@admin.register(GenerationRecord)
class GenerationRecordAdmin(admin.ModelAdmin):
    list_display = ["instruction", "status", "channel", "product_name", "user", "created_at"]
    list_filter = ["status", "channel"]
    search_fields = ["instruction", "product_name", "user__username"]
