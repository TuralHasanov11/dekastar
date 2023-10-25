from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag(takes_context=True)
def build_language_path(context, **kwargs):
    path = kwargs.get('path')
    language = kwargs.get('lang')
    currentLanguage = kwargs.get('current_language')
    prefix = f"/{currentLanguage}/"
    if currentLanguage in (item[0] for item in settings.LANGUAGES):
        newPrefix = f"/{language}/"
        if prefix in path and language != settings.LANGUAGE_CODE:
            return path.replace(prefix, newPrefix)
        elif prefix not in path and language is not settings.LANGUAGE_CODE:
            return newPrefix.rstrip("/")+path
        elif (prefix in path and language is settings.LANGUAGE_CODE) or (language is not settings.LANGUAGE_CODE):
            return f"/{path.replace(prefix, '')}"
    return path


