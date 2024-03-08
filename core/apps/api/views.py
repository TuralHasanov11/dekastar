import logging

from apps.api import pagination, serializers
from apps.main.models import (
    Banner,
    CompanyInfo,
    ContactEmail,
    ContactPhone,
    SiteImage,
    SiteText,
)
from apps.orders.cart_processor import CartProcessor
from apps.orders.models import Order
from apps.store.favorites_processor import FavoritesProcessor
from apps.store.forms import ProductFilterForm
from apps.store.models import Brand, Category, Collection, Product
from django.conf import settings
from django.db import transaction
from django.db.models import Count, OuterRef, Subquery
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.permissions import HasAPIKey

logger = logging.getLogger("main")


class FavoritesAddView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = serializers.FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            favorites = FavoritesProcessor(request)
            favorites.add(product_id=int(data.get("product_id")))
            return Response(data={"added": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoritesRemoveView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = serializers.FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            favorites = FavoritesProcessor(request)
            favorites.remove(product_id=int(data.get("product_id")))
            return Response(data={"added": False}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartAddView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = serializers.CartSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                cart = CartProcessor(request)
                product = Product.products.cart_queryset().get(id=data.get("product_id"))
                item = cart.add(product=product, quantity=data.get("product_quantity"))
                return Response(
                    data={
                        "quantity": len(cart),
                        "total_price": cart.get_total_price,
                        "item": item,
                        "total_regular_price": cart.get_total_regular_price,
                        "total_discount": cart.get_total_discount,
                    },
                    status=status.HTTP_200_OK,
                )
            except Product.DoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND, data={"message": _("Product was not found")}
                )
            except Exception as err:
                logger.error(str(err))
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={"message": str(err)})
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CartUpdateView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = serializers.CartSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                cart = CartProcessor(request)
                product = Product.products.cart_queryset().get(id=data.get("product_id"))
                item = cart.update(product=product, quantity=data.get("product_quantity"))
                return Response(
                    data={
                        "quantity": len(cart),
                        "total_price": cart.get_total_price,
                        "item": item,
                        "total_regular_price": cart.get_total_regular_price,
                        "total_discount": cart.get_total_discount,
                    },
                    status=status.HTTP_200_OK,
                )
            except Product.DoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND, data={"message": _("Product was not found")}
                )
            except Exception as err:
                logger.error(str(err))
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={"message": str(err)})
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CartRemoveView(APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = serializers.CartSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                cart = CartProcessor(request)
                cart.remove(product_id=data.get("product_id"))
                return Response(
                    data={"quantity": len(cart), "total_price": cart.get_total_price},
                    status=status.HTTP_200_OK,
                )
            except Product.DoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND, data={"message": _("Product was not found")}
                )
            except Exception as err:
                logger.error(str(err))
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data={"message": str(err)})
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CartDetailView(APIView):
    http_method_names = ["get"]

    def get(self, request):
        cart = CartProcessor(request)
        return Response(data=cart.cart)


class CategoryListView(generics.ListAPIView):
    serializer_class = serializers.CategorySerializer
    model = Category
    permission_classes = [HasAPIKey]

    def get_queryset(self):
        translation.activate(self.request.GET.get("lang", settings.LANGUAGE_CODE))
        return self.model.categories.list_queryset()


class FilterListView(APIView):
    http_method_names = ["get"]
    form_class = ProductFilterForm
    permission_classes = [HasAPIKey]

    def get(self, request):
        query_params = request.GET.copy()
        form = self.form_class(query_params)
        translation.activate(query_params.get("lang", settings.LANGUAGE_CODE))

        if not form.is_valid():
            return Response(data=form.errors, status=status.HTTP_400_BAD_REQUEST)

        data = {}
        categories = Category.categories.list_queryset()
        brands = Brand.brands.list_queryset()

        data["current_category"] = {}
        data["ancestor_categories"] = []

        if form.cleaned_data.get("category") != "":
            current_category = Category.categories.list_queryset().get(slug=query_params.get("category"))
            ancestor_categories = current_category.get_ancestors(ascending=False, include_self=True)
            ancestor_categories_serializer = serializers.CategorySerializer(ancestor_categories, many=True)
            data["ancestor_categories"] = ancestor_categories_serializer.data
            if current_category:
                brands = brands.filter(collection_brand__category=current_category)
                current_category_serializer = serializers.CategorySerializer(current_category)
                data["current_category"] = current_category_serializer.data

        collections = (
            Collection.collections.list_queryset()
            .filter(brand__in=brands)
            .annotate(
                products_count=Subquery(
                    Product.objects.values("collection_id")
                    .annotate(count=Count("id"))
                    .filter(collection_id=OuterRef("id"), is_active=True)
                    .values("count")[:1]
                )
            )
        )

        if form.cleaned_data.get("collection", None):
            collection = Collection.objects.get(slug=form.cleaned_data.get("collection"))
            data["current_brand"] = serializers.BrandSerializer(brands.get(id=collection.brand_id)).data

        category_list_serializer = serializers.CategorySerializer(categories, many=True)
        data["categories"] = category_list_serializer.data
        collection_list_serializer = serializers.CollectionSerializer(collections, many=True)
        data["collections"] = collection_list_serializer.data
        brand_list_serializer = serializers.BrandSerializer(brands, many=True)
        data["brands"] = brand_list_serializer.data
        return Response(data=data)


class ProductListView(APIView):
    serializer_class = serializers.ProductSerializer
    model = Product
    form_class = ProductFilterForm
    http_method_names = ["get"]
    permission_classes = [HasAPIKey]

    def get(self, request):
        query_params = request.GET.copy()
        form = self.form_class(query_params)
        products = Product.products
        if form.is_valid():
            data = form.cleaned_data
            if data.get("type", None) == "new":
                products = Product.products.new_products_queryset()
            elif data.get("type", None) == "discounted":
                products = Product.products.discounted_products_queryset()
            else:
                products = Product.products.filter_queryset(
                    data=form.cleaned_data, categories=Category.categories.list_queryset()
                )
        else:
            products = products.list_queryset().all()

        paginator = pagination.ProductPagination()
        serializer = serializers.ProductSerializer(paginator.paginate_queryset(products, request), many=True)

        return paginator.get_paginated_response(serializer.data)


class PrivacyPolicyView(APIView):
    http_method_names = ["get"]
    permission_classes = [HasAPIKey]

    def get(self, request):
        privacy_policy_text = SiteText.site_texts.privacy_policy(
            language=request.GET.get("lang", settings.LANGUAGE_CODE)
        )
        privacy_policy_image = SiteImage.site_images.privacy_policy_image()
        return Response(
            data={
                "privacy_policy_text": privacy_policy_text,
                "privacy_policy_image": str(privacy_policy_image),
            }
        )


class DeliveryPolicyView(APIView):
    http_method_names = ["get"]
    permission_classes = [HasAPIKey]

    def get(self, request):
        delivery_policy_text = SiteText.site_texts.delivery_policy(
            language=request.GET.get("lang", settings.LANGUAGE_CODE)
        )
        delivery_policy_image = SiteImage.site_images.delivery_policy_image()
        return Response(
            data={
                "delivery_policy_text": delivery_policy_text,
                "delivery_policy_image": str(delivery_policy_image),
            }
        )


class ContactView(APIView):
    http_method_names = ["get"]
    permission_classes = [HasAPIKey]

    def get(self, request):
        contact_emails_serializer = serializers.ContactEmailSerializer(
            ContactEmail.contact_emails.list_queryset(), many=True
        )
        contact_phones_serializer = serializers.ContactPhoneSerializer(
            ContactPhone.contact_phones.list_queryset(), many=True
        )
        company_info_serializer = serializers.CompanyInfoSerializer(
            CompanyInfo.company_infos.detail_queryset(
                language=request.GET.get("lang", settings.LANGUAGE_CODE)
            )
        )
        contact_image = SiteImage.site_images.contact_image()
        return Response(
            data={
                "contact_emails": contact_emails_serializer.data,
                "contact_phones": contact_phones_serializer.data,
                "company_info": company_info_serializer.data,
                "contact_image": str(contact_image),
            }
        )


class AboutView(APIView):
    http_method_names = ["get"]
    permission_classes = [HasAPIKey]

    def get(self, request):
        about_text = SiteText.site_texts.about(language=request.GET.get("lang", settings.LANGUAGE_CODE))
        about_image = SiteImage.site_images.about_image()
        return Response(
            data={
                "about_text": about_text,
                "about_image": str(about_image),
            }
        )


class BannerListView(generics.ListAPIView):
    permission_classes = [HasAPIKey]
    queryset = Banner.banners.list_queryset()
    serializer_class = serializers.BannerSerializer


class ProductDetailView(APIView):
    permission_classes = [HasAPIKey]
    model = Product
    serializer_class = serializers.ProductDetailSerializer
    http_method_names = ["get"]

    def get(self, request, slug):
        translation.activate(request.GET.get("lang", settings.LANGUAGE_CODE))
        try:
            product = self.model.products.detail_queryset().get(slug=slug)
            return Response(data=serializers.ProductDetailSerializer(product).data)
        except self.model.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class RelatedProductListView(generics.ListAPIView):
    permission_classes = [HasAPIKey]
    serializer_class = serializers.ProductSerializer
    model = Product

    def get_queryset(self):
        translation.activate(self.request.GET.get("lang", settings.LANGUAGE_CODE))
        product = self.model.products.get(slug=self.kwargs.get("slug"))
        return self.model.products.related_products_queryset(product=product)


class CheckoutView(APIView):
    serializer_class = serializers.CheckoutSerializer
    http_method_names = ["post"]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            data.pop("terms_agreed")
            cart = data.pop("cart")
            with transaction.atomic():
                order = Order(
                    **data,
                    total_paid=sum(item["price"] * item["quantity"] for item in cart),
                )
                order.save()
                for item in cart:
                    order.add_item(
                        item["product_id"],
                        item["product_quantity_type"],
                        item["price"],
                        item["price"] * item["quantity"],
                        item["quantity"],
                    )
                return Response(data={"order_id": str(order.uuid)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
