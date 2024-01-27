from django.conf import settings


def get_image_absolute_path(image_url: str) -> str:
    return settings.SITE_URL + image_url