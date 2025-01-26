from django.contrib import admin

from .models import Admin, SearchWord


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ("name", "telegram_id", "created_at", "words_list")
    search_fields = ("name", "telegram_id")
    filter_horizontal = ("words", "channels")

    def words_list(self, obj):
        return ", ".join([word.word for word in obj.words.all()[:5]])

    words_list.short_description = "Ключевые слова (Превью 5шт)"

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": ("telegram_id", "name"),
                "description": "Основные данные об администраторе.",
            },
        ),
        (
            "Дополнительная информация",
            {
                "fields": ("words", "channels"),
                "description": "Ключевые слова и каналы, доступные администратору.",
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(SearchWord)
class SearchWordAdmin(admin.ModelAdmin):
    list_display = ("word", "lemma", "admin_list")
    search_fields = ("word", "lemma")
    list_editable = ("lemma",)

    def admin_list(self, obj):
        return ", ".join(
            [admin.name or admin.telegram_id for admin in obj.admins.all()],
        )

    admin_list.short_description = "Администраторы"
