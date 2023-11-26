from apps.main import views
from django.urls import path
from django.utils.translation import gettext_lazy as _

app_name = "apps.main"

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path(_("privacy-policy"), views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path(_("delivery-policy"), views.DeliveryPolicyView.as_view(), name="delivery-policy"),
    path(_("about"), views.AboutView.as_view(), name="about"),
    path(_("contact"), views.ContactView.as_view(), name="contact"),
]
