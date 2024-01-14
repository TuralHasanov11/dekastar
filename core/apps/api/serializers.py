from apps.main.models import Banner, CompanyInfo, ContactEmail, ContactPhone, SiteText
from apps.store.models import (
    Brand,
    Category,
    Collection,
    Product,
    ProductImage,
    ProductInformation,
)
from rest_framework import serializers


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
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent", "cover_image", "category_name", "created_at", "updated_at")


class BrandSerializer(serializers.ModelSerializer):
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


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.ReadOnlyField()

    class Meta:
        model = Collection
        fields = ("id", "name", "slug", "cover_image", "products_count", "created_at", "updated_at")


class CollectionDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Collection
        fields = ("id", "name", "slug", "cover_image", "category", "brand", "created_at", "updated_at")


class ProductSerializer(serializers.ModelSerializer):
    is_active_display_value = serializers.ReadOnlyField()
    in_stock_display_value = serializers.ReadOnlyField()

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
            "get_image_feature",
            "is_active_display_value",
            "in_stock_display_value",
            "created_at",
            "updated_at",
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
    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_feature")


class ProductInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInformation
        fields = ("id", "language", "text")


class ProductDetailSerializer(serializers.ModelSerializer):
    in_stock_display_value = serializers.ReadOnlyField()
    collection = CollectionDetailSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    information = ProductInformationSerializer()

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
            "get_image_feature",
            "in_stock_display_value",
            "collection",
            "images",
            "information",
            "created_at",
            "updated_at",
        )
