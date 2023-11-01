from apps.api.serializers import FavoritesSerializer
from apps.store.favorites_processor import FavoritesProcessor
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class FavoritesAddView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            favorites = FavoritesProcessor(request)
            favorites.add(productId=int(data.get('product_id')))
            return Response(data={"added": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoritesRemoveView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            favorites = FavoritesProcessor(request)
            favorites.remove(productId=int(data.get('product_id')))
            return Response(data={"added": False}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
