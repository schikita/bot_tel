from django.contrib import admin

from .models import Admin, SearchWord


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "name", "created_at")
    search_fields = ("telegram_id", "name")
    filter_horizontal = ("words",)


@admin.register(SearchWord)
class SearchWordAdmin(admin.ModelAdmin):
    list_display = ("word", "lemma")
    search_fields = ("word", "lemma")

    def get_admins(self, obj):
        return ", ".join(
            [admin.name or admin.telegram_id for admin in obj.admins.all()],
        )

    get_admins.short_description = "Администраторы"
