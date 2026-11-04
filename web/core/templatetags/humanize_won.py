"""금액 표시: 19200000 → '1,920만 원' (만 원 단위, 1억 이상은 '1.9억 원')."""
from django import template

register = template.Library()


@register.filter
def won(value) -> str:
    try:
        v = float(value)
    except (TypeError, ValueError):
        return "-"
    if abs(v) >= 1e8:
        return f"{v / 1e8:,.1f}억 원"
    if abs(v) >= 1e4:
        return f"{round(v / 1e4):,}만 원"
    return f"{round(v):,}원"


@register.filter
def comma(value) -> str:
    """21945 → '21,945'"""
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return value
