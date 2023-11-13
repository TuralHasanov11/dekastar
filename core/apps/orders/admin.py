from apps.orders.models import Order, OrderItem
from django.contrib import admin


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("name", "total_paid", "phone", "created_at")
    ordering = ("-created_at", )
    inlines = [
        OrderItemInline,
    ]
    readonly_fields = ["seen"]
