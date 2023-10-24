from django.db import models
from django.utils.translation import gettext_lazy as _
from shared import custom_model_fields


class SiteText(models.Model):
    language = custom_model_fields.LanguageField()
    privacy_policy = custom_model_fields.TextField()
    delivery_policy = custom_model_fields.TextField()
    about = custom_model_fields.TextField()
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    class Meta:
        verbose_name_plural = "Site Texts"

    def __str__(self):
        return _("Site text") + " " + self.language


class SocialMediaLink(models.Model):
    class Platforms(models.TextChoices):
        INSTAGRAM = "INSTAGRAM", _("Instagram")
        FACEBOOK = "FACEBOOK", _("Facebook")

    platform = models.CharField(max_length=50, choices=Platforms.choices)
    link = models.URLField()

    class Meta:
        verbose_name_plural = _("Social Media links")

    def __str__(self):
        return self.link


class ContactEmail(models.Model):
    email = models.EmailField()

    class Meta:
        verbose_name_plural = _("Contact Emails")

    def __str__(self):
        return self.email


class ContactPhone(models.Model):
    phone = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = _("Contact Phones")

    def __str__(self):
        return self.phone


class CompanyInfo(models.Model):
    language = custom_model_fields.LanguageField()
    address = models.TextField()
    working_hours = models.CharField(max_length=255)

    def __str__(self):
        return self.address
