from rest_framework import serializers
from .models import SignUp, User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignUp
        fields = (
            'id',
            'email',
            'step',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
        )
