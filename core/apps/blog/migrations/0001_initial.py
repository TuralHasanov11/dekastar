# Generated manually for Blog app scaffold

import shared.custom_model_fields
from django.db import migrations, models

import apps.blog.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
                ),
                ("title", models.CharField(max_length=255, unique=True)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("summary", models.TextField(blank=True)),
                ("body", shared.custom_model_fields.TextUploadingField(blank=True, null=True)),
                (
                    "cover_image",
                    shared.custom_model_fields.WEBPField(
                        blank=True,
                        null=True,
                        upload_to=apps.blog.models.blog_post_cover_image_path,
                    ),
                ),
                ("is_published", models.BooleanField(default=False)),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", shared.custom_model_fields.CreatedAtField(auto_now_add=True)),
                ("updated_at", shared.custom_model_fields.UpdatedAtField(auto_now=True)),
            ],
            options={
                "ordering": ["-published_at", "-created_at"],
                "verbose_name_plural": "Blog Posts",
            },
        ),
    ]