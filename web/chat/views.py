import json

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core import ai_client
from products.models import Product

from .models import ChatMessage, ChatSession

MAX_MESSAGE_LENGTH = 5000


@login_required
def session_list(request):
    return render(request, "chat/session_list.html", {
        "sessions": request.user.chat_sessions.select_related("product"),
        "products": request.user.products.all(),
    })


@login_required
@require_POST
def session_create(request):
    product = None
    if product_id := request.POST.get("product"):
        product = get_object_or_404(Product, pk=product_id, owner=request.user)
    session = ChatSession.objects.create(user=request.user, product=product)
    return redirect("chat:room", pk=session.pk)


@login_required
def room(request, pk):
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    return render(request, "chat/room.html", {
        "session": session,
        "messages_data": [m.to_dict() for m in session.messages.all()],
    })


@login_required
@require_POST
def session_delete(request, pk):
    get_object_or_404(ChatSession, pk=pk, user=request.user).delete()
    return redirect("chat:list")


@login_required
@require_POST
def send(request, pk):
    """채팅 메시지 전송 (프론트에서 fetch로 호출).

    요청: {"message": "..."}  (CSRF 토큰은 X-CSRFToken 헤더)
    응답: {"user": ChatMessage, "assistant": ChatMessage}  / 실패 시 {"error": "..."}
    """
    session = get_object_or_404(ChatSession, pk=pk, user=request.user)
    try:
        message = str(json.loads(request.body or b"{}").get("message", "")).strip()
    except (ValueError, AttributeError):
        return JsonResponse({"error": "잘못된 요청 형식입니다."}, status=400)
    if not message:
        return JsonResponse({"error": "메시지를 입력해 주세요."}, status=400)
    if len(message) > MAX_MESSAGE_LENGTH:
        return JsonResponse({"error": f"메시지는 최대 {MAX_MESSAGE_LENGTH:,}자까지 보낼 수 있습니다."}, status=400)

    try:
        response = ai_client.chat(message, session.product_card(), session.context or None, session.history())
    except ai_client.AIServiceError as error:
        return JsonResponse({"error": error.message}, status=502)

    with transaction.atomic():
        user_message = ChatMessage.objects.create(session=session, role=ChatMessage.Role.USER, content=message)
        assistant_message = ChatMessage.objects.create(
            session=session,
            role=ChatMessage.Role.ASSISTANT,
            content=response.get("message", ""),
            intent=response.get("intent", ""),
            response=response,
        )
        session.context = response.get("context") or session.context
        if session.title == "새 대화":
            session.title = message[:40]
        session.save()

    return JsonResponse({"user": user_message.to_dict(), "assistant": assistant_message.to_dict()})
