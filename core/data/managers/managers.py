from django.db import models


class QuerySet(models.QuerySet):
    def list_queryset(self):
        return self

    def detail_queryset(self):
        return self


class ModelManager(models.Manager):
    _queryset: QuerySet = QuerySet

    def get_queryset(self):
        return self._queryset(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset().all()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()

    def create_many_by_languages(self, languages):
        return self.get_queryset().bulk_create([self.model(language=lang[0]) for lang in languages])
