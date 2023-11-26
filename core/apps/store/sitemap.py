from apps.store.models import Category, Product
from django.contrib.sitemaps import Sitemap


class ProductSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Product.products.all()
    
    def lastmod(self, obj):
        return obj.updated_at


class CategorySiteMap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Category.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at