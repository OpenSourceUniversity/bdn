from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from bdn.auth.models import User
from bdn.auth.utils import recover_to_addr


class SignatureAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])
        user = AnonymousUser()
        if b'auth_signature' in headers and b'auth_eth_address' in headers:
            signature = headers['auth_signature'].decode()
            eth_address = headers['auth_eth_address'].decode()
            try:
                recovered_eth_address = recover_to_addr(eth_address, signature)
                if eth_address.lower() == recovered_eth_address[2:].lower():
                    user, _ = User.objects.get_or_create(
                        username=recovered_eth_address.lower())
            except ValueError:
                pass
        scope['user'] = user
        return self.inner(scope)


def SignatureAuthMiddlewareStack(inner):
    return SignatureAuthMiddleware(AuthMiddlewareStack(inner))
