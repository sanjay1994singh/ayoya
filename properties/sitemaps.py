from django.contrib.sitemaps import Sitemap

from .models import Property


class PropertySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Property.objects.filter(status=Property.Status.PUBLISHED)

    def lastmod(self, obj):
        return obj.updated_at
