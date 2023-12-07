from apps.main.models import ContactEmail, ContactPhone, SocialMediaLink
from apps.store.models import Category
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def default_header_menu(request):
    categories = Category.categories.list_queryset().all()
    return {
        "default_header_menu": [
            {"title": _("Home"), "route": reverse("apps.main:index")},
            {
                "title": _("Categories"),
                "route": reverse("apps.store:category-products"),
                "children": [
                    {
                        "title": category.category_name,
                        "route": reverse(
                            "apps.store:category-products",
                            kwargs={"category": category.slug},
                        ),
                    }
                    for category in categories
                ],
            },
            {"title": _("About Us"), "route": reverse("apps.main:about")},
            {"title": _("Contact"), "route": reverse("apps.main:contact")},
        ]
    }


def default_footer_menu(request):
    categories = Category.categories.list_queryset().all()
    contact_phone = ContactPhone.objects.first()
    contact_email = ContactEmail.objects.first()
    return {
        "default_footer_menu": [
            {
                "title": _("Categories"),
                "children": [
                    {
                        "title": category.category_name,
                        "route": reverse(
                            "apps.store:category-products",
                            kwargs={"category": category.slug},
                        ),
                    }
                    for category in categories
                ],
            },
            {
                "title": _("About the Company"),
                "children": [
                    {"title": _("About Us"), "route": reverse("apps.main:about")},
                    {"title": _("Contact"), "route": reverse("apps.main:contact")},
                    {
                        "title": _("Privacy Policy"),
                        "route": reverse("apps.main:privacy-policy"),
                    },
                    {
                        "title": _("Delivery Policy"),
                        "route": reverse("apps.main:delivery-policy"),
                    },
                ],
            },
            {
                "title": _("Contact Us"),
                "children": [
                    {"title": _("Telephone"), "route": f"tel:{getattr(contact_phone, 'phone', '')}"},
                    {"title": _("E-mail"), "route": f"mailto:{getattr(contact_email, 'email', '')}"},
                ],
            },
        ]
    }


def default_footer_social_links(request):
    return {"default_footer_social_links": SocialMediaLink.social_media_links.list_queryset()}


def whatsapp_number(request):
    return {"whatsapp_number": settings.WHATSAPP_NUMBER}
