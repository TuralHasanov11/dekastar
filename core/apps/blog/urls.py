from django.urls import path

from apps.blog import views

app_name = "apps.blog"

urlpatterns = [
	path("", views.BlogPostListView.as_view(), name="blog-list"),
	path("<slug:slug>", views.BlogPostDetailView.as_view(), name="blog-detail"),
]