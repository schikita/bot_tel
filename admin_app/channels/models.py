from django.db import models
import uuid


from django.db import models
import uuid
from datetime import datetime, timedelta


class Channel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_link = models.URLField(unique=True, verbose_name="Ссылка на Telegram-канал")
    channel_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя канала")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    priority = models.IntegerField(default=1, verbose_name="Приоритет парсинга")  # Чем выше значение, тем выше приоритет
    interval_minutes = models.PositiveIntegerField(default=2, verbose_name="Интервал парсинга в минутах")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    last_scanned_at = models.DateTimeField(blank=True, null=True, verbose_name="Последнее сканирование")
    scan_interval = models.PositiveIntegerField(default=2, verbose_name="Интервал сканирования (минуты)")
    next_scan_at = models.DateTimeField(blank=True, null=True, verbose_name="Следующее сканирование")

    def calculate_next_scan(self):
        """Рассчитать время следующего сканирования."""
        if self.last_scanned_at:
            self.next_scan_at = self.last_scanned_at + timedelta(minutes=self.scan_interval)
        else:
            self.next_scan_at = datetime.now() + timedelta(minutes=self.scan_interval)

    def save(self, *args, **kwargs):
        if not self.next_scan_at:
            self.calculate_next_scan()
        super().save(*args, **kwargs)

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
