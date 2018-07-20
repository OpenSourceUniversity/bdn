from rest_framework import serializers
from .models import Profile


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
            'learner_site',
            'phone_number',
            'learner_country',
            #'learner_avatar',
            'academy_name',
            'academy_website',
            'academy_email',
            'academy_country',
            'academy_about',
            #'academy_logo',
            'company_name',
            'company_website',
            'company_email',
            'company_country',
            'company_about',
            #'company_logo',
        )
class LearnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'learner_email',
            'learner_position',
            'learner_specialisation',
            'learner_about',
            'learner_site',
            'phone_number',
            'learner_country',
            #'learner_avatar',
        )
class AcademyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'academy_name',
            'academy_website',
            'academy_email',
            'academy_country',
            'academy_about',
            #'academy_logo',
        )
class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'company_name',
            'company_website',
            'company_email',
            'company_country',
            'company_about',
            #'company_logo',
        )