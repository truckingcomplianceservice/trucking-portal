from django import template
register = template.Library()


@register.filter
def dictkey(d, key):
    try:
        return d.get(key)
    except (AttributeError, TypeError):
        return None


import re as _re
from django.utils.safestring import mark_safe
from django.utils.html import escape as _escape


def _digits(v):
    return _re.sub(r"[^0-9+]", "", v or "")


@register.filter
def tel(value):
    """Render a phone number as a tap-to-call link. Usage: {{ d.phone|tel }}"""
    if not value:
        return "—"
    d = _digits(value)
    if not d:
        return _escape(value)
    return mark_safe(f'<a href="tel:{d}" style="color:var(--blue,#1e6fb8);text-decoration:none">{_escape(value)}</a>')


@register.filter
def call_text(value):
    """Render a phone number with both Call and Text quick links.
    Usage: {{ d.phone|call_text }}"""
    if not value:
        return mark_safe('<span class="sub">No phone</span>')
    d = _digits(value)
    if not d:
        return _escape(value)
    return mark_safe(
        f'<span>{_escape(value)}</span> '
        f'<a href="tel:{d}" style="margin-left:6px;text-decoration:none">📞</a> '
        f'<a href="sms:{d}" style="margin-left:2px;text-decoration:none">💬</a>')
