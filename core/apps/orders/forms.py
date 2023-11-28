from apps.orders.models import Order
from django import forms
from django.utils.translation import gettext_lazy as _


class CheckoutForm(forms.Form):
    name = forms.CharField(
        label=_("Your name"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "title": _("Please enter your full name"),
                "placeholder": _("Your name"),
            }
        ),
        error_messages={"required": _("Please enter your full name")},
        required=True,
    )
    phone = forms.CharField(
        label=_("Phone"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "title": _("Please enter your phone"), "placeholder": _("Phone")}
        ),
        error_messages={"required": _("Please enter your phone")},
        required=True,
        help_text=_("+994xxxxxxxxx"),
    )
    address = forms.CharField(
        label=_("Your address"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "title": _("Please enter your address"),
                "placeholder": _("Your address"),
            }
        ),
        error_messages={"required": _("Please enter your address")},
    )
    terms_agreed = forms.BooleanField(widget=forms.CheckboxInput(attrs={"id": "termsAgreed"}), required=True)

    class Meta:
        model = Order
        fields = ("name", "phone", "terms_agreed", "address")
