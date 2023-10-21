import os

from django.conf import settings


def config(request):
    return {
        "config": {
            "app": {
                "name": os.environ.get("APP_NAME", ""),
                "debug": settings.DEBUG
            },
        }
    }
