from rest_framework import serializers
from .models import Connections, FileUpload


class ConnectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connections
        fields = (
            'contacts_holder',
            'first_name',
            'last_name',
            'email_address',
            'company_name',
            'position_title',
            'connected_on',
        )


class FileUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileUpload
        fields = (
            'created',
            'owner',
            'datafile',
        )
