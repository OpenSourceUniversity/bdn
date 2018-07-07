from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


class SignatureAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        signature = request.META.get('X_SIGNATURE')
        eth_address = request.META.get('X_ETH_ADDRESS')
        if not signature or not eth_address:
            return None

        try:
            user, _ = User.objects.get_or_create(username=eth_address.lower())
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
