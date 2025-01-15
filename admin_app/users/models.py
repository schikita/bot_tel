from django.db import models
import uuid
from django.utils.timezone import now
from django.core.validators import MinLengthValidator

class Admin(models.Model):
    """
    Модель для администраторов.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_id = models.CharField(max_length=255, unique=True, verbose_name="Telegram ID")
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя администратора")  # Поле необязательное
    created_at = models.DateTimeField(default=now, verbose_name="Дата создания")

    def __str__(self):
        return self.name or str(self.telegram_id)


class SearchWord(models.Model):
    """
    Модель для ключевых слов.
    """
    word = models.CharField(
        max_length=255,
        verbose_name="Ключевое слово",
        unique=True,
        validators=[MinLengthValidator(2)],
    )
    lemma = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Лемма слова",
    )
    admins = models.ManyToManyField(
        "Admin",
        related_name="search_words",
        verbose_name="Администраторы",
    )

    def save(self, *args, **kwargs):      
        self.word = self.word.lower()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

    def __str__(self):
        return self.word

   
