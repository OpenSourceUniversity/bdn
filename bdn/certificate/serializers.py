import datetime
from django.db.models import Q
from rest_framework import serializers
from bdn.industry.serializers import IndustrySerializer
from bdn.skill.serializers import SkillSerializer
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    industries = IndustrySerializer(many=True, read_only=True)

    class Meta:
        model = Certificate
        fields = (
            'id',
            'holder',
            'user_eth_address',
            'academy_title',
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
    skills = SkillSerializer(many=True, read_only=True)
    industries = IndustrySerializer(many=True, read_only=True)

    verifications = serializers.\
        SerializerMethodField('_verifications')

    is_expired = serializers.\
        SerializerMethodField('_is_expired')

    def _verifications(self, obj):
        from bdn.verification.serializers import VerificationCertificateSerializer  # noqa
        verifiers = obj.verification_set.all().filter(
            Q(state='verified') | Q(state='revoked'))
        verifier_list = verifiers.values_list(
            'verifier', flat=True).distinct()
        group_by_verifier = []
        for verifier in verifier_list:
            group_by_verifier.append(VerificationCertificateSerializer(
                        verifiers.filter(
                            verifier=verifier).order_by('date_last_modified'),
                        many=True, read_only=True).data)
        return group_by_verifier

    def _is_expired(self, obj):
        if obj.expiration_date:
            return obj.expiration_date.replace(tzinfo=None) < datetime.\
                datetime.now().replace(tzinfo=None)

    class Meta:
        model = Certificate
        fields = (
            'id',
            'user_eth_address',
            'academy_title',
            'academy_link',
            'program_title',
            'course_title',
            'course_link',
            'industries',
            'skills',
            'learner_eth_address',
            'score',
            'duration',
            'expiration_date',
            'verifications',
            'is_expired',
        )
