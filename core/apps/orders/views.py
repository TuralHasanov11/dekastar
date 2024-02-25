from typing import Any

from apps.orders.cart_processor import CartProcessor
from apps.orders.forms import CheckoutForm
from apps.orders.models import Order
from apps.orders.order_processor import OrderProcessor
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class CheckoutView(TemplateView):
    template_name = "orders/checkout.html"
    http_method_names = ["get", "post"]
    form_class = CheckoutForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context

    def post(self, request):
        form = self.form_class(request.POST)
        cart = CartProcessor(request)
        if form.is_valid():
            data = form.cleaned_data
            data.pop("terms_agreed")
            with transaction.atomic():
                order = Order(
                    **data,
                    total_paid=cart.get_total_price,
                )
                order.save()
                for item in cart:
                    order.add_item(
                        item["product"]["id"],
                        item["product"]["quantity_type"],
                        item["price"],
                        item["total_price"],
                        item["quantity"],
                    )
                order_processor = OrderProcessor(request=request)
                order_processor.create(order_id=str(order.uuid))
                cart.clear()
                return redirect("apps.orders:success")
        messages.error(request, _("Order cannot be placed!"))
        return render(request, self.template_name, {"form": form})


class SuccessView(TemplateView):
    template_name = "orders/success.html"
    http_method_names = ["get"]

    def get(self, request):
        order_processor = OrderProcessor(request=request)
        try:
            order = Order.objects.get(uuid=order_processor.order_id)
            return render(request, self.template_name, context={"order": order})
        except Order.DoesNotExist:
            return redirect("apps.main:index")
