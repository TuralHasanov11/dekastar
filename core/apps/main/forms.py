from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Your name"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "title": _("Please enter your full name"), "placeholder": _("Your name")}
        ),
        error_messages={"required": _("Please enter your full name")},
        required=True,
    )
    email = forms.EmailField(
        label=_("Your email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "title": _("Please enter your email address"),
                "placeholder": _("Your email"),
            }
        ),
        error_messages={"required": _("Please enter your email address")},
        required=True,
    )
    subject = forms.CharField(
        label=_("Subject"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Subject"), "title": _("Please select a subject")}
        ),
        error_messages={"required": _("Please select a subject")},
        required=True,
    )
    message = forms.CharField(
        label=_("Your message"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": _("Your message"),
                "cols": 40,
                "rows": 10,
                "title": _("Please enter your message"),
            }
        ),
        error_messages={"required": _("Please enter your message")},
        required=True,
    )
