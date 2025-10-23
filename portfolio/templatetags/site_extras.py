from django import template
from django.templatetags.static import static

register = template.Library()

@register.simple_tag(takes_context=True)
def absolute_static(context, path: str) -> str:
    """
    Build an absolute URL for a static asset using the current request.
    Falls back to relative static URL if request is missing.
    Usage: {% absolute_static 'images/og-default.svg' %}
    """
    try:
        url = static(path)
    except Exception:
        url = path
    request = context.get('request')
    if request:
        try:
            return request.build_absolute_uri(url)
        except Exception:
            return url
    return url

@register.simple_tag(takes_context=True)
def absolute_url(context, url_path: str) -> str:
    """
    Convert a relative/media URL into an absolute URL using the current request.
    Usage: {% absolute_url obj.image.url %}
    """
    if not url_path:
        return ''
    request = context.get('request')
    if request:
        try:
            return request.build_absolute_uri(url_path)
        except Exception:
            return url_path
    return url_path
