from django.urls import path
from .views import RegisterUserView, UserLoginView, UserProfileView, RefreshTokenView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]

