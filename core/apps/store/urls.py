from apps.store import views
from django.urls import path

app_name = "apps.store"

urlpatterns = [
    path("", views.index),
]
