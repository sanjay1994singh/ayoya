from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "user_type", "phone", "city", "is_verified", "is_staff")
    list_filter = ("user_type", "is_verified", "is_staff", "is_active")
    search_fields = ("username", "email", "first_name", "last_name", "phone", "company_name")
    fieldsets = UserAdmin.fieldsets + (
        (
            "Real estate profile",
            {
                "fields": (
                    "user_type",
                    "phone",
                    "alternate_phone",
                    "profile_image",
                    "avatar_url",
                    "bio",
                    "company_name",
                    "license_number",
                    "website",
                    "address",
                    "city",
                    "state",
                    "country",
                    "postal_code",
                    "preferred_location",
                    "min_budget",
                    "max_budget",
                    "is_verified",
                    "accepts_terms",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Real estate profile",
            {
                "classes": ("wide",),
                "fields": ("email", "user_type", "phone", "accepts_terms"),
            },
        ),
    )
