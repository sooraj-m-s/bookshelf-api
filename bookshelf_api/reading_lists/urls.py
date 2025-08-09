from django.urls import path
from .views import (
    CreateReadingListView, UpdateReadingListView, DeleteReadingListView, ListReadingListsView,
    AddBookToListView, RemoveBookFromListView, ReorderListView, ListBooksInListView
)


urlpatterns = [
    path('', ListReadingListsView.as_view(), name='list_reading_lists'),
    path('create/', CreateReadingListView.as_view(), name='create_reading_list'),
    path('<int:list_id>/update/', UpdateReadingListView.as_view(), name='update_reading_list'),
    path('<int:list_id>/delete/', DeleteReadingListView.as_view(), name='delete_reading_list'),
    path('<int:list_id>/add-book/', AddBookToListView.as_view(), name='add_book_to_list'),
    path('<int:list_id>/remove-book/', RemoveBookFromListView.as_view(), name='remove_book_from_list'),
    path('<int:list_id>/reorder/', ReorderListView.as_view(), name='reorder_list'),
    path('<int:list_id>/list-books/', ListBooksInListView.as_view(), name='list_books_in_list'),
]

