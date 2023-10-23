
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
                "title": _("Contact Information"),
                "route": reverse("apps.administration:contact"),
                "icon": "phone",
            },
            {
                "title": _("User List"),
                "route": reverse("apps.administration:user-list"),
                "icon": "user",
            },
        ]
    }
