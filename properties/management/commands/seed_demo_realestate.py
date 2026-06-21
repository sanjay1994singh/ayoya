from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw, ImageFont

from properties.models import Amenity, Category, Inquiry, Property, PropertyImage, Review, SavedSearch


class Command(BaseCommand):
    help = "Seed Ayoya Realestate with demo users, real estate master data, and property listings."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Ayoya Realestate demo data...")
        with transaction.atomic():
            users = self.create_users()
            categories = self.create_categories()
            amenities = self.create_amenities()
            properties = self.create_properties(users, categories, amenities)
            self.create_interactions(users, properties)
        self.stdout.write(self.style.SUCCESS(f"Seed complete: {len(properties)} properties ready with demo images."))

    def create_users(self):
        User = get_user_model()
        users = {}
        user_data = [
            {
                "username": "ayoya_agent",
                "email": "agent@ayoyagroup.com",
                "first_name": "Aarav",
                "last_name": "Kapoor",
                "user_type": User.USER_TYPE_AGENT,
                "phone": "9876500011",
                "company_name": "Ayoya Prime Realty",
                "city": "Noida",
                "state": "Uttar Pradesh",
                "bio": "Verified agent handling residential and commercial mandates across NCR.",
            },
            {
                "username": "ayoya_owner",
                "email": "owner@ayoyagroup.com",
                "first_name": "Meera",
                "last_name": "Sharma",
                "user_type": User.USER_TYPE_SELLER,
                "phone": "9876500022",
                "city": "Gurugram",
                "state": "Haryana",
                "bio": "Owner listing premium rental and resale homes directly.",
            },
            {
                "username": "ayoya_buyer",
                "email": "buyer@ayoyagroup.com",
                "first_name": "Rohan",
                "last_name": "Verma",
                "user_type": User.USER_TYPE_BUYER,
                "phone": "9876500033",
                "city": "Delhi",
                "state": "Delhi",
                "preferred_location": "Noida, Gurugram, Delhi",
                "min_budget": Decimal("3500000"),
                "max_budget": Decimal("15000000"),
                "bio": "Looking for verified family homes and investment properties.",
            },
        ]
        for item in user_data:
            user, created = User.objects.update_or_create(
                username=item["username"],
                defaults={**item, "is_verified": True, "accepts_terms": True},
            )
            if created:
                user.set_password("Demo@12345")
                user.save(update_fields=["password"])
            users[item["username"]] = user
        return users

    def create_categories(self):
        rows = [
            ("Apartment", "Ready-to-move and under-construction flats in prime locations."),
            ("Villa", "Independent luxury villas and gated community homes."),
            ("Plot", "Residential and investment land parcels."),
            ("Office", "Modern office spaces for startups and enterprises."),
            ("Shop", "Retail shops and showroom-ready commercial spaces."),
            ("Farm House", "Weekend homes, farm houses, and open lifestyle properties."),
        ]
        categories = {}
        for name, description in rows:
            category, _ = Category.objects.update_or_create(name=name, defaults={"description": description, "is_active": True})
            categories[name] = category
        return categories

    def create_amenities(self):
        names = [
            "Lift",
            "Power Backup",
            "Club House",
            "Swimming Pool",
            "Gym",
            "Security",
            "Park",
            "Covered Parking",
            "Metro Nearby",
            "Modular Kitchen",
            "CCTV",
            "Rainwater Harvesting",
        ]
        amenities = {}
        for name in names:
            amenity, _ = Amenity.objects.update_or_create(name=name)
            amenities[name] = amenity
        return amenities

    def create_properties(self, users, categories, amenities):
        demo_rows = [
            {
                "title": "Sunlit 3 BHK Apartment Near Sector 62 Metro",
                "category": "Apartment",
                "owner": users["ayoya_agent"],
                "purpose": Property.Purpose.SALE,
                "property_type": Property.Type.RESIDENTIAL,
                "price": "12500000",
                "price_label": "negotiable",
                "city": "Noida",
                "state": "Uttar Pradesh",
                "locality": "Sector 62",
                "area_sqft": 1680,
                "bedrooms": 3,
                "bathrooms": 3,
                "balconies": 2,
                "parking_spaces": 1,
                "furnishing": "Semi furnished",
                "color": (18, 97, 73),
                "amenities": ["Lift", "Power Backup", "Security", "Metro Nearby", "Covered Parking"],
            },
            {
                "title": "Premium 4 BHK Golf Course Road Villa",
                "category": "Villa",
                "owner": users["ayoya_owner"],
                "purpose": Property.Purpose.SALE,
                "property_type": Property.Type.RESIDENTIAL,
                "price": "42500000",
                "price_label": "all inclusive",
                "city": "Gurugram",
                "state": "Haryana",
                "locality": "Golf Course Road",
                "area_sqft": 3600,
                "bedrooms": 4,
                "bathrooms": 5,
                "balconies": 3,
                "parking_spaces": 2,
                "furnishing": "Fully furnished",
                "color": (37, 95, 133),
                "amenities": ["Club House", "Swimming Pool", "Gym", "Security", "CCTV"],
            },
            {
                "title": "Corner Residential Plot In Yamuna Expressway",
                "category": "Plot",
                "owner": users["ayoya_agent"],
                "purpose": Property.Purpose.SALE,
                "property_type": Property.Type.LAND,
                "price": "7800000",
                "price_label": "registry ready",
                "city": "Greater Noida",
                "state": "Uttar Pradesh",
                "locality": "Yamuna Expressway",
                "area_sqft": 2400,
                "bedrooms": 0,
                "bathrooms": 0,
                "balconies": 0,
                "parking_spaces": 0,
                "furnishing": "Open plot",
                "color": (197, 139, 43),
                "amenities": ["Security", "Park", "Rainwater Harvesting"],
            },
            {
                "title": "Fully Furnished Studio Apartment For Rent",
                "category": "Apartment",
                "owner": users["ayoya_owner"],
                "purpose": Property.Purpose.RENT,
                "property_type": Property.Type.RESIDENTIAL,
                "price": "28000",
                "price_label": "per month",
                "city": "Delhi",
                "state": "Delhi",
                "locality": "Saket",
                "area_sqft": 620,
                "bedrooms": 1,
                "bathrooms": 1,
                "balconies": 1,
                "parking_spaces": 1,
                "furnishing": "Fully furnished",
                "color": (116, 73, 146),
                "amenities": ["Lift", "Power Backup", "Security", "Modular Kitchen"],
            },
            {
                "title": "High Street Retail Shop With Frontage",
                "category": "Shop",
                "owner": users["ayoya_agent"],
                "purpose": Property.Purpose.LEASE,
                "property_type": Property.Type.COMMERCIAL,
                "price": "85000",
                "price_label": "per month",
                "city": "Noida",
                "state": "Uttar Pradesh",
                "locality": "Sector 18",
                "area_sqft": 520,
                "bedrooms": 0,
                "bathrooms": 1,
                "balconies": 0,
                "parking_spaces": 1,
                "furnishing": "Unfurnished",
                "color": (180, 80, 54),
                "amenities": ["Security", "CCTV", "Metro Nearby", "Power Backup"],
            },
            {
                "title": "Managed Office Space In Cyber City",
                "category": "Office",
                "owner": users["ayoya_agent"],
                "purpose": Property.Purpose.RENT,
                "property_type": Property.Type.COMMERCIAL,
                "price": "240000",
                "price_label": "per month",
                "city": "Gurugram",
                "state": "Haryana",
                "locality": "Cyber City",
                "area_sqft": 2800,
                "bedrooms": 0,
                "bathrooms": 3,
                "balconies": 0,
                "parking_spaces": 3,
                "furnishing": "Fully furnished",
                "color": (34, 117, 151),
                "amenities": ["Lift", "Power Backup", "Security", "Covered Parking", "CCTV"],
            },
            {
                "title": "Luxury Farm House With Pool And Lawn",
                "category": "Farm House",
                "owner": users["ayoya_owner"],
                "purpose": Property.Purpose.SALE,
                "property_type": Property.Type.RESIDENTIAL,
                "price": "31500000",
                "price_label": "clear title",
                "city": "Faridabad",
                "state": "Haryana",
                "locality": "Surajkund Road",
                "area_sqft": 10800,
                "bedrooms": 5,
                "bathrooms": 5,
                "balconies": 2,
                "parking_spaces": 4,
                "furnishing": "Fully furnished",
                "color": (58, 122, 74),
                "amenities": ["Swimming Pool", "Park", "Security", "Rainwater Harvesting"],
            },
            {
                "title": "Budget 2 BHK Ready Flat In Raj Nagar Extension",
                "category": "Apartment",
                "owner": users["ayoya_agent"],
                "purpose": Property.Purpose.SALE,
                "property_type": Property.Type.RESIDENTIAL,
                "price": "4850000",
                "price_label": "home loan available",
                "city": "Ghaziabad",
                "state": "Uttar Pradesh",
                "locality": "Raj Nagar Extension",
                "area_sqft": 980,
                "bedrooms": 2,
                "bathrooms": 2,
                "balconies": 1,
                "parking_spaces": 1,
                "furnishing": "Semi furnished",
                "color": (92, 104, 120),
                "amenities": ["Lift", "Power Backup", "Park", "Security"],
            },
            {
                "title": "Penthouse With Terrace Garden And City View",
                "category": "Apartment",
                "owner": users["ayoya_owner"],
                "purpose": Property.Purpose.SALE,
                "property_type": Property.Type.RESIDENTIAL,
                "price": "28500000",
                "price_label": "premium listing",
                "city": "Delhi",
                "state": "Delhi",
                "locality": "Dwarka",
                "area_sqft": 2450,
                "bedrooms": 4,
                "bathrooms": 4,
                "balconies": 4,
                "parking_spaces": 2,
                "furnishing": "Fully furnished",
                "color": (82, 87, 166),
                "amenities": ["Lift", "Power Backup", "Gym", "Security", "Modular Kitchen"],
            },
            {
                "title": "Warehouse Space Near Industrial Corridor",
                "category": "Office",
                "owner": users["ayoya_agent"],
                "purpose": Property.Purpose.LEASE,
                "property_type": Property.Type.INDUSTRIAL,
                "price": "165000",
                "price_label": "per month",
                "city": "Manesar",
                "state": "Haryana",
                "locality": "Sector 8",
                "area_sqft": 6200,
                "bedrooms": 0,
                "bathrooms": 2,
                "balconies": 0,
                "parking_spaces": 4,
                "furnishing": "Industrial shell",
                "color": (95, 89, 73),
                "amenities": ["Security", "CCTV", "Power Backup", "Covered Parking"],
            },
        ]

        seeded = []
        for index, row in enumerate(demo_rows, start=1):
            image_name = self.make_demo_image(index, row["title"], row["city"], row["color"])
            defaults = {
                "owner": row["owner"],
                "category": categories[row["category"]],
                "purpose": row["purpose"],
                "property_type": row["property_type"],
                "status": Property.Status.PUBLISHED,
                "short_description": f"{row['locality']} listing with verified ownership, clear pricing, and responsive Ayoya inquiry support.",
                "description": self.description_html(row),
                "price": Decimal(row["price"]),
                "price_label": row["price_label"],
                "area_sqft": row["area_sqft"],
                "bedrooms": row["bedrooms"],
                "bathrooms": row["bathrooms"],
                "balconies": row["balconies"],
                "parking_spaces": row["parking_spaces"],
                "furnishing": row["furnishing"],
                "address": f"{row['locality']}, {row['city']}",
                "locality": row["locality"],
                "city": row["city"],
                "state": row["state"],
                "country": "India",
                "postal_code": "110001",
                "is_featured": index <= 6,
                "is_verified": True,
                "main_image": f"properties/main/{image_name}",
            }
            property_obj, _ = Property.objects.update_or_create(title=row["title"], defaults=defaults)
            property_obj.amenities.set([amenities[name] for name in row["amenities"]])
            self.create_gallery(property_obj, index, row)
            seeded.append(property_obj)
        return seeded

    def description_html(self, row):
        return (
            f"<h2>{row['title']}</h2>"
            f"<p>This {row['category'].lower()} in {row['locality']}, {row['city']} is listed with verified details, "
            "clear ownership information, and quick inquiry support.</p>"
            "<ul>"
            f"<li>Area: {row['area_sqft']} sq ft</li>"
            f"<li>Configuration: {row['bedrooms']} bedrooms, {row['bathrooms']} bathrooms</li>"
            f"<li>Furnishing: {row['furnishing']}</li>"
            "</ul>"
        )

    def image_path(self, folder, filename):
        path = Path(settings.MEDIA_ROOT) / folder
        path.mkdir(parents=True, exist_ok=True)
        return path / filename

    def make_demo_image(self, index, title, city, color):
        filename = f"demo-property-{index:02d}.jpg"
        path = self.image_path("properties/main", filename)
        self.draw_image(path, title, city, color)
        return filename

    def create_gallery(self, property_obj, index, row):
        for gallery_index in range(1, 3):
            filename = f"demo-property-{index:02d}-gallery-{gallery_index}.jpg"
            path = self.image_path("properties/gallery", filename)
            color = tuple(min(240, channel + gallery_index * 18) for channel in row["color"])
            self.draw_image(path, f"{row['category']} View {gallery_index}", row["locality"], color)
            image, _ = PropertyImage.objects.update_or_create(
                property=property_obj,
                caption=f"{row['title']} view {gallery_index}",
                defaults={"sort_order": gallery_index, "image": f"properties/gallery/{filename}"},
            )

    def draw_image(self, path, title, subtitle, color):
        width, height = 1200, 800
        image = Image.new("RGB", (width, height), color)
        draw = ImageDraw.Draw(image)
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle((0, height - 250, width, height), fill=(0, 0, 0, 120))
        overlay_draw.rectangle((60, 60, width - 60, height - 300), outline=(255, 255, 255, 135), width=8)
        image = Image.alpha_composite(image.convert("RGBA"), overlay)
        draw = ImageDraw.Draw(image)
        font_large = ImageFont.load_default(size=54)
        font_small = ImageFont.load_default(size=34)
        draw.text((90, height - 220), "Ayoya Realestate", fill=(255, 255, 255), font=font_small)
        draw.text((90, height - 165), title[:42], fill=(255, 255, 255), font=font_large)
        draw.text((90, height - 95), subtitle, fill=(245, 219, 167), font=font_small)
        image.convert("RGB").save(path, "JPEG", quality=90)

    def create_interactions(self, users, properties):
        buyer = users["ayoya_buyer"]
        for property_obj in properties[:5]:
            Inquiry.objects.update_or_create(
                property=property_obj,
                email=buyer.email,
                defaults={
                    "user": buyer,
                    "name": buyer.get_full_name(),
                    "phone": buyer.phone,
                    "message": "Please share more details, visit timing, and final price.",
                },
            )
        for property_obj in properties[:4]:
            property_obj.favorites.get_or_create(user=buyer)
        for property_obj in properties[:3]:
            Review.objects.update_or_create(
                property=property_obj,
                user=buyer,
                defaults={"rating": 5, "comment": "Clear property information and helpful listing details.", "is_approved": True},
            )
        SavedSearch.objects.update_or_create(
            user=buyer,
            name="NCR homes under 1.5 Cr",
            defaults={
                "query": {"city": "Noida", "max_price": "15000000", "purpose": "sale"},
                "email_alerts": True,
            },
        )
