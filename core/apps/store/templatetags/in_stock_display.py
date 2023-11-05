from django import template
from django.template.defaultfilters import stringfilter
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter
@stringfilter
def in_stock_display(value: bool):
    return _("In Stock") if value is True else _("Not In Stock")
