from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from PIL import Image
from shared import custom_model_fields


class SiteText(models.Model):
    language = custom_model_fields.LanguageField()
    privacy_policy = custom_model_fields.TextField()
    delivery_policy = custom_model_fields.TextField()
    about = custom_model_fields.TextField()
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    objects = models.Manager()

    class Meta:
        verbose_name_plural = "Site Texts"

    def __str__(self):
        return _("Site text") + " " + self.language


class SocialMediaLink(models.Model):
    class Platforms(models.TextChoices):
        INSTAGRAM = "INSTAGRAM", _("Instagram")
        FACEBOOK = "FACEBOOK", _("Facebook")
        TWITTER = "TWITTER", _("Twitter")
        PINTEREST = "PINTEREST", _("Pinterest")
        GOOGLEPLUS = "GOOGLEPLUS", _("GooglePlus")

    platform = models.CharField(max_length=50, choices=Platforms.choices)
    link = models.URLField()

    objects = models.Manager()

    class Meta:
        verbose_name_plural = _("Social Media links")

    def __str__(self):
        return self.link


class ContactEmail(models.Model):
    email = models.EmailField()

    objects = models.Manager()

    class Meta:
        verbose_name_plural = _("Contact Emails")

    def __str__(self):
        return self.email


class ContactPhone(models.Model):
    phone = models.CharField(max_length=30)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = _("Contact Phones")

    def __str__(self):
        return self.phone


class CompanyInfo(models.Model):
    language = custom_model_fields.LanguageField()
    address = models.TextField()
    working_hours = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return self.address


class SiteImage(models.Model):
    contact_image = models.ImageField(upload_to="site/", null=True, blank=True)
    about_image = models.ImageField(upload_to="site/", null=True, blank=True)
    privacy_policy_image = models.ImageField(upload_to="site/", null=True, blank=True)
    delivery_policy_image = models.ImageField(upload_to="site/", null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name_plural = _("Site Images")


def site_image_compressor(sender, **kwargs):
    with Image.open(kwargs["instance"].contact_image.path) as contact_image:
        contact_image.save(
            kwargs["instance"].contact_image.path, optimize=True, quality=15
        )
    with Image.open(kwargs["instance"].about_image.path) as about_image:
        about_image.save(kwargs["instance"].about_image.path, optimize=True, quality=15)
    with Image.open(
        kwargs["instance"].privacy_policy_image.path
    ) as privacy_policy_image:
        privacy_policy_image.save(
            kwargs["instance"].privacy_policy_image.path, optimize=True, quality=15
        )
    with Image.open(
        kwargs["instance"].delivery_policy_image.path
    ) as delivery_policy_image:
        delivery_policy_image.save(
            kwargs["instance"].delivery_policy_image.path, optimize=True, quality=15
        )


post_save.connect(site_image_compressor, sender=SiteImage)


def banner_image_path(instance, filename):
    return f"banners/{instance.id}-{filename}"


class Banner(models.Model):
    image = models.ImageField(upload_to=banner_image_path)
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = _("Banners")

    objects = models.Manager()
