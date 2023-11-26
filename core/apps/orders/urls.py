from apps.orders import views
from django.urls import path

app_name = "apps.orders"

urlpatterns = [
    path("checkout", views.CheckoutView.as_view(), name="checkout"),
    path("success", views.SuccessView.as_view(), name="success"),
]
