import io

from ckeditor import fields as ckeditor_fields
from ckeditor_uploader import fields as ckeditor_uploader_fields
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.translation import gettext_lazy as _
from PIL import Image


class LanguageField(models.CharField):
    description = _("Language field")

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 2
        kwargs["choices"] = settings.LANGUAGES
        kwargs["default"] = settings.LANGUAGE_CODE
        super().__init__(*args, **kwargs)


class CreatedAtField(models.DateTimeField):
    description = _("Created at field")

    def __init__(self, *args, **kwargs):
        kwargs["auto_now_add"] = True
        kwargs["editable"] = (False,)
        super().__init__(*args, **kwargs)


class UpdatedAtField(models.DateTimeField):
    description = _("Updated at field")

    def __init__(self, *args, **kwargs):
        kwargs["auto_now"] = True
        super().__init__(*args, **kwargs)


class TextField(ckeditor_fields.RichTextField):
    description = _("Text field")

    def __init__(self, *args, **kwargs):
        kwargs["null"] = True
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class TextUploadingField(ckeditor_uploader_fields.RichTextUploadingField):
    def __init__(self, *args, **kwargs):
        kwargs["null"] = True
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)


class ProductQuantityType(models.TextChoices):
    SQUARE_METER = "SQUARE_METER", _("Square Meter")
    NUMBER = "NUMBER", _("Number")


class WEBPFieldFile(ImageFieldFile):
    def save(self, name, content, save=True):
        content.file.seek(0)
        image = Image.open(content.file)
        image_bytes = io.BytesIO()
        image.save(fp=image_bytes, format="WEBP")
        image_content_file = ContentFile(content=image_bytes.getvalue())
        super().save(name, image_content_file, save)


class WEBPField(models.ImageField):
    attr_class = WEBPFieldFile
