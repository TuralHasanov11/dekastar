import uuid

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_cleanup import cleanup
from shared import custom_model_fields


def blog_post_cover_image_path(instance, filename):
    return f"blog-posts/{uuid.uuid4()}.webp"


@cleanup.select
class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    summary = models.TextField(blank=True)
    body = custom_model_fields.TextUploadingField()
    cover_image = custom_model_fields.WEBPField(upload_to=blog_post_cover_image_path, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    class Meta:
        ordering = ["-published_at", "-created_at"]
        verbose_name_plural = _("Blog Posts")

    def __str__(self):
        return str(self.title)

    @property
    def status_display(self):
        return _("Published") if self.is_published else _("Draft")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
        if not self.is_published:
            self.published_at = None
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("apps.blog:blog-detail", kwargs={"slug": self.slug})