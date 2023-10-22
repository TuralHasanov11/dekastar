from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class LanguageField(models.CharField):
    description = _("Language field")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = settings.LANGUAGES
        kwargs['default'] = settings.LANGUAGE_CODE
        super().__init__(*args, **kwargs)


class CreatedAtField(models.DateTimeField):
    description = _("Created at field")

    def __init__(self, *args, **kwargs):
        kwargs['auto_now_add'] = True
        super().__init__(*args, **kwargs)


class UpdatedAtField(models.DateTimeField):
    description = _("Updated at field")

    def __init__(self, *args, **kwargs):
        kwargs['auto_now'] = True
        super().__init__(*args, **kwargs)


class TextField(RichTextField):
    description = _("Text field")

    def __init__(self, *args, **kwargs):
        kwargs['null'] = True
        kwargs['blank'] = True
        super().__init__(*args, **kwargs)