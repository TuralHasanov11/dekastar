# from django.http import HttpRequest
from apps.main.forms import ContactForm
from apps.main.models import CompanyInfo, ContactEmail, ContactPhone, SiteText
from django.contrib import messages
from django.core.mail import BadHeaderError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "main/index.html"
    http_method_names = ['get']


class PrivacyPolicyView(TemplateView):
    template_name = "main/privacy-policy.html"
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        site_text = SiteText.objects.filter(language=get_language()).only(
            'language', 'privacy_policy').first()
        return render(request, self.template_name, {'privacy_policy': site_text.privacy_policy})


class DeliveryPolicyView(TemplateView):
    template_name = "main/delivery-policy.html"
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        site_text = SiteText.objects.filter(language=get_language()).only(
            'language', 'delivery_policy').first()
        return render(request, self.template_name, {'delivery_policy': site_text.delivery_policy})


class ContactView(TemplateView):
    template_name = "main/contact.html"
    form_class = ContactForm
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        contact_emails = ContactEmail.objects.all()
        contact_phones = ContactPhone.objects.all()
        company_info = CompanyInfo.objects.filter(
            language=get_language()).first()
        return render(request, self.template_name, {
            "form": form,
            "contact_emails": contact_emails,
            "contact_phones": contact_phones,
            "company_info": company_info
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # data = form.cleaned_data
            try:
                # content = render_to_string("main/emails/contact.html", {
                #     'message': data["message"],
                #     'name': data["name"],
                #     'email': data["email"],
                # }, request=request)

                # msg = EmailMessage(
                #     subject=data["subject"],
                #     body=content,
                #     from_email=os.environ.get("DEFAULT_FROM_EMAIL"),
                #     to=[os.environ.get("SUPPORT_EMAIL_ADDRESS")],
                #     reply_to={os.environ.get("SUPPORT_EMAIL_ADDRESS")}
                # )
                # msg.content_subtype = "html"
                # msg.send()
                messages.success(request, _('Message was sent successfully!'))
                return redirect(reverse("apps.main:contact")+"#contact-form")
            except BadHeaderError:
                messages.error(request, _("Message cannot be sent!"))
        messages.error(request, _("Message cannot be sent!"))
        return render(request, self.template_name, {"form": form})


class AboutView(TemplateView):
    template_name = "main/about.html"
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        site_text = SiteText.objects.filter(language=get_language()).only(
            'language', 'about').first()
        return render(request, self.template_name, {'about': site_text.about})
