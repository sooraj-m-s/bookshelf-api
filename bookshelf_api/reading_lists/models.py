from django.db import models


class ReadingList(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey('users.Users', to_field='id', on_delete=models.CASCADE, related_name='reading_lists')

    class Meta:
        verbose_name = 'Reading List'
        verbose_name_plural = 'Reading Lists'


class ReadingListItem(models.Model):
    reading_list = models.ForeignKey(ReadingList, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey('books.Books', on_delete=models.CASCADE, related_name='reading_list_items')
    listing_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reading List Item'
        verbose_name_plural = 'Reading List Items'
        ordering = ['listing_order', '-updated_at']

