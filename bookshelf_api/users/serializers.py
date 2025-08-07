from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from .services import UserService



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True, 'min_length': 4},
        }

    def validate_username(self, value):
        value = value.strip()
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise serializers.ValidationError("Username must contain only letters and spaces")
        return value

    def validate_email(self, value):
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
            raise serializers.ValidationError("Invalid email format")
        return value

    def validate_password(self, value):
        value = value.strip()
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', value):
            raise serializers.ValidationError("Password must contain at least one special character")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Password must contain at least one number")
        return value

    def create(self, validated_data):
        return UserService.register_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

