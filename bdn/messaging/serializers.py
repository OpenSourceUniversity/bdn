from rest_framework import serializers
from bdn.profiles.serializers import ProfileSerializer, UserSerializer
from .models import Thread, Message


class ThreadGetSerializer(serializers.ModelSerializer):
    owner_profile = serializers.\
        SerializerMethodField('_owner_profile')
    opponent_profile = serializers.\
        SerializerMethodField('_opponent_profile')
    unread_count = serializers.\
        SerializerMethodField('_unread_count')
    last_message = serializers.\
        SerializerMethodField('_last_message')

    def _owner_profile(self, obj):
        return ProfileSerializer(obj.owner.profile).data

    def _opponent_profile(self, obj):
        return ProfileSerializer(obj.opponent.profile).data

    def _unread_count(self, obj):
        return Message.objects.all().filter(
            thread=obj, read=False).exclude(
            sender=self.context['request'].user).count()

    def _last_message(self, obj):
        return MessageGetSerializer(Message.objects.all().filter(
                    thread=obj).first()).data

    class Meta:
        model = Thread
        fields = (
            'id',
            'owner',
            'owner_profile',
            'opponent',
            'opponent_profile',
            'unread_count',
            'last_message',
        )


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = (
            'id',
            'owner',
            'opponent',
        )


class MessageGetSerializer(serializers.ModelSerializer):
    sender = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Message
        fields = (
            'thread',
            'sender',
            'text',
            'read',
            'created',
        )


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = (
            'id',
            'thread',
            'sender',
            'text',
            'read',
            'created',
        )
