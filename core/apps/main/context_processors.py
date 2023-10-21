from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def default_header_menu(request):
    return {
        "default_header_menu": [
            {"title": _("Home"), "route": reverse("apps.main:index")},
            {"title": _("About Us"), "route": reverse("apps.main:about")},
            {"title": _("Contact"), "route": reverse("apps.main:contact")},
        ]
    }


def default_footer_menu(request):
    return {
        "default_footer_menu": [
            {
                "title": _("Categories"),
                "children": [

                ],
            },
            {
                "title": _("About the Company"),
                "children": [
                    {"title": _("About Us"), "route": reverse(
                        "apps.main:about")},
                    {"title": _("Contact"), "route": reverse(
                        "apps.main:contact")},
                    {"title": _("Privacy Policy"), "route": reverse(
                        "apps.main:privacy-policy")},
                ],
            },
            {
                "title": _("Contact Us"),
                "children": [
                    {"title": _("Telephone"), "route": ""},
                    {"title": _("Address"), "route": ""},
                    {"title": _("E-mail"), "route": ""},
                ],
            }
        ]
    }


def default_footer_social_links(request):
    return {
        "default_footer_social_links": [
            {
                "link": "",
                "icon": "fa fa-facebook"
            },
            {
                "link": "",
                "icon": "fa fa-facebook"
            },
            {
                "link": "",
                "icon": "fa fa-facebook"
            }
        ]
    }
