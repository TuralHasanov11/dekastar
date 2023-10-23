from typing import Any

from apps.administration.forms import (AboutTextFormSet, LoginForm,
                                       PasswordChangeForm,
                                       PrivacyPolicyTextFormSet,
                                       UserCreateForm, UserUpdateForm)
from apps.main.models import SiteText
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, DeleteView


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
            {"name": _("Users"), "route": reverse(
                "apps.administration:user-list")},
        ]
        return context


class PrivacyPolicyView(LoginRequiredMixin, TemplateView):
    template_name = "administration/privacy-policy.html"
    http_method_names = ["get", "post"]
    form_class = PrivacyPolicyTextFormSet
    redirect_url_name = "apps.administration:privacy-policy"

    def get(self, request, *args, **kwargs):
        if SiteText.objects.count() == 0:
            SiteText.objects.bulk_create(
                [SiteText(language=lang[0]) for lang in settings.LANGUAGES])
        site_texts = SiteText.objects.all().order_by(
            'language').only('language', 'privacy')
        form = self.form_class(
            initial=site_texts)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            initial=SiteText.objects.all().order_by('language').only('language', 'privacy'), data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(
                    'Privacy Policy texts were saved successfully!'))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _(
                    "Privacy Policy texts cannot be saved!"))
        messages.error(request, _("Privacy Policy texts cannot be saved!"))
        return render(request, self.template_name, {"form": form})


class AboutView(LoginRequiredMixin, TemplateView):
    template_name = "administration/about.html"
    http_method_names = ["get", "post"]
    form_class = AboutTextFormSet
    redirect_url_name = "apps.administration:about"

    def get(self, request, *args, **kwargs):
        if SiteText.objects.count() == 0:
            SiteText.objects.bulk_create(
                [SiteText(language=lang[0]) for lang in settings.LANGUAGES])
        site_texts = SiteText.objects.all().order_by(
            'language').only('language', 'about')
        form = self.form_class(
            initial=site_texts)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            initial=SiteText.objects.all().order_by('language').only('language', 'about'), data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(
                    'About Us texts were saved successfully!'))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _("About Us texts cannot be saved!"))
        messages.error(request, _("About Us texts cannot be saved!"))
        return render(request, self.template_name, {"form": form})


class ContactView(LoginRequiredMixin, TemplateView):
    template_name = "administration/contact.html"
    http_method_names = ["get", "post"]


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    next_page = reverse_lazy("apps.main:index")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "administration/auth/profile.html"
    http_method_names = ["get", "post"]
    form_class = UserUpdateForm
    redirect_url_name = "apps.administration:auth-profile"

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            instance=request.user, data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(
                    'User information were saved successfully!'))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _("User information cannot be saved!"))
        messages.error(request, _("User information cannot be saved!"))
        return render(request, self.template_name, {"form": form})


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    redirect_field_name = reverse_lazy("apps.administration:index")
    redirect_authenticated_user = True
    template_name = 'administration/auth/login.html'


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'administration/auth/password-change.html'
    success_url = reverse_lazy("apps.administration:auth-profile")
    form_class = PasswordChangeForm


class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = 'administration/users/list.html'
    context_object_name = "users"


class UserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = get_user_model()
    form_class = UserCreateForm
    login_url = reverse_lazy('apps.administration:index')
    template_name = 'administration/users/create.html'
    success_message = _("User was created successfully!")
    success_url = reverse_lazy('apps.administration:user-list')


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = get_user_model()
    # queryset = get_user_model().staff.all()
    success_message = _("User was deleted successfully!")
    success_url = reverse_lazy('apps.administration:user-list')
