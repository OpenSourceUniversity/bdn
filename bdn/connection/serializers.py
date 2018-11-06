from rest_framework import serializers
from .models import Connection


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = (
            'owner_id',
            'full_name',
            'email',
            'company_name',
            'position_title',
            'connected_on',
            'user_id',
        )
