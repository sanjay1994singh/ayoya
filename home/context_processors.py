from django.conf import settings


def site_meta(request):
    absolute_root = f"{settings.SITE_SCHEME}://{settings.SITE_DOMAIN}"
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_DOMAIN": settings.SITE_DOMAIN,
        "ABSOLUTE_ROOT": absolute_root,
        "DEFAULT_META_DESCRIPTION": "Ayoya Realestate helps buyers, sellers, owners, and agents discover verified homes, plots, rentals, villas, shops, and commercial properties.",
        "DEFAULT_META_KEYWORDS": "Ayoya Realestate, real estate, buy property, sell property, rent property, property agents, verified properties, homes, flats, plots, commercial property",
    }
