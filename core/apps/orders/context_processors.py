from apps.orders.cart_processor import CartProcessor


def cart(request):
    return {"cart": CartProcessor(request)}
