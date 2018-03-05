from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = (
            'uid',
            'index',
            'academy',
            'course',
            'learner',
            'name',
            'subject',
            'verified',
            'score',
            'creator',
            'expiration_date',
        )
