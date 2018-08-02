from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
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
            # 'learner_avatar',
            'academy_name',
            'academy_website',
            'academy_email',
            'academy_country',
            'academy_about',
            # 'academy_logo',
            'company_name',
            'company_website',
            'company_email',
            'company_country',
            'company_about',
            # 'company_logo',
        )


class LearnerProfileSerializer(serializers.ModelSerializer):
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
            # 'learner_avatar',
        )


class AcademyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'academy_name',
            'academy_website',
            'academy_email',
            'academy_country',
            'academy_about',
            # 'academy_logo',
        )


class CompanyProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'company_name',
            'company_website',
            'company_email',
            'company_country',
            'company_about',
            # 'company_logo',
        )
