import enum

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


class OrderStatusIndication(enum.Enum):
    PENDING = "warning"
    PAID = "info"
    DELIVERED = "success"
    RETURNED = "dark"
    CANCELLED = "danger"


@register.filter
@stringfilter
def get_order_status_indication(value):
    return OrderStatusIndication[value].value
