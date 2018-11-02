from rest_framework import serializers
from bdn.certificate.serializers import CertificateSerializer
from .models import Verification


class VerificationSerializer(serializers.ModelSerializer):
    certificate = CertificateSerializer(many=False, read_only=True)
    granted_to_eth_address = serializers.\
        SerializerMethodField('_granted_to_eth_address')
    verifier_eth_address = serializers.\
        SerializerMethodField('_verifier_eth_address')

    def _granted_to_eth_address(self, obj):
        return obj.granted_to.username

    def _verifier_eth_address(self, obj):
        return obj.verifier.username

    class Meta:
        model = Verification
        fields = (
            'id',
            'certificate',
            'state',
            'granted_to',
            'granted_to_eth_address',
            'verifier',
            'verifier_eth_address',
        )


class VerificationCertificateSerializer(serializers.ModelSerializer):
    verifier_eth_address = serializers.\
        SerializerMethodField('_verifier_eth_address')

    verifier_name = serializers.\
        SerializerMethodField('_verifier_name')

    def _verifier_eth_address(self, obj):
        return obj.verifier.username

    def _verifier_name(self, obj):
        profile_type = obj.verifier_type
        if profile_type:
            return obj.verifier.profile.name_by_profile_type(profile_type)

    class Meta:
        model = Verification
        fields = (
            'id',
            'state',
            'verifier_type',
            'verifier_name',
            'verifier_eth_address',
            'date_last_modified',
            'tx_hash',
        )


class VerificationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Verification
        fields = (
            'id',
            'certificate',
            'state',
            'granted_to',
            'granted_to_type',
            'verifier',
            'verifier_type',
        )
