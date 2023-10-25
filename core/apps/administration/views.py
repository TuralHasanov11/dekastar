from typing import Any

from apps.administration.forms import (AboutTextFormSet, CompanyInfoFormSet,
                                       ContactEmailForm, ContactPhoneForm,
                                       DeliveryPolicyTextFormSet, LoginForm,
                                       PasswordChangeForm,
                                       PrivacyPolicyTextFormSet, SiteImageForm,
                                       SocialMediaLinkForm, UserCreateForm,
                                       UserUpdateForm)
from apps.main.models import (CompanyInfo, ContactEmail, ContactPhone,
                              SiteImage, SiteText, SocialMediaLink)
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
            {"name": _("Delivery Policy"), "route": reverse(
                "apps.administration:delivery-policy")},
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
            'language').only('language', 'privacy_policy')
        form = self.form_class(
            initial=site_texts)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            initial=SiteText.objects.all().order_by('language').only('language', 'privacy_policy'), data=request.POST)
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


class DeliveryPolicyView(LoginRequiredMixin, TemplateView):
    template_name = "administration/delivery-policy.html"
    http_method_names = ["get", "post"]
    form_class = DeliveryPolicyTextFormSet
    redirect_url_name = "apps.administration:delivery-policy"

    def get(self, request, *args, **kwargs):
        if SiteText.objects.count() == 0:
            SiteText.objects.bulk_create(
                [SiteText(language=lang[0]) for lang in settings.LANGUAGES])
        site_texts = SiteText.objects.all().order_by(
            'language').only('language', 'delivery')
        form = self.form_class(
            initial=site_texts)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            initial=SiteText.objects.all().order_by('language').only('language', 'delivery_policy'), data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(
                    'Delivery Policy texts were saved successfully!'))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _(
                    "Delivery Policy texts cannot be saved!"))
        messages.error(request, _("Delivery Policy texts cannot be saved!"))
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
    http_method_names = ["get"]
    social_media_link_form_class = SocialMediaLinkForm
    contact_phone_form_class = ContactPhoneForm
    contact_email_form_class = ContactEmailForm
    company_info_form_class = CompanyInfoFormSet

    def get(self, request, *args, **kwargs):
        if CompanyInfo.objects.count() == 0:
            CompanyInfo.objects.bulk_create(
                [CompanyInfo(language=lang[0]) for lang in settings.LANGUAGES])
        social_media_link_form = self.social_media_link_form_class()
        contact_email_form = self.contact_email_form_class()
        contact_phone_form = self.contact_phone_form_class()
        company_info_form = self.company_info_form_class(initial=CompanyInfo.objects.all())
        social_media_links = SocialMediaLink.objects.all()
        contact_emails = ContactEmail.objects.all()
        contact_phones = ContactPhone.objects.all()
        return render(request, self.template_name, {
            "social_media_link_form": social_media_link_form,
            "contact_email_form": contact_email_form,
            "company_info_form": company_info_form,
            "contact_phone_form": contact_phone_form,
            "social_media_links": social_media_links,
            "contact_emails": contact_emails,
            "contact_phones": contact_phones,
        })


class ContactEmailCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ContactEmail
    form_class = ContactEmailForm
    http_method_names = ["post"]
    success_message = _("Contact email was added successfully!")

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#contact-email-form"


class ContactEmailDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ContactEmail
    success_message = _("Contact email was deleted successfully!")

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#contact-email-form"


class ContactPhoneCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ContactPhone
    form_class = ContactPhoneForm
    http_method_names = ["post"]
    success_message = _("Contact phone was added successfully!")

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#contact-phone-form"


class ContactPhoneDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ContactPhone
    success_message = _("Contact phone was deleted successfully!")

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#contact-phone-form"


class SocialMediaLinkCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = SocialMediaLink
    form_class = SocialMediaLinkForm
    http_method_names = ["post"]
    success_message = _("Social media link was added successfully!")

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#social-media-link-form"


class SocialMediaLinkDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = SocialMediaLink
    success_message = _(
        "Social media link was deleted successfully!")

    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#social-media-link-form"


class CompanyInfoCreateView(LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    model = CompanyInfo
    form_class = CompanyInfoFormSet
    http_method_names = ["post"]
    success_message = _("Company info was saved successfully!")
    redirect_url_name = "apps.administration:contact"

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            initial=CompanyInfo.objects.all(), data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(
                    'Company info was saved successfully!'))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _("Company info cannot be saved!"))
        messages.error(request, _("Company info cannot be saved!"))
        return redirect(self.redirect_url_name)
    
    def get_success_url(self) -> str:
        return reverse("apps.administration:contact") + "#company-info-form"
    

class SiteImagesView(LoginRequiredMixin, TemplateView):
    template_name = "administration/site-images.html"
    http_method_names = ["get", "post"]
    form_class = SiteImageForm
    redirect_url_name = "apps.administration:site-images"

    def get(self, request, *args, **kwargs):
        try:
            site_image = SiteImage.objects.first()
        except SiteImage.DoesNotExist:
            site_image = SiteImage()
            site_image.save()
        form = self.form_class(instance=site_image)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            instance=SiteText.objects.first(), data=request.POST, files=request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _(
                    'Site images were saved successfully!'))
                return redirect(self.redirect_url_name)
            except Exception:
                messages.error(request, _(
                    "Site images cannot be saved!"))
        messages.error(request, _("Site images cannot be saved!"))
        return render(request, self.template_name, {"form": form})


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
