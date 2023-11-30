from apps.administration import views
from django.urls import path

app_name = "apps.administration"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="index"),
    path("privacy-policy", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("delivery-policy", views.DeliveryPolicyView.as_view(), name="delivery-policy"),
    path("about", views.AboutView.as_view(), name="about"),
    path("contact", views.ContactView.as_view(), name="contact"),
    path(
        "contact-email",
        views.ContactEmailCreateView.as_view(),
        name="contact-email-create",
    ),
    path(
        "contact-phone",
        views.ContactPhoneCreateView.as_view(),
        name="contact-phone-create",
    ),
    path(
        "social-media-link",
        views.SocialMediaLinkCreateView.as_view(),
        name="social-media-link-create",
    ),
    path(
        "company-info",
        views.CompanyInfoCreateView.as_view(),
        name="company-info-create",
    ),
    path(
        "contact-email/<int:pk>",
        views.ContactEmailDeleteView.as_view(),
        name="contact-email-delete",
    ),
    path(
        "contact-phone/<int:pk>",
        views.ContactPhoneDeleteView.as_view(),
        name="contact-phone-delete",
    ),
    path(
        "social-media-link/<int:pk>",
        views.SocialMediaLinkDeleteView.as_view(),
        name="social-media-link-delete",
    ),
    path("banners", views.BannerListCreateView.as_view(), name="banner-list-create"),
    path(
        "banners/<int:pk>",
        views.BannerUpdateDeleteView.as_view(),
        name="banner-update-delete",
    ),
    path("site-images", views.SiteImagesView.as_view(), name="site-images"),
    path("users", views.UserListView.as_view(), name="user-list"),
    path("users/create", views.UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/delete", views.UserDeleteView.as_view(), name="user-delete"),
    path("auth/login", views.LoginView.as_view(), name="auth-login"),
    path("auth/logout", views.LogoutView.as_view(), name="auth-logout"),
    path(
        "auth/password-change",
        views.PasswordChangeView.as_view(),
        name="auth-password-change",
    ),
    path("auth/profile", views.ProfileView.as_view(), name="auth-profile"),
    path(
        "store/categories",
        views.CategoryListCreateView.as_view(),
        name="store-category-list-create",
    ),
    path(
        "store/categories/<int:pk>",
        views.CategoryUpdateDeleteView.as_view(),
        name="store-category-update-delete",
    ),
    path(
        "store/brands",
        views.BrandListCreateView.as_view(),
        name="store-brand-list-create",
    ),
    path(
        "store/brands/<int:pk>",
        views.BrandUpdateDeleteView.as_view(),
        name="store-brand-update-delete",
    ),
    path(
        "store/product-models",
        views.ProductModelListCreateView.as_view(),
        name="store-product-model-list-create",
    ),
    path(
        "store/product-models/<int:pk>",
        views.ProductModelUpdateDeleteView.as_view(),
        name="store-product-model-update-delete",
    ),
    path("store/products", views.ProductListView.as_view(), name="store-product-list"),
    path(
        "store/products/create",
        views.ProductCreateView.as_view(),
        name="store-product-create",
    ),
    path(
        "store/products/<int:pk>",
        views.ProductUpdateDeleteView.as_view(),
        name="store-product-update-delete",
    ),
    path("orders", views.OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>", views.OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/status-change", views.OrderStatusChangeView.as_view(), name="order-status-change"),
]
