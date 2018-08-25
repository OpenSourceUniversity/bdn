from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    eth_address = serializers.\
        SerializerMethodField('_eth_address')

    def _eth_address(self, obj):
        return obj.user.username

    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'user',
            'eth_address',
            'verified',
        )
