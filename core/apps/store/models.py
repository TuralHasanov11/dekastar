from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Prefetch
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


def category_image_path(instance, filename):
    return f"categories/{instance.name}/{filename}"


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, related_name="children", null=True, blank=True
    )
    cover_image = models.ImageField(upload_to=category_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("apps.store:category-products", kwargs={"slug": self.slug})


def brand_image_path(instance, filename):
    return f"brands/{instance.slug}/{filename}"


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    cover_image = models.ImageField(upload_to=brand_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("Brands")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.select_related("category").prefetch_related(
            Prefetch(
                "product_image",
                queryset=ProductImage.objects.filter(is_feature=True),
                to_attr="image_feature",
            ),
        )

    def detail_queryset(self):
        return (
            self.select_related("category")
            .select_related("brand")
            .prefetch_related(
                Prefetch(
                    "product_image",
                    queryset=ProductImage.objects.filter(is_feature=True),
                    to_attr="image_feature",
                ),
                Prefetch("product_image", to_attr="images"),
            )
        )


class ProductAdminQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.select_related("category").prefetch_related(
            Prefetch(
                "product_image",
                queryset=ProductImage.objects.filter(is_feature=True),
                to_attr="image_feature",
            ),
        )

    def detail_queryset(self):
        pass


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db).filter(is_active=True)

    def list_queryset(self):
        return self.get_queryset().list_queryset()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()


class ProductAdminManager(models.Manager):
    def get_queryset(self):
        return ProductAdminQuerySet(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset()

    def detail_queryset(self):
        return self.get_queryset()


class Product(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    brand = models.ForeignKey(
        Brand,
        related_name="product_brand",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        related_name="product_category",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    regular_price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.IntegerField(
        default=0,
        blank=True,
        validators=[MaxValueValidator(99), MinValueValidator(0)],
        null=True,
    )
    discount_price = models.DecimalField(
        default=0, blank=True, max_digits=6, decimal_places=2
    )
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(auto_now=True)

    products = ProductManager()
    admin_products = ProductAdminManager()
    objects = models.Manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("apps.store:product-detail", kwargs={"slug": self.slug})

    @property
    def in_stock_display_value(self):
        return _("In Stock") if self.in_stock else _("Not in Stock")

    @property
    def get_image_feature(self):
        return (
            self.image_feature[0].image.url
            if hasattr(self, "image_feature")
            and len(self.image_feature) > 0
            and self.image_feature[0].image
            else ""
        )

    @property
    def is_active_display_value(self):
        return _("Active") if self.is_active else _("Not Active")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.discount is not None:
            self.discount_price = (
                self.regular_price - self.regular_price * self.discount / 100
            )
        else:
            self.discount_price = self.regular_price
        return super().save(*args, **kwargs)


def product_image_path(instance, filename):
    return f"products/{instance.product.id}/{filename}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_image"
    )
    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-is_feature",)
