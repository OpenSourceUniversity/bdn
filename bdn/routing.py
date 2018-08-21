# flake8: noqa

from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import (
    AllowedHostsOriginValidator, OriginValidator)
from bdn.auth.signature_auth_middleware import SignatureAuthMiddlewareStack
from bdn.notifications_extensions.consumers import NotificationConsumer

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(SignatureAuthMiddlewareStack(URLRouter(
        [
            url(r"^notifications/", NotificationConsumer),
        ]
    ))),
})
