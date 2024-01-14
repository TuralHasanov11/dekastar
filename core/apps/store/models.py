from apps.store import filters
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, Prefetch
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django_cleanup import cleanup
from mptt.models import MPTTModel, TreeForeignKey, TreeManager
from PIL import Image
from shared import custom_model_fields


class CategoryQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.prefetch_related(
            Prefetch(
                "category_attribute",
                queryset=CategoryAttribute.objects.filter(language=get_language()),
                to_attr="attribute",
            ),
        )

    def detail_queryset(self):
        return self.prefetch_related(
            Prefetch(
                "category_attribute",
                queryset=CategoryAttribute.objects.filter(language=get_language()),
                to_attr="attribute",
            ),
        )


class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset().all()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()

    def ancestors_queryset(self, category):
        return category.get_ancestors(ascending=False, include_self=True)


class CategoryAdminQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.prefetch_related(
            Prefetch(
                "category_attribute",
                queryset=CategoryAttribute.objects.filter(language=get_language()),
                to_attr="attribute",
            ),
        )

    def detail_queryset(self):
        return self.prefetch_related(
            Prefetch(
                "category_attribute",
                queryset=CategoryAttribute.objects.filter(language=get_language()),
                to_attr="attribute",
            ),
        )


class CategoryAdminManager(models.Manager):
    def get_queryset(self):
        return CategoryAdminQuerySet(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset().annotate(product_count=Count("collection_category")).all()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()


def category_image_path(instance, filename):
    return f"categories/{instance.name}/{filename}"


class CategoryTreeManager(TreeManager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db).prefetch_related(
            Prefetch(
                "category_attribute",
                queryset=CategoryAttribute.objects.filter(language=get_language()),
                to_attr="attribute",
            ),
        )


class Category(MPTTModel):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.PROTECT, related_name="children", null=True, blank=True)
    cover_image = models.ImageField(upload_to=category_image_path)
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    categories = CategoryManager()
    admin_categories = CategoryAdminManager()
    manager = CategoryTreeManager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("Categories")

    @property
    def category_name(self) -> str:
        return (
            self.attribute[0].name
            if hasattr(self, "attribute") and len(self.attribute) > 0 and self.attribute[0].name
            else self.name
        )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("apps.store:category-products", kwargs={"category": self.slug})


def brand_image_path(instance, filename):
    return f"brands/{instance.slug}/{filename}"


@cleanup.select
class CategoryAttribute(models.Model):
    category = models.ForeignKey(Category, related_name="category_attribute", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    language = custom_model_fields.LanguageField()

    objects = models.Manager()

    def __str__(self):
        return str(self.name)


class BrandQuerySet(models.QuerySet):
    def list_queryset(self):
        return self

    def detail_queryset(self):
        return self


class BrandManager(models.Manager):
    def get_queryset(self):
        return BrandQuerySet(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()


@cleanup.select
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    cover_image = models.ImageField(upload_to=brand_image_path)
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    objects = models.Manager()
    brands = BrandManager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("Brands")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


def collection_image_path(instance, filename):
    return f"collections/{instance.slug}/{filename}"


class CollectionQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.select_related("brand").prefetch_related(
            Prefetch(
                "category",
                queryset=Category.categories.list_queryset(),
            ),
        )

    def detail_queryset(self):
        return self


class CollectionManager(models.Manager):
    def get_queryset(self):
        return CollectionQuerySet(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset().all()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()


@cleanup.select
class Collection(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    cover_image = models.ImageField(upload_to=collection_image_path, null=True, blank=True)
    brand = models.ForeignKey(
        Brand,
        related_name="collection_brand",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        related_name="collection_category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    objects = models.Manager()
    collections = CollectionManager()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("Collections")

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.prefetch_related(
            Prefetch(
                "collection",
                queryset=Collection.objects.all(),
            ),
        ).prefetch_related(
            Prefetch(
                "product_image",
                queryset=ProductImage.objects.filter(is_feature=True),
                to_attr="image_feature",
            ),
        )

    def detail_queryset(self):
        return self.prefetch_related(
            Prefetch(
                "collection",
                queryset=Collection.objects.all(),
            ),
        ).prefetch_related(
            Prefetch(
                "product_image",
                queryset=ProductImage.objects.filter(is_feature=True),
                to_attr="image_feature",
            ),
            Prefetch("product_image", to_attr="images"),
            Prefetch(
                "product_information",
                queryset=ProductInformation.objects.filter(language=get_language()),
                to_attr="information",
            ),
        )

    def cart_queryset(self):
        return (
            self.prefetch_related(
                Prefetch(
                    "product_image",
                    queryset=ProductImage.objects.filter(is_feature=True),
                    to_attr="image_feature",
                ),
            )
            .filter(in_stock=True, is_active=True)
            .only("name", "slug", "discount_price", "regular_price", "in_stock", "is_active")
        )


class ProductAdminQuerySet(models.QuerySet):
    def list_queryset(self):
        return self.prefetch_related(
            Prefetch(
                "collection",
                queryset=Collection.collections.list_queryset(),
            ),
        ).prefetch_related(
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

    def count_queryset(self):
        return self.get_queryset().count()

    def detail_queryset(self):
        return self.get_queryset().detail_queryset()

    def cart_queryset(self):
        return self.get_queryset().cart_queryset()

    def new_products_queryset(self):
        return self.get_queryset().list_queryset().order_by("-created_at").all()[:6]

    def discounted_products_queryset(self):
        return self.get_queryset().list_queryset().filter(discount__gt=0).order_by("-updated_at")[:6]

    def filter_queryset(self, data, categories):
        return filters.OrderingFilter(
            filters.InStockFilter(
                filters.CollectionFilter(
                    filters.BrandFilter(
                        filters.CategoryFilter(
                            filters.PriceFilter(
                                filters.SearchFilter(self.list_queryset(), data).queryset,
                                data,
                            ).queryset,
                            data,
                            categories,
                        ).queryset,
                        data,
                    ).queryset,
                    data,
                ).queryset,
                data,
            ).queryset,
            data,
        ).queryset

    def in_stock_count(self, queryset):
        return queryset.filter(in_stock=True).count()

    def related_products_queryset(self, product):
        return (
            self.get_queryset()
            .list_queryset()
            .filter(collection=product.collection)
            .exclude(slug=product.slug)
        )


class ProductAdminManager(models.Manager):
    def get_queryset(self):
        return ProductAdminQuerySet(self.model, using=self._db)

    def list_queryset(self):
        return self.get_queryset().list_queryset()

    def detail_queryset(self):
        return self.get_queryset()


@cleanup.select
class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    collection = models.ForeignKey(
        Collection,
        related_name="product_collection",
        on_delete=models.SET_NULL,
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
    discount_price = models.DecimalField(default=0, blank=True, max_digits=6, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    quantity_type = models.CharField(
        max_length=50,
        choices=custom_model_fields.ProductQuantityType.choices,
        default=custom_model_fields.ProductQuantityType.NUMBER,
    )
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    objects = models.Manager()
    products = ProductManager()
    admin_products = ProductAdminManager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("apps.store:product-detail", kwargs={"slug": self.slug})

    @property
    def get_image_feature(self):
        return (
            self.image_feature[0].image.url
            if hasattr(self, "image_feature") and len(self.image_feature) > 0 and self.image_feature[0].image
            else ""
        )

    @property
    def get_information(self):
        return (
            self.information[0].text
            if hasattr(self, "information") and len(self.information) > 0 and self.information[0].text
            else ""
        )

    @property
    def is_active_display_value(self):
        return _("Active") if self.is_active else _("Not Active")

    @property
    def in_stock_display_value(self):
        return _("In Stock") if self.in_stock is True else _("Not In Stock")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.discount is not None:
            self.discount_price = self.regular_price - self.regular_price * self.discount / 100
        else:
            self.discount_price = self.regular_price
        return super().save(*args, **kwargs)


def product_image_path(instance, filename):
    return f"products/{instance.product.id}/{filename}"


@cleanup.select
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(upload_to=product_image_path, null=True, blank=True)
    is_feature = models.BooleanField(default=False)
    created_at = custom_model_fields.CreatedAtField()
    updated_at = custom_model_fields.UpdatedAtField()

    objects = models.Manager()

    class Meta:
        ordering = ("-is_feature",)


@cleanup.select
class ProductInformation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_information")
    language = custom_model_fields.LanguageField()
    text = custom_model_fields.TextUploadingField()

    objects = models.Manager()


def product_image_compressor(sender, **kwargs):
    if kwargs["instance"].image:
        with Image.open(kwargs["instance"].image.path) as image:
            image.save(kwargs["instance"].image.path, optimize=True, quality=15)


def category_image_compressor(sender, **kwargs):
    if kwargs["instance"].cover_image:
        with Image.open(kwargs["instance"].cover_image.path) as image:
            image.save(kwargs["instance"].cover_image.path, optimize=True, quality=15)


def brand_image_compressor(sender, **kwargs):
    if kwargs["instance"].cover_image:
        with Image.open(kwargs["instance"].cover_image.path) as image:
            image.save(kwargs["instance"].cover_image.path, optimize=True, quality=15)


def collection_image_compressor(sender, **kwargs):
    if kwargs["instance"].cover_image:
        with Image.open(kwargs["instance"].cover_image.path) as image:
            image.save(kwargs["instance"].cover_image.path, optimize=True, quality=15)


post_save.connect(product_image_compressor, sender=ProductImage)
post_save.connect(category_image_compressor, sender=Category)
post_save.connect(brand_image_compressor, sender=Brand)
post_save.connect(collection_image_compressor, sender=Collection)
