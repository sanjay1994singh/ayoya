from django.conf import settings


def site_meta(request):
    absolute_root = f"{settings.SITE_SCHEME}://{settings.SITE_DOMAIN}"
    return {
        "SITE_NAME": settings.SITE_NAME,
        "SITE_DOMAIN": settings.SITE_DOMAIN,
        "ABSOLUTE_ROOT": absolute_root,
    }
