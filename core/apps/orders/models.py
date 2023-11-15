import uuid

from apps.store.models import Product
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Prefetch
from shared import custom_model_fields


class OrderQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.only("name", "phone", "seen", "total_paid", "created_at")
    
    def detail_queryset(self):
        return (
            self.prefetch_related(
                Prefetch(
                    "items",
                    queryset=OrderItem.objects.prefetch_related(Prefetch(
                        "product",
                        queryset=Product.admin_products.list_queryset().all(),
                    )).all(),
                ),
            )
        )


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()


class Order(models.Model):
    name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{12}$')
    phone = models.CharField(validators=[phone_regex], max_length=17)
    total_paid = models.DecimalField(max_digits=7, decimal_places=2)
    uuid = models.UUIDField(unique=True, null=True, blank=True, default=uuid.uuid4())
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    orders = OrderManager()

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.name)
    
    def mark_as_seen(self) -> None:
        self.seen = True
        self.save()
        return True


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='order_items', on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    quantity_type = models.CharField(max_length=50,
                                     choices=custom_model_fields.ProductQuantityType.choices,
                                     default=custom_model_fields.ProductQuantityType.NUMBER)
    sub_total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.sub_total)
