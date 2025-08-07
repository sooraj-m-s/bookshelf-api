from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
import logging


logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def register_user(username, email, password):
        User = get_user_model()
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            raise ValidationError({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
        except IntegrityError as e:
            logger.error(f"Database error creating user: {e}")
            raise ValidationError({"error": "Unable to create user due to database error"}, code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error creating user: {e}")
            raise ValidationError({"error": "An unexpected error occurred"}, code=status.HTTP_400_BAD_REQUEST)
        
        return user

    @staticmethod
    def login_user(username, password):
        User = get_user_model()
        username = username.strip()
        password = password.strip()

        if not username or not password:
            raise ValidationError({"error": "Username and password are required"}, code=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError({"error": "Invalid username or password"}, code=status.HTTP_401_UNAUTHORIZED)

        return user

