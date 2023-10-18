from apps.main import views
from django.urls import path

app_name = "apps.main"

urlpatterns = [
    path("", views.index),
]
