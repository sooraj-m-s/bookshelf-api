from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
import logging
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .services import UserService


logger = logging.getLogger(__name__)

@permission_classes([AllowAny])
class RegisterUserView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as e:
            logger.error(f"Authentication error during registration: {e}")
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error during user registration: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([AllowAny])
class UserLoginView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = UserService.login_user(
                    username=serializer.validated_data['username'],
                    password=serializer.validated_data['password']
                )
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'user': {
                        'username': user.username,
                        'email': user.email
                    },
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error during user login: {e}")
            return Response({'error': e.detail['error']}, status=e.status_code)
        except Exception as e:
            logger.error(f"Unexpected error during user login: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

