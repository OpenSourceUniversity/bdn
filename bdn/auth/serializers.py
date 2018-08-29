from rest_framework import serializers
from .models import SignUp


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUp
        fields = (
            'id',
            'email',
            'step',
        )
