
from apps.store.models import Product


class FavoritesProcessor:
    favorites: list[int]
    products: list[Product]

    def __init__(self, request):
        self.session = request.session
        try:
            favorites_container: list[int] = self.session["favorites"]
            products = Product.products.list_queryset().filter(id__in=favorites_container)
        except Exception:
            self.session["favorites"] = []
            favorites_container = []

        self.favorites = []
        self.products = []
        if favorites_container:
            for product in products:
                self.favorites.append(product.id)
            self.products = products
            self.session["favorites"] = self.favorites
        self.save()

    def __iter__(self):
        for item in self.products:
            yield item

    def __len__(self):
        return len(self.favorites)

    def add(self, product_id: int):
        try:
            if product_id not in self.favorites:
                self.favorites.append(product_id)
                self.session["favorites"] = self.favorites
                self.save()
        except Exception as exception:
            raise exception

    def remove(self, product_id: int) -> None:
        try:
            if product_id in self.favorites:
                self.favorites.remove(product_id)
                self.session["favorites"] = self.favorites
                self.save()
        except Exception as exception:
            raise exception

    def clear(self) -> None:
        try:
            del self.favorites
            self.session["favorites"] = []
            self.save()
        except Exception as exception:
            raise exception

    def save(self) -> None:
        self.session.modified = True
