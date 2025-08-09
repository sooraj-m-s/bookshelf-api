from rest_framework import serializers
from books.serializers import BookSerializer
from .models import ReadingList, ReadingListItem


class ReadingListItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = ReadingListItem
        fields = ['id', 'book', 'listing_order']


class ReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ['id', 'name']


class ReadingListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ['name']


class ReadingListUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ['name']


class AddBookToListSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    listing_order = serializers.IntegerField(required=False, min_value=1)


class RemoveBookFromListSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()


class ReorderListSerializer(serializers.Serializer):
    book_ids = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    def validate_book_ids(self, value):
        if len(value) != len(set(value)):
            raise serializers.ValidationError("Book IDs must be unique.")
        return value

