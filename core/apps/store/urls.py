from apps.store import views
from django.urls import path

app_name = "apps.store"

urlpatterns = [
    path("categories", views.index, name="category-products"),
    path("categories/<str:slug>", views.index, name="category-products"),
    path("products/<str:slug>", views.index, name="product-detail"),
]
