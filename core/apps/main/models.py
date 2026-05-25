import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_cleanup import cleanup
from shared import custom_model_fields

from apps.main import managers


@cleanup.select
class SiteText(models.Model):
    language = custom_model_fields.LanguageField()
    privacy_policy = custom_model_fields.TextField()
    delivery_policy = custom_model_fields.TextField()
    about = custom_model_fields.TextField()
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    objects = models.Manager()
    site_texts = managers.SiteTextManager()

    class Meta:
        verbose_name_plural = "Site Texts"

    def __str__(self):
        return _("Site text") + " " + self.language


@cleanup.select
class SocialMediaLink(models.Model):
    class Platforms(models.TextChoices):
        INSTAGRAM = "INSTAGRAM", _("Instagram")
        FACEBOOK = "FACEBOOK", _("Facebook")
        TWITTER = "TWITTER", _("Twitter")
        PINTEREST = "PINTEREST", _("Pinterest")
        GOOGLEPLUS = "GOOGLEPLUS", _("GooglePlus")
        TIKTOK = "TIKTOK", _("TikTok")

    platform = models.CharField(max_length=50, choices=Platforms.choices)
    link = models.URLField()

    objects = models.Manager()
    social_media_links = managers.SocialMediaLinkManager()

    class Meta:
        verbose_name_plural = _("Social Media Links")

    def __str__(self):
        return str(self.link)


@cleanup.select
class ContactEmail(models.Model):
    email = models.EmailField()

    objects = models.Manager()
    contact_emails = managers.ContactEmailManager()

    class Meta:
        verbose_name_plural = _("Contact Emails")

    def __str__(self):
        return str(self.email)


@cleanup.select
class ContactPhone(models.Model):
    phone = models.CharField(max_length=30)

    objects = models.Manager()
    contact_phones = managers.ContactPhoneManager()

    class Meta:
        verbose_name_plural = _("Contact Phones")

    def __str__(self):
        return str(self.phone)


@cleanup.select
class CompanyInfo(models.Model):
    language = custom_model_fields.LanguageField()
    address = models.TextField()
    working_hours = models.CharField(max_length=255)

    objects = models.Manager()
    company_infos = managers.CompanyInfoManager()

    def __str__(self):
        return str(self.address)


def site_image_path(instance, filename):
    return f"site/{uuid.uuid4()}.webp"


@cleanup.select
class SiteImage(models.Model):
    contact_image = custom_model_fields.WEBPField(upload_to=site_image_path, null=True, blank=True)
    about_image = custom_model_fields.WEBPField(upload_to=site_image_path, null=True, blank=True)
    privacy_policy_image = custom_model_fields.WEBPField(upload_to=site_image_path, null=True, blank=True)
    delivery_policy_image = custom_model_fields.WEBPField(upload_to=site_image_path, null=True, blank=True)

    objects = models.Manager()
    site_images = managers.SiteImageManager()

    class Meta:
        verbose_name_plural = _("Site Images")


def banner_image_path(instance, filename):
    return f"banners/{uuid.uuid4()}.webp"


@cleanup.select
class Banner(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    image = custom_model_fields.WEBPField(upload_to=banner_image_path)
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = _("Banners")

    @property
    def is_active_display(self):
        return _("Active") if self.is_active else _("Not Active")
