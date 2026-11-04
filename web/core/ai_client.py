"""
FastAPI AI 서버(3차 엔진) 호출 클라이언트.

Django 쪽 코드는 이 모듈만 통해서 AI 서버를 부른다. 엔드포인트와 요청/응답 형식은
저장소 루트 src/cosmetic_agent/domain/schemas.py, domain/chat.py 의 Pydantic 모델과 같다.
"""
from __future__ import annotations

import logging
from typing import Any

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """AI 서버 호출 실패. message는 사용자에게 그대로 보여줘도 되는 문장이다."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


def _detail(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return ""
    detail = body.get("detail") if isinstance(body, dict) else None
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list) and detail:
        # FastAPI 422 검증 오류: [{"loc": [...], "msg": "..."}]
        first = detail[0]
        return f"{'.'.join(str(p) for p in first.get('loc', [])[1:])}: {first.get('msg', '')}"
    return ""


def _request(method: str, path: str, **kwargs) -> Any:
    url = f"{settings.AI_API_URL}{path}"
    try:
        response = httpx.request(method, url, timeout=settings.AI_API_TIMEOUT, **kwargs)
        response.raise_for_status()
    except httpx.TimeoutException as error:
        logger.warning("AI 서버 응답 시간 초과: %s", path)
        raise AIServiceError("AI 서버 응답이 늦어지고 있습니다. 잠시 후 다시 시도해 주세요.") from error
    except httpx.HTTPStatusError as error:
        status = error.response.status_code
        detail = _detail(error.response)
        logger.warning("AI 서버 오류 %s %s: %s", status, path, detail)
        if status == 422:
            message = f"입력값을 확인해 주세요. ({detail})" if detail else "입력값을 확인해 주세요."
        elif status == 503:
            message = detail or "AI 서버의 검색 DB 또는 모델을 사용할 수 없습니다."
        else:
            message = "AI 서버에서 오류가 발생했습니다."
        raise AIServiceError(message, status) from error
    except httpx.HTTPError as error:
        logger.warning("AI 서버 연결 실패: %s (%s)", path, type(error).__name__)
        raise AIServiceError("AI 서버에 연결하지 못했습니다. 서버가 실행 중인지 확인해 주세요.") from error
    return response.json()


def health() -> dict:
    return _request("GET", "/health")


def review(copy_text: str, product: dict) -> dict:
    """단일 문구 검토. 응답: ReviewResponse"""
    return _request("POST", "/review", json={"copy_text": copy_text, "product": product})


def review_bulk(full_text: str, product: dict) -> list[dict]:
    """상세페이지 전체 검토(문장별). 응답: list[ReviewResponse]"""
    return _request("POST", "/review/bulk", json={"full_text": full_text, "product": product})


def generate(payload: dict) -> dict:
    """광고문 생성. payload: GenerateRequest, 응답: GenerateResponse"""
    return _request("POST", "/generate", json=payload)


def chat(message: str, product: dict, context: dict | None = None, history: list[dict] | None = None) -> dict:
    """통합 챗봇. history는 최근 12턴까지. 응답: ChatResponse"""
    payload: dict[str, Any] = {"message": message, "product": product, "history": (history or [])[-12:]}
    if context:
        payload["context"] = context
    return _request("POST", "/chat", json=payload)


def search(query: str, scope: str = "공통") -> list[dict]:
    return _request("GET", "/search", params={"q": query, "scope": scope})
