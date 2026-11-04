"""3차 원본 홈을 좌우로 넘기는 8장짜리 화면(자비스 HUD · 어두운 유리)으로 다시 묶는다.

원본을 새로 쓰지 않는다. 배포 화면에서 떠 온 HTML(orig_main.html)에서 섹션을 id · class 로 그대로 잘라
장(slide)마다 넣는다 → 원본 문구 · 사진 · 교정 장면 · 토끼 · 방울 물결이 그대로 남는다.
원본 CSS(app/components/styles/base.css · home.css)도 그대로 쓰고, 색과 배치만 jarvis.css 가 덮는다.

실행: python web/scripts/build_jarvis_home.py <capture 폴더>
출력: web/templates/core/landing_jarvis.html, web/static/orig/{base,home}.css, web/static/js/orig-{motion,drip}.js
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from port_original_home import convert_html, css_paths  # noqa: E402

WEB = Path(__file__).resolve().parents[1]
REPO = WEB.parent
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class _Finder(HTMLParser):
    """조건에 맞는 첫(또는 n번째) 요소의 시작 · 끝 위치를 찾는다."""

    def __init__(self, html: str, test, nth: int = 0):
        super().__init__(convert_charrefs=False)
        self.html, self.test, self.nth = html, test, nth
        self.lines = [0]
        for m in re.finditer("\n", html):
            self.lines.append(m.end())
        self.depth, self.start, self.stop, self.found = 0, None, None, 0

    def _pos(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        if self.stop is not None:
            return
        if self.start is None:
            if self.test(tag, dict(attrs)):
                if self.found == self.nth:
                    self.start, self.depth = self._pos(), (0 if tag in VOID else 1)
                    if tag in VOID:
                        self.stop = self.start + len(self.get_starttag_text())
                    return
                self.found += 1
        elif tag not in VOID:
            self.depth += 1

    def handle_endtag(self, tag):
        if self.start is None or self.stop is not None or tag in VOID:
            return
        self.depth -= 1
        if self.depth == 0:
            pos = self._pos()
            self.stop = self.html.index(">", pos) + 1


def grab(html: str, *, cls: str | None = None, id: str | None = None, tag: str | None = None, nth: int = 0) -> str:
    def test(t, a):
        if tag and t != tag:
            return False
        if id and a.get("id") != id:
            return False
        return not cls or set(cls.split()) <= set((a.get("class") or "").split())
    f = _Finder(html, test, nth)
    f.feed(html)
    if f.start is None or f.stop is None:
        raise SystemExit(f"원본에서 못 찾음: cls={cls} id={id} nth={nth}")
    return html[f.start:f.stop]


def slide(key: str, title: str, inner: str, *, bg: str = "", cls: str = "") -> str:
    data_bg = f' data-bg="{{% static \'{bg}\' %}}"' if bg else ""
    return (f'<section class="jv-slide {cls}" id="s-{key}" data-title="{title}"{data_bg} aria-label="{title}">\n'
            f'<div class="jv-frame"><i class="c tl"></i><i class="c tr"></i><i class="c bl"></i><i class="c br"></i></div>\n'
            f'<div class="jv-body">{inner}</div>\n</section>\n')


def main(capture: Path) -> None:
    src = (capture / "orig_main.html").read_text(encoding="utf-8")
    h = convert_html(src)   # 사진 경로 → {% static %}, 버튼 → 링크

    hero = (
        '<div class="jv-hero st-key-home_hero">'
        + grab(h, cls="bw-h-scene")
        + '<div class="jv-hero-copy bw">'
        + grab(h, cls="bw-h-hero")
        + '<div class="jv-cta"><a class="jv-btn" href="{% url \'accounts:signup\' %}">시작하기 <span>→</span></a>'
          '<a class="bw-h-ghost" href="#s-demo">실제 검토 보기</a></div>'
        + grab(h, cls="bw-h-meta")
        + grab(h, cls="bw-h-proof")
        + "</div></div>"
    )
    band = '<div class="bw jv-band">' + grab(h, cls="bw-h-band-type") + "</div>"
    cta = grab(h, cls="bw-h-cta") if 'class="bw-h-cta' in h else ""

    slides = [
        slide("hero", "처음", hero, cls="is-hero"),
        slide("demo", "검토 장면", '<div class="bw">' + grab(h, id="bw-demo") + "</div>"),
        slide("skin", "피부에 닿는 문구", '<div class="bw">' + grab(h, cls="bw-h-skin", tag="section") + "</div>" + band),
        slide("problem", "문제", '<div class="bw">' + grab(h, id="bw-problem") + "</div>",
              bg="landing/editorial-amber.webp", cls="is-photo"),
        slide("how", "검토 방식", '<div class="bw">' + grab(h, id="bw-how") + "</div>",
              bg="landing/editorial-serum.webp", cls="is-photo"),
        slide("features", "기능", '<div class="bw">' + grab(h, id="bw-features") + "</div>"),
        slide("forecast", "예상 매출", '<div class="bw">' + grab(h, id="bw-forecast")
              + '<div class="jv-cta"><a class="jv-btn ghost" href="{% url \'accounts:signup\' %}">예상 매출 시나리오 열기 <span>→</span></a></div></div>'),
        slide("sources", "근거 자료", '<div class="bw">' + grab(h, id="bw-sources") + grab(h, cls="bw-h-close", tag="section")
              + cta + '<div class="jv-cta"><a class="jv-btn" href="{% url \'accounts:signup\' %}">검토 시작하기 <span>→</span></a></div></div>',
              bg="landing/editorial-documents.webp", cls="is-photo"),
    ]
    scripts = re.findall(r"<script>.*?</script>", src, flags=re.S)
    motion = next(s for s in scripts if "bw-js" in s)
    drip = next(s for s in scripts if "__bwDrip" in s)
    (WEB / "static" / "js" / "orig-motion.js").write_text(motion[8:-9], encoding="utf-8")
    (WEB / "static" / "js" / "orig-drip.js").write_text(drip[8:-9], encoding="utf-8")

    styles = REPO / "app" / "components" / "styles"
    (WEB / "static" / "orig").mkdir(exist_ok=True)
    for name in ("base", "home"):
        (WEB / "static" / "orig" / f"{name}.css").write_text(css_paths((styles / f"{name}.css").read_text(encoding="utf-8")), encoding="utf-8")

    nav = "".join(f'<button type="button" data-go="{i}"><b class="n">{i + 1:02d}</b><span>{t}</span></button>'
                  for i, t in enumerate(["처음", "검토 장면", "피부에 닿는 문구", "문제", "검토 방식", "기능", "예상 매출", "근거 자료"]))
    logo = grab(h, cls="bw-h-logo")
    page = f"""{{% load static %}}<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Beaurette · 화장품 광고 문구 검토</title>
<link rel="icon" href="{{% static 'brand/rabbit-avatar.webp' %}}">
<link rel="stylesheet" href="{{% static 'orig/base.css' %}}">
<link rel="stylesheet" href="{{% static 'orig/home.css' %}}">
<link rel="stylesheet" href="{{% static 'css/jarvis.css' %}}">
</head>
{{# 3차 원본 홈을 8장 가로 화면으로 묶은 것 — web/scripts/build_jarvis_home.py 가 만든다. 직접 고치지 말고 스크립트를 다시 돌린다 #}}
<body class="jv" data-slide="0">
<div class="jv-bg" aria-hidden="true"><div class="jv-bg-photo"></div><canvas class="jv-particles"></canvas><div class="jv-grid"></div><div class="jv-vignette"></div><div class="jv-scan"></div></div>
<header class="jv-top">
  <div class="jv-logo bw">{logo}</div>
  <p class="jv-sys"><i></i>BEAURETTE · AD REVIEW SYSTEM <b data-clock></b></p>
  <a class="jv-btn sm" href="{{% url 'accounts:login' %}}">로그인</a>
  <a class="jv-btn sm solid" href="{{% url 'accounts:signup' %}}">시작하기 <span>→</span></a>
</header>
<div class="jv-hud" aria-hidden="true"><i class="r1"></i><i class="r2"></i><p class="jv-read l" data-read></p><p class="jv-read r mono">LAT 37.5665 · LNG 126.9780<br>RAG · RULES · VERIFY</p></div>
<main class="jv-deck" id="main" tabindex="-1">
{''.join(slides)}
</main>
<nav class="jv-pager" aria-label="화면 넘기기">
  <button type="button" class="jv-arrow" data-step="-1" aria-label="이전 화면">←</button>
  <div class="jv-steps">{nav}</div>
  <p class="jv-count mono"><b data-cur>01</b> / 08</p>
  <button type="button" class="jv-arrow" data-step="1" aria-label="다음 화면">→</button>
</nav>
<a class="jv-chat" href="{{% url 'chat:list' %}}" aria-label="뷰렛 챗봇 열기"><img src="{{% static 'brand/rabbit-avatar.webp' %}}" alt="" width="48" height="48"></a>
<script src="{{% static 'js/orig-motion.js' %}}"></script>
<script src="{{% static 'js/orig-drip.js' %}}"></script>
<script src="{{% static 'js/glass.js' %}}"></script>
<script src="{{% static 'js/jarvis.js' %}}"></script>
</body>
</html>
"""
    (WEB / "templates" / "core" / "landing_jarvis.html").write_text(page, encoding="utf-8")
    print("slides", len(slides), "template", len(page))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
