
from apps.store.models import Product
from django.utils.translation import gettext_lazy as _


class FavoritesProcessor:
    favorites: list[int]
    products: list[Product]

    def __init__(self, request):
        self.session = request.session
        try:
            favoritesContainer: list[int] = self.session["favorites"]
            products = Product.products.list_queryset().filter(id__in=[key for key in favoritesContainer])
        except Exception:
            self.session["favorites"] = []
            favoritesContainer = []

        self.favorites = []
        self.products = []
        if favoritesContainer:
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

    def add(self, productId: int):
        try:
            if productId not in self.favorites:
                self.favorites.append(productId)
                self.session["favorites"] = self.favorites
                self.save()
        except Exception:
            raise Exception(_("Product cannot be added to Favorites"))

    def remove(self, productId: int) -> None:
        try:
            if productId in self.favorites:
                self.favorites.remove(productId)
                self.session["favorites"] = self.favorites
                self.save()
        except Exception:
            raise Exception(_("Product is not removed from Favorites"))

    def clear(self) -> None:
        try:
            del self.favorites
            self.session["favorites"] = []
            self.save()
        except Exception:
            raise Exception(_("Favorites cannot be cleared"))

    def save(self) -> None:
        self.session.modified = True
