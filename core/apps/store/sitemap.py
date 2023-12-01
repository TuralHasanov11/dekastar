from apps.store.models import Brand, Category, Collection, Product
from django.contrib.sitemaps import Sitemap


class ProductSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class CategorySiteMap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class CollectionSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Collection.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class BrandSiteMap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Brand.objects.all()

    def lastmod(self, obj):
        return obj.updated_at
