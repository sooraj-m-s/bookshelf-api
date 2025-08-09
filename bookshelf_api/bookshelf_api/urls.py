from django.contrib import admin
from django.urls import path, include

# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi


# schema_view = get_schema_view(
#     openapi.Info(
#         title="Bookshelf API",
#         default_version='v1',
#         description="API for managing books and reading lists",
#     ),
#     public=True,
#     permission_classes=[permissions.AllowAny],
# )


api_patterns = [
    path('', include('users.urls')),
    path('books/', include('books.urls')),
    path('reading-lists/', include('reading_lists.urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),

    # Documentation URL
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

