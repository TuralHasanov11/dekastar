from apps.orders import views
from django.urls import path
from django.utils.translation import gettext_lazy as _

app_name = "apps.orders"

urlpatterns = [
    path(_("checkout"), views.CheckoutView.as_view(), name="checkout"),
    path(_("success"), views.SuccessView.as_view(), name="success"),
]
