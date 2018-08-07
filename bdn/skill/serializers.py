from rest_framework import serializers
from bdn.skill.models import Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = (
            'id',
            'name',
            'standardized',
        )
