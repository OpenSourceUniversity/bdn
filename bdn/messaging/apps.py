from django.apps import AppConfig


class MessagingConfig(AppConfig):
    name = 'bdn.messaging'

    def ready(self):
        from . import signals # noqa
