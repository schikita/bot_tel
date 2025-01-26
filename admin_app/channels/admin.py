from django.contrib import admin

from .models import Channel, Post


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "url",
        "is_active",
        "interval_minutes",
        "created_at",
        "updated_at",
        "next_parse_at",
    )
    list_filter = ("is_active", "interval_minutes", "created_at")
    search_fields = ("name", "url")
    list_editable = ("is_active", "interval_minutes")
    actions = ["activate_channels", "deactivate_channels"]

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": ("name", "url", "is_active"),
                "description": "Основные данные о канале.",
            },
        ),
        (
            "Дополнительная информация",
            {
                "fields": ("interval_minutes",),
                "classes": ("collapse",),
                "description": "Технические данные.",
            },
        ),
    )

    @admin.action(description="Активировать выбранные каналы")
    def activate_channels(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Деактивировать выбранные каналы")
    def deactivate_channels(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("channel", "post_id", "text_preview", "published_at", "created_at")
    list_filter = ("published_at", "channel")
    search_fields = ("text", "post_id", "channel__name", "channel__url")
    readonly_fields = ("created_at",)

    def text_preview(self, obj):
        return obj.text[:50] + "..." if obj.text else ""

    text_preview.short_description = "Текст поста (превью)"

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": ("channel", "post_id", "text", "published_at"),
                "description": "Основные данные о посте.",
            },
        ),
        (
            "Дополнительная информация",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
                "description": "Технические данные.",
            },
        ),
    )
