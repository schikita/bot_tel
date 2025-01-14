from django.db import models
import uuid


class Admin(models.Model):
    """
    Модель для администраторов.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_id = models.CharField(max_length=255, unique=True, verbose_name="Telegram ID")

    def __str__(self):
        return f"Админ {self.telegram_id}"


class SearchWord(models.Model):
    """
    Модель для ключевых слов.
    """
    word = models.CharField(max_length=255, unique=True, verbose_name="Ключевое слово")
    lemma = models.CharField(max_length=255, blank=True, null=True, verbose_name="Лемма слова")
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, verbose_name="Админ")

    def __str__(self):
        return self.word
