from rest_framework import serializers
from .models import Verification


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = (
            'id',
            'certificate',
            'state',
            'granted_to',
        )
