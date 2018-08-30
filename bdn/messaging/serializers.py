from rest_framework import serializers
from bdn.profiles.serializers import ProfileSerializer, UserSerializer
from .models import Thread, Message


class ThreadGetSerializer(serializers.ModelSerializer):
    owner_profile = serializers.\
        SerializerMethodField('_owner_profile')
    opponent_profile = serializers.\
        SerializerMethodField('_opponent_profile')

    def _owner_profile(self, obj):
        return ProfileSerializer(obj.owner.profile).data

    def _opponent_profile(self, obj):
        return ProfileSerializer(obj.opponent.profile).data

    class Meta:
        model = Thread
        fields = (
            'id',
            'owner',
            'owner_profile',
            'opponent',
            'opponent_profile',
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
