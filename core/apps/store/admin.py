from apps.store.models import (
    Brand,
    Category,
    CategoryAttribute,
    Collection,
    Product,
    ProductImage,
)
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "brand", "category")
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
    ]
    list_display = ("name", "collection")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image")


class CategoryAttributeInline(admin.TabularInline):
    model = CategoryAttribute


@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):
    list_display = ("category", "name", "language")


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ("tree_actions", "indented_title")
    list_display_links = ("indented_title",)
    inlines = [
        CategoryAttributeInline,
    ]
    prepopulated_fields = {"slug": ("name",)}
