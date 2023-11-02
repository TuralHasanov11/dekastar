from typing import Any

from apps.store.forms import ProductFilterForm
from apps.store.models import Brand, Category, Product
from django.core import paginator
from django.db.models import Count
from django.views.generic import DetailView, TemplateView


class CategoryProductsView(TemplateView):
    template_name = "store/category-products.html"
    paginate_by = 1
    form_class = ProductFilterForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        form = self.form_class(self.request.GET)
        if form.is_valid():
            print(form.cleaned_data)

        context["products"] = paginator.Paginator(
            Product.products.list_queryset().all(),
            self.request.GET.get("paginate_by", self.paginate_by),
        ).get_page(self.request.GET.get("page", 1))
        context["categories"] = Category.objects.annotate(
            products_count=Count("product_category")
        ).all()
        context["brands"] = Brand.objects.annotate(
            products_count=Count("product_brand")
        ).all()
        context["all_products_count"] = sum(
            [category.products_count for category in context["categories"]]
        )
        context["in_stock_products_count"] = (
            Product.products.list_queryset().filter(in_stock=True).count()
        )
        context["filter_form"] = form
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/products/detail.html"
    context_object_name = "product"
    queryset = model.products.detail_queryset()
    related_product_count = 10

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["related_products"] = self.model.products.list_queryset().filter(
            category=self.object.category
        )[: self.related_product_count]
        return context


class FavoritesView(TemplateView):
    template_name = "store/products/favorites.html"
