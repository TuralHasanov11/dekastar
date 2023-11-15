import enum

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.translation import gettext_lazy as _

register = template.Library()


class ProductQuantityType(enum.Enum):
    SQUARE_METER = "m<sup>2</sup>"
    NUMBER = _("number")


@register.filter
@stringfilter
def get_product_quantity_type_display(value):
    return ProductQuantityType[value].value
