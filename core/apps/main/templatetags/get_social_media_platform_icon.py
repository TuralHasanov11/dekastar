from django import template
from django.template.defaultfilters import stringfilter
from shared.social_media_platform_icons import SocialMediaPlatformIconContainer

register = template.Library()


@register.filter
@stringfilter
def get_social_media_platform_icon(value):
    print(SocialMediaPlatformIconContainer[value].value)
    return SocialMediaPlatformIconContainer[value].value