from django.contrib.auth.models import User
from rest_framework import serializers

from main_app.models import UserProfile, Category, Transaction, Budget, Notification


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['currency', 'budget_limit_notification']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'user']
        read_only_fields = ['id', 'user']

    def validate(self, data):
        if data['type'] not in Category.CATEGORY_TYPES:
            raise serializers.ValidationError({"type": "Invalid category type. Must be 'expense' or 'income'."})
        return data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'category', 'amount', 'date', 'description', 'is_recurring', 'recurrence_period', 'user']
        read_only_fields = ['id', 'date', 'user']

    def validate(self, data):
        # Ensure that recurrence_period is provided only if `is_recurring` is True
        if data.get('is_recurring') and not data.get('recurrence_period'):
            raise serializers.ValidationError({
                'recurrence_period': 'This field is required for recurring transactions.'
            })
        if not data.get('is_recurring') and data.get('recurrence_period'):
            raise serializers.ValidationError({
                'recurrence_period': 'This field should be blank for non-recurring transactions.'
            })
        return data


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'category', 'amount', 'start_date', 'end_date', 'user']
        read_only_fields = ['id', 'user']

    def validate(self, data):
        # Ensure start_date is before end_date
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({
                'start_date': 'Start date must be before the end date.'
            })
        # Ensure budget is non-negative
        if data['amount'] < 0:
            raise serializers.ValidationError({
                'amount': 'Budget amount must be greater than zero.'
            })
        return data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'created_at', 'is_read', 'user']
        read_only_fields = ['id', 'created_at', 'user', 'message']


class NotificationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']
        extra_kwargs = {
            'is_read': {'required': True}
        }
