from apps.store.favorites_processor import FavoritesProcessor


def favorites(request):
    return {"favorites": FavoritesProcessor(request)}
