from rest_framework import serializers
from .models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    eth_address = serializers.\
        SerializerMethodField('_eth_address')

    def _eth_address(self, obj):
        return obj.user.username

    class Meta:
        model = Provider
        fields = (
            'id',
            'name',
            'user',
            'eth_address',
            'verified',
        )
