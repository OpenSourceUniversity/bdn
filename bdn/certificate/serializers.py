from rest_framework import serializers
from .models import Certificate
from bdn.course.serializers import ProviderSerializer


class CertificateSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(many=False, read_only=True)

    class Meta:
        model = Certificate
        fields = (
            'id',
            'user_eth_address',
            'academy_title',
            'academy_address',
            'provider',
            'academy_link',
            'program_title',
            'course_title',
            'course_link',
            'subject',
            'skills',
            'learner_eth_address',
            'verified',
            'verification_tx',
            'ipfs_hash',
            'score',
            'duration',
            'expiration_date',
        )


class CertificateLearnerSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(many=False, read_only=True)

    class Meta:
        model = Certificate
        fields = (
            'id',
            'user_eth_address',
            'academy_title',
            'academy_address',
            'provider',
            'academy_link',
            'program_title',
            'course_title',
            'course_link',
            'subject',
            'skills',
            'learner_eth_address',
            'ipfs_hash',
            'score',
            'duration',
            'expiration_date',
        )

class CertificateViewProfileSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(many=False, read_only=True)

    class Meta:
        model = Certificate
        fields = (
            'id',
            'user_eth_address',
            'academy_title',
            'academy_address',
            'provider',
            'academy_link',
            'program_title',
            'course_title',
            'course_link',
            'subject',
            'skills',
            'learner_eth_address',
            'verified',
            'score',
            'duration',
            'expiration_date',
        )
