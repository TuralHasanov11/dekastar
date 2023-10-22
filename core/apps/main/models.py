from django.db import models
from django.utils.translation import gettext_lazy as _
from shared import custom_model_fields


class SiteText(models.Model):
    language = custom_model_fields.LanguageField()
    privacy_policy = custom_model_fields.TextField()
    about = custom_model_fields.TextField()
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    class Meta:
        verbose_name_plural = "Site Texts"

    def __str__(self):
        return _("Site text") + " " + self.language
