import datetime
import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Prefetch
from django.utils.translation import gettext_lazy as _
from shared import custom_model_fields

from apps.store.models import Product


class OrderQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.only("name", "phone", "seen", "total_paid", "created_at")

    def detail_queryset(self):
        return self.prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.prefetch_related(
                    Prefetch(
                        "product",
                        queryset=Product.admin_products.list_queryset().all(),
                    )
                ).all(),
            ),
        )


class OrderManager(models.Manager):
    def get_queryset(self):
        return OrderQuerySet(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending")
        PAID = "PAID", _("Paid")
        DELIVERED = "DELIVERED", _("Delivered")
        RETURNED = "RETURNED", _("Returned")
        CANCELLED = "CANCELLED", _("Cancelled")

    name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r"^\+?1?\d{12}$")
    phone = models.CharField(validators=[phone_regex], max_length=17)
    total_paid = models.DecimalField(max_digits=7, decimal_places=2)
    uuid = models.UUIDField(unique=True, null=True, blank=True)
    seen = models.BooleanField(default=False)
    address = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    orders = OrderManager()
    objects = models.Manager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.name)

    @property
    def status_display(self):
        return self.get_status_display()

    def mark_as_seen(self) -> bool:
        self.seen = True
        self.save()
        return True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.code is None:
            self.code = (
                self.name[0].capitalize() + str(self.pk) + "-" + datetime.datetime.now().strftime("%Y%m%d")
            )
        if self.uuid is None:
            self.uuid = uuid.uuid4()
        return super().save(*args, **kwargs)

    def add_item(self, product_id, quantity_type, price, sub_total, quantity) -> None:
        Order.items.create(
            product_id=product_id,
            quantity_type=quantity_type,
            price=price,
            sub_total=sub_total,
            quantity=quantity,
        )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    quantity_type = models.CharField(
        max_length=50,
        choices=custom_model_fields.ProductQuantityType.choices,
        default=custom_model_fields.ProductQuantityType.NUMBER,
    )
    sub_total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    def __str__(self):
        return str(self.sub_total)
