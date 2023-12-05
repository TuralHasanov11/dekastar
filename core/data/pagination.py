from django.core import paginator
from django.db.models import QuerySet


class Pagination:
    @staticmethod
    def paginate_queryset(queryset: QuerySet, page: int, page_size: int = 1):
        return paginator.Paginator(
            queryset,
            page_size,
        ).get_page(page)
