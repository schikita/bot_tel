from django.contrib import admin
from .models import Channel, Post

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_name', 'telegram_link', 'active', 'created_at')
    list_filter = ('active',)
    search_fields = ('channel_name', 'telegram_link')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'channel')
    search_fields = ('post_id', 'channel__channel_name')
