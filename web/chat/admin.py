from django.contrib import admin

from .models import ChatMessage, ChatSession


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    fields = ["role", "intent", "content", "created_at"]
    readonly_fields = ["created_at"]


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "product", "updated_at"]
    search_fields = ["title", "user__username"]
    inlines = [ChatMessageInline]
