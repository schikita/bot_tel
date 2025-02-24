import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model

User = get_user_model()


class Admin(models.Model):
    """Модель для администраторов."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    telegram_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Telegram ID",
        help_text='ID пользователя в Telegram. Например, 80567890, можно узнать у @userinfobot, группы чатов начинаются с знака "-" (минус).',
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Имя администратора",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    words = models.ManyToManyField(
        "SearchWord",
        blank=True,
        related_name="admins",
        verbose_name="Ключевые слова, доступные админу",
    )
    channels = models.ManyToManyField(
        "channels.Channel",
        blank=True,
        related_name="admins",
        verbose_name="Каналы, на которые подписан администратор",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="admins",
        verbose_name="Пользователь",
        default=None,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def __str__(self):
        return self.name or self.telegram_id


class SearchWord(models.Model):
    """Модель для ключевых слов."""

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

    def clean(self):
        self.word = self.word.lower()

        if len(self.word) < 2:
            raise ValidationError(
                {"word": _("Ключевое слово должно содержать минимум 2 символа.")},
            )

        if (
            SearchWord.objects.filter(word__iexact=self.word)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError({"word": _(f"Слово {self.word} уже существует.")})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ключевое слово"
        verbose_name_plural = "Ключевые слова"

    def __str__(self):
        return self.word


class ExcludedPhrase(models.Model):
    """Модель для хранения исключаемых фраз."""
    phrase = models.CharField(
        max_length=255,
        verbose_name="Исключаемая фраза",
        unique=True,
        validators=[MinLengthValidator(2)],
    )

    class Meta:
        verbose_name = "Исключаемая фраза"
        verbose_name_plural = "Исключаемые фразы"
        db_table = "excluded_phrase"

    def __str__(self):
        return self.phrase