from typing import Any

from apps.store.forms import ProductFilterForm
from apps.store.models import Brand, Category, Collection, Product
from data import pagination
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView


class CategoryProductsView(TemplateView):
    template_name = "store/category-products.html"
    paginate_by = 10
    form_class = ProductFilterForm
    __breadcrumb = [
        {"route": reverse_lazy("apps.main:index"), "title": _("Home")},
        {"route": reverse_lazy("apps.store:category-products"), "title": _("Products")},
    ]

    def __add_categories_to_breadcrumb(self, categories):
        self.__breadcrumb += [
            {
                "route": reverse(
                    "apps.store:category-products",
                    kwargs={"category": category.slug},
                ),
                "title": category,
            }
            for category in categories
        ]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.update(kwargs)
        form = self.form_class(query_params)

        categories = Category.objects.all()
        brands = Brand.brands.list_queryset()

        if form.is_valid():
            products = Product.products.filter_queryset(
                data=form.cleaned_data, categories=categories
            )

            context["products"] = pagination.Pagination.paginate_queryset(
                queryset=products,
                page=query_params.get("page"),
                page_size=query_params.get("paginate_by", self.paginate_by),
            )

            if form.cleaned_data.get("category", None):
                current_category = Category.categories.list_queryset().get(slug=kwargs.get("category"))
                ancestor_categories = current_category.get_ancestors(ascending=False, include_self=True)
                context["current_category"] = current_category
                if ancestor_categories:
                    self.__add_categories_to_breadcrumb(ancestor_categories)

                brands = brands.filter(collection_brand__category=current_category).distinct()

            # collections = (
            #     Collection.collections.list_queryset()
            #     .filter(brand__in=brands)
            #     .annotate(
            #         products_count=Subquery(
            #             Product.objects.values("collection_id")
            #             .annotate(count=Count("id"))
            #             .filter(collection_id=OuterRef("id"), is_active=True)
            #             .values("count")[:1]
            #         )
            #     )
            # )

            collections = (
                Collection.collections.list_queryset()
                .filter(brand__in=brands)
                .annotate(
                    products_count=Count("product_collection")
                )
            )

            if form.cleaned_data.get("collection", None):
                form.data["brand"] = brands.get(
                    id=Collection.objects.get(slug=query_params.get("collection")).brand_id
                ).slug

            context["brands"] = brands
            context["collections"] = collections
            context["categories"] = categories
            context["all_products_count"] = products.count()
            context["in_stock_products_count"] = Product.products.in_stock_count(products)
            context["filter_form"] = form
            context["breadcrumb"] = self.__breadcrumb

            return context

        return redirect("apps.store:category-products")


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/products/detail.html"
    context_object_name = "product"
    queryset = model.products.detail_queryset()
    __breadcrumb = [
        {"route": reverse_lazy("apps.main:index"), "title": _("Home")},
        {"route": reverse_lazy("apps.store:category-products"), "title": _("Products")},
    ]

    def __add_categories_to_breadcrumb(self, categories):
        self.__breadcrumb += [
            {
                "route": reverse(
                    "apps.store:category-products",
                    kwargs={"category": category.slug},
                ),
                "title": category.category_name,
            }
            for category in categories
        ]

    def __add_collection_to_breadcrumb(self, collection):
        self.__breadcrumb += [
            {
                "route": reverse(
                    "apps.store:category-products",
                    kwargs={
                        "category": collection.category.slug,
                    },
                )
                + f"?collection={collection.slug}",
                "title": collection.name,
            },
        ]

    def __add_product_to_breadcrumb(self, product):
        self.__breadcrumb += [
            {
                "route": self.request.path,
                "title": product.name,
            },
        ]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if getattr(self.get_object(), "collection"):
            ancestor_categories = Category.categories.ancestors_queryset(
                self.get_object().collection.category
            )

            if ancestor_categories:
                self.__add_categories_to_breadcrumb(ancestor_categories)

            self.__add_collection_to_breadcrumb(self.get_object().collection)

        self.__add_product_to_breadcrumb(self.get_object())

        context["related_products"] = self.model.products.related_products_queryset(product=self.get_object())
        context["breadcrumb"] = self.__breadcrumb
        return context


class FavoritesView(TemplateView):
    template_name = "store/products/favorites.html"
    __breadcrumb = [
        {"route": reverse_lazy("apps.main:index"), "title": _("Home")},
        {"route": reverse_lazy("apps.store:favorites"), "title": _("Favorites")},
    ]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = self.__breadcrumb
        return context
