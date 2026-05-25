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
                "title": _("Categories"),
                "route": reverse("apps.administration:store-category-list-create"),
                "icon": "book",
            },
            {
                "title": _("Brands"),
                "route": reverse("apps.administration:store-brand-list-create"),
                "icon": "globe",
            },
            {
                "title": _("Collections"),
                "route": reverse("apps.administration:store-collection-list-create"),
                "icon": "aperture",
            },
            {
                "title": _("Products"),
                "route": reverse("apps.administration:store-product-list"),
                "icon": "shopping-bag",
            },
            {
                "title": _("Orders"),
                "route": reverse("apps.administration:order-list"),
                "icon": "shopping-cart",
            },
            {
                "title": _("Banners"),
                "route": reverse("apps.administration:banner-list-create"),
                "icon": "image",
            },
            {
                "title": _("Site Images"),
                "route": reverse("apps.administration:site-images"),
                "icon": "layout",
            },
            {
                "title": _("About Us"),
                "route": reverse("apps.administration:about"),
                "icon": "file-text",
            },
            {
                "title": _("Privacy Policy"),
                "route": reverse("apps.administration:privacy-policy"),
                "icon": "lock",
            },
            {
                "title": _("Delivery Policy"),
                "route": reverse("apps.administration:delivery-policy"),
                "icon": "truck",
            },
            {
                "title": _("Contact Information"),
                "route": reverse("apps.administration:contact"),
                "icon": "phone",
            },
            {
                "title": _("Users"),
                "route": reverse("apps.administration:user-list"),
                "permission": "auth.view_user",
                "icon": "user",
            },
            {
                "title": _("Blog Posts"),
                "route": reverse("apps.administration:blog-list"),
                "icon": "file"
            }
        ]
    }
