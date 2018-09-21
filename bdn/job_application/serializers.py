from rest_framework import serializers
from bdn.job.serializers import JobSerializer
from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(many=False, read_only=True)
    issuer_eth_address = serializers.\
        SerializerMethodField('_issuer_eth_address')

    def _issuer_eth_address(self, obj):
        return obj.issuer.username

    class Meta:
        model = JobApplication
        fields = (
            'id',
            'job',
            'issuer',
            'issuer_eth_address',
            'state',
            'date_created',
            'date_last_modified',
        )
