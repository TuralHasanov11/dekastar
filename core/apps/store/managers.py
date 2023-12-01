# from data.managers.managers import ModelManager, QuerySet
# from django.db import models
# from django.db.models import Prefetch
# from django.utils.translation import get_language
# from django.utils.translation import gettext_lazy as _


# class ProductQuerySet(models.QuerySet):
#     def list_queryset(self):
#         return self.prefetch_related(
#             Prefetch(
#                 "collection",
#                 queryset=Collection.objects.all(),
#             ),
#         ).prefetch_related(
#             Prefetch(
#                 "product_image",
#                 queryset=ProductImage.objects.filter(is_feature=True),
#                 to_attr="image_feature",
#             ),
#         )

#     def detail_queryset(self):
#         return self.prefetch_related(
#             Prefetch(
#                 "collection",
#                 queryset=Collection.objects.all(),
#             ),
#         ).prefetch_related(
#             Prefetch(
#                 "product_image",
#                 queryset=ProductImage.objects.filter(is_feature=True),
#                 to_attr="image_feature",
#             ),
#             Prefetch("product_image", to_attr="images"),
#             Prefetch(
#                 "product_information",
#                 queryset=ProductInformation.objects.filter(language=get_language()),
#                 to_attr="information",
#             ),
#         )

#     def cart_queryset(self):
#         return (
#             self.prefetch_related(
#                 Prefetch(
#                     "product_image",
#                     queryset=ProductImage.objects.filter(is_feature=True),
#                     to_attr="image_feature",
#                 ),
#             )
#             .filter(in_stock=True, is_active=True)
#             .only("name", "slug", "discount_price", "regular_price", "in_stock", "is_active")
#         )


# class ProductAdminQuerySet(models.QuerySet):
#     def list_queryset(self):
#         return self.prefetch_related(
#             Prefetch(
#                 "collection",
#                 queryset=Collection.collections.list_queryset(),
#             ),
#         ).prefetch_related(
#             Prefetch(
#                 "product_image",
#                 queryset=ProductImage.objects.filter(is_feature=True),
#                 to_attr="image_feature",
#             ),
#         )

#     def detail_queryset(self):
#         pass


# class ProductManager(ModelManager):
#     _queryset = ProductQuerySet

#     def get_queryset(self):
#         return self._queryset(self.model, using=self._db)

#     def list_queryset(self):
#         return self.get_queryset().list_queryset()

#     def count_queryset(self):
#         return self.get_queryset().count()

#     def detail_queryset(self):
#         return self.get_queryset().detail_queryset()

#     def cart_queryset(self):
#         return self.get_queryset().cart_queryset()

#     def new_products_queryset(self):
#         return self.get_queryset().list_queryset().order_by("-created_at").all()[:6]

#     def discounted_products_queryset(self):
#         return self.get_queryset().list_queryset().filter(discount__gt=0).order_by("-updated_at")[:6]

