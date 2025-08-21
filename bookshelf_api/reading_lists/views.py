from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import permission_classes
import logging
from books.models import Books
from .models import ReadingList
from .services import ReadingListService
from .serializers import (
    ReadingListSerializer, ReadingListCreateSerializer, ReadingListUpdateSerializer, AddBookToListSerializer,
    RemoveBookFromListSerializer, ReorderListSerializer, ReadingListItemSerializer
)


logger = logging.getLogger(__name__)

@permission_classes([IsAuthenticated])
class CreateReadingListView(APIView):
    def post(self, request):
        try:
            serializer = ReadingListCreateSerializer(data=request.data)
            if serializer.is_valid():
                reading_list = ReadingListService.create_reading_list(request.user, serializer.validated_data['name'])
                return Response({'message': 'Reading list created', 'id': reading_list.id}, status=201)
                
            return Response(serializer.errors, status=400)
        except ValidationError as e:
            logger.error(f"Validation error during reading list creation: {e}")
            return Response({'error': e.detail}, status=e.status_code)
        except Exception as e:
            logger.error(f"Error creating reading list: {e}")
            return Response({'error': 'Internal server error'}, status=500)


@permission_classes([IsAuthenticated])
class UpdateReadingListView(APIView):
    def put(self, request, list_id):
        try:
            reading_list = ReadingList.objects.get(user=request.user, id=list_id)
            serializer = ReadingListUpdateSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.update(reading_list, serializer.validated_data)
                return Response({'message': 'Reading list updated'}, status=200)
            
            return Response(serializer.errors, status=400)
        except ReadingList.DoesNotExist:
            logger.error(f"Reading list not found: {list_id}")
            return Response({'error': 'Reading list not found'}, status=404)
        except Exception as e:
            logger.error(f"Error updating reading list: {e}")
            return Response({'error': 'Internal server error'}, status=500)


@permission_classes([IsAuthenticated])
class DeleteReadingListView(APIView):
    def delete(self, request, list_id):
        try:
            reading_list = ReadingList.objects.get(user=request.user, id=list_id)
            reading_list.delete()
            return Response({'message': 'Reading list deleted'}, status=200)
        except ReadingList.DoesNotExist:
            logger.error(f"Reading list not found for deletion: {list_id}")
            return Response({'error': 'Reading list not found'}, status=404)
        except Exception as e:
            logger.error(f"Error deleting reading list: {e}")
            return Response({'error': 'Internal server error'}, status=500)


@permission_classes([IsAuthenticated])
class ListReadingListsView(APIView):
    def get(self, request):
        try:
            reading_lists = ReadingList.objects.filter(user=request.user)
            serializer = ReadingListSerializer(reading_lists, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error listing reading lists: {e}")
            return Response({'error': 'Internal server error'}, status=500)


@permission_classes([IsAuthenticated])
class AddBookToListView(APIView):
    def post(self, request, list_id):
        try:
            reading_list = ReadingList.objects.get(user=request.user, id=list_id)
            serializer = AddBookToListSerializer(data=request.data)
            if serializer.is_valid():
                book_id = serializer.validated_data['book_id']
                listing_order = serializer.validated_data.get('listing_order')
                ReadingListService.add_book_to_list(reading_list, book_id, listing_order)

                return Response({'message': 'Book added to list'}, status=201)
            return Response(serializer.errors, status=400)
        except ReadingList.DoesNotExist:
            return Response({'error': 'Reading list not found'}, status=404)
        except Books.DoesNotExist:
            logger.error(f"Book not found: {book_id}")
            return Response({'error': 'Book not found'}, status=404)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return Response({'error': e.detail}, status=e.status_code)
        except Exception as e:
            logger.error(f"Unexpected error adding book to list: {e}")
            return Response({'error': 'Internal server error'}, status=500)


@permission_classes([IsAuthenticated])
class RemoveBookFromListView(APIView):
    def delete(self, request, list_id):
        try:
            reading_list = ReadingList.objects.get(user=request.user, id=list_id)
            serializer = RemoveBookFromListSerializer(data=request.data)
            if serializer.is_valid():
                book_id = serializer.validated_data['book_id']
                book = Books.objects.get(id=book_id)
                ReadingListService.remove_book_from_list(reading_list, book)

                return Response({'message': 'Book removed from list'}, status=200)
            return Response(serializer.errors, status=400)
        
        except ReadingList.DoesNotExist:
            return Response({'error': 'Reading list not found or inaccessible'}, status=404)
        except Books.DoesNotExist:
            logger.error(f"Book not found: {book_id}")
            return Response({'error': 'Book not found'}, status=404)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            return Response({'error': e.detail}, status=400)
        except Exception as e:
            logger.error(f"Unexpected error removing book from list: {e}")
            return Response({'error': 'Internal server error'}, status=500)


@permission_classes([IsAuthenticated])
class ReorderListView(APIView):
    def patch(self, request, list_id):
        try:
            reading_list = ReadingList.objects.get(user=request.user, id=list_id)
            serializer = ReorderListSerializer(data=request.data)
            if serializer.is_valid():
                book_ids = serializer.validated_data['book_ids']
                ReadingListService.reorder_list(reading_list, book_ids)

                return Response({'message': 'List reordered'}, status=200)
            return Response(serializer.errors, status=400)
        
        except ReadingList.DoesNotExist:
            return Response({'error': 'Reading list not found'}, status=404)
        except ValidationError as e:
            return Response({'error': e.detail}, status=e.status_code)
        except Exception as e:
            logger.error(f"Unexpected error reordering list: {e}")
            return Response({'error': 'Internal server error'}, status=500)


@permission_classes([IsAuthenticated])
class ListBooksInListView(APIView):
    def get(self, request, list_id):
        try:
            reading_list = ReadingList.objects.get(user=request.user, id=list_id)
            page = request.query_params.get('page', 1)
            page_size = request.query_params.get('page_size', 10)
            page_obj = ReadingListService.get_paginated_items(reading_list, int(page), int(page_size))
            serializer = ReadingListItemSerializer(page_obj.object_list, many=True)
            return Response({
                'count': page_obj.paginator.count,
                'next': page_obj.next_page_number() if page_obj.has_next() else None,
                'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
                'results': serializer.data
            })
        
        except ReadingList.DoesNotExist:
            return Response({'error': 'Reading list not found'}, status=404)
        except ValidationError as e:
            return Response({'error': e.detail}, status=e.status_code)
        except Exception as e:
            logger.error(f"Error listing books: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=500)

