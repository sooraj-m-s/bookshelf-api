from rest_framework import serializers
from PIL import Image, UnidentifiedImageError
from datetime import date
import logging
from .models import Books


logger = logging.getLogger(__name__)

class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Books
        fields = ['id', 'title', 'author', 'genre', 'published_date', 'is_available', 'slug']

    def get_author(self, obj):
        return obj.author.username

    def get_genre(self, obj):
        return obj.genre.name


class BookUploadSerializer(serializers.ModelSerializer):
    cover_image = serializers.ImageField(required=False)
    genre = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Books
        fields = ['title', 'description', 'pages', 'genre', 'published_date', 'cover_image', 'is_available']
        extra_kwargs = {
            'title': {'required': True, 'max_length': 255},
            'cover_image': {'required': False},
            'pages': {'required': True},
            'published_date': {'required': True},
            'description': {'required': False},
            'is_available': {'required': False},
        }

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty")
        if Books.objects.filter(title=value).exists():
            raise serializers.ValidationError("A book with this title already exists")
        return value

    def validate_pages(self, value):
        if value <= 0:
            raise serializers.ValidationError("Pages cannot be less than 1")
        return value

    def validate_published_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Published date cannot be in the future")
        return value

    def validate_cover_image(self, value):
        max_size_bytes = 5 * 1024 * 1024
        if getattr(value, "size", 0) > max_size_bytes:
            raise serializers.ValidationError("Image file size must be less than 5MB")

        original_pos = 0
        if hasattr(value, "tell"):
            try:
                original_pos = value.tell()
            except Exception:
                pass

        try:
            try:
                value.seek(0)
            except Exception:
                pass

            img = Image.open(value)
            img.verify()

            try:
                value.seek(0)
            except Exception:
                pass

            img2 = Image.open(value)
            PIL_ALLOWED_FORMATS = {"JPEG", "PNG", "GIF", "WEBP", "BMP", "TIFF"}
            if img2.format not in PIL_ALLOWED_FORMATS:
                raise serializers.ValidationError(f"Invalid image format: {img2.format}.")
        except (UnidentifiedImageError, OSError) as e:
            raise serializers.ValidationError(f"Invalid image file: {e}")
        finally:
            try:
                value.seek(original_pos)
            except Exception:
                try:
                    value.seek(0)
                except Exception:
                    pass
        return value

    def validate_genre(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Genre cannot be empty")
        if len(value) > 100:
            raise serializers.ValidationError("Genre name must be 100 characters or less")
        return value

