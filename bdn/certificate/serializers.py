from rest_framework import serializers
from bdn.provider.serializers import ProviderSerializer
from bdn.category.serializers import CategorySerializer
from bdn.skill.serializers import SkillSerializer
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(many=False, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

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
            'categories',
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
    skills = SkillSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

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
            'categories',
            'skills',
            'learner_eth_address',
            'ipfs_hash',
            'score',
            'duration',
            'expiration_date',
        )


class CertificateViewProfileSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(many=False, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

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
            'categories',
            'skills',
            'learner_eth_address',
            'verified',
            'score',
            'duration',
            'expiration_date',
        )
