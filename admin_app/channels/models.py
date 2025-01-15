from django.db import models
import uuid
from django.utils.timezone import now
from django.core.validators import MinValueValidator


class Channel(models.Model):
    """
    Модель для Telegram-каналов.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя канала")
    url = models.URLField(unique=True, verbose_name="Ссылка на Telegram-канал")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    interval_minutes = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1)],  # Ограничение: минимум 1 минута
        verbose_name="Интервал парсинга в минутах"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name or self.url

    def __str__(self):
        return self.channel_name or self.telegram_link



class Post(models.Model):
    """
    Модель для хранения информации о постах Telegram-каналов.
    """
    id = models.AutoField(primary_key=True)
    channel = models.ForeignKey(
        'Channel', 
        on_delete=models.CASCADE,
        related_name="posts",  
        verbose_name="Канал"
    )
    post_id = models.PositiveIntegerField(verbose_name="ID поста", unique=True)
    text = models.TextField(verbose_name="Текст поста", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления в БД")
    published_at = models.DateTimeField(default=now, verbose_name="Дата публикации")
    last_parsed_at = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Время последнего парсинга"
    )
    next_parse_at = models.DateTimeField(
        blank=True, 
        null=True, 
        verbose_name="Время начала следующего парсинга"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"Пост {self.post_id} из канала {self.channel}"