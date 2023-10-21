from apps.main import views
from django.urls import path

app_name = "apps.main"

urlpatterns = [
    path("", views.HomeView.as_view(), name="index"),
    path("privacy-policy", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("about", views.AboutView.as_view(), name="about"),
    path("contact", views.ContactView.as_view(), name="contact"),
]
