from django.apps import AppConfig


class NotificationConfig(AppConfig):
    name = 'bdn.notifications_extensions'

    def ready(self):
        from . import signals # noqa
