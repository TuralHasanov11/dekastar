from django.views.generic import DetailView, ListView

from apps.blog.models import BlogPost


class BlogPostListView(ListView):
	model = BlogPost
	template_name = "blog/index.html"
	context_object_name = "blog_posts"
	queryset = BlogPost.objects.filter(is_published=True).order_by("-published_at", "-created_at")


class BlogPostDetailView(DetailView):
	model = BlogPost
	template_name = "blog/detail.html"
	context_object_name = "blog_post"
	queryset = BlogPost.objects.filter(is_published=True)
