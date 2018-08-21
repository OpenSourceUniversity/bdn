from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from notifications.models import Notification

from .serializers import NotificationSerializer


def notification_saved(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        serializer = NotificationSerializer(instance)
        recipient = instance.recipient
        group_name = recipient.username.lower()
        group_send = async_to_sync(channel_layer.group_send)
        group_send(group_name, {
            'type': 'notification.send',
            'payload': serializer.data
        })


post_save.connect(notification_saved, sender=Notification)
