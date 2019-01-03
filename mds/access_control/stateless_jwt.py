from django.utils.encoding import smart_text
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from django.conf import settings
from .authenticate import authenticate


class StatelessJwtAuthentication(BaseAuthentication):
    def authenticate(self, request):
        encoded_jwt = self.extract_token(request)
        if encoded_jwt is None:
            return None

        user = authenticate(settings.AUTH_MEANS, encoded_jwt)

        return user, None

    @staticmethod
    def extract_token(request):
        auth_header = get_authorization_header(request)

        if not auth_header:
            return None

        auth_header_prefix = "Bearer ".lower()
        auth = smart_text(auth_header)

        if not auth.lower().startswith(auth_header_prefix):
            return None

        return auth[len(auth_header_prefix) :]
