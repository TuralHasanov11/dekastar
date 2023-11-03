from django import forms
from django.utils.translation import gettext_lazy as _


class ProductFilterForm(forms.Form):
    PAGINATE_BY_CHOICES = [
        ("10", "10"),
        ("20", "20"),
        ("30", "30"),
        ("", _("All")),
    ]

    ORDER_BY_CHOICES = [
        ("name", _("Name")),
        ("discount_price", _("Price") + " : " + _("lowest")),
        ("-discount_price", _("Price") + " : " + _("highest")),
    ]

    VIEW_CHOICES = [
        ("grid", _("Grid")),
        ("list", _("List")),
    ]

    category = forms.IntegerField(required=False)
    in_stock = forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={"id": "inStock"}), initial=0
    )
    brand = forms.IntegerField(required=False)
    paginate_by = forms.ChoiceField(
        required=False,
        choices=PAGINATE_BY_CHOICES,
        widget=forms.Select(attrs={"id": "paginateByInput"}),
    )
    order_by = forms.ChoiceField(
        required=False,
        choices=ORDER_BY_CHOICES,
        widget=forms.Select(attrs={"id": "orderByInput"}),
    )
    view = forms.ChoiceField(
        required=False,
        choices=VIEW_CHOICES,
    )

    class Meta:
        fields = ("category", "in_stock", "brand", "paginate_by", "order_by", "view")
