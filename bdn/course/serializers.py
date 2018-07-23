from rest_framework import serializers
from .models import Course, Skill, Category, Provider, Department


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            'id',
            'name',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = (
            'id',
            'name',
            'eth_address',
        )


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = (
            'id',
            'name',
        )


class CourseSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    provider = ProviderSerializer(many=False, read_only=True)
    department = DepartmentSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id',
            'title',
            'description',
            'external_link',
            'image_url',
            'provider',
            'department',
            'tutor',
            'categories',
            'skills',
            'is_featured',
        )
