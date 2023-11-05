from typing import Any

from apps.store import filters
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
        query_params = self.request.GET.copy()
        query_params.update(kwargs)
        form = self.form_class(query_params)

        context["categories"] = Category.objects.add_related_count(
            Category.categories.list_queryset().all(),
            Product,
            "category",
            "products_count",
            cumulative=True,
        )

        products = Product.products.list_queryset().all()

        if form.is_valid():
            products = filters.OrderingFilter(
                filters.InStockFilter(
                    filters.BrandFilter(
                        filters.CategoryFilter(
                            filters.PriceFilter(products, form.cleaned_data).queryset,
                            form.cleaned_data,
                            context["categories"],
                        ).queryset,
                        form.cleaned_data,
                    ).queryset,
                    form.cleaned_data,
                ).queryset,
                form.cleaned_data,
            ).queryset

        context["products"] = paginator.Paginator(
            products,
            query_params.get("paginate_by", self.paginate_by),
        ).get_page(query_params.get("page", 1))

        context["brands"] = Brand.objects.annotate(
            products_count=Count("product_brand")
        ).all()
        context["all_products_count"] = Product.products.count_queryset()
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
