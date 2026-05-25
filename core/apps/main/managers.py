from data.managers.managers import ModelManager, QuerySet

from apps.api import utils


class SiteTextQuerySet(QuerySet):
    pass


class SiteTextManager(ModelManager):
    _queryset = SiteTextQuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()

    def privacy_policy(self, language):
        return getattr(
            self.get_queryset()
            .list_queryset()
            .filter(language=language)
            .only("language", "privacy_policy")
            .first(),
            "privacy_policy",
            "",
        )

    def delivery_policy(self, language):
        return getattr(
            self.get_queryset()
            .list_queryset()
            .filter(language=language)
            .only("language", "delivery_policy")
            .first(),
            "delivery_policy",
            "",
        )

    def about(self, language):
        return getattr(
            self.get_queryset().list_queryset().filter(language=language).only("language", "about").first(),
            "about",
            "",
        )


class SocialMediaLinkQuerySet(QuerySet):
    pass


class SocialMediaLinkManager(ModelManager):
    _queryset = SocialMediaLinkQuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)


class ContactEmailQuerySet(QuerySet):
    pass


class ContactEmailManager(ModelManager):
    _queryset = ContactEmailQuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)


class ContactPhoneQuerySet(QuerySet):
    pass


class ContactPhoneManager(ModelManager):
    _queryset = ContactPhoneQuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)


class CompanyInfoQuerySet(QuerySet):
    pass


class CompanyInfoManager(ModelManager):
    _queryset = CompanyInfoQuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)

    def detail_queryset(self, language):
        return self.get_queryset().filter(language=language).first()


class SiteImageQuerySet(QuerySet):
    pass


class SiteImageManager(ModelManager):
    _queryset = SiteImageQuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset()

    def detail_queryset(self):
        return self.get_queryset()

    def privacy_policy_image(self):
        image = getattr(
            self.get_queryset().detail_queryset().only("privacy_policy_image").first(),
            "privacy_policy_image",
            "",
        )
        return utils.get_image_absolute_path(image.url) if image else ""

    def delivery_policy_image(self):
        image = getattr(
            self.get_queryset().detail_queryset().only("delivery_policy_image").first(),
            "delivery_policy_image",
            "",
        )
        return utils.get_image_absolute_path(image.url) if image else ""

    def about_image(self):
        image = getattr(self.get_queryset().detail_queryset().only("about_image").first(), "about_image", "")
        return utils.get_image_absolute_path(image.url) if image else ""

    def contact_image(self):
        image = getattr(
            self.get_queryset().detail_queryset().only("contact_image").first(), "contact_image", ""
        )
        return utils.get_image_absolute_path(image.url) if image else ""
