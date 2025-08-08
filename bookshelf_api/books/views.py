from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
import logging
from .models import Books
from .services import BookService
from .serializers import BookSerializer, BookUploadSerializer


logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@permission_classes([IsAuthenticated])
class BookListView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
    pagination_class = StandardResultsSetPagination


@permission_classes([IsAuthenticated])
class BookUploadView(APIView):
    def post(self, request):
        try:
            serializer = BookUploadSerializer(data=request.data)
            if serializer.is_valid():
                book = BookService.create_book(validated_data=serializer.validated_data, user=request.user)
                return Response(
                    {
                        'message': 'Book uploaded successfully',
                        'book': {
                            'id': book.id,
                            'title': book.title,
                            'slug': book.slug
                        }
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            logger.error(f"Validation error during book upload: {e}")
            return Response({'error': e.detail}, status=e.status_code)
        except Exception as e:
            logger.error(f"Unexpected error during book upload: {e}")
            return Response({'error': 'An unexpected error occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

