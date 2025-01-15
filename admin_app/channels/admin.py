from django.contrib import admin
from .models import Channel, Post

@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ("url", "name", "is_active", "created_at", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("url", "name")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'channel')
    search_fields = ('post_id', 'channel__name', 'channel__url')

