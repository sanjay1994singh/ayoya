from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

try:
    from django_ckeditor_5.fields import CKEditor5Field
except ImportError:
    CKEditor5Field = models.TextField


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=80, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("properties:category", kwargs={"slug": self.slug})


class Amenity(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Amenities"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Property(TimeStampedModel):
    class Purpose(models.TextChoices):
        SALE = "sale", "For Sale"
        RENT = "rent", "For Rent"
        LEASE = "lease", "For Lease"

    class Type(models.TextChoices):
        RESIDENTIAL = "residential", "Residential"
        COMMERCIAL = "commercial", "Commercial"
        LAND = "land", "Land / Plot"
        INDUSTRIAL = "industrial", "Industrial"

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        SOLD = "sold", "Sold"
        RENTED = "rented", "Rented"
        ARCHIVED = "archived", "Archived"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="properties")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="properties")
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="properties")
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True, blank=True)
    short_description = models.CharField(max_length=280, blank=True)
    description = CKEditor5Field("Description", config_name="default", blank=True)
    purpose = models.CharField(max_length=20, choices=Purpose.choices, default=Purpose.SALE)
    property_type = models.CharField(max_length=30, choices=Type.choices, default=Type.RESIDENTIAL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    price = models.DecimalField(max_digits=14, decimal_places=2)
    price_label = models.CharField(max_length=80, blank=True, help_text="Example: negotiable, per month, all inclusive")
    area_sqft = models.PositiveIntegerField(blank=True, null=True)
    bedrooms = models.PositiveSmallIntegerField(default=0)
    bathrooms = models.PositiveSmallIntegerField(default=0)
    balconies = models.PositiveSmallIntegerField(default=0)
    floor_number = models.IntegerField(blank=True, null=True)
    total_floors = models.PositiveSmallIntegerField(blank=True, null=True)
    parking_spaces = models.PositiveSmallIntegerField(default=0)
    furnishing = models.CharField(max_length=80, blank=True)
    year_built = models.PositiveSmallIntegerField(blank=True, null=True)
    address = models.CharField(max_length=255)
    locality = models.CharField(max_length=160, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    country = models.CharField(max_length=120, default="India")
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    main_image = models.ImageField(upload_to="properties/main/", blank=True, null=True)
    video_url = models.URLField(blank=True)
    virtual_tour_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)

    class Meta:
        ordering = ["-is_featured", "-created_at"]
        indexes = [
            models.Index(fields=["status", "purpose", "city"]),
            models.Index(fields=["property_type", "price"]),
            models.Index(fields=["slug"]),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.title}-{self.city}")[:210]
            candidate = base_slug
            counter = 2
            while Property.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base_slug}-{counter}"
                counter += 1
            self.slug = candidate
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description:
            self.meta_description = (self.short_description or f"{self.title} in {self.city}, {self.state}")[:160]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("properties:detail", kwargs={"slug": self.slug})


class PropertyImage(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="properties/gallery/")
    caption = models.CharField(max_length=160, blank=True)
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "created_at"]

    def __str__(self):
        return f"{self.property} image"


class Inquiry(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inquiries")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="inquiries")
    name = models.CharField(max_length=140)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    is_contacted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Inquiries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Inquiry for {self.property}"


class Favorite(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="favorites")

    class Meta:
        unique_together = ("user", "property")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} saved {self.property}"


class Review(TimeStampedModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rating}/5 for {self.property}"


class SavedSearch(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_searches")
    name = models.CharField(max_length=120)
    query = models.JSONField(default=dict, blank=True)
    email_alerts = models.BooleanField(default=True)

    def __str__(self):
        return self.name
