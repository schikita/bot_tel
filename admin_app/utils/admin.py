from django.contrib import admin
from .models import Log, Setting

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'level', 'message')
    search_fields = ('level', 'message')

@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')
    search_fields = ('key',)
