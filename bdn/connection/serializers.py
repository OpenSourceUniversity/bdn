from rest_framework import serializers
from .models import FileUpload, Connection


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileUpload
        fields = (
            'created',
            'owner',
            'datafile',
        )


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
