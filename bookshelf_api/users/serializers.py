from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
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


class UserProfileSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'new_password']
        extra_kwargs = {
            'username': {'required': True, 'min_length': 4},
            'email': {'required': True},
        }

    def validate_username(self, value):
        if value is not None:
            value = value.strip()
            if not re.match(r'^[a-zA-Z\s]+$', value):
                raise serializers.ValidationError("Username must contain only letters and spaces")
        return value

    def validate_email(self, value):
        if value is not None:
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', value):
                raise serializers.ValidationError("Invalid email format")
        return value
    
    def validate_new_password(self, value):
        value = value.strip()
        if value is not None:
            if not re.search(r'[A-Z]', value):
                raise serializers.ValidationError("Password must contain at least one uppercase letter")
            if not re.search(r'[a-z]', value):
                raise serializers.ValidationError("Password must contain at least one lowercase letter")
            if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:"\\|,.<>\/?]', value):
                raise serializers.ValidationError("Password must contain at least one special character")
            if not re.search(r'[0-9]', value):
                raise serializers.ValidationError("Password must contain at least one number")
        return value

    def validate(self, data):
        user = self.instance
        if not any(key in data for key in ['username', 'email', 'new_password']):
            raise serializers.ValidationError("At least one field (username, email, or new_password) is required")
        if 'username' in data and get_user_model().objects.filter(username=data['username']).exclude(id=user.id).exists():
            raise serializers.ValidationError("This username is already taken")
        if 'email' in data and get_user_model().objects.filter(email=data['email']).exclude(id=user.id).exists():
            raise serializers.ValidationError("This email is already in use")
        
        return data

    def update(self, instance, validated_data):
        user = instance
        if 'username' in validated_data:
            user.username = validated_data['username']
        if 'email' in validated_data:
            user.email = validated_data['email']
        if 'new_password' in validated_data:
            user.set_password(validated_data['new_password'])
        user.save()

        return user

