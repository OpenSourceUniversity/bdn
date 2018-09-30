from rest_framework import serializers
from bdn.industry.serializers import IndustrySerializer
from bdn.company.serializers import CompanySerializer
from bdn.skill.serializers import SkillSerializer
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    industries = IndustrySerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'location',
            'salary',
            'overview',
            'skills',
            'description',
            'image_url',
            'company',
            'industries',
            'posted',
            'closes',
            'experience',
            'hours',
            'languages',
            'is_featured',
        )


class JobCreateSerializer(serializers.ModelSerializer):
    industries = IndustrySerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    company = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'location',
            'salary',
            'overview',
            'skills',
            'description',
            'image_url',
            'company',
            'industries',
            'posted',
            'closes',
            'experience',
            'hours',
            'languages',
        )
