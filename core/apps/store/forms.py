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

    category = forms.SlugField(required=False, initial=None)
    in_stock = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"id": "inStock"}),
        initial=False,
    )
    brand = forms.SlugField(required=False, initial=None)
    collection = forms.SlugField(required=False, initial=None)
    paginate_by = forms.ChoiceField(
        required=False,
        choices=PAGINATE_BY_CHOICES,
        widget=forms.Select(attrs={"id": "paginateByInput"}),
    )
    order_by = forms.ChoiceField(
        required=False,
        choices=ORDER_BY_CHOICES,
        widget=forms.Select(attrs={"id": "orderByInput"}),
        initial=None,
    )
    view = forms.ChoiceField(required=False, choices=VIEW_CHOICES, initial=None)
    min_price = forms.IntegerField(required=False, initial=None)
    max_price = forms.IntegerField(required=False, initial=None)
    search = forms.CharField(max_length=255, required=False, initial=None)

    class Meta:
        fields = (
            "category",
            "in_stock",
            "brand",
            "collection",
            "paginate_by",
            "order_by",
            "view",
            "min_price",
            "max_price",
            "search"
        )
