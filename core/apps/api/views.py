import logging

from apps.api.serializers import CartSerializer, FavoritesSerializer
from apps.orders.cart_processor import CartProcessor
from apps.store.favorites_processor import FavoritesProcessor
from apps.store.models import Product
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger('main')


class FavoritesAddView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            favorites = FavoritesProcessor(request)
            favorites.add(product_id=int(data.get('product_id')))
            return Response(data={"added": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoritesRemoveView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = FavoritesSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            favorites = FavoritesProcessor(request)
            favorites.remove(product_id=int(data.get('product_id')))
            return Response(data={"added": False}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartAddView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                cart = CartProcessor(request)
                product = Product.products.cart_queryset().get(id=data.get("product_id"))
                item = cart.add(product=product, quantity=data.get('product_quantity', None))
                return Response(data={'quantity': len(cart), 
                                      'total_price': cart.get_total_price, 
                                      "item": item, 
                                      "total_regular_price": cart.get_total_regular_price, 
                                      "total_discount": cart.get_total_discount},
                                status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND,
                                data={"message": _("Product was not found")})
            except Exception as err:
                logger.error(str(err))
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={"message": str(err)})
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class CartRemoveView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            try:
                data = serializer.validated_data
                cart = CartProcessor(request)
                cart.remove(product_id=data.get("product_id"))
                return Response(data={'quantity': len(cart), 'total_price': cart.get_total_price},
                                status=status.HTTP_200_OK)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND,
                                data={"message": _("Product was not found")})
            except Exception as err:
                logger.error(str(err))
                return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                data={"message": str(err)})
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
