from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for key, val in kwargs.items():
        query[key] = val
    return query.urlencode()
