from apps.main.models import SiteText
from django.contrib import admin


@admin.register(SiteText)
class SiteTextAdmin(admin.ModelAdmin):
    pass
