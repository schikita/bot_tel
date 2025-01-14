from django.db import models
import uuid


class Channel(models.Model):
    """
    Модель для хранения информации о Telegram-каналах.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_link = models.URLField(unique=True, verbose_name="Ссылка на Telegram-канал")
    channel_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя канала")
    active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.channel_name or self.telegram_link


class Post(models.Model):
    """
    Модель для хранения информации о постах Telegram-каналов.
    """
    id = models.AutoField(primary_key=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, verbose_name="Канал")
    post_id = models.CharField(max_length=255, verbose_name="ID поста")

    class Meta:
        unique_together = ('post_id', 'channel')

    def __str__(self):
        return f"Пост {self.post_id} из {self.channel}"
