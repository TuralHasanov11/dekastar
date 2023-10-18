from apps.administration import views
from django.urls import path

app_name = "apps.administration"

urlpatterns = [
    path("", views.index),
]
