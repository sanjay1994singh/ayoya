from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import InquiryForm, PropertyForm, PropertySearchForm, ReviewForm
from .models import Category, Favorite, Property


def filtered_properties(request, category_slug=None):
    properties = Property.objects.filter(status=Property.Status.PUBLISHED).select_related("category", "owner").prefetch_related("amenities")
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        properties = properties.filter(category=category)

    form = PropertySearchForm(request.GET or None)
    if form.is_valid():
        q = form.cleaned_data.get("q")
        purpose = form.cleaned_data.get("purpose")
        property_type = form.cleaned_data.get("property_type")
        city = form.cleaned_data.get("city")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        bedrooms = form.cleaned_data.get("bedrooms")
        if q:
            properties = properties.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(locality__icontains=q))
        if purpose:
            properties = properties.filter(purpose=purpose)
        if property_type:
            properties = properties.filter(property_type=property_type)
        if city:
            properties = properties.filter(city__icontains=city)
        if min_price is not None:
            properties = properties.filter(price__gte=min_price)
        if max_price is not None:
            properties = properties.filter(price__lte=max_price)
        if bedrooms is not None:
            properties = properties.filter(bedrooms__gte=bedrooms)
    return properties, form, category


def property_list(request, slug=None):
    properties, form, category = filtered_properties(request, slug)
    paginator = Paginator(properties, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    title = f"{category.name} Properties" if category else "Properties"
    return render(request, "properties/list.html", {"page_obj": page_obj, "form": form, "category": category, "title": title})


def property_detail(request, slug):
    property_obj = get_object_or_404(Property.objects.select_related("owner", "category").prefetch_related("amenities", "images"), slug=slug, status=Property.Status.PUBLISHED)
    Property.objects.filter(pk=property_obj.pk).update(views_count=property_obj.views_count + 1, updated_at=timezone.now())
    inquiry_form = InquiryForm(request.POST or None)
    review_form = ReviewForm()
    if request.method == "POST" and inquiry_form.is_valid():
        inquiry = inquiry_form.save(commit=False)
        inquiry.property = property_obj
        if request.user.is_authenticated:
            inquiry.user = request.user
        inquiry.save()
        messages.success(request, "Your inquiry has been sent.")
        return redirect(property_obj.get_absolute_url())
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(user=request.user, property=property_obj).exists()
    return render(
        request,
        "properties/detail.html",
        {"property": property_obj, "inquiry_form": inquiry_form, "review_form": review_form, "is_favorite": is_favorite},
    )


@login_required
def property_create(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            form.save_m2m()
            messages.success(request, "Property created.")
            return redirect(property_obj.get_absolute_url())
    else:
        form = PropertyForm()
    return render(request, "properties/form.html", {"form": form, "title": "Add property"})


@login_required
def property_edit(request, slug):
    property_obj = get_object_or_404(Property, slug=slug, owner=request.user)
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            property_obj = form.save()
            messages.success(request, "Property updated.")
            return redirect(property_obj.get_absolute_url())
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, "properties/form.html", {"form": form, "title": "Edit property"})


@login_required
def toggle_favorite(request, slug):
    property_obj = get_object_or_404(Property, slug=slug, status=Property.Status.PUBLISHED)
    favorite, created = Favorite.objects.get_or_create(user=request.user, property=property_obj)
    if not created:
        favorite.delete()
        messages.info(request, "Removed from favorites.")
    else:
        messages.success(request, "Saved to favorites.")
    return redirect(property_obj.get_absolute_url())
