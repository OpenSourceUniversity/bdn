from rest_framework import serializers
from bdn.category.serializers import CategorySerializer
from bdn.company.serializers import CompanySerializer
from bdn.skill.serializers import SkillSerializer
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
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
            'external_link',
            'image_url',
            'company',
            'categories',
            'posted',
            'closes',
            'experience',
            'hours',
            'job_type',
            'languages',
            'is_featured',
        )
