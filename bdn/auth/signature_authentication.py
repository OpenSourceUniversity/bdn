from bdn.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from bdn.auth.utils import recover_to_addr


class SignatureAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        signature = request.META.get('HTTP_AUTH_SIGNATURE')
        eth_address = request.META.get('HTTP_AUTH_ETH_ADDRESS')
        if not signature or not eth_address:
            return None

        try:
            recovered_eth_address = recover_to_addr(eth_address, signature)
        except ValueError:
            return None

        if eth_address.lower() != recovered_eth_address[2:].lower():
            return None

        try:
            user, _ = User.objects.get_or_create(
                username=recovered_eth_address.lower())
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
