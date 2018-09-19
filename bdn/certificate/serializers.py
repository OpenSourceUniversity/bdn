from django.db.models import Q
from django.utils import timezone
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
            'institution_title',
            'institution_link',
            'program_title',
            'certificate_title',
            'course_link',
            'industries',
            'skills',
            'ipfs_hash',
            'checksum_hash',
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

    holder_eth_address = serializers.\
        SerializerMethodField('_holder_eth_address')

    verifications = serializers.\
        SerializerMethodField('_verifications')

    is_expired = serializers.\
        SerializerMethodField('_is_expired')

    holder_names = serializers.\
        SerializerMethodField('_holder_names')

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
            return obj.expiration_date < timezone.now()

    def _holder_eth_address(self, obj):
        return obj.holder.username

    def _holder_names(self, obj):
        return obj.holder.profile.full_name

    class Meta:
        model = Certificate
        fields = (
            'id',
            'holder',
            'holder_names',
            'holder_eth_address',
            'user_eth_address',
            'institution_title',
            'institution_link',
            'program_title',
            'certificate_title',
            'course_link',
            'industries',
            'skills',
            'score',
            'duration',
            'expiration_date',
            'verifications',
            'ipfs_hash',
            'is_expired',
        )
