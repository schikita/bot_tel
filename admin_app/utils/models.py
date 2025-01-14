from django.db import models


class Log(models.Model):
    """
    Модель для хранения логов.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    level = models.CharField(max_length=50, verbose_name="Уровень")
    message = models.TextField(verbose_name="Сообщение")
    additional_data = models.JSONField(blank=True, null=True, verbose_name="Дополнительные данные")

    def __str__(self):
        return f"[{self.level}] {self.message}"


class Setting(models.Model):
    """
    Модель для хранения настроек.
    """
    key = models.CharField(max_length=255, unique=True, verbose_name="Ключ")
    value = models.JSONField(verbose_name="Значение")

    def __str__(self):
        return self.key
