from typing import Any

from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, UpdateView


class DashboardView(TemplateView):
    template_name = "administration/index.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["creator_dashboards"] = [
            {"name": _("About Us"), "route": reverse(
                "apps.administration:about")},
            {"name": _("Privacy Policy"), "route": reverse(
                "apps.administration:privacy-policy")},
            {"name": _("Contact"), "route": reverse(
                "apps.administration:contact")},
        ]
        return context


class PrivacyPolicyView(UpdateView):
    template_name = "administration/privacy-policy.html"


class AboutView(UpdateView):
    template_name = "administration/about.html"


class ContactView(UpdateView):
    template_name = "administration/contact.html"
