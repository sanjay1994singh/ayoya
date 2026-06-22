from django.conf import settings
from social_core.backends.google import GoogleOAuth2


class AyoyaGoogleOAuth2(GoogleOAuth2):
    name = "google-oauth2"

    def get_redirect_uri(self, state=None):
        return settings.SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI
