from rest_framework import serializers
from .models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = (
            'id',
            'user',
            'subscribed',
            'news_subscribed',
            'wallet',
            'save_wallet',
        )


class UserSettingsWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = (
            'wallet',
        )
