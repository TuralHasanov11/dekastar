from apps.store import views
from django.urls import path
from django.utils.translation import gettext_lazy as _

app_name = "apps.store"

urlpatterns = [
    path(_("categories"), views.CategoryProductsView.as_view(), name="category-products"),
    path(
        _("categories/<str:category>"),
        views.CategoryProductsView.as_view(),
        name="category-products",
    ),
    path(
       _("products/<str:slug>"), views.ProductDetailView.as_view(), name="product-detail"
    ),
    path(_("favorites"), views.FavoritesView.as_view(), name="favorites"),
]
