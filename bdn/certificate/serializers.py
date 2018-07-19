from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = (
            'user_eth_address',
            'uid',
            'index',
            'academy',
            'course',
            'learner',
            'name',
            'subject',
            'skills',
            'verified',
            'score',
            'creator',
            'expiration_date',
        )
