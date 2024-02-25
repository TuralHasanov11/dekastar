from __future__ import annotations

from apps.api import utils
from apps.main.models import Banner, CompanyInfo, ContactEmail, ContactPhone, SiteText
from apps.orders.models import Order
from apps.store.models import (
    Brand,
    Category,
    Collection,
    Product,
    ProductImage,
    ProductInformation,
)
from rest_framework import serializers
from shared import custom_model_fields


class FavoritesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    class Meta:
        fields = ("product_id",)


class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_quantity = serializers.IntegerField(required=False, default=1)

    class Meta:
        fields = (
            "product_id",
            "product_quantity",
        )


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "discount",
            "discount_price",
            "regular_price",
            "in_stock",
            "is_active",
            "get_image_feature",
            "quantity_type",
        )


class CategorySerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent", "cover_image", "category_name", "created_at", "updated_at")

    def get_cover_image(self, obj):
        return utils.get_image_absolute_path(obj.cover_image.url) if hasattr(obj.cover_image, "url") else ""


class BrandSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "slug",
            "cover_image",
            "created_at",
            "updated_at",
        )

    def get_cover_image(self, obj):
        return utils.get_image_absolute_path(obj.cover_image.url) if hasattr(obj.cover_image, "url") else ""


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.ReadOnlyField()
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ("id", "name", "slug", "cover_image", "products_count", "created_at", "updated_at")

    def get_cover_image(self, obj):
        return utils.get_image_absolute_path(obj.cover_image.url) if hasattr(obj.cover_image, "url") else ""


class CollectionDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Collection
        fields = ("id", "name", "slug", "cover_image", "category", "brand", "created_at", "updated_at")

    def get_cover_image(self, obj):
        return utils.get_image_absolute_path(obj.cover_image.url) if hasattr(obj.cover_image, "url") else ""


class ProductSerializer(serializers.ModelSerializer):
    is_active_display_value = serializers.ReadOnlyField()
    in_stock_display_value = serializers.ReadOnlyField()
    collection = CollectionSerializer(read_only=True)
    image_feature_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "regular_price",
            "discount",
            "discount_price",
            "in_stock",
            "is_active_display_value",
            "in_stock_display_value",
            "image_feature_url",
            "collection",
            "created_at",
            "updated_at",
        )

    def get_image_feature_url(self, obj):
        return (
            utils.get_image_absolute_path(obj.get_image_feature) if hasattr(obj, "get_image_feature") else ""
        )


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteText
        fields = ("id", "language", "privacy_policy")


class DeliveryPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteText
        fields = ("id", "language", "delivery_policy")


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteText
        fields = ("id", "language", "about")


class ContactEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactEmail
        fields = "__all__"


class ContactPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPhone
        fields = "__all__"


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = "__all__"


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_feature")

    def get_image(self, obj):
        return utils.get_image_absolute_path(obj.image.url) if hasattr(obj.image, "url") else ""


class ProductInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInformation
        fields = ("id", "language", "text")


class ProductDetailSerializer(serializers.ModelSerializer):
    in_stock_display_value = serializers.ReadOnlyField()
    collection = CollectionDetailSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    information_text = serializers.SerializerMethodField()
    image_feature_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "regular_price",
            "discount",
            "discount_price",
            "in_stock",
            "in_stock_display_value",
            "collection",
            "images",
            "information_text",
            "image_feature_url",
            "created_at",
            "updated_at",
        )

    def get_image_feature_url(self, obj):
        return (
            utils.get_image_absolute_path(obj.get_image_feature) if hasattr(obj, "get_image_feature") else ""
        )

    def get_information_text(self, obj):
        return obj.get_information


class CheckoutItemSerializer(serializers.Serializer):
    price = serializers.DecimalField(required=True, max_digits=6, decimal_places=2)
    quantity = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)
    product_quantity_type = serializers.ChoiceField(
        required=True,
        initial=custom_model_fields.ProductQuantityType.NUMBER,
        choices=custom_model_fields.ProductQuantityType.choices
    )

    class Meta:
        fields = ("price", "quantity", "product_id", "product_quantity_type")


class CheckoutSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    terms_agreed = serializers.BooleanField(required=True)
    cart = CheckoutItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = ("name", "phone", "terms_agreed", "address")
