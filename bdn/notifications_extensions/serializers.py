import json
from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_active_profile_type = serializers.\
        SerializerMethodField('_actor_active_profile_type')

    actor_name = serializers.\
        SerializerMethodField('_actor_name')

    recipient_active_profile_type = serializers.\
        SerializerMethodField('_recipient_active_profile_type')

    actor_content_type_name = serializers.\
        SerializerMethodField('_actor_content_type_name')

    action_object_content_type_name = serializers.\
        SerializerMethodField('_action_object_content_type_name')

    target_content_type_name = serializers.\
        SerializerMethodField('_target_content_type_name')

    def _actor_name(self, obj):
        profile_type = self._actor_active_profile_type(obj)
        if profile_type:
            return obj.actor.profile.name_by_profile_type(profile_type)

    def _actor_active_profile_type(self, obj):
        if obj.data:
            return obj.data.get('actor_active_profile_type')

    def _recipient_active_profile_type(self, obj):
        if obj.data:
            return obj.data.get('recipient_active_profile_type')

    def _action_object_content_type_name(self, obj):
        if not obj.action_object_content_type:
            return None
        return obj.action_object_content_type.name

    def _actor_content_type_name(self, obj):
        if not obj.actor_content_type:
            return None
        return obj.actor_content_type.name

    def _target_content_type_name(self, obj):
        if not obj.target_content_type:
            return None
        return obj.target_content_type.name

    class Meta:
        model = Notification
        fields = (
            'id',
            'level',
            'actor_content_type',
            'actor_content_type_name',
            'actor_object_id',
            'actor_active_profile_type',
            'actor_name',
            'verb',
            'description',
            'target_content_type',
            'target_content_type_name',
            'target_object_id',
            'action_object_content_type',
            'action_object_content_type_name',
            'action_object_object_id',
            'timestamp',
            'public',
            'deleted',
            'data',
            'unread',
            'timesince',
            'recipient_active_profile_type',
        )
