from rest_framework import serializers
from .models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    eth_address = serializers.\
        SerializerMethodField('_eth_address')

    academy_url = serializers.\
        SerializerMethodField('_academy_url')

    def _eth_address(self, obj):
        if obj.user:
            return obj.user.username

    def _academy_url(self, obj):
        if obj.user:
            return obj.user.profile.academy_website

    class Meta:
        model = Provider
        fields = (
            'id',
            'name',
            'user',
            'academy_url',
            'eth_address',
            'verified',
        )
