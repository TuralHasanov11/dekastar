from ckeditor.widgets import CKEditorWidget
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class LanguageField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['label'] = _("Language")
        kwargs['choices'] = settings.LANGUAGES
        kwargs['widget'] = forms.Select(
            attrs={"class": "form-select form-select-sm", 'readonly': True,
                   'title': _('Please select language')})
        kwargs['disabled'] = True
        super().__init__(*args, **kwargs)


class TextField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = CKEditorWidget()
        kwargs['required'] = True
        super().__init__(*args, **kwargs)
