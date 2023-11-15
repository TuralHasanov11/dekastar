from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def build_language_path(context, **kwargs):
    path = kwargs.get("path")
    language = kwargs.get("lang")
    current_language = kwargs.get("current_language")
    prefix = f"/{current_language}/"
    if current_language in (item[0] for item in settings.LANGUAGES):
        new_prefix = f"/{language}/"
        if prefix in path and language != settings.LANGUAGE_CODE:
            path = path.replace(prefix, new_prefix)
        elif prefix not in path and language is not settings.LANGUAGE_CODE:
            path = new_prefix.rstrip("/") + path
        elif (prefix in path and language is settings.LANGUAGE_CODE) or (
            language is not settings.LANGUAGE_CODE
        ):
            path = f"/{path.replace(prefix, '')}"
    return path
