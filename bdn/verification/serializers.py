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
