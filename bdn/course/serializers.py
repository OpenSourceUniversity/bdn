from rest_framework import serializers
from bdn.industry.serializers import IndustrySerializer
from bdn.provider.serializers import ProviderSerializer
from bdn.skill.serializers import SkillSerializer
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    industries = IndustrySerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    provider = ProviderSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'external_link',
            'image_url',
            'provider',
            'tutor',
            'industries',
            'skills',
            'is_featured',
        )


class CourseCreateSerializer(serializers.ModelSerializer):
    industries = IndustrySerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    provider = ProviderSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'external_link',
            'image_url',
            'provider',
            'tutor',
            'industries',
            'skills',
        )
