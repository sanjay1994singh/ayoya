from django.conf import settings
from django.shortcuts import redirect


class CanonicalHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        canonical_host = getattr(settings, "SITE_DOMAIN", "").split(":")[0]
        current_host = request.get_host().split(":")[0]
        if canonical_host and current_host == f"www.{canonical_host}":
            target = f"{settings.SITE_SCHEME}://{canonical_host}{request.get_full_path()}"
            return redirect(target, permanent=True)
        return self.get_response(request)
