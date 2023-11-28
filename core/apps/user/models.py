from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(superuser=False, is_staff=False)


class User(BaseUserManager):
    objects = UserManager()

    class Meta:
        proxy = True
