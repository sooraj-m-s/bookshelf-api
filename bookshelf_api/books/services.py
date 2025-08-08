import cloudinary.uploader
import logging
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Books, Genre
from decouple import config
from .models import Books


logger = logging.getLogger(__name__)

class BookService:
    @staticmethod
    def create_book(validated_data, user):
        try:
            cover_image = validated_data.pop('cover_image', None)
            genre_name = validated_data.pop('genre')
            cover_image_url = None

            genre, _ = Genre.objects.get_or_create(
                name=genre_name,
                defaults={'name': genre_name}
            )

            # Image upload to Cloudinary
            if cover_image:
                try:
                    upload_result = cloudinary.uploader.upload(
                        cover_image,
                        upload_preset=config('cloudinary_upload_preset'),
                        resource_type='image'
                    )
                    cover_image_url = upload_result['secure_url']
                except Exception as e:
                    logger.error(f"Cloudinary upload failed: {e}")
                    raise ValidationError({"error": "Failed to upload cover image"}, code=status.HTTP_400_BAD_REQUEST)

            book = Books.objects.create(
                author=user,
                title=validated_data['title'],
                description=validated_data.get('description', ''),
                pages=validated_data['pages'],
                genre=genre,
                published_date=validated_data['published_date'],
                is_available=validated_data.get('is_available', True),
                cover_image=cover_image_url,
            )
            
            return book
        except Exception as e:
            logger.error(f"Error creating book: {e}")
            raise ValidationError({"error": "Failed to create book due to an unexpected error"}, code=status.HTTP_400_BAD_REQUEST)

