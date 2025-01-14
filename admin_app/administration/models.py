from django.db import models
import uuid
from django.utils.timezone import now

class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_id = models.CharField(max_length=255, unique=True, verbose_name="Telegram ID")
    name = models.CharField(max_length=255, verbose_name="Имя администратора")
    created_at = models.DateTimeField(default=now, verbose_name="Дата создания")

    def __str__(self):
        return self.name or str(self.telegram_id)



class SearchWord(models.Model):
    """
    Модель для ключевых слов.
    """
    word = models.CharField(max_length=255, unique=True, verbose_name="Ключевое слово")
    lemma = models.CharField(max_length=255, blank=True, null=True, verbose_name="Лемма слова")
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE, verbose_name="Админ")

    def __str__(self):
        return self.word
