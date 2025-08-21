from django.contrib import admin
from .models import ReadingList, ReadingListItem


admin.site.register(ReadingList)
admin.site.register(ReadingListItem)