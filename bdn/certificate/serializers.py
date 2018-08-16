from rest_framework import serializers
from bdn.provider.serializers import ProviderSerializer
from bdn.industry.serializers import IndustrySerializer
from bdn.skill.serializers import SkillSerializer
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(many=False, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    industries = IndustrySerializer(many=True, read_only=True)

    class Meta:
        model = Certificate
        fields = (
            'id',
            'user_eth_address',
            'academy_title',
            'provider',
            'academy_link',
            'program_title',
            'course_title',
            'course_link',
            'industries',
            'skills',
            'learner_eth_address',
            'verified',
            'verification_tx',
            'ipfs_hash',
            'score',
            'duration',
            'expiration_date',
        )

    def to_internal_value(self, data):
        if data.get('score', None) == '':
            data.pop('score')
        if data.get('duration', None) == '':
            data.pop('duration')
        return super(CertificateSerializer, self).to_internal_value(data)


class CertificateViewProfileSerializer(serializers.ModelSerializer):
    provider = ProviderSerializer(many=False, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    industries = IndustrySerializer(many=True, read_only=True)

    class Meta:
        model = Certificate
        fields = (
            'id',
            'user_eth_address',
            'academy_title',
            'provider',
            'academy_link',
            'program_title',
            'course_title',
            'course_link',
            'industries',
            'skills',
            'learner_eth_address',
            'verified',
            'score',
            'duration',
            'expiration_date',
        )
