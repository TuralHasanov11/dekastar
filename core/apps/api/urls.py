from apps.api import views
from django.urls import path

app_name = "apps.api"

urlpatterns = [
    path("favorites/add", views.FavoritesAddView.as_view(), name="store-favorites-add"),
    path("favorites/remove", views.FavoritesRemoveView.as_view(), name="store-favorites-remove"),
    path("cart/add", views.CartAddView.as_view(), name="orders-cart-add"),
    path("cart/update", views.CartUpdateView.as_view(), name="orders-cart-update"),
    path("cart/remove", views.CartRemoveView.as_view(), name="orders-cart-remove"),
    path("cart/detail", views.CartDetailView.as_view(), name="orders-cart-detail"),
]
