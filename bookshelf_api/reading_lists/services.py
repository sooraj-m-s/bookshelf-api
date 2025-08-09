from django.db import transaction, IntegrityError
from django.db.models import F, Max
from rest_framework.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage
import logging
from .models import ReadingList, ReadingListItem


logger = logging.getLogger(__name__)

class ReadingListService:
    @staticmethod
    def create_reading_list(user, name):
        try:
            return ReadingList.objects.create(user=user, name=name)
        except IntegrityError:
            logger.error(f"Failed to create reading list: {name}")
            raise ValidationError("A reading list with this name already exists.")

    @staticmethod
    def add_book_to_list(reading_list, book, listing_order=None):
        if ReadingListItem.objects.filter(reading_list=reading_list, book=book).exists():
            raise ValidationError("Book already in list.")
        try:
            with transaction.atomic():
                if listing_order is not None:
                    ReadingListItem.objects.filter(
                        reading_list=reading_list,
                        listing_order__gte=listing_order
                    ).update(listing_order=F('listing_order') + 1)
                    ReadingListItem.objects.create(reading_list=reading_list, book=book, listing_order=listing_order)
                else:
                    max_order = ReadingListItem.objects.filter(reading_list=reading_list).aggregate(Max('listing_order'))['listing_order__max']
                    new_order = (max_order or 0) + 1
                    ReadingListItem.objects.create(reading_list=reading_list, book=book, listing_order=new_order)

        except IntegrityError:
            logger.error(f"Failed to add book to list: {book.id}")
            raise ValidationError("Failed to add book to list due to an unexpected error.")

    @staticmethod
    def remove_book_from_list(reading_list, book):
        try:
            item = ReadingListItem.objects.get(reading_list=reading_list, book=book)
            order = item.listing_order
            item.delete()
            ReadingListItem.objects.filter(reading_list=reading_list, listing_order__gt=order).update(listing_order=F('listing_order') - 1)
        except ReadingListItem.DoesNotExist:
            logger.error(f"Failed to remove book from list: {book.id}")
            raise ValidationError("Book not in list.")
        except Exception as e:
            logger.error(f"Unexpected error removing book from list: {e}")
            raise ValidationError("Internal server error")

    @staticmethod
    def reorder_list(reading_list, book_ids):
        try:
            current_items = ReadingListItem.objects.filter(reading_list=reading_list)
            current_book_ids = [item.book_id for item in current_items]
            if set(book_ids) != set(current_book_ids):
                raise ValidationError("Provided book IDs do not match the list.")
            with transaction.atomic():
                for order, book_id in enumerate(book_ids, start=1):
                    ReadingListItem.objects.filter(reading_list=reading_list, book_id=book_id).update(listing_order=order)
        
        except ValidationError as e:
            logger.error(f"Validation error during reordering: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error reordering list: {e}")
            raise ValidationError("Failed to reorder list due to an unexpected error")

    @staticmethod
    def get_paginated_items(reading_list, page, page_size):
        items = ReadingListItem.objects.filter(reading_list=reading_list).order_by('listing_order')
        paginator = Paginator(items, page_size)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            raise ValidationError("Page not found.")
        return page_obj

