from django.contrib.auth.models import User
from rest_framework import serializers

from main_app.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'currency', 'budget_limit_notification']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, created = UserProfile.objects.update_or_create(user=user,
                                                                currency=validated_data.pop('currency'),
                                                                budget_limit_notification=validated_data.pop(
                                                                    'budget_limit_notification'))
        return profile
