from typing import Dict

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _

sitemaps: Dict = {}


urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("logs/", include("log_viewer.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("api/", include("apps.api.urls", namespace="apps.api")),
]

urlpatterns += i18n_patterns(
    path("", include("apps.main.urls", namespace="apps.main")),
    path(_("store/"), include("apps.store.urls", namespace="apps.store")),
    path(_("orders/"), include("apps.orders.urls", namespace="apps.orders")),
    path("admin/", include("apps.administration.urls", namespace="apps.administration")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(r"^languages/", include("rosetta.urls")),
        path('api-auth/', include('rest_framework.urls'))
    ]
