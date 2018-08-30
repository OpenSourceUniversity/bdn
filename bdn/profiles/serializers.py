from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from bdn.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'first_name',
            'last_name',
            'learner_email',
            'learner_position',
            'learner_specialisation',
            'learner_about',
            'public_profile',
            'learner_site',
            'phone_number',
            'learner_country',
            'learner_avatar',
            'academy_name',
            'academy_website',
            'academy_email',
            'academy_country',
            'academy_about',
            'academy_logo',
            'academy_verified',
            'company_name',
            'company_website',
            'company_email',
            'company_country',
            'company_about',
            'company_logo',
            'company_verified',
        )


class LearnerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    certificates_count = SerializerMethodField('_certificates_count')

    def _certificates_count(self, obj):
        return obj.user.certificate_set.all().count()

    class Meta:
        model = Profile
        fields = (
            'user',
            'first_name',
            'last_name',
            'learner_email',
            'learner_position',
            'learner_specialisation',
            'learner_about',
            'public_profile',
            'learner_site',
            'phone_number',
            'learner_country',
            'learner_avatar',
            'certificates_count',
        )


class AcademyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    courses_count = SerializerMethodField('_courses_count')

    def _courses_count(self, obj):
        return obj.user.provider.course_set.all().count()

    class Meta:
        model = Profile
        fields = (
            'user',
            'academy_name',
            'academy_website',
            'academy_email',
            'academy_country',
            'academy_about',
            'academy_logo',
            'academy_verified',
            'courses_count',
        )


class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    jobs_count = SerializerMethodField('_jobs_count')

    def _jobs_count(self, obj):
        return obj.user.company.job_set.all().count()

    class Meta:
        model = Profile
        fields = (
            'user',
            'company_name',
            'company_website',
            'company_email',
            'company_country',
            'company_about',
            'company_logo',
            'company_verified',
            'jobs_count',
        )
