import logging
from urllib.parse import parse_qsl
from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from bdn.auth.models import User
from bdn.auth.utils import recover_to_addr


logger = logging.getLogger(__name__)


class SignatureAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        querystring = scope['query_string'].decode()
        query_params = dict(parse_qsl(querystring))
        eth_address = query_params.get('auth_eth_address')
        auth_signature = query_params.get('auth_signature')
        user = AnonymousUser()

        if auth_signature and eth_address:
            try:
                recovered_eth_address = recover_to_addr(
                    eth_address, auth_signature)
                if eth_address.lower() == recovered_eth_address[2:].lower():
                    user, _ = User.objects.get_or_create(
                        username=recovered_eth_address.lower())
                    logger.info('Authenticating {}'.format(user.username))
            except ValueError:
                logger.warning('Could not authenticate {}'.format(eth_address))
        else:
            logger.warning('No auth parameters provided to WebSocket')

        scope['user'] = user
        return self.inner(scope)


def SignatureAuthMiddlewareStack(inner):
    return SignatureAuthMiddleware(AuthMiddlewareStack(inner))
