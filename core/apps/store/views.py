from typing import Any

from apps.store.forms import ProductFilterForm
from apps.store.models import Brand, Category, Collection, Product
from data import pagination
from django.db.models import Count, OuterRef, Subquery
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView


class CategoryProductsView(TemplateView):
    template_name = "store/category-products.html"
    paginate_by = 10
    form_class = ProductFilterForm

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        query_params = self.request.GET.copy()
        query_params.update(kwargs)
        form = self.form_class(query_params)

        context["categories"] = Category.objects.all()

        if form.is_valid():
            products = Product.products.filter_queryset(
                data=form.cleaned_data, categories=context["categories"]
            )
        else:
            products = Product.products.list_queryset().all()

        context["products"] = pagination.Pagination.paginate_queryset(
            queryset=products,
            page=query_params.get("page"),
            page_size=query_params.get("paginate_by", self.paginate_by),
        )

        context["breadcrumb"] = [
            {"route": reverse("apps.main:index"), "title": _("Home")},
            {"route": reverse("apps.store:category-products"), "title": _("Products")},
        ]

        if kwargs.get("category", None) is not None:
            current_category = Category.categories.list_queryset().get(slug=kwargs.get("category"))
            ancestor_categories = current_category.get_ancestors(ascending=False, include_self=True)
            context["current_category"] = current_category
            if ancestor_categories and len(ancestor_categories) > 0:
                context["breadcrumb"] += [
                    {
                        "route": reverse(
                            "apps.store:category-products",
                            kwargs={"category": category.slug},
                        ),
                        "title": category,
                    }
                    for category in ancestor_categories
                ]

        context["brands"] = Brand.brands.list_queryset()

        if "current_category" in context:
            context["brands"] = context["brands"].filter(
                collection_brand__category=context["current_category"]
            )

        context["collections"] = (
            Collection.collections.list_queryset()
            .filter(brand__in=context["brands"])
            .annotate(
                products_count=Subquery(
                    Product.objects.values("collection_id")
                    .annotate(count=Count("id"))
                    .filter(collection_id=OuterRef("id"), is_active=True)
                    .values("count")[:1]
                )
            )
        )

        context["all_products_count"] = products.count()
        context["in_stock_products_count"] = Product.products.in_stock_count(products)
        context["filter_form"] = form

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/products/detail.html"
    context_object_name = "product"
    queryset = model.products.detail_queryset()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["related_products"] = self.model.products.related_products_queryset(product=self.get_object())
        context["breadcrumb"] = [
            {"route": reverse("apps.main:index"), "title": _("Home")},
            {"route": reverse("apps.store:category-products"), "title": _("Products")},
        ]

        if getattr(self.get_object(), "collection"):
            ancestor_categories = Category.categories.ancestors_queryset(
                self.get_object().collection.category
            )

            if ancestor_categories and len(ancestor_categories) > 0:
                context["breadcrumb"] += [
                    {
                        "route": reverse(
                            "apps.store:category-products",
                            kwargs={"category": category.slug},
                        ),
                        "title": category.category_name,
                    }
                    for category in ancestor_categories
                ]

            context["breadcrumb"] += [
                {
                    "route": reverse(
                        "apps.store:category-products",
                        kwargs={
                            "category": self.get_object().collection.category.slug,
                        },
                    )
                    + f"?collection={self.get_object().collection.slug}",
                    "title": self.get_object().collection.name,
                },
            ]

        context["breadcrumb"] += [
            {
                "route": self.request.path,
                "title": self.get_object().name,
            },
        ]
        return context


class FavoritesView(TemplateView):
    template_name = "store/products/favorites.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["breadcrumb"] = [
            {"route": reverse("apps.main:index"), "title": _("Home")},
            {"route": reverse("apps.store:favorites"), "title": _("Favorites")},
        ]
        return context
