from rest_framework import status
from rest_framework.exceptions import ValidationError
from decouple import config
from django.db import transaction
from django.utils.text import slugify
import cloudinary.uploader, logging
from .models import Books, Genre
from .models import Books


logger = logging.getLogger(__name__)

class BookService:
    @staticmethod
    def create_book(validated_data, user):
        try:
            cover_image = validated_data.pop('cover_image', None)
            genre_name = validated_data.pop('genre')
            cover_image_url = None

            with transaction.atomic():
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
                    cover_image=cover_image_url,
                )
                
                return book
        except Exception as e:
            logger.error(f"Error creating book: {e}")
            raise ValidationError({"error": "Failed to create book due to an unexpected error"}, code=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def update_book(slug, validated_data, user):
        with transaction.atomic():
            try:
                book = Books.objects.filter(is_deleted=False).get(slug=slug)

                if book.author.id != user.id:
                    raise ValidationError({"error": "You are not authorized to update this book"}, code=status.HTTP_403_FORBIDDEN)

                update_fields = {}
                for field, value in validated_data.items():
                    if field == 'genre':
                        genre, _ = Books.objects.get_or_create(name=value, defaults={'name': value})
                        update_fields['genre'] = genre
                    elif field == 'cover_image':
                        if value:
                            try:
                                upload_result = cloudinary.uploader.upload(
                                    value,
                                    upload_preset=config('cloudinary_upload_preset'),
                                    resource_type='image'
                                )
                                new_cover_image_url = upload_result['secure_url']
                                # Delete old image if it exists
                                if book.cover_image:
                                    cloudinary.uploader.destroy(
                                        cloudinary.CloudinaryImage(book.cover_image).public_id,
                                        invalidate=True
                                    )
                                update_fields['cover_image'] = new_cover_image_url
                            except Exception as e:
                                logger.error(f"Cloudinary upload failed: {e}")
                                raise ValidationError({"error": "Failed to upload cover image"}, code=status.HTTP_400_BAD_REQUEST)
                    else:
                        update_fields[field] = value

                for field, value in update_fields.items():
                    setattr(book, field, value)
                    if field == 'title':
                        book.slug = slugify(value)
                book.save()
                return book
            except Books.DoesNotExist:
                logger.warning(f"Book not found or already deleted with slug: {slug}")
                raise ValidationError({"error": "Book not found or already deleted"}, code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Error updating book with slug {slug}: {str(e)}")
                raise ValidationError({"error": f"An unexpected error occurred: {str(e)}"}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def delete_book(slug, user):
        with transaction.atomic():
            try:
                book = Books.objects.filter(is_deleted=False).get(slug=slug)

                if book.author.id != user.id:
                    logger.warning(f"Unauthorized delete attempt on book {book.title} by user {user.username}")
                    raise ValidationError({"error": "You are not authorized to delete this book"}, code=status.HTTP_403_FORBIDDEN)

                book.is_deleted = True
                book.save()
                return book
            except Books.DoesNotExist:
                logger.warning(f"Book not found or already deleted with slug: {slug}")
                raise ValidationError({"error": "Book not found"}, code=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                logger.error(f"Error deleting book with slug {slug}: {str(e)}")
                raise ValidationError({"error": f"An unexpected error occurred: {str(e)}"}, code=status.HTTP_500_INTERNAL_SERVER_ERROR)

