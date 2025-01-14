from django.db import models


class SearchWord(models.Model):
    word = models.CharField(max_length=255, unique=True, verbose_name="Ключевое слово")
    lemma = models.CharField(max_length=255, blank=True, null=True, verbose_name="Лемма слова")

    def __str__(self):
        return self.word


class Admin(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True, verbose_name="Telegram ID")

    def __str__(self):
        return f"Админ {self.telegram_id}"
