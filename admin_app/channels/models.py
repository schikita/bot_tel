import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, URLValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def channel_url_validator(value) -> None:
    if not value:
        raise ValidationError(_("Ссылка на канал не может быть пустой."))

    url_validator = URLValidator()
    try:
        url_validator(value)
    except ValidationError:
        raise ValidationError(_("Неверный формат URL."))

    if not value.startswith("https://t.me/s/"):
        raise ValidationError(
            _("Неверный формат ссылки на канал, ожидается https://t.me/s/<username>"),
        )

    if len(value.split("/")) < 3 or not value.split("/")[4]:
        raise ValidationError(
            _("Неверный формат ссылки на канал, ожидается https://t.me/s/<username>"),
        )


class Channel(models.Model):
    """Модель для Telegram-каналов."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Имя канала",
    )
    url = models.CharField(
        unique=True,
        verbose_name="Ссылка на Telegram-канал",
        validators=[channel_url_validator],
        help_text="Формат ссылки: https://t.me/s/<username>",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    interval_minutes = models.PositiveIntegerField(
        default=2,
        validators=[MinValueValidator(1)],
        verbose_name="Интервал парсинга в минутах",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    next_parse_at = models.DateTimeField(
        blank=True,
        null=True,
        db_index=True,
        auto_now_add=True,
        verbose_name="Время начала следующего парсинга",
    )

    class Meta:
        verbose_name = "Канал"
        verbose_name_plural = "Каналы"

    def __str__(self):
        return self.name or self.url


class Post(models.Model):
    """Модель для хранения информации о постах Telegram-каналов."""

    id = models.AutoField(primary_key=True)
    channel = models.ForeignKey(
        "Channel",
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Канал",
    )
    post_id = models.PositiveIntegerField(verbose_name="ID поста")
    text = models.TextField(verbose_name="Текст поста", blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления в БД",
    )
    published_at = models.DateTimeField(verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        unique_together = ("post_id", "channel")

    def __str__(self):
        return f"Пост {self.post_id} из канала {self.channel}"
