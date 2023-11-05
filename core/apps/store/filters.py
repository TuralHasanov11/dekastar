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
        if "order_by" in self._data:
            self._queryset = self._queryset.order_by(self._data["order_by"])
        return self._queryset


class CategoryFilter(Filter):
    @property
    def queryset(self) -> QuerySet:
        if "category" in self._data and type(self._data["category"]) is int:
            self._queryset = self._queryset.filter(category=self._data["category"])
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
        if "brand" in self._data and type(self._data["brand"]) is int:
            self._queryset = self._queryset.filter(brand=self._data["brand"])
        return self._queryset
