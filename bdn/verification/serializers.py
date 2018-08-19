from rest_framework import serializers
from bdn.certificate.serializers import CertificateSerializer
from .models import Verification


class VerificationSerializer(serializers.ModelSerializer):
    certificate = CertificateSerializer(many=False, read_only=True)

    class Meta:
        model = Verification
        fields = (
            'id',
            'certificate',
            'state',
            'granted_to',
            'verifier',
        )
