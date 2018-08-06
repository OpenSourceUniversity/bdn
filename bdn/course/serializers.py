from rest_framework import serializers
from bdn.skill.serializers import SkillSerializer
from .models import Course, Category, Provider


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            'id',
            'name',
            'eth_address',
        )


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
