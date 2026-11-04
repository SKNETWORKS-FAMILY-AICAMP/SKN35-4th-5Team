"""3차 원본 홈(배포된 Streamlit 화면)을 Django 템플릿으로 옮긴다.

원본을 다시 만들지 않고, 헤드리스 브라우저로 떠 온 화면을 그대로 쓴다.
  입력: <capture>/orig_main.html  (stMainBlockContainer 의 렌더된 HTML)
        <capture>/orig.css        (그 화면에 걸린 모든 CSS 규칙 — Streamlit + 3차 base.css · home.css)
        <capture>/orig_meta.json  (stApp 까지의 바깥 껍데기 클래스)
  출력: web/templates/core/landing_original.html, web/static/css/original.css

바꾸는 것은 Django 에서 동작하게 하는 최소한뿐이다:
  - 사진 · 글꼴 · 커서 경로 → {% static %}
  - Streamlit 버튼(시작하기 등) → 회원가입 링크, 챗봇 팝오버 → /chat/ 링크 (클래스는 그대로라 모양이 같다)
  - Streamlit 아이콘 글꼴(Material Symbols) 글자 → 화살표 문자
  - 챗봇 팝오버를 끌어 옮기던 Streamlit 전용 스크립트는 뺀다 (교정 장면 · 방울 물결 스크립트는 그대로)

실행: python web/scripts/port_original_home.py <capture 폴더>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
SIGNUP = "{% url 'accounts:signup' %}"
CHAT = "{% url 'chat:list' %}"


def static_paths(text: str) -> str:
    # /app/static/landing/x.webp?v=2 · app/static/fonts/x.woff2 → {% static 'landing/x.webp' %}
    return re.sub(r"/?app/static/([\w./@-]+?)(\?v=\d+)?(?=[\"')\s])", lambda m: "{% static '" + m.group(1) + "' %}", text)


def css_paths(text: str) -> str:
    # CSS 는 정적 파일이라 템플릿 태그를 못 쓴다 → /static/ 절대 경로
    return re.sub(r"/?app/static/([\w./@-]+?)(\?v=\d+)?(?=[\"')])", r"/static/\1", text)


def convert_html(html: str) -> str:
    # 챗봇 팝오버를 끌어 옮기던 스크립트(세 번째 script) 제거
    html = re.sub(r"<script>\s*/\* Keep Streamlit's native popover.*?</script>", "", html, flags=re.S)
    # Material Symbols 아이콘 글자
    icon = re.compile(r'<span[^>]*data-testid="stIconMaterial"[^>]*>([a-z_]+)</span>')
    html = icon.sub(lambda m: {"arrow_forward": "→", "expand_more": "", "chat_bubble": "💬"}.get(m.group(1), ""), html)

    # 버튼 → 링크. 챗봇 팝오버는 /chat/, 나머지(시작하기 · 시나리오 열기)는 회원가입
    def button(m: re.Match) -> str:
        attrs, inner = m.group(1), m.group(2)
        href = CHAT if 'stPopoverButton' in attrs else SIGNUP
        attrs = re.sub(r'\s(type|kind|aria-haspopup|aria-expanded)="[^"]*"', "", attrs)
        return f'<a href="{href}" role="button"{attrs}>{inner}</a>'

    html = re.sub(r"<button([^>]*)>(.*?)</button>", button, html, flags=re.S)
    return static_paths(html)


def convert_css(css: str) -> str:
    # Streamlit 번들의 글꼴(KaTeX · Source Sans 등, ../media/...)은 이 화면에서 쓰지 않는다
    css = re.sub(r"@font-face\s*\{[^{}]*url\(\"?\.\./media/[^{}]*\}", "", css)
    return css_paths(css)


def main(capture: Path) -> None:
    html = (capture / "orig_main.html").read_text(encoding="utf-8")
    css = (capture / "orig.css").read_text(encoding="utf-8")
    meta = json.loads((capture / "orig_meta.json").read_text(encoding="utf-8"))

    # stApp → … → stMain 껍데기 (stMainBlockContainer 는 html 안에 이미 있다)
    shell = [c for c in reversed(meta["chain"][1:]) if c["testid"] not in ("stScreencast", "")
             or "emotion" in c["cls"]]
    open_tags = "".join(
        f'<{c["tag"].lower()} class="{c["cls"]}"' + (f' data-testid="{c["testid"]}"' if c["testid"] else "") + ">"
        for c in shell)
    close_tags = "".join(f'</{c["tag"].lower()}>' for c in reversed(shell))

    page = (
        "{% load static %}<!doctype html>\n<html lang=\"ko\">\n<head>\n"
        "<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>Beaurette · 화장품 광고 문구 검토</title>\n"
        "<link rel=\"icon\" href=\"{% static 'brand/rabbit-avatar.webp' %}\">\n"
        "<link rel=\"stylesheet\" href=\"{% static 'css/original.css' %}\">\n"
        "{% block head %}{% endblock %}\n"
        "</head>\n<body>\n"
        "{# 3차 원본 홈 — web/scripts/port_original_home.py 로 배포 화면에서 옮겼다. 직접 고치지 말고 위 스크립트를 다시 돌린다 #}\n"
        f"{open_tags}\n{convert_html(html)}\n{close_tags}\n"
        "{% block extra %}{% endblock %}\n"
        "</body>\n</html>\n"
    )
    (WEB / "templates" / "core" / "landing_original.html").write_text(page, encoding="utf-8")
    (WEB / "static" / "css" / "original.css").write_text(convert_css(css), encoding="utf-8")
    print("template", len(page), "css", len(convert_css(css)))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
