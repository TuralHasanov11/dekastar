from apps.administration import views
from django.urls import path

app_name = "apps.administration"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="index"),
    path("privacy-policy", views.PrivacyPolicyView.as_view(), name="privacy-policy"),
    path("about", views.AboutView.as_view(), name="about"),
    path("contact", views.ContactView.as_view(), name="contact"),
]
