from rest_framework import serializers
from bdn.job.serializers import JobSerializer
from bdn.certificate.models import Certificate
from bdn.certificate.serializers import CertificateViewProfileSerializer
from bdn.profiles.serializers import (
    LearnerProfileSerializer, CompanyProfileSerializer)
from .models import JobApplication


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = (
            'id',
            'job',
            'issuer',
            'state',
            'date_created',
            'date_last_modified',
        )


class JobApplicationViewSerializer(serializers.ModelSerializer):
    job = JobSerializer(many=False, read_only=False)
    issuer_eth_address = serializers.\
        SerializerMethodField('_issuer_eth_address')
    certificates = serializers.\
        SerializerMethodField('_certificates')
    issuer_profile = serializers.\
        SerializerMethodField('_issuer_profile')

    def _issuer_eth_address(self, obj):
        return obj.issuer.username

    def _issuer_profile(self, obj):
        return LearnerProfileSerializer(
            obj.issuer.profile, read_only=True).data

    def _certificates(self, obj):
        certificates = Certificate.objects.all().filter(
            holder=obj.issuer)
        return CertificateViewProfileSerializer(
            certificates, many=True, read_only=True).data

    class Meta:
        model = JobApplication
        fields = (
            'id',
            'job',
            'issuer',
            'issuer_profile',
            'certificates',
            'issuer_eth_address',
            'state',
            'date_created',
            'date_last_modified',
        )


class JobApplicationLearnerViewSerializer(serializers.ModelSerializer):
    job = JobSerializer(many=False, read_only=False)
    company_eth_address = serializers.\
        SerializerMethodField('_company_eth_address')
    certificates = serializers.\
        SerializerMethodField('_certificates')
    company_profile = serializers.\
        SerializerMethodField('_company_profile')

    def _company_eth_address(self, obj):
        return obj.job.company.user.username

    def _company_profile(self, obj):
        return CompanyProfileSerializer(
            obj.job.company.user.profile, read_only=True).data

    def _certificates(self, obj):
        certificates = Certificate.objects.all().filter(
            holder=obj.issuer)
        return CertificateViewProfileSerializer(
            certificates, many=True, read_only=True).data

    class Meta:
        model = JobApplication
        fields = (
            'id',
            'job',
            'issuer',
            'company_profile',
            'certificates',
            'company_eth_address',
            'state',
            'date_created',
            'date_last_modified',
        )
