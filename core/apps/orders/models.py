import uuid

from apps.store.models import Product
from django.core.validators import RegexValidator
from django.db import models
from shared import custom_model_fields


class Order(models.Model):
    name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{12}$')
    phone = models.CharField(validators=[phone_regex], max_length=17)
    total_paid = models.DecimalField(max_digits=7, decimal_places=2)
    uuid = models.UUIDField(unique=True, null=True, blank=True, default=uuid.uuid4())
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return str(self.name)


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
