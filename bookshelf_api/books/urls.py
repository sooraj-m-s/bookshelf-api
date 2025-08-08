from django.urls import path
from .views import BookListView, BookUploadView, BookDeleteView, BookEditView


urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
    path('upload/', BookUploadView.as_view(), name='book-upload'),
    path('edit/<slug:slug>/', BookEditView.as_view(), name='book-edit'),
    path('delete/<slug:slug>/', BookDeleteView.as_view(), name='book-delete'),
]

