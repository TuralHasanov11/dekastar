from django import template
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.filter
def in_stock_display(value: bool):
    return _("In Stock") if value is True else _("Not In Stock")
