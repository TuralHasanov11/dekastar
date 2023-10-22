from typing import Any

from apps.administration.forms import LoginForm, PasswordChangeForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, UpdateView


class DashboardView(LoginRequiredMixin, TemplateView):
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


class PrivacyPolicyView(LoginRequiredMixin, TemplateView):
    template_name = "administration/privacy-policy.html"
    http_method_names = ["get", "post"]


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = "administration/about.html"
    http_method_names = ["get", "post"]


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = "administration/contact.html"
    http_method_names = ["get", "post"]


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy("apps.main:index")


class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = "administration/profile.html"


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    redirect_field_name = reverse_lazy("apps.administration:index")
    redirect_authenticated_user = True
    template_name = 'administration/auth/login.html'


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'administration/auth/password-change.html'
    success_url = reverse_lazy("apps.administration:auth-profile")
    form_class = PasswordChangeForm
