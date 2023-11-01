from typing import Any

from apps.store.favorites_processor import FavoritesProcessor
from apps.store.models import Product
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView


def index(request: HttpRequest):
    return render(request, "apps/store/index.html")


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/products/detail.html'
    context_object_name = 'product'
    queryset = model.products.detail_queryset()
    related_product_count = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["related_products"] = self.model.products.list_queryset().filter(
            category=self.object.category)[:self.related_product_count]
        return context


class FavoritesView(TemplateView):
    template_name = 'store/products/favorites.html'
