from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from bdn.messaging.models import Message

from .serializers import MessageGetSerializer


def message_saved(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        serializer = MessageGetSerializer(instance)
        serilaizer_str = serializer.data.copy()
        serilaizer_str['thread'] = str(serilaizer_str['thread'])
        thread = instance.thread
        if thread.owner == instance.sender:
            recipient = thread.opponent
        else:
            recipient = thread.owner
        group_name = 'messages_{}'.format(recipient.username.lower())
        group_send = async_to_sync(channel_layer.group_send)
        group_send(group_name, {
            'type': 'chat.message',
            'payload': serilaizer_str
        })


post_save.connect(message_saved, sender=Message)
