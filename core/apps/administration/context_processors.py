
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def admin_menu(request):
    return {
        "admin_menu": [
            {
                "title": _("Dashboard"),
                "route": reverse("apps.administration:index"),
                "icon": "activity",
            },
            {
                "title": _("Banners"),
                "route": reverse("apps.administration:banner-list-create"),
                "permission": "main.view_banner",
                "icon": "image",
            },
            {
                "title": _("About Us"),
                "route": reverse("apps.administration:about"),
                "permission": "main.view_sitetext",
                "icon": "file-text",
            },
            {
                "title": _("Privacy Policy"),
                "route": reverse("apps.administration:privacy-policy"),
                "permission": "main.view_sitetext",
                "icon": "lock",
            },
            {
                "title": _("Delivery Policy"),
                "route": reverse("apps.administration:delivery-policy"),
                "permission": "main.view_sitetext",
                "icon": "truck",
            },
            {
                "title": _("Contact Information"),
                "route": reverse("apps.administration:contact"),
                "permission": "main.view_companyinfo",
                "icon": "phone",
            },
            {
                "title": _("Users"),
                "route": reverse("apps.administration:user-list"),
                "permission": "auth.view_user",
                "icon": "user",
            },
            {
                "title": _("Categories"),
                "route": reverse("apps.administration:store-category-list-create"),
                "permission": "store.view_category",
                "icon": "book",
            },
            {
                "title": _("Brands"),
                "route": reverse("apps.administration:store-brand-list-create"),
                "permission": "store.view_brand",
                "icon": "globe",
            },
            {
                "title": _("Models"),
                "route": reverse("apps.administration:store-product-model-list-create"),
                "permission": "store.view_productmodel",
                "icon": "aperture",
            },
            {
                "title": _("Products"),
                "route": reverse("apps.administration:store-product-list"),
                "permission": "store.view_product",
                "icon": "shopping-bag",
            },
            {
                "title": _("Orders"),
                "route": reverse("apps.administration:order-list"),
                "permission": "orders.view_order",
                "icon": "shopping-cart",
            },
        ]
    }
