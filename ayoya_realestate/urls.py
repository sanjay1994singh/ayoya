from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from home.sitemaps import StaticViewSitemap
from properties.sitemaps import PropertySitemap

sitemaps = {
    "static": StaticViewSitemap,
    "properties": PropertySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("accounts.dashboard_urls")),
    path("properties/", include("properties.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
