from django.contrib import admin

from .models import Amenity, Category, Favorite, Inquiry, Property, PropertyImage, Review, SavedSearch


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "city", "purpose", "property_type", "price", "status", "is_featured", "is_verified", "owner")
    list_filter = ("status", "purpose", "property_type", "city", "is_featured", "is_verified")
    search_fields = ("title", "city", "locality", "address", "owner__username", "owner__email")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("amenities",)
    inlines = [PropertyImageInline]
    fieldsets = (
        ("Owner and publishing", {"fields": ("owner", "status", "is_featured", "is_verified")}),
        ("Core details", {"fields": ("title", "slug", "category", "amenities", "short_description", "description")}),
        ("Pricing and type", {"fields": ("purpose", "property_type", "price", "price_label")}),
        ("Features", {"fields": ("area_sqft", "bedrooms", "bathrooms", "balconies", "floor_number", "total_floors", "parking_spaces", "furnishing", "year_built")}),
        ("Location", {"fields": ("address", "locality", "city", "state", "country", "postal_code", "latitude", "longitude")}),
        ("Media", {"fields": ("main_image", "video_url", "virtual_tour_url")}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("property", "name", "phone", "is_contacted", "created_at")
    list_filter = ("is_contacted", "created_at")
    search_fields = ("name", "email", "phone", "property__title")


admin.site.register(Favorite)
admin.site.register(Review)
admin.site.register(SavedSearch)
