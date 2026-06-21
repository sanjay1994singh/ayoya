from django.contrib.sitemaps import Sitemap

from .models import Category, Property


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at


class PropertySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Property.objects.filter(status=Property.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at
