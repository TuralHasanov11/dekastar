from data.managers.managers import ModelManager, QuerySet


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
        return (
            self.get_queryset()
            .list_queryset()
            .filter(language=language)
            .only("language", "privacy_policy")
            .first()
        )

    def delivery_policy(self, language):
        return (
            self.get_queryset()
            .list_queryset()
            .filter(language=language)
            .only("language", "delivery_policy")
            .first()
        )

    def about(self, language):
        return self.get_queryset().list_queryset().filter(language=language).only("language", "about").first()


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


class BannerQuerySet(QuerySet):
    pass


class BannerManager(ModelManager):
    _queryset = CompanyInfoQuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset().filter(is_active=True).order_by("-id")

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()
