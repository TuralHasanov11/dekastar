import os
from typing import Any

from django.contrib import messages
from django.core.mail import BadHeaderError, EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from apps.main.forms import ContactForm
from apps.main.models import (
    Banner,
    CompanyInfo,
    ContactEmail,
    ContactPhone,
    SiteImage,
    SiteText,
)
from apps.store.models import Category, Product


class HomeView(TemplateView):
    template_name = "main/index.html"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.categories.list_queryset()
        context["new_products"] = Product.products.new_products_queryset()
        context["discounted_products"] = Product.products.discounted_products_queryset()
        context["banners"] = Banner.objects.filter(is_active=True).order_by("-id")
        return context


class PrivacyPolicyView(TemplateView):
    template_name = "main/privacy-policy.html"
    http_method_names = ["get"]

    def get(self, request):
        privacy_policy = SiteText.site_texts.privacy_policy(language=get_language())
        privacy_policy_image = SiteImage.site_images.privacy_policy_image()
        return render(
            request,
            self.template_name,
            {"privacy_policy": privacy_policy, "privacy_policy_image": privacy_policy_image},
        )


class DeliveryPolicyView(TemplateView):
    template_name = "main/delivery-policy.html"
    http_method_names = ["get"]

    def get(self, request):
        delivery_policy = SiteText.site_texts.delivery_policy(language=get_language())
        delivery_policy_image = SiteImage.site_images.delivery_policy_image()
        return render(
            request,
            self.template_name,
            {
                "delivery_policy": delivery_policy,
                "delivery_policy_image": delivery_policy_image,
            },
        )


class ContactView(TemplateView):
    template_name = "main/contact.html"
    form_class = ContactForm
    http_method_names = ["get", "post"]

    def get(self, request):
        form = self.form_class()
        contact_emails = ContactEmail.contact_emails.list_queryset()
        contact_phones = ContactPhone.contact_phones.list_queryset()
        company_info = CompanyInfo.company_infos.detail_queryset(language=get_language())
        contact_image = SiteImage.site_images.contact_image()
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "contact_emails": contact_emails,
                "contact_phones": contact_phones,
                "company_info": company_info,
                "contact_image": contact_image,
            },
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                content = render_to_string(
                    "main/emails/contact.html",
                    {
                        "message": data["message"],
                        "name": data["name"],
                        "email": data["email"],
                    },
                    request=request,
                )

                msg = EmailMessage(
                    subject=data["subject"],
                    body=content,
                    from_email=os.environ.get("DEFAULT_FROM_EMAIL"),
                    to=[os.environ.get("SUPPORT_EMAIL_ADDRESS")],
                    reply_to={os.environ.get("SUPPORT_EMAIL_ADDRESS")},
                )
                msg.content_subtype = "html"
                msg.send()
                messages.success(request, _("Message was sent successfully!"))
                return redirect(reverse("apps.main:contact") + "#contact-form")
            except BadHeaderError:
                messages.error(request, _("Message cannot be sent!"))
        messages.error(request, _("Message cannot be sent!"))
        return render(request, self.template_name, {"form": form})


class AboutView(TemplateView):
    template_name = "main/about.html"
    http_method_names = ["get"]

    def get(self, request):
        about = SiteText.site_texts.about(language=get_language())
        about_image = SiteImage.site_images.about_image()
        return render(
            request,
            self.template_name,
            {"about": about, "about_image": about_image},
        )
