class OrderProcessor:
    def __init__(self, request) -> None:
        self.session = request.session
        self.order = self.session.get("order", {})

    @property
    def order_id(self) -> str:
        return str(self.order.get("order_id", ""))
    
    def create(self, order_id) -> None:
        self.order = {
            "order_id": order_id,
        }            
        self.session["order"] = self.order
        self.save()

    def clear(self) -> None:
        del self.order
        self.session["order"] = {}
        self.save()

    def save(self) -> None:
        self.session.modified = True
