from rest_framework import serializers
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


class NotificationSerializer(serializers.ModelSerializer):
    action_object_content_type_interpretation = serializers.\
        SerializerMethodField('content_type_interpretator')

    def content_type_interpretator(self, obj):
        return ContentType.objects.get_for_id(
            id=obj.action_object_content_type.id).name

    class Meta:
        model = Notification
        fields = (
            'id',
            'level',
            'actor_content_type',
            'actor_object_id',
            'verb',
            'description',
            'target_content_type',
            'target_object_id',
            'action_object_content_type',
            'action_object_content_type_interpretation',
            'action_object_object_id',
            'timestamp',
            'public',
            'deleted',
            'data',
            'unread',
        )
