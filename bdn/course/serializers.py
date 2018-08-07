from rest_framework import serializers
from bdn.category.serializers import CategorySerializer
from bdn.provider.serializers import ProviderSerializer
from bdn.skill.serializers import SkillSerializer
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
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
            'categories',
            'skills',
            'is_featured',
        )
