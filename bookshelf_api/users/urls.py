from django.urls import path
from .views import health_check, RegisterUserView, UserLoginView, UserProfileView, RefreshTokenView


urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]

