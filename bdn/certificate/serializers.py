from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = (
            'id',
            'user_eth_address',
            'academy_title',
            'academy_address',
            'academy_link',
            'program_title',
            'course_title',
            'course_link',
            'subject',
            'skills',
            'learner_eth_address',
            'verified',
            'ipfs_hash',
            'score',
            'duration',
            'expiration_date',
        )
