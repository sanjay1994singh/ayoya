from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from properties.models import Category, Property


def home(request):
    featured = list(Property.objects.filter(status=Property.Status.PUBLISHED, is_featured=True).select_related("category", "owner")[:6])
    latest = list(Property.objects.filter(status=Property.Status.PUBLISHED).select_related("category", "owner")[:9])
    categories = Category.objects.filter(is_active=True)[:8]
    context = {
        "featured": featured,
        "featured_portrait": [item for item in featured if item.image_orientation == "portrait"],
        "featured_landscape": [item for item in featured if item.image_orientation == "landscape"],
        "latest": latest,
        "latest_portrait": [item for item in latest if item.image_orientation == "portrait"],
        "latest_landscape": [item for item in latest if item.image_orientation == "landscape"],
        "categories": categories,
        "title": "Ayoya Realestate - Buy, Sell, Rent Properties",
        "meta_description": "AYOYA GROUP is your trusted real estate channel partner for residential plots, commercial plots, flats, and investment properties in Vrindavan, Mathura, Barsana, Goverdhan, and Radha Kund.",
        "meta_keywords": "AYOYA GROUP, Ayoya Realestate, Vrindavan property, Mathura property, Goverdhan property, Barsana property, Radha Kund property, real estate channel partner",
        "og_image": "/static/images/ayoya-group-banner.jpeg",
    }
    return render(request, "home/home.html", context)


def about(request):
    return render(
        request,
        "home/about.html",
        {
            "title": "About AYOYA GROUP - Real Estate Channel Partner in Vrindavan",
            "meta_description": "AYOYA GROUP is an independent real estate channel partner helping customers buy residential plots, commercial plots, flats, and investment properties in Vrindavan, Mathura, Barsana, Goverdhan, and nearby areas.",
            "meta_keywords": "AYOYA GROUP, Ayoya Realestate, real estate channel partner Vrindavan, property in Mathura, plots in Vrindavan, flats in Mathura, Barsana property, Goverdhan property",
        },
    )


def contact(request):
    return render(
        request,
        "home/contact.html",
        {
            "title": "Contact AYOYA GROUP - Real Estate in Mathura and Vrindavan",
            "meta_description": "Contact AYOYA GROUP for residential plots, commercial plots, flats, and investment property guidance in Vrindavan, Mathura, Barsana, Goverdhan, and nearby areas.",
            "meta_keywords": "contact AYOYA GROUP, Ayoya Realestate phone, ayoyarealestate@gmail.com, Mathura real estate, Vrindavan property advisor",
        },
    )


def robots_txt(request):
    sitemap_url = f"{settings.SITE_SCHEME}://{settings.SITE_DOMAIN}/sitemap.xml"
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /accounts/login/",
        "Disallow: /accounts/register/",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
