from apps.main.models import (CompanyInfo, ContactEmail, ContactPhone,
                              SiteImage, SiteText, SocialMediaLink)
from django.contrib import admin


@admin.register(SiteText)
class SiteTextAdmin(admin.ModelAdmin):
    pass


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactEmail)
class ContactEmailAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactPhone)
class ContactPhoneAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteImage)
class SiteImageAdmin(admin.ModelAdmin):
    pass
