from django.http import HttpResponse
from django.shortcuts import render

from properties.models import Category, Property


def home(request):
    featured = Property.objects.filter(status=Property.Status.PUBLISHED, is_featured=True).select_related("category", "owner")[:6]
    latest = Property.objects.filter(status=Property.Status.PUBLISHED).select_related("category", "owner")[:9]
    categories = Category.objects.filter(is_active=True)[:8]
    context = {
        "featured": featured,
        "latest": latest,
        "categories": categories,
        "title": "Ayoya Realestate - Buy, Sell, Rent Properties",
        "meta_description": "Find verified homes, apartments, plots, commercial spaces, and real estate agents on Ayoya Realestate.",
    }
    return render(request, "home/home.html", context)


def about(request):
    return render(request, "home/about.html", {"title": "About Ayoya Realestate"})


def contact(request):
    return render(request, "home/contact.html", {"title": "Contact Ayoya Realestate"})


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Sitemap: /sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
