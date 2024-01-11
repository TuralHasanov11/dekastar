from decimal import Decimal

from apps.api.serializers import CartProductSerializer
from apps.store.models import Product


class CartProcessor:
    def __init__(self, request):
        self.session = request.session
        try:
            cart_container = self.session["cart"]
            products = Product.products.list_queryset().filter(
                id__in=[key for key in cart_container.keys()], in_stock=True
            )
        except Exception:
            self.session["cart"] = {}
            cart_container = {}

        self.cart = {}
        self.products = []
        if cart_container:
            for product in products:
                self.cart[str(product.id)] = {
                    "price": str(product.discount_price),
                    "quantity": next(
                        cart_container[key]["quantity"]
                        for key in cart_container.keys()
                        if int(key) == product.id
                    ),
                    "product": CartProductSerializer(product).data,
                }
            self.products = products
            self.session["cart"] = self.cart
        self.save()

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            item["total_price"] = str(Decimal(item["price"]) * item["quantity"])
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    @property
    def get_total_price(self) -> Decimal:
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    @property
    def get_total_regular_price(self) -> Decimal:
        return sum(
            Decimal(item["product"]["regular_price"]) * item["quantity"] for item in self.cart.values()
        )

    @property
    def get_total_discount(self) -> Decimal:
        return (self.get_total_regular_price - self.get_total_price) * (-1)

    def add(self, product: Product, quantity: int = None):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += quantity
        else:
            self.cart[product_id] = {"price": str(product.discount_price), "quantity": quantity}

        self.cart[product_id]["product"] = CartProductSerializer(product).data
        self.session["cart"] = self.cart
        self.save()
        return self.cart[product_id]

    def update(self, product: Product, quantity: int):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]["quantity"] = quantity

        if self.cart[product_id]["quantity"] < 1:
            self.cart.pop(product_id)
            return None

        self.cart[product_id]["product"] = CartProductSerializer(product).data
        self.session["cart"] = self.cart
        self.save()
        return self.cart[product_id]

    def remove(self, product_id: int) -> None:
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session["cart"] = self.cart
            self.save()

    def clear(self) -> None:
        del self.cart
        self.session["cart"] = {}
        self.save()

    def save(self) -> None:
        self.session.modified = True
