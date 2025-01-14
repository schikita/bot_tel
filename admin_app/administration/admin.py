from django.contrib import admin
from .models import SearchWord, Admin

@admin.register(SearchWord)
class SearchWordAdmin(admin.ModelAdmin):
    list_display = ('word', 'lemma', 'admin')
    search_fields = ('word', 'lemma')

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('telegram_id',)
    search_fields = ('telegram_id',)
