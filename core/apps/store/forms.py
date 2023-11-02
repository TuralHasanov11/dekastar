from django import forms


class ProductFilterForm(forms.Form):
    category = forms.IntegerField(required=False)
    in_stock = forms.IntegerField(required=False, initial=0)
    brand = forms.IntegerField(required=False)

    class Meta:
        fields = ("category", "in_stock", "brand")
