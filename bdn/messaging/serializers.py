from rest_framework import serializers
from .models import Thread, Message


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = (
            'id',
            'owner',
            'opponent',
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            'id',
            'dialog',
            'sender',
            'text',
            'read',
            'created',
        )
