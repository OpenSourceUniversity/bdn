from rest_framework import serializers
from bdn.auth.serializers import UserSerializer
from .models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UserSettings
        fields = (
            'id',
            'user',
            'subscribed',
            'news_subscribed',
            'save_wallet',
        )


class UserSettingsWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = (
            'save_wallet',
            'wallet',
        )
