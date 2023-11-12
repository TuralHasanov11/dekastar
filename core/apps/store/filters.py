from abc import ABC

from django.db.models.query import QuerySet


class Filter(ABC):
    _queryset: QuerySet = None
    _data: dict = None

    def __init__(self, queryset: QuerySet, data: dict) -> None:
        self._queryset = queryset
        self._data = data

    @property
    def queryset(self) -> QuerySet:
        return self._queryset


class OrderingFilter(Filter):
    @property
    def queryset(self) -> QuerySet:
        if "order_by" in self._data and self._data["order_by"]:
            self._queryset = self._queryset.order_by(self._data["order_by"])
        return self._queryset


class CategoryFilter(Filter):
    def __init__(self, queryset: QuerySet, data, categories):
        super().__init__(queryset, data)
        self._categories = categories

    @property
    def queryset(self) -> QuerySet:
        if "category" in self._data and self._data.get("category"):
            current_category = next(
                filter(
                    lambda category: category.slug == self._data.get("category"),
                    self._categories,
                ),
                None,
            )
            if current_category is not None:
                filteredCategoryIds = [
                    cat.id
                    for cat in current_category.get_descendants(include_self=True)
                ]
                self._queryset = self._queryset.filter(
                    category__id__in=filteredCategoryIds
                )
        return self._queryset


class InStockFilter(Filter):
    @property
    def queryset(self) -> QuerySet:
        if "in_stock" in self._data and self._data["in_stock"] is True:
            self._queryset = self._queryset.filter(in_stock=True)
        return self._queryset


class BrandFilter(Filter):
    @property
    def queryset(self) -> QuerySet:
        if "brand" in self._data and isinstance(self._data["brand"]) is int:
            self._queryset = self._queryset.filter(brand=self._data["brand"])
        return self._queryset


class PriceFilter(Filter):
    @property
    def queryset(self) -> QuerySet:
        if (
            "min_price" in self._data
            and "max_price" in self._data
            and isinstance(self._data["min_price"]) is int
            and isinstance(self._data["max_price"]) is int
        ):
            self._queryset = self._queryset.filter(
                discount_price__lte=self._data["max_price"],
                discount_price__gte=self._data["min_price"],
            )
        elif "min_price" in self._data and isinstance(self._data["min_price"]) is int:
            self._queryset = self._queryset.filter(
                discount_price__gte=self._data["min_price"],
            )
        elif "max_price" in self._data and isinstance(self._data["max_price"]) is int:
            self._queryset = self._queryset.filter(
                discount_price__lte=self._data["max_price"],
            )
        return self._queryset
