from apps.store import views
from django.urls import path

app_name = "apps.store"

urlpatterns = [
    path("categories", views.CategoryProductsView.as_view(), name="category-products"),
    path("categories/<str:slug>", views.CategoryProductsView.as_view(), name="category-products"),
    path("products/<str:slug>", views.ProductDetailView.as_view(), name="product-detail"),
    path("favorites", views.FavoritesView.as_view(), name="favorites"),
]
