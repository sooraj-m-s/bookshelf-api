from django.contrib import admin
from django.urls import path, include


api_patterns = [
    path('', include('users.urls')),
    path('books/', include('books.urls')),
    path('reading-lists/', include('reading_lists.urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns))
]

