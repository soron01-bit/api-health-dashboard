from django.contrib import admin
from .models import DataEntry


@admin.register(DataEntry)
class DataEntryAdmin(admin.ModelAdmin):
	list_display = ('date', 'title', 'category', 'value', 'status')
	list_filter = ('status', 'category', 'date')
	search_fields = ('title', 'category', 'notes')
