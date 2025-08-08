from django.urls import path
from .views import BookListView, BookUploadView


urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('upload/', BookUploadView.as_view(), name='book-upload'),
]

