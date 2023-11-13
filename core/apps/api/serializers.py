from apps.store.models import Product
from rest_framework import serializers


class FavoritesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    class Meta:
        fields = ('product_id',)


class CartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_quantity = serializers.IntegerField(required=False, default=None)

    class Meta:
        fields = ('product_id', "product_quantity",)


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "slug", "discount", "discount_price",
                  "regular_price", "in_stock", "is_active", "get_image_feature")
