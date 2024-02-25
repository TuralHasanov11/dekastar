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
    path("store/categories", views.CategoryListView.as_view(), name="category-list"),
    path("store/filters", views.FilterListView.as_view(), name="filter-list"),
    path("store/products", views.ProductListView.as_view(), name="product-list"),
    path("privacy-policy", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("delivery-policy", views.DeliveryPolicyView.as_view(), name="delivery-policy"),
    path("about", views.AboutView.as_view(), name="about"),
    path("contact", views.ContactView.as_view(), name="contact"),
    path("banners", views.BannerListView.as_view(), name="banner-list"),
    path("store/products/<str:slug>", views.ProductDetailView.as_view(), name="product-detail"),
    path(
        "store/products/<str:slug>/related-products",
        views.RelatedProductListView.as_view(),
        name="related-product-list",
    ),
    path("checkout", views.CheckoutView.as_view(), name="checkout"),
]
