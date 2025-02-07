from django.contrib import admin

from .models import Admin, SearchWord


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ("name", "telegram_id", "created_at")
    search_fields = ("name", "telegram_id")
    filter_horizontal = ("words", "channels")

    def get_queryset(self, request):
        """Ограничивает видимость записей в админке."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        """Автоматически устанавливает текущего пользователя при создании."""
        if not obj.user_id:
            obj.user = request.user
        obj.save()

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
    list_display = ("id", "word", "lemma")
    search_fields = ("word", "lemma")
    list_editable = ("word",)
