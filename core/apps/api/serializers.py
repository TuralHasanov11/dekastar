from rest_framework import serializers


class FavoritesSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    class Meta:
        fields = ('product_id',)
