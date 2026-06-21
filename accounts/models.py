from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    USER_TYPE_BUYER = "buyer"
    USER_TYPE_AGENT = "agent"
    USER_TYPE_SELLER = "seller"
    USER_TYPE_CHOICES = (
        (USER_TYPE_BUYER, "Buyer"),
        (USER_TYPE_AGENT, "Agent"),
        (USER_TYPE_SELLER, "Seller / Owner"),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default=USER_TYPE_BUYER)
    phone = models.CharField(max_length=20, blank=True)
    alternate_phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to="users/profile/", blank=True, null=True)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    company_name = models.CharField(max_length=160, blank=True)
    license_number = models.CharField(max_length=80, blank=True)
    website = models.URLField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, blank=True, default="India")
    postal_code = models.CharField(max_length=20, blank=True)
    preferred_location = models.CharField(max_length=160, blank=True)
    min_budget = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    max_budget = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    accepts_terms = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("accounts:profile", kwargs={"username": self.username})

    @property
    def display_avatar(self):
        if self.profile_image:
            return self.profile_image.url
        return self.avatar_url
